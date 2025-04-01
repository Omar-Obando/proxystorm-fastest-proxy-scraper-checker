# ProxyStorm v1.0
## Ultra Fast Proxy Scraper & Verifier

[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Stars](https://img.shields.io/github/stars/Omar-Obando/proxystorm-fastest-proxy-scraper-checker?style=social)](https://github.com/Omar-Obando/proxystorm-fastest-proxy-scraper-checker)

## 🌟 Features

- **Ultra Fast Scraping**: Optimized for maximum speed
- **Multi-Protocol Support**: HTTP, SOCKS4, SOCKS5
- **Smart Verification**: Configurable latency and threads
- **Bilingual Interface**: English and Spanish
- **Multiple Output Formats**: IP:PORT, PORT:IP, protocol://IP:PORT
- **Caching System**: 30-minute cache for faster results
- **Resource Efficient**: Optimized memory usage
- **Cross-Platform**: Works on Windows and Linux
- **UVLoop Support**: Enhanced performance on Linux (2-4x faster)

## 🚀 Installation

1. Clone the repository:
```bash
git clone https://github.com/Omar-Obando/proxystorm-fastest-proxy-scraper-checker.git
cd proxystorm-fastest-proxy-scraper-checker
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## 💻 Usage

1. Run the program:
```bash
python proxy_scraper.py
```

2. Select your language (English/Español)

3. Choose operation mode:
   - Scrape Only: Only collects proxies
   - Scrape+Verify: Collects and verifies proxies
   - Exit: Close program

4. Select protocol:
   - HTTP
   - SOCKS4
   - SOCKS5
   - All protocols

5. Configure settings:
   - Number of proxies (0 for all)
   - Latency limit (ms)
   - Number of threads

6. Choose output format:
   - IP:PORT
   - PORT:IP
   - protocol://IP:PORT

7. Save results (optional)

## ⚙️ Configuration Guide

### Latency Settings
- Default: 1500ms
- Recommended range: 100-2000ms
- Lower latency = fewer proxies but faster
- Higher latency = more proxies but slower

### Thread Settings
- Default: 200 threads
- Recommended range: 100-1000
- More threads = faster but more resource usage
- Less threads = slower but more stable

### System Requirements
- Windows: 500 concurrent connections
- Linux: 2000 concurrent connections (with UVLoop)
- Minimum 4GB RAM recommended
- Python 3.7 or higher

### Performance Optimization
- **Linux**: Uses UVLoop for enhanced performance (2-4x faster)
- **Windows**: Uses WindowsSelectorEventLoopPolicy for stability
- **Memory**: Optimized for low memory usage
- **Network**: Configurable connection limits per platform

## 📊 Performance Metrics

- Average scraping speed: 50,000+ proxies/minute
- Verification speed: 1000+ proxies/minute
- Memory usage: ~100MB
- Cache size: 1GB
- Cache duration: 30 minutes

## 🔧 Technical Details

### Dependencies
- aiohttp: Async HTTP client
- colorama: Colored terminal output
- diskcache: Caching system
- uvloop: Enhanced event loop (Linux only, 2-4x faster)

### File Structure
```
proxystorm/
├── proxy_scraper.py    # Main program
├── sites.txt          # Proxy sources
├── cache/            # Cache directory
└── requirements.txt   # Dependencies
```

### Cache System
- Location: ./cache
- Size limit: 1GB
- TTL: 30 minutes
- Automatic cleanup

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## 📞 Contact

- GitHub: [@Omar-Obando](https://github.com/Omar-Obando)
- Email: [Your Email]

---

# ProxyStorm v1.0
## Scraper y Verificador de Proxies Ultra Rápido

[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Stars](https://img.shields.io/github/stars/Omar-Obando/proxystorm-fastest-proxy-scraper-checker?style=social)](https://github.com/Omar-Obando/proxystorm-fastest-proxy-scraper-checker)

## 🌟 Características

- **Scraping Ultra Rápido**: Optimizado para máxima velocidad
- **Soporte Multi-Protocolo**: HTTP, SOCKS4, SOCKS5
- **Verificación Inteligente**: Latencia y threads configurables
- **Interfaz Bilingüe**: Inglés y Español
- **Múltiples Formatos de Salida**: IP:PUERTO, PUERTO:IP, protocolo://IP:PUERTO
- **Sistema de Caché**: 30 minutos de caché para resultados más rápidos
- **Eficiente en Recursos**: Uso de memoria optimizado
- **Multiplataforma**: Funciona en Windows y Linux
- **Soporte UVLoop**: Rendimiento mejorado en Linux (2-4x más rápido)

## 🚀 Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/Omar-Obando/proxystorm-fastest-proxy-scraper-checker.git
cd proxystorm-fastest-proxy-scraper-checker
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

## 💻 Uso

1. Ejecutar el programa:
```bash
python proxy_scraper.py
```

2. Seleccionar idioma (English/Español)

3. Elegir modo de operación:
   - Solo Scrapear: Solo recopila proxies
   - Scrapear+Verificar: Recopila y verifica proxies
   - Salir: Cerrar programa

4. Seleccionar protocolo:
   - HTTP
   - SOCKS4
   - SOCKS5
   - Todos los protocolos

5. Configurar ajustes:
   - Número de proxies (0 para todos)
   - Límite de latencia (ms)
   - Número de threads

6. Elegir formato de salida:
   - IP:PUERTO
   - PUERTO:IP
   - protocolo://IP:PUERTO

7. Guardar resultados (opcional)

## ⚙️ Guía de Configuración

### Ajustes de Latencia
- Por defecto: 1500ms
- Rango recomendado: 100-2000ms
- Menor latencia = menos proxies pero más rápidos
- Mayor latencia = más proxies pero más lentos

### Ajustes de Threads
- Por defecto: 200 threads
- Rango recomendado: 100-1000
- Más threads = más rápido pero más uso de recursos
- Menos threads = más lento pero más estable

### Requisitos del Sistema
- Windows: 500 conexiones concurrentes
- Linux: 2000 conexiones concurrentes (con UVLoop)
- Mínimo 4GB RAM recomendado
- Python 3.7 o superior

### Optimización de Rendimiento
- **Linux**: Usa UVLoop para rendimiento mejorado (2-4x más rápido)
- **Windows**: Usa WindowsSelectorEventLoopPolicy para estabilidad
- **Memoria**: Optimizado para bajo uso de memoria
- **Red**: Límites de conexión configurables por plataforma

## 📊 Métricas de Rendimiento

- Velocidad promedio de scraping: 50,000+ proxies/minuto
- Velocidad de verificación: 1000+ proxies/minuto
- Uso de memoria: ~100MB
- Tamaño de caché: 1GB
- Duración de caché: 30 minutos

## 🔧 Detalles Técnicos

### Dependencias
- aiohttp: Cliente HTTP asíncrono
- colorama: Salida de terminal coloreada
- diskcache: Sistema de caché
- uvloop: Event loop mejorado (solo Linux, 2-4x más rápido)

### Estructura de Archivos
```
proxystorm/
├── proxy_scraper.py    # Programa principal
├── sites.txt          # Fuentes de proxies
├── cache/            # Directorio de caché
└── requirements.txt   # Dependencias
```

### Sistema de Caché
- Ubicación: ./cache
- Límite de tamaño: 1GB
- TTL: 30 minutos
- Limpieza automática

## 📝 Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Por favor lee [CONTRIBUTING.md](CONTRIBUTING.md) para más detalles.

## 📞 Contacto

- GitHub: [@Omar-Obando](https://github.com/Omar-Obando)
- Email: [Tu Email]

## 🙏 Acknowledgments / Agradecimientos

- [TheSpeedX](https://github.com/TheSpeedX) por las listas de proxies
- Todos los contribuidores y usuarios del proyecto 