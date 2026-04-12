# 📦 Installation Guide

Complete installation guide for the YouTube DL Audio & Video Processing Suite.

## 🎯 System Requirements

### Minimum Requirements
- **Operating System**: Windows 10, macOS 10.14, or Ubuntu 18.04+
- **Python**: 3.7 or higher
- **RAM**: 4GB minimum (8GB recommended)
- **Storage**: 5GB free space minimum (20GB recommended)
- **Internet**: Stable connection for downloads

### Recommended Requirements
- **CPU**: 4+ cores, 3GHz+
- **RAM**: 8GB+ (16GB for large files)
- **Storage**: SSD with 50GB+ free space
- **GPU**: NVIDIA GPU with CUDA support (optional, for acceleration)

## 🛠️ Step-by-Step Installation

### Step 1: Install System Dependencies

#### 🍎 macOS Installation

```bash
# Install Homebrew (if not already installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python 3 and FFmpeg
brew install python3 ffmpeg

# Verify installations
python3 --version  # Should show 3.7+
ffmpeg -version    # Should show FFmpeg version
```

#### 🐧 Ubuntu/Debian Installation

```bash
# Update package list
sudo apt update && sudo apt upgrade -y

# Install Python, pip, and system dependencies
sudo apt install -y python3 python3-pip python3-venv python3-dev
sudo apt install -y ffmpeg git curl wget

# Install additional audio/video libraries
sudo apt install -y libsndfile1 libsndfile1-dev
sudo apt install -y libavcodec-dev libavformat-dev libswscale-dev

# Verify installations
python3 --version
ffmpeg -version
```

#### 🏢 CentOS/RHEL Installation

```bash
# Enable EPEL repository
sudo yum install -y epel-release

# Install Python and development tools
sudo yum groupinstall -y "Development Tools"
sudo yum install -y python3 python3-pip python3-devel

# Install FFmpeg (from RPM Fusion)
sudo yum install -y https://download1.rpmfusion.org/free/el/rpmfusion-free-release-7.noarch.rpm
sudo yum install -y ffmpeg ffmpeg-devel

# Install additional dependencies
sudo yum install -y libsndfile-devel
```

#### 🪟 Windows Installation

**Option 1: Using Chocolatey (Recommended)**
```powershell
# Install Chocolatey (if not installed)
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Install Python and FFmpeg
choco install python3 ffmpeg git

# Refresh environment variables
refreshenv
```

**Option 2: Manual Installation**
1. Download Python 3.7+ from [python.org](https://www.python.org/downloads/)
2. Download FFmpeg from [ffmpeg.org](https://ffmpeg.org/download.html#build-windows)
3. Add both to your system PATH
4. Install Git from [git-scm.com](https://git-scm.com/download/win)

### Step 2: Download the Project

```bash
# Option 1: Using Git (recommended)
git clone <repository-url>
cd "Youtube DL"

# Option 2: Download ZIP
# Download and extract the project ZIP file
# Navigate to the extracted folder
```

### Step 3: Create Python Virtual Environment

```bash
# Navigate to project directory
cd "/path/to/Youtube DL"

# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
# On macOS/Linux:
source .venv/bin/activate

# On Windows:
.venv\Scripts\activate

# You should see (.venv) in your terminal prompt
```

### Step 4: Install Python Dependencies

```bash
# Ensure you're in the virtual environment
# Update pip to latest version
pip install --upgrade pip setuptools wheel

# Install project dependencies
pip install -r requirements.txt

# Verify key installations
python -c "import yt_dlp; print('✅ yt-dlp installed')"
python -c "import librosa; print('✅ librosa installed')"
python -c "import moviepy; print('✅ moviepy installed')"
```

### Step 5: Install Spleeter (Audio Separation)

Spleeter requires a separate environment due to TensorFlow dependencies:

```bash
# Create Spleeter virtual environment
python3 -m venv spleeter_env

# Activate Spleeter environment
# On macOS/Linux:
source spleeter_env/bin/activate

# On Windows:
spleeter_env\Scripts\activate

# Install Spleeter with TensorFlow
pip install --upgrade pip
pip install spleeter[tensorflow]

# For GPU support (NVIDIA only):
# pip install spleeter[tensorflow-gpu]

# Test Spleeter installation
spleeter separate -h

# Deactivate Spleeter environment
deactivate

# Return to main project environment
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate   # Windows
```

### Step 6: Verify Installation

Run the verification script:

```bash
# Create and run verification script
python3 -c "
print('🔍 Verifying installation...\n')

# Test imports
try:
    import yt_dlp
    print('✅ yt-dlp: OK')
except ImportError:
    print('❌ yt-dlp: FAILED')

try:
    import librosa
    print('✅ librosa: OK')
except ImportError:
    print('❌ librosa: FAILED')

try:
    import soundfile
    print('✅ soundfile: OK')
except ImportError:
    print('❌ soundfile: FAILED')

try:
    import moviepy
    print('✅ moviepy: OK')
except ImportError:
    print('❌ moviepy: FAILED')

try:
    import stable_whisper
    print('✅ stable-whisper: OK')
except ImportError:
    print('❌ stable-whisper: FAILED')

# Test FFmpeg
import subprocess
try:
    result = subprocess.run(['ffmpeg', '-version'], 
                          capture_output=True, text=True)
    if result.returncode == 0:
        print('✅ FFmpeg: OK')
    else:
        print('❌ FFmpeg: FAILED')
except FileNotFoundError:
    print('❌ FFmpeg: NOT FOUND')

# Test Spleeter
try:
    result = subprocess.run(['spleeter_env/bin/spleeter', '-h'], 
                          capture_output=True, text=True)
    if result.returncode == 0:
        print('✅ Spleeter: OK')
    else:
        print('❌ Spleeter: Check installation')
except FileNotFoundError:
    print('⚠️  Spleeter: Run from spleeter_env')

print('\n🎉 Installation verification complete!')
"
```

## 🔧 Advanced Installation Options

### GPU Acceleration Setup (NVIDIA)

For faster processing with NVIDIA GPUs:

```bash
# Check if CUDA is available
nvidia-smi

# Install CUDA toolkit (if not already installed)
# Visit: https://developer.nvidia.com/cuda-downloads

# Install GPU-accelerated TensorFlow in Spleeter environment
source spleeter_env/bin/activate
pip uninstall tensorflow
pip install tensorflow-gpu==2.8.0

# Test GPU availability
python -c "
import tensorflow as tf
print('GPU Available:', tf.config.list_physical_devices('GPU'))
"
```

### Docker Installation (Alternative)

For containerized deployment:

```bash
# Create Dockerfile
cat > Dockerfile << EOF
FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    ffmpeg \\
    git \\
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install -r requirements.txt

# Copy application code
COPY . .

# Create directories
RUN mkdir -p downloads temp output

# Set default command
CMD ["python", "app.py"]
EOF

# Build Docker image
docker build -t youtube-dl-suite .

# Run container
docker run -it -v $(pwd)/downloads:/app/downloads youtube-dl-suite
```

### Development Installation

For contributors and developers:

```bash
# Clone repository
git clone <repository-url>
cd "Youtube DL"

# Install development dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install

# Run tests
pytest tests/
```

## 🐛 Troubleshooting Installation

### Common Issues and Solutions

#### Python Version Issues
```bash
# Error: Python 3.7+ required
# Solution: Install correct Python version

# Check current version
python3 --version

# Install Python 3.9 (Ubuntu)
sudo apt install python3.9 python3.9-venv python3.9-dev

# Use specific version
python3.9 -m venv .venv
```

#### FFmpeg Installation Issues
```bash
# Error: FFmpeg not found
# Solution depends on OS:

# Ubuntu: Add universe repository
sudo add-apt-repository universe
sudo apt update
sudo apt install ffmpeg

# macOS: Install via Homebrew
brew install ffmpeg

# Windows: Add to PATH
# Download from https://ffmpeg.org/download.html
# Extract to C:\ffmpeg
# Add C:\ffmpeg\bin to system PATH
```

#### Permission Issues
```bash
# Error: Permission denied
# Solution: Fix permissions

# Make directories writable
chmod 755 downloads temp output

# Fix virtual environment permissions
chmod -R 755 .venv spleeter_env

# On Windows, run as Administrator
```

#### Memory Issues During Installation
```bash
# Error: Out of memory during pip install
# Solution: Install packages individually

pip install yt-dlp
pip install librosa
pip install soundfile
pip install moviepy
pip install stable-whisper

# Use no-cache option
pip install --no-cache-dir -r requirements.txt
```

#### TensorFlow/Spleeter Issues
```bash
# Error: TensorFlow compatibility
# Solution: Use specific versions

# Uninstall conflicting versions
pip uninstall tensorflow tensorflow-gpu

# Install compatible version
pip install tensorflow==2.8.0

# For Apple Silicon Macs
pip install tensorflow-macos tensorflow-metal
```

#### Network/Firewall Issues
```bash
# Error: SSL/Network errors
# Solution: Configure pip

# Use trusted hosts
pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org -r requirements.txt

# Use proxy (if needed)
pip install --proxy http://proxy.company.com:port -r requirements.txt
```

### Platform-Specific Issues

#### macOS Issues
```bash
# Error: Command Line Tools not installed
xcode-select --install

# Error: Permission denied on Homebrew
sudo chown -R $(whoami) /usr/local/var/homebrew
```

#### Windows Issues
```powershell
# Error: Microsoft Visual C++ required
# Solution: Install Visual Studio Build Tools
# Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/

# Error: Long path support
# Enable long paths in Windows 10/11:
# Open Group Policy Editor (gpedit.msc)
# Navigate to: Computer Configuration > Administrative Templates > System > Filesystem
# Enable "Enable Win32 long paths"
```

#### Linux Issues
```bash
# Error: Missing development headers
sudo apt install python3-dev build-essential

# Error: Audio library issues
sudo apt install libasound2-dev portaudio19-dev

# Error: SSL certificate issues
pip install --upgrade certifi
```

## ✅ Post-Installation Setup

### Create Directory Structure
```bash
# Create required directories
mkdir -p downloads temp output logs

# Set permissions
chmod 755 downloads temp output logs
```

### Environment Configuration
```bash
# Create .env file for custom settings
cat > .env << EOF
# Custom paths
DOWNLOAD_PATH=./downloads
TEMP_PATH=./temp
OUTPUT_PATH=./output

# Processing settings
MAX_WORKERS=4
WHISPER_MODEL=base
AUDIO_QUALITY=192

# Logging
LOG_LEVEL=INFO
LOG_FILE=./logs/app.log
EOF
```

### Test Installation
```bash
# Quick functionality test
python3 -c "
from app import convert_to_audio
print('✅ Audio processing: Ready')
"

python3 -c "
from movies import download_movie
print('✅ Video downloading: Ready')
"

python3 -c "
from karaoke_generator import main
print('✅ Karaoke generation: Ready')
"
```

## 🚀 Next Steps

After successful installation:

1. **Read the main README.md** for usage instructions
2. **Try the Quick Start examples**
3. **Configure settings** in the applications
4. **Join the community** for support and updates

### Recommended First Steps
```bash
# Test with a short video
python3 app.py
# Enter: https://www.youtube.com/watch?v=dQw4w9WgXcQ

# Create your first karaoke video
python3 karaoke_generator.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

---

## 📞 Installation Support

If you encounter issues not covered here:

1. **Check the logs**: Look in `logs/` directory for error details
2. **Search existing issues**: Check GitHub issues for similar problems
3. **Create a new issue**: Provide full error output and system info
4. **Join our Discord**: Get real-time help from the community

### System Information Collection
```bash
# Collect system info for bug reports
python3 -c "
import platform
import sys
print(f'OS: {platform.system()} {platform.release()}')
print(f'Python: {sys.version}')
print(f'Architecture: {platform.machine()}')
"

pip list | grep -E 'yt-dlp|librosa|moviepy|tensorflow'
```

**Happy installing! 🎉**