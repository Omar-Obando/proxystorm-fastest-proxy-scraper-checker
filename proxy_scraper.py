"""
ProxyStorm v1.0
Ultra Fast Proxy Scraper & Verifier

This module provides a high-performance proxy scraping and verification system.
It uses asynchronous I/O and optimized algorithms to achieve maximum speed.

Features:
- Multi-protocol support (HTTP, SOCKS4, SOCKS5)
- Configurable latency and thread settings
- Bilingual interface (English/Spanish)
- Multiple output formats
- Smart caching system
- Cross-platform optimization
- UVLoop support for Linux (enhanced performance)

Author: Omar Obando
License: MIT
"""

import asyncio
import aiohttp
import platform
from datetime import datetime
from diskcache import Cache
from colorama import init, Fore
import json
from typing import List, Dict, Optional, Set
import re
import time
import sys
import os
import socket

# Inicialización de colorama para Windows
init()

# Crear directorio de caché si no existe
CACHE_DIR = './cache'
if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

# Configuración de caché con TTL de 30 minutos para mayor frescura de datos
cache = Cache(CACHE_DIR, size_limit=int(1e9), ttl=1800)

# Configuración del event loop según el sistema operativo
if platform.system() == 'Linux':
    try:
        import uvloop
        uvloop.install()
        print(f"{Fore.GREEN}✓ UVLoop activado para mejor rendimiento en Linux{Fore.RESET}")
    except ImportError:
        print(f"{Fore.YELLOW}⚠ UVLoop no disponible, usando event loop estándar{Fore.RESET}")
elif platform.system() == 'Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    print(f"{Fore.YELLOW}ℹ Usando WindowsSelectorEventLoopPolicy para Windows{Fore.RESET}")

# Menú bilingüe simplificado
MENU = {
    'en': {
        'language_select': "🌐 Select Language:\n1. English\n2. Español",
        'mode_select': "🔥 MODE:\n1. Scrape Only\n2. Scrape+Verify\n3. Exit",
        'protocol_select': "🔒 Select Protocol:\n1. HTTP\n2. SOCKS4\n3. SOCKS5\n4. All",
        'format_select': "📝 Format:\n1. IP:PORT\n2. PORT:IP\n3. protocol://IP:PORT",
        'output_question': "Save results? [y/N]: ",
        'stats': "📊 Stats:\nTotal: {total}\nAlive: {alive}\nDead: {dead}\nProgress: {progress}%",
        'proxy_limit': "Number of proxies (0=all): ",
        'latency_select': "⚡ Latency (ms):\n0. Default (1500ms)\nOr enter custom value (recommended: 100-2000ms)\nNote: Lower latency = fewer proxies but faster\n> ",
        'threads_select': "🧵 Threads:\n0. Default (200 threads)\nOr enter custom value (recommended: 100-1000)\nNote: More threads = faster but more resource usage\n> "
    },
    'es': {
        'language_select': "🌐 Idioma:\n1. English\n2. Español",
        'mode_select': "🔥 MODO:\n1. Solo Scrapear\n2. Scrapear+Verificar\n3. Salir",
        'protocol_select': "🔒 Protocolo:\n1. HTTP\n2. SOCKS4\n3. SOCKS5\n4. Todos",
        'format_select': "📝 Formato:\n1. IP:PUERTO\n2. PUERTO:IP\n3. protocolo://IP:PUERTO",
        'output_question': "¿Guardar? [y/N]: ",
        'stats': "📊 Stats:\nTotal: {total}\nVivos: {alive}\nMuertos: {dead}\nProgreso: {progress}%",
        'proxy_limit': "Número de proxies (0=todos): ",
        'latency_select': "⚡ Latencia (ms):\n0. Por defecto (1500ms)\nO ingrese valor personalizado (recomendado: 100-2000ms)\nNota: Menor latencia = menos proxies pero más rápidos\n> ",
        'threads_select': "🧵 Threads:\n0. Por defecto (200 threads)\nO ingrese valor personalizado (recomendado: 100-1000)\nNota: Más threads = más rápido pero más uso de recursos\n> "
    }
}

# ASCII Art para el menú principal
STORM_ART = """
 
           ,-'-.     _.,  
        . (    '("'-'  ').  
     ( ' ((  |.      )\/( ) 
      '(  )) | () |" |  | ')
         ( . ,-. ,-.. __.) 
           /)  /  ' /         
          /   /) / /                By Omar Obando
"""

class Proxy:
    """
    Clase que representa un proxy con sus atributos básicos.
    
    Attributes:
        ip (str): Dirección IP del proxy
        port (int): Puerto del proxy
        protocol (str): Protocolo del proxy (http/socks4/socks5)
        latency (float): Latencia del proxy en milisegundos
    """
    __slots__ = ('ip', 'port', 'protocol', 'latency')
    
    def __init__(self, ip: str, port: int, protocol: str, latency: float = 0):
        """
        Inicializa un nuevo proxy.
        
        Args:
            ip (str): Dirección IP
            port (int): Puerto
            protocol (str): Protocolo
            latency (float, optional): Latencia. Defaults to 0.
        """
        self.ip = ip
        self.port = port
        self.protocol = protocol
        self.latency = latency

    def __str__(self):
        """Retorna la representación en string del proxy."""
        return f"{self.protocol}://{self.ip}:{self.port}"

    def format(self, format_type: int) -> str:
        """
        Formatea el proxy según el tipo especificado.
        
        Args:
            format_type (int): Tipo de formato (1=IP:PORT, 2=PORT:IP, 3=protocol://IP:PORT)
            
        Returns:
            str: Proxy formateado
        """
        if format_type == 1:
            return f"{self.ip}:{self.port}"
        elif format_type == 2:
            return f"{self.port}:{self.ip}"
        else:
            return f"{self.protocol}://{self.ip}:{self.port}"
    
    def __eq__(self, other):
        """Compara dos proxies por IP y puerto."""
        if not isinstance(other, Proxy):
            return False
        return (self.ip == other.ip and self.port == other.port)
    
    def __hash__(self):
        """Genera un hash único para el proxy basado en IP y puerto."""
        return hash((self.ip, self.port))

class ProxyScraper:
    """
    Clase principal para scraping y verificación de proxies.
    
    Esta clase maneja todas las operaciones relacionadas con la obtención
    y verificación de proxies, incluyendo el manejo de sesiones HTTP,
    caché, y procesamiento asíncrono.
    """
    
    def __init__(self):
        """
        Inicializa el scraper con configuraciones por defecto.
        """
        self.sources = self.load_sources()
        self.verified_proxies = set()
        self.session = None
        self.max_connections = 500 if platform.system() == 'Windows' else 2000
        self.semaphore = asyncio.Semaphore(self.max_connections)
        self.stats = {'total': 0, 'alive': 0, 'dead': 0}
        self.ip_pattern = re.compile(r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$')
        self.seen_proxies = set()
        self.cache = Cache(CACHE_DIR, size_limit=int(1e9), ttl=1800)
        self.latency_limit = 1500
        self.batch_size = 200  # Valor por defecto

    async def __aenter__(self):
        """Inicializa la sesión al entrar al contexto."""
        await self.init_session()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Cierra la sesión y la caché al salir del contexto."""
        await self.close_session()
        self.cache.close()

    def is_valid_ip(self, ip: str) -> bool:
        """
        Verifica si una IP es válida.
        
        Args:
            ip (str): IP a verificar
            
        Returns:
            bool: True si la IP es válida
        """
        return bool(self.ip_pattern.match(ip))

    def is_valid_port(self, port: int) -> bool:
        """
        Verifica si un puerto es válido.
        
        Args:
            port (int): Puerto a verificar
            
        Returns:
            bool: True si el puerto es válido
        """
        return 0 < port < 65536

    def load_sources(self) -> Dict[str, List[str]]:
        """
        Carga las fuentes de proxies desde sites.txt o usa fuentes por defecto.
        
        Returns:
            Dict[str, List[str]]: Diccionario con las fuentes por protocolo
        """
        sources = {
            'http': [],
            'socks4': [],
            'socks5': []
        }
        
        try:
            with open('sites.txt', 'r') as f:
                for line in f:
                    line = line.strip()
                    if not line or not line.startswith('http'):
                        continue
                    
                    if 'socks4' in line.lower():
                        sources['socks4'].append(line)
                    elif 'socks5' in line.lower():
                        sources['socks5'].append(line)
                    else:
                        sources['http'].append(line)
        except FileNotFoundError:
            sources = {
                'http': ["https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt"],
                'socks4': ["https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks4.txt"],
                'socks5': ["https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt"]
            }
        
        return sources

    async def init_session(self):
        """
        Inicializa la sesión HTTP con configuraciones optimizadas.
        """
        if not self.session:
            connector = aiohttp.TCPConnector(
                limit=self.max_connections,
                ttl_dns_cache=300,
                force_close=True,
                enable_cleanup_closed=True,
                use_dns_cache=True,
                ssl=False,
                limit_per_host=0,
                family=socket.AF_INET  # Forzar IPv4 para mayor velocidad
            )
            
            self.session = aiohttp.ClientSession(
                connector=connector,
                timeout=aiohttp.ClientTimeout(total=10, connect=2),  # Aumentado significativamente
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0.4472.124',
                    'Accept': '*/*',
                    'Connection': 'close',
                    'Accept-Encoding': 'gzip, deflate',
                    'Cache-Control': 'no-cache'
                }
            )

    async def fetch_proxies(self, url: str, protocol: str) -> Set[Proxy]:
        """
        Obtiene proxies desde una URL específica.
        
        Args:
            url (str): URL de la fuente
            protocol (str): Protocolo de los proxies
            
        Returns:
            Set[Proxy]: Conjunto de proxies encontrados
        """
        cache_key = f"proxies_{url}_{protocol}"
        try:
            cached_proxies = self.cache.get(cache_key)
            if cached_proxies:
                return cached_proxies
        except:
            pass

        proxies = set()
        try:
            async with self.session.get(url, timeout=3) as response:
                if response.status == 200:
                    content = await response.text()
                    for line in content.splitlines():
                        if ':' in line:
                            try:
                                ip, port = line.strip().split(':')
                                port = int(port)
                                if self.is_valid_ip(ip) and self.is_valid_port(port):
                                    proxy = Proxy(ip, port, protocol)
                                    if proxy not in self.seen_proxies:
                                        self.seen_proxies.add(proxy)
                                        proxies.add(proxy)
                            except:
                                continue
            
            if proxies:
                try:
                    self.cache.set(cache_key, proxies)
                except:
                    pass
            return proxies
        except:
            return set()

    async def check_proxy(self, proxy: Proxy) -> bool:
        """
        Verifica si un proxy está funcionando.
        
        Args:
            proxy (Proxy): Proxy a verificar
            
        Returns:
            bool: True si el proxy está funcionando
        """
        if not self.session:
            self.session = await self.init_session()
            
        # URLs de prueba optimizadas y más ligeras
        test_urls = [
            "http://ip-api.com/json/",
            "http://httpbin.org/ip",
            "http://ipinfo.io/json"
        ]
        
        # Timeout más permisivo
        timeout = aiohttp.ClientTimeout(total=5.0)  # Aumentado a 5 segundos
        
        for url in test_urls:
            try:
                start_time = time.time()
                async with self.session.get(
                    url,
                    proxy=f"{proxy.protocol}://{proxy.ip}:{proxy.port}",
                    timeout=timeout,
                    allow_redirects=False,
                    ssl=False,
                    headers={
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0.4472.124',
                        'Accept': 'application/json',
                        'Connection': 'close',
                        'Accept-Encoding': 'gzip, deflate',
                        'Cache-Control': 'no-cache'
                    }
                ) as response:
                    if response.status in [200, 201, 202]:
                        latency = (time.time() - start_time) * 1000
                        if latency < self.latency_limit:  # Usar el límite de latencia configurado
                            proxy.latency = latency
                            return True
            except Exception:
                continue
                
        return False

    async def verify_proxies(self, proxies: List[Proxy], target_count: int = 0) -> List[Proxy]:
        """
        Verifica un conjunto de proxies en lotes.
        
        Args:
            proxies (List[Proxy]): Lista de proxies a verificar
            target_count (int, optional): Número objetivo de proxies. Defaults to 0.
            
        Returns:
            List[Proxy]: Lista de proxies verificados y funcionando
        """
        verified = []
        total = len(proxies)
        processed = 0
        alive = 0
        dead = 0
        
        # Usar el tamaño de lote configurado
        batch_size = self.batch_size
        
        # Procesar en lotes más grandes
        for i in range(0, total, batch_size):
            batch = proxies[i:i + batch_size]
            tasks = []
            
            for proxy in batch:
                if target_count and alive >= target_count:
                    break
                    
                tasks.append(self.check_proxy(proxy))
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for proxy, result in zip(batch, results):
                if isinstance(result, bool) and result:
                    verified.append(proxy)
                    alive += 1
                else:
                    dead += 1
                    
                processed += 1
                if processed % 100 == 0:  # Actualizar stats cada 100 proxies
                    print(f"\n📊 Stats:")
                    print(f"Total: {total}")
                    print(f"Vivos: {alive}")
                    print(f"Muertos: {dead}")
                    print(f"Progreso: {int(processed/total*100)}%")
                    
            # Pausa más larga entre lotes
            await asyncio.sleep(0.2)  # Aumentado a 0.2 segundos
            
        return verified

    async def hyper_scrape(self, protocols: List[str], limit: int = 0) -> List[Proxy]:
        """
        Realiza scraping de proxies desde múltiples fuentes en paralelo.
        
        Args:
            protocols (List[str]): Lista de protocolos a scrapear
            limit (int, optional): Límite de proxies a obtener. Defaults to 0.
            
        Returns:
            List[Proxy]: Lista de proxies encontrados
        """
        tasks = []
        for protocol in protocols:
            for url in self.sources.get(protocol, []):
                tasks.append(self.fetch_proxies(url, protocol))
        
        results = await asyncio.gather(*tasks)
        all_proxies = set()
        for proxy_set in results:
            all_proxies.update(proxy_set)
        
        proxies_list = list(all_proxies)
        if limit > 0:
            proxies_list = proxies_list[:limit]
        
        return proxies_list

    async def close_session(self):
        """Cierra la sesión HTTP si está abierta."""
        if self.session and not self.session.closed:
            await self.session.close()
            self.session = None

    def save_proxies(self, proxies: List[Proxy], filename: str, format_type: int):
        """
        Guarda los proxies en un archivo.
        
        Args:
            proxies (List[Proxy]): Lista de proxies a guardar
            filename (str): Nombre base del archivo
            format_type (int): Tipo de formato para guardar
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{filename}_{timestamp}.txt"
        
        with open(filename, 'w') as f:
            for proxy in sorted(proxies, key=lambda x: x.latency):
                f.write(f"{proxy.format(format_type)}\n")
        print(f"{Fore.GREEN}✓ Guardado en {filename}{Fore.RESET}")

async def main():
    """
    Función principal que maneja el flujo del programa.
    """
    async with ProxyScraper() as scraper:
        print(f"{Fore.CYAN}{STORM_ART}{Fore.RESET}")
        print(f"{Fore.CYAN}{MENU['en']['language_select']}{Fore.RESET}")
        lang_choice = input("> ")
        language = 'es' if lang_choice == '2' else 'en'
        
        try:
            while True:
                print(f"\n{Fore.CYAN}{MENU[language]['mode_select']}{Fore.RESET}")
                mode_choice = input("> ")
                
                if mode_choice == '3':
                    break
                    
                print(f"\n{Fore.CYAN}{MENU[language]['protocol_select']}{Fore.RESET}")
                protocol_choice = input("> ")
                protocols = {
                    '1': ['http'],
                    '2': ['socks4'],
                    '3': ['socks5'],
                    '4': ['http', 'socks4', 'socks5']
                }.get(protocol_choice, ['http'])
                
                if mode_choice in ['1', '2']:
                    print(f"\n{Fore.CYAN}{MENU[language]['proxy_limit']}{Fore.RESET}")
                    limit = int(input("> ") or "0")
                    
                    print(f"\n{Fore.CYAN}{MENU[language]['latency_select']}{Fore.RESET}")
                    latency_choice = input("> ")
                    scraper.latency_limit = 1500 if latency_choice == "0" else int(latency_choice)
                    
                    print(f"\n{Fore.CYAN}{MENU[language]['threads_select']}{Fore.RESET}")
                    threads_choice = input("> ")
                    scraper.batch_size = 200 if threads_choice == "0" else int(threads_choice)
                    
                    print(f"\n{Fore.YELLOW}Scraping...{Fore.RESET}")
                    proxies = await scraper.hyper_scrape(protocols, limit if mode_choice == '1' else 0)
                    print(f"{Fore.GREEN}Found: {len(proxies)}{Fore.RESET}")
                    
                    if mode_choice == '2':
                        print(f"\n{Fore.YELLOW}Verifying...{Fore.RESET}")
                        proxies = await scraper.verify_proxies(proxies, limit)
                        print(f"{Fore.GREEN}Verified: {len(proxies)}{Fore.RESET}")
                    
                    print(f"\n{Fore.CYAN}{MENU[language]['format_select']}{Fore.RESET}")
                    format_type = int(input("> "))
                    
                    save = input(f"\n{MENU[language]['output_question']}").lower()
                    if save == 'y':
                        scraper.save_proxies(proxies, "proxies", format_type)
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}Terminado por usuario{Fore.RESET}")
        except Exception as e:
            print(f"\n{Fore.RED}Error: {str(e)}{Fore.RESET}")

if __name__ == "__main__":
    print(f"{Fore.CYAN}=== ProxyStorm v1.0 ==={Fore.RESET}")
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Terminado por usuario{Fore.RESET}")
    except Exception as e:
        print(f"\n{Fore.RED}Error: {str(e)}{Fore.RESET}") 