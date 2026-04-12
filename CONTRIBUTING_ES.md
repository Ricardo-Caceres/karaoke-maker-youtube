# 🤝 Contribuir a la Suite de YouTube DL

¡Gracias por tu interés en contribuir a la Suite de Procesamiento de Audio y Video de YouTube DL! Este documento proporciona guías comprensivas para colaboradores.

## 📋 Tabla de Contenidos

- [Empezando](#empezando)
- [Entorno de Desarrollo](#entorno-de-desarrollo)
- [Estándares de Código](#estándares-de-código)
- [Flujo de Contribución](#flujo-de-contribución)
- [Guías de Pruebas](#guías-de-pruebas)
- [Estándares de Documentación](#estándares-de-documentación)
- [Reportes de Errores](#reportes-de-errores)
- [Solicitudes de Características](#solicitudes-de-características)
- [Proceso de Lanzamiento](#proceso-de-lanzamiento)
- [Guías de Comunidad](#guías-de-comunidad)

## 🚀 Empezando

### Prerrequisitos

Antes de contribuir, asegúrate de tener:
- Python 3.7+ instalado
- Git configurado con tus credenciales
- FFmpeg instalado en tu sistema
- Entendimiento básico de conceptos de procesamiento de audio/video
- Familiaridad con la estructura del proyecto

### Áreas Donde Necesitamos Ayuda

Damos la bienvenida a contribuciones en estas áreas:

#### 🎯 Alta Prioridad
- [ ] **Optimización de Rendimiento**: Mejorar velocidad de procesamiento y uso de memoria
- [ ] **Manejo de Errores**: Mejores mensajes de error y mecanismos de recuperación
- [ ] **Soporte de Plataformas**: Añadir soporte para más plataformas de video
- [ ] **Documentación**: Mejorar y expandir la documentación
- [ ] **Pruebas**: Incrementar cobertura de pruebas y añadir pruebas de integración

#### 🎨 Prioridad Media
- [ ] **Interfaz Web**: Crear una GUI basada en web usando Flask/Django
- [ ] **Procesamiento por Lotes**: Mejorar operaciones masivas y gestión de colas
- [ ] **Gestión de Configuración**: Mejor soporte para archivos de configuración
- [ ] **Registro**: Características mejoradas de registro y depuración
- [ ] **Internacionalización**: Soporte multi-idioma

#### 🔮 Ideas Futuras
- [ ] **Aplicación Móvil**: Interfaz móvil React Native o Flutter
- [ ] **Integración en la Nube**: Soporte de procesamiento AWS/GCP
- [ ] **Procesamiento en Tiempo Real**: Generación de karaoke en vivo
- [ ] **IA Avanzada**: Mejor detección de letras y sincronización
- [ ] **Sistema de Plugins**: Arquitectura extensible para procesadores personalizados

## 🛠️ Entorno de Desarrollo

### 1. Fork y Clone

```bash
# Primero haz fork del repositorio en GitHub, luego:
git clone https://github.com/TU_USUARIO/youtube-dl-suite.git
cd youtube-dl-suite

# Añadir remote upstream
git remote add upstream https://github.com/PROPIETARIO_ORIGINAL/youtube-dl-suite.git
```

### 2. Configurar Entorno de Desarrollo

```bash
# Crear entorno virtual
python3 -m venv dev_env
source dev_env/bin/activate  # En Windows: dev_env\Scripts\activate

# Instalar dependencias de desarrollo
pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Configurar entorno de Spleeter
python3 -m venv spleeter_env
source spleeter_env/bin/activate
pip install spleeter[tensorflow]
deactivate
source dev_env/bin/activate
```

### 3. Instalar Herramientas de Desarrollo

```bash
# Formateo y linting de código
pip install black flake8 isort mypy

# Framework de pruebas
pip install pytest pytest-cov pytest-mock

# Hooks de pre-commit
pip install pre-commit
pre-commit install

# Herramientas de documentación
pip install sphinx sphinx-rtd-theme
```

## 📝 Estándares de Código

### Guías de Estilo Python

Seguimos **PEP 8** con algunas modificaciones:

```python
# Longitud de línea: 88 caracteres (por defecto de Black)
# Usar comillas dobles para strings
ejemplo_string = "Hola, mundo!"

# Type hints son requeridos para funciones públicas
def procesar_audio(ruta_archivo: str, calidad: int = 192) -> str:
    """Procesar archivo de audio con calidad especificada."""
    pass

# Usar nombres de variables descriptivos
ruta_archivo_audio = "downloads/cancion.mp3"  # ✅ Bueno
f = "downloads/cancion.mp3"                   # ❌ Malo

# Constantes en MAYÚSCULAS
CALIDAD_AUDIO_DEFAULT = 192
MAX_REINTENTOS = 3
```

### Manejo de Errores

```python
# Usar excepciones específicas
def download_audio(url: str) -> str:
    """Descargar audio con manejo adecuado de errores."""
    
    if not url.startswith(('http://', 'https://')):
        raise ValueError(f"Formato de URL inválido: {url}")
    
    try:
        # Lógica de descarga aquí
        return audio_path
    except subprocess.CalledProcessError as e:
        # Registrar el error con contexto
        logger.error(f"yt-dlp falló para URL {url}: {e.stderr}")
        raise DownloadError(f"Falló descargar audio de {url}") from e
    except Exception as e:
        logger.exception(f"Error inesperado descargando {url}")
        raise ProcessingError(f"Fallo inesperado de descarga: {e}") from e
```

## 🔄 Flujo de Contribución

### Convención de Nombres de Ramas

```bash
# Ramas de características
git checkout -b feature/add-batch-processing
git checkout -b feature/web-interface

# Ramas de corrección de errores
git checkout -b fix/memory-leak-in-processor
git checkout -b fix/unicode-handling

# Ramas de documentación
git checkout -b docs/api-reference-update
git checkout -b docs/installation-guide
```

### Formato de Mensaje de Commit

Usamos [Conventional Commits](https://www.conventionalcommits.org/):

```bash
# Tipos:
feat:     # Nueva característica
fix:      # Corrección de error
docs:     # Cambios en documentación
style:    # Cambios de estilo de código
refactor: # Refactorización de código
perf:     # Mejoras de rendimiento
test:     # Añadir o actualizar pruebas
chore:    # Tareas de mantenimiento

# Ejemplos:
feat(karaoke): añadir opciones de estilo de video personalizado

fix(audio): resolver fuga de memoria en separación de voz

docs(api): actualizar firmas de función en referencia
```

## 🧪 Guías de Pruebas

### Estructura de Pruebas

```
tests/
├── unit/                   # Pruebas unitarias
│   ├── test_app.py
│   ├── test_karaoke_generator.py
│   └── test_movies.py
├── integration/            # Pruebas de integración
│   ├── test_full_pipeline.py
│   └── test_batch_processing.py
├── fixtures/               # Datos de prueba
│   ├── sample_audio.mp3
│   └── sample_video.mp4
└── conftest.py            # Configuración compartida
```

### Ejecutar Pruebas

```bash
# Ejecutar todas las pruebas
pytest

# Ejecutar con cobertura
pytest --cov=. --cov-report=html

# Ejecutar tipos específicos de pruebas
pytest -m unit          # Solo pruebas unitarias
pytest -m integration   # Solo pruebas de integración

# Ejecutar con salida verbose
pytest -v

# Ejecutar archivo de prueba específico
pytest tests/unit/test_app.py
```

## 📚 Estándares de Documentación

### Documentación de Código

```python
# Usar docstrings estilo Google
def procesar_video(
    url: str,
    formato_salida: str = "mp4",
    calidad: str = "best"
) -> str:
    """
    Procesar video desde URL con parámetros especificados.
    
    Esta función descarga y procesa video desde plataformas compatibles,
    aplicando la configuración de calidad y formato especificada.
    
    Args:
        url: URL del video de plataforma compatible.
        formato_salida: Formato de salida deseado. 'mp4', 'mkv', 'avi'.
        calidad: Configuración de calidad. 'best', 'worst', o '720p'.
    
    Returns:
        Ruta al archivo de video procesado como string.
    
    Raises:
        ValueError: Si el formato de URL es inválido.
        DownloadError: Si el video no se puede descargar.
        ProcessingError: Si el procesamiento del video falla.
    
    Example:
        >>> video_path = procesar_video("https://www.youtube.com/watch?v=ID")
        >>> print(f"Video guardado en: {video_path}")
    """
```

## 🐛 Reportes de Errores

### Plantilla de Reporte de Error

```markdown
## 🐛 Reporte de Error

### Descripción
Una descripción clara de qué es el error.

### Comportamiento Esperado
Lo que esperabas que pasara.

### Comportamiento Actual
Lo que realmente pasó.

### Pasos para Reproducir
1. Ve a '...'
2. Haz clic en '....'
3. Desplázate hacia '....'
4. Ve el error

### Entorno
- SO: [ej. macOS 12.0, Ubuntu 20.04, Windows 11]
- Versión de Python: [ej. 3.9.7]
- Versión del Proyecto: [ej. 1.2.3]
- Versión de FFmpeg: [salida de `ffmpeg -version`]

### Salida del Error
```
Pegar mensajes de error aquí
```

### Contexto Adicional
Añadir cualquier otro contexto sobre el problema.
```

## 💡 Solicitudes de Características

### Plantilla de Solicitud de Característica

```markdown
## 🚀 Solicitud de Característica

### Resumen
Descripción breve de la característica que te gustaría ver.

### Motivación
¿Por qué se necesita esta característica? ¿Qué problema resuelve?

### Descripción Detallada
Proporciona una descripción detallada de la característica.

### Casos de Uso
- Caso de uso 1: [descripción]
- Caso de uso 2: [descripción]
- Caso de uso 3: [descripción]

### Implementación Propuesta
Si tienes ideas sobre cómo podría implementarse.

### Alternativas Consideradas
¿Qué otros enfoques has considerado?
```

## 🚀 Proceso de Lanzamiento

### Numeración de Versiones

Usamos [Versionado Semántico](https://semver.org/):

- **MAYOR**: Cambios que rompen compatibilidad
- **MENOR**: Nuevas características (compatible hacia atrás)
- **PARCHE**: Correcciones de errores (compatible hacia atrás)

## 🤝 Guías de Comunidad

### Código de Conducta

Estamos comprometidos a proporcionar una experiencia acogedora e inclusiva para todos. Esperamos que todos los colaboradores:

- **Sean Respetuosos**: Traten a todos con respeto y amabilidad
- **Sean Colaborativos**: Trabajen juntos hacia objetivos comunes
- **Sean Inclusivos**: Den la bienvenida a recién llegados
- **Sean Profesionales**: Mantengan comunicación profesional
- **Sean Pacientes**: Ayuden a otros a aprender y crecer

### Canales de Comunicación

- **GitHub Issues**: Reportes de errores y solicitudes de características
- **GitHub Discussions**: Preguntas generales y chat de comunidad
- **Discord**: Chat en tiempo real y discusiones de voz
- **Email**: Contacto directo con mantenedores

### Obtener Ayuda

Si necesitas ayuda:

1. **Revisa la Documentación**: README, referencia de API, y guías
2. **Busca Issues**: Busca preguntas o problemas similares
3. **Pregunta en Discussions**: Publica en GitHub Discussions
4. **Únete a Discord**: Obtén ayuda en tiempo real de la comunidad
5. **Contacta Mantenedores**: Email para asuntos urgentes

### Reconocimiento

Reconocemos a los colaboradores de varias maneras:

- **Lista de Colaboradores**: Listados en README.md y repositorio
- **Notas de Lanzamiento**: Contribuciones importantes mencionadas
- **Salón de la Fama**: Reconocimiento especial para contribuciones significativas
- **Swag**: Stickers y camisetas para colaboradores activos

---

## 📞 Contacto

Para preguntas sobre contribuir:

- 📧 **Email**: maintainers@youtube-dl-suite.com
- 💬 **Discord**: [Únete a nuestro servidor](https://discord.gg/INVITE_LINK)
- 📱 **Twitter**: [@YouTubeDLSuite](https://twitter.com/YouTubeDLSuite)
- 🐙 **GitHub**: [Abrir una discusión](https://github.com/OWNER/REPO/discussions)

¡Gracias por contribuir a la Suite de YouTube DL! 🎉

---

*Última actualización: 2024-01-15*