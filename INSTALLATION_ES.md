# 📦 Guía de Instalación

Guía completa de instalación para la Suite de Procesamiento de Audio y Video de YouTube DL.

## 🎯 Requisitos del Sistema

### Requisitos Mínimos
- **Sistema Operativo**: Windows 10, macOS 10.14, o Ubuntu 18.04+
- **Python**: 3.7 o superior
- **RAM**: 4GB mínimo (8GB recomendado)
- **Almacenamiento**: 5GB de espacio libre mínimo (20GB recomendado)
- **Internet**: Conexión estable para descargas

### Requisitos Recomendados
- **CPU**: 4+ núcleos, 3GHz+
- **RAM**: 8GB+ (16GB para archivos grandes)
- **Almacenamiento**: SSD con 50GB+ de espacio libre
- **GPU**: GPU NVIDIA con soporte CUDA (opcional, para aceleración)

## 🛠️ Instalación Paso a Paso

### Paso 1: Instalar Dependencias del Sistema

#### 🍎 Instalación en macOS

```bash
# Instalar Homebrew (si no está instalado)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Instalar Python 3 y FFmpeg
brew install python3 ffmpeg

# Verificar instalaciones
python3 --version  # Debería mostrar 3.7+
ffmpeg -version    # Debería mostrar la versión de FFmpeg
```

#### 🐧 Instalación en Ubuntu/Debian

```bash
# Actualizar lista de paquetes
sudo apt update && sudo apt upgrade -y

# Instalar Python, pip y dependencias del sistema
sudo apt install -y python3 python3-pip python3-venv python3-dev
sudo apt install -y ffmpeg git curl wget

# Instalar bibliotecas adicionales de audio/video
sudo apt install -y libsndfile1 libsndfile1-dev
sudo apt install -y libavcodec-dev libavformat-dev libswscale-dev

# Verificar instalaciones
python3 --version
ffmpeg -version
```

#### 🏢 Instalación en CentOS/RHEL

```bash
# Habilitar repositorio EPEL
sudo yum install -y epel-release

# Instalar Python y herramientas de desarrollo
sudo yum groupinstall -y "Development Tools"
sudo yum install -y python3 python3-pip python3-devel

# Instalar FFmpeg (desde RPM Fusion)
sudo yum install -y https://download1.rpmfusion.org/free/el/rpmfusion-free-release-7.noarch.rpm
sudo yum install -y ffmpeg ffmpeg-devel

# Instalar dependencias adicionales
sudo yum install -y libsndfile-devel
```

#### 🪟 Instalación en Windows

**Opción 1: Usando Chocolatey (Recomendado)**
```powershell
# Instalar Chocolatey (si no está instalado)
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Instalar Python y FFmpeg
choco install python3 ffmpeg git

# Actualizar variables de entorno
refreshenv
```

**Opción 2: Instalación Manual**
1. Descargar Python 3.7+ desde [python.org](https://www.python.org/downloads/)
2. Descargar FFmpeg desde [ffmpeg.org](https://ffmpeg.org/download.html#build-windows)
3. Añadir ambos al PATH del sistema
4. Instalar Git desde [git-scm.com](https://git-scm.com/download/win)

### Paso 2: Descargar el Proyecto

```bash
# Opción 1: Usando Git (recomendado)
git clone <repository-url>
cd "Youtube DL"

# Opción 2: Descargar ZIP
# Descargar y extraer el archivo ZIP del proyecto
# Navegar a la carpeta extraída
```

### Paso 3: Crear Entorno Virtual de Python

```bash
# Navegar al directorio del proyecto
cd "/ruta/a/Youtube DL"

# Crear entorno virtual
python3 -m venv .venv

# Activar entorno virtual
# En macOS/Linux:
source .venv/bin/activate

# En Windows:
.venv\Scripts\activate

# Deberías ver (.venv) en tu prompt de terminal
```

### Paso 4: Instalar Dependencias de Python

```bash
# Asegurar que estás en el entorno virtual
# Actualizar pip a la última versión
pip install --upgrade pip setuptools wheel

# Instalar dependencias del proyecto
pip install -r requirements.txt

# Verificar instalaciones clave
python -c "import yt_dlp; print('✅ yt-dlp instalado')"
python -c "import librosa; print('✅ librosa instalado')"
python -c "import moviepy; print('✅ moviepy instalado')"
```

### Paso 5: Instalar Spleeter (Separación de Audio)

Spleeter requiere un entorno separado debido a las dependencias de TensorFlow:

```bash
# Crear entorno virtual de Spleeter
python3 -m venv spleeter_env

# Activar entorno de Spleeter
# En macOS/Linux:
source spleeter_env/bin/activate

# En Windows:
spleeter_env\Scripts\activate

# Instalar Spleeter con TensorFlow
pip install --upgrade pip
pip install spleeter[tensorflow]

# Para soporte GPU (solo NVIDIA):
# pip install spleeter[tensorflow-gpu]

# Probar instalación de Spleeter
spleeter separate -h

# Desactivar entorno de Spleeter
deactivate

# Regresar al entorno principal del proyecto
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate   # Windows
```

### Paso 6: Verificar Instalación

Ejecutar el script de verificación:

```bash
# Crear y ejecutar script de verificación
python3 -c "
print('🔍 Verificando instalación...\n')

# Probar imports
try:
    import yt_dlp
    print('✅ yt-dlp: OK')
except ImportError:
    print('❌ yt-dlp: FALLÓ')

try:
    import librosa
    print('✅ librosa: OK')
except ImportError:
    print('❌ librosa: FALLÓ')

try:
    import soundfile
    print('✅ soundfile: OK')
except ImportError:
    print('❌ soundfile: FALLÓ')

try:
    import moviepy
    print('✅ moviepy: OK')
except ImportError:
    print('❌ moviepy: FALLÓ')

try:
    import stable_whisper
    print('✅ stable-whisper: OK')
except ImportError:
    print('❌ stable-whisper: FALLÓ')

# Probar FFmpeg
import subprocess
try:
    result = subprocess.run(['ffmpeg', '-version'], 
                          capture_output=True, text=True)
    if result.returncode == 0:
        print('✅ FFmpeg: OK')
    else:
        print('❌ FFmpeg: FALLÓ')
except FileNotFoundError:
    print('❌ FFmpeg: NO ENCONTRADO')

# Probar Spleeter
try:
    result = subprocess.run(['spleeter_env/bin/spleeter', '-h'], 
                          capture_output=True, text=True)
    if result.returncode == 0:
        print('✅ Spleeter: OK')
    else:
        print('❌ Spleeter: Revisar instalación')
except FileNotFoundError:
    print('⚠️  Spleeter: Ejecutar desde spleeter_env')

print('\n🎉 ¡Verificación de instalación completa!')
"
```

## 🔧 Opciones de Instalación Avanzada

### Configuración de Aceleración GPU (NVIDIA)

Para procesamiento más rápido con GPUs NVIDIA:

```bash
# Verificar si CUDA está disponible
nvidia-smi

# Instalar CUDA toolkit (si no está instalado)
# Visitar: https://developer.nvidia.com/cuda-downloads

# Instalar TensorFlow acelerado por GPU en el entorno de Spleeter
source spleeter_env/bin/activate
pip uninstall tensorflow
pip install tensorflow-gpu==2.8.0

# Probar disponibilidad de GPU
python -c "
import tensorflow as tf
print('GPU Disponible:', tf.config.list_physical_devices('GPU'))
"
```

### Instalación con Docker (Alternativa)

Para despliegue en contenedores:

```bash
# Crear Dockerfile
cat > Dockerfile << EOF
FROM python:3.9-slim

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \\
    ffmpeg \\
    git \\
    && rm -rf /var/lib/apt/lists/*

# Establecer directorio de trabajo
WORKDIR /app

# Copiar requirements
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install -r requirements.txt

# Copiar código de aplicación
COPY . .

# Crear directorios
RUN mkdir -p downloads temp output

# Establecer comando por defecto
CMD ["python", "app.py"]
EOF

# Construir imagen Docker
docker build -t youtube-dl-suite .

# Ejecutar contenedor
docker run -it -v $(pwd)/downloads:/app/downloads youtube-dl-suite
```

### Instalación para Desarrollo

Para colaboradores y desarrolladores:

```bash
# Clonar repositorio
git clone <repository-url>
cd "Youtube DL"

# Instalar dependencias de desarrollo
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Instalar hooks de pre-commit
pre-commit install

# Ejecutar pruebas
pytest tests/
```

## 🐛 Solución de Problemas de Instalación

### Problemas Comunes y Soluciones

#### Problemas de Versión de Python
```bash
# Error: Se requiere Python 3.7+
# Solución: Instalar versión correcta de Python

# Verificar versión actual
python3 --version

# Instalar Python 3.9 (Ubuntu)
sudo apt install python3.9 python3.9-venv python3.9-dev

# Usar versión específica
python3.9 -m venv .venv
```

#### Problemas de Instalación de FFmpeg
```bash
# Error: FFmpeg no encontrado
# Solución depende del SO:

# Ubuntu: Añadir repositorio universe
sudo add-apt-repository universe
sudo apt update
sudo apt install ffmpeg

# macOS: Instalar vía Homebrew
brew install ffmpeg

# Windows: Añadir al PATH
# Descargar desde https://ffmpeg.org/download.html
# Extraer a C:\ffmpeg
# Añadir C:\ffmpeg\bin al PATH del sistema
```

#### Problemas de Permisos
```bash
# Error: Permiso denegado
# Solución: Corregir permisos

# Hacer directorios escribibles
chmod 755 downloads temp output

# Corregir permisos del entorno virtual
chmod -R 755 .venv spleeter_env

# En Windows, ejecutar como Administrador
```

#### Problemas de Memoria Durante la Instalación
```bash
# Error: Sin memoria durante pip install
# Solución: Instalar paquetes individualmente

pip install yt-dlp
pip install librosa
pip install soundfile
pip install moviepy
pip install stable-whisper

# Usar opción no-cache
pip install --no-cache-dir -r requirements.txt
```

#### Problemas de TensorFlow/Spleeter
```bash
# Error: Compatibilidad de TensorFlow
# Solución: Usar versiones específicas

# Desinstalar versiones conflictivas
pip uninstall tensorflow tensorflow-gpu

# Instalar versión compatible
pip install tensorflow==2.8.0

# Para Macs con Apple Silicon
pip install tensorflow-macos tensorflow-metal
```

#### Problemas de Red/Firewall
```bash
# Error: Errores SSL/Red
# Solución: Configurar pip

# Usar hosts confiables
pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org -r requirements.txt

# Usar proxy (si es necesario)
pip install --proxy http://proxy.company.com:port -r requirements.txt
```

### Problemas Específicos de Plataforma

#### Problemas en macOS
```bash
# Error: Command Line Tools no instaladas
xcode-select --install

# Error: Permiso denegado en Homebrew
sudo chown -R $(whoami) /usr/local/var/homebrew
```

#### Problemas en Windows
```powershell
# Error: Microsoft Visual C++ requerido
# Solución: Instalar Visual Studio Build Tools
# Descargar desde: https://visualstudio.microsoft.com/visual-cpp-build-tools/

# Error: Soporte de rutas largas
# Habilitar rutas largas en Windows 10/11:
# Abrir Editor de Directivas de Grupo (gpedit.msc)
# Navegar a: Configuración del equipo > Plantillas administrativas > Sistema > Sistema de archivos
# Habilitar "Habilitar rutas largas de Win32"
```

#### Problemas en Linux
```bash
# Error: Headers de desarrollo faltantes
sudo apt install python3-dev build-essential

# Error: Problemas de biblioteca de audio
sudo apt install libasound2-dev portaudio19-dev

# Error: Problemas de certificado SSL
pip install --upgrade certifi
```

## ✅ Configuración Post-Instalación

### Crear Estructura de Directorios
```bash
# Crear directorios requeridos
mkdir -p downloads temp output logs

# Establecer permisos
chmod 755 downloads temp output logs
```

### Configuración del Entorno
```bash
# Crear archivo .env para configuraciones personalizadas
cat > .env << EOF
# Rutas personalizadas
DOWNLOAD_PATH=./downloads
TEMP_PATH=./temp
OUTPUT_PATH=./output

# Configuraciones de procesamiento
MAX_WORKERS=4
WHISPER_MODEL=base
AUDIO_QUALITY=192

# Registro
LOG_LEVEL=INFO
LOG_FILE=./logs/app.log
EOF
```

### Probar Instalación
```bash
# Prueba rápida de funcionalidad
python3 -c "
from app import convert_to_audio
print('✅ Procesamiento de audio: Listo')
"

python3 -c "
from movies import download_movie
print('✅ Descarga de videos: Listo')
"

python3 -c "
from karaoke_generator import main
print('✅ Generación de karaoke: Listo')
"
```

## 🚀 Próximos Pasos

Después de una instalación exitosa:

1. **Lee el README_ES.md principal** para instrucciones de uso
2. **Prueba los ejemplos de Inicio Rápido**
3. **Configura ajustes** en las aplicaciones
4. **Únete a la comunidad** para soporte y actualizaciones

### Primeros Pasos Recomendados
```bash
# Probar con un video corto
python3 app.py
# Ingresa: https://www.youtube.com/watch?v=dQw4w9WgXcQ

# Crear tu primer video de karaoke
python3 karaoke_generator.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

---

## 📞 Soporte de Instalación

Si encuentras problemas no cubiertos aquí:

1. **Revisa los logs**: Busca en el directorio `logs/` para detalles de errores
2. **Busca problemas existentes**: Revisa los issues de GitHub para problemas similares
3. **Crea un nuevo issue**: Proporciona la salida completa del error e información del sistema
4. **Únete a nuestro Discord**: Obtén ayuda en tiempo real de la comunidad

### Recopilación de Información del Sistema
```bash
# Recopilar información del sistema para reportes de errores
python3 -c "
import platform
import sys
print(f'SO: {platform.system()} {platform.release()}')
print(f'Python: {sys.version}')
print(f'Arquitectura: {platform.machine()}')
"

pip list | grep -E 'yt-dlp|librosa|moviepy|tensorflow'
```

**¡Feliz instalación! 🎉**