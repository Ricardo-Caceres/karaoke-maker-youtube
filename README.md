# YouTube DL Audio & Video Processing Suite

A comprehensive Python toolkit for downloading, processing, and creating karaoke content from YouTube and other video platforms. This suite includes three main applications for different media processing needs.

![Python Version](https://img.shields.io/badge/python-3.7%2B-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Applications](#applications)
  - [Audio Processor (app.py)](#audio-processor-apppy)
  - [Karaoke Generator](#karaoke-generator-karaoke_generatorpy)
  - [Movie Downloader](#movie-downloader-moviespy)
- [Usage Examples](#usage-examples)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

This project provides a complete solution for:
- **Audio Extraction**: Convert YouTube videos to high-quality audio files
- **Voice Separation**: Separate vocals from instrumental tracks
- **Karaoke Creation**: Generate synchronized karaoke videos with lyrics
- **Video Downloading**: Download videos from various platforms

## ✨ Features

### 🎵 Audio Processing
- High-quality audio extraction (192kbps MP3)
- Advanced voice/music separation using Librosa
- Support for multiple audio formats
- Batch processing capabilities

### 🎤 Karaoke Generation
- Automatic lyrics transcription using Whisper AI
- Synchronized subtitle generation
- Customizable video styling
- Multiple export formats

### 📹 Video Downloading
- Support for 100+ video platforms
- Best quality automatic selection
- Bulk download capabilities
- Progress tracking

### 🔧 Technical Features
- Cross-platform compatibility (Windows, macOS, Linux)
- Robust error handling
- Modular architecture
- Extensive logging
- Memory-efficient processing

## 🚀 Installation

### Prerequisites

- Python 3.7 or higher
- FFmpeg (required for audio/video processing)
- At least 2GB free disk space

### System Dependencies

#### macOS
```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install FFmpeg
brew install ffmpeg
```

#### Ubuntu/Debian
```bash
sudo apt update
sudo apt install ffmpeg python3-pip python3-venv
```

#### Windows
```bash
# Install FFmpeg using Chocolatey
choco install ffmpeg

# Or download from: https://ffmpeg.org/download.html
```

### Python Environment Setup

1. **Clone or download the project**
```bash
git clone <repository-url>
cd "Youtube DL"
```

2. **Create virtual environment**
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install Python dependencies**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

4. **Install Spleeter (for karaoke generation)**
```bash
# Create Spleeter environment
python3 -m venv spleeter_env
source spleeter_env/bin/activate  # On Windows: spleeter_env\Scripts\activate
pip install spleeter[tensorflow]
deactivate
```

### Verification
```bash
# Test installations
python3 -c "import yt_dlp, librosa, moviepy; print('All dependencies installed successfully!')"
```

## 🏃‍♂️ Quick Start

### Basic Audio Extraction
```bash
python3 app.py
# Enter YouTube URL when prompted
```

### Generate Karaoke Video
```bash
python3 karaoke_generator.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

### Download Video
```bash
python3 movies.py
# Enter video URL when prompted
```

## 📱 Applications

### Audio Processor (app.py)

**Purpose**: Convert YouTube videos to audio and separate vocals from instrumentals.

#### Features:
- **High-Quality Audio Extraction**: Converts videos to 192kbps MP3
- **Voice Separation**: Uses harmonic-percussive separation
- **Automatic Processing**: Handles the entire pipeline automatically

#### Usage:
```bash
python3 app.py
```

#### Process Flow:
1. Prompts for YouTube URL
2. Downloads audio in best available quality
3. Converts to MP3 format
4. Separates vocals and background music
5. Saves files to `downloads/` directory

#### Output Files:
- `downloads/{video_title}.mp3` - Original audio
- `downloads/voice.wav` - Extracted vocals
- `downloads/background.wav` - Background music

#### Code Example:
```python
from app import convert_to_audio, separate_voice

# Convert video to audio
audio_file = convert_to_audio("https://youtube.com/watch?v=...")

# Separate vocals from background
separate_voice(audio_file)
```

### Karaoke Generator (karaoke_generator.py)

**Purpose**: Create professional karaoke videos with synchronized lyrics.

#### Features:
- **AI-Powered Transcription**: Uses Whisper for accurate lyrics
- **Source Separation**: Creates clean instrumental tracks
- **Video Generation**: Produces MP4 karaoke videos
- **Customizable Styling**: Adjustable fonts, colors, and layouts

#### Usage:
```bash
python3 karaoke_generator.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

#### Command Line Options:
```bash
# Basic usage
python3 karaoke_generator.py "YOUTUBE_URL"

# The script automatically:
# 1. Downloads audio
# 2. Separates vocals/instrumental
# 3. Generates timed lyrics
# 4. Creates karaoke video
```

#### Process Pipeline:

1. **Audio Download**
   - Extracts audio from YouTube
   - Saves as MP3 in `temp/` directory

2. **Vocal Separation**
   - Uses Spleeter AI for clean separation
   - Generates `vocals.wav` and `accompaniment.wav`

3. **Lyrics Generation**
   - Transcribes vocals using Whisper AI
   - Creates time-synchronized lyrics
   - Groups words into readable lines

4. **Video Creation**
   - Creates 1280x720 HD video
   - Adds synchronized subtitle overlay
   - Exports as MP4 with instrumental audio

#### Output:
- `output/{song_title}_karaoke.mp4` - Final karaoke video
- `temp/{song_title}/` - Intermediate files

#### Configuration Options:

Edit the `create_karaoke_video()` function to customize:

```python
# Video settings
RESOLUTION = (1280, 720)  # HD resolution
BACKGROUND_COLOR = (25, 25, 112)  # Dark blue
FONT_SIZE = 60
FONT_COLOR = 'white'
HIGHLIGHT_COLOR = 'yellow'

# Lyrics settings  
MAX_WORDS_PER_LINE = 8  # Words per subtitle line
SUBTITLE_POSITION = 0.65  # Vertical position (0.0 = top, 1.0 = bottom)
```

### Movie Downloader (movies.py)

**Purpose**: Download videos from various platforms in the best available quality.

#### Features:
- **Multi-Platform Support**: YouTube, Vimeo, DailyMotion, and 100+ sites
- **Quality Selection**: Automatically selects best available quality
- **Smart Naming**: Handles special characters in filenames
- **Format Detection**: Preserves original video format

#### Usage:
```bash
python3 movies.py
```

#### Supported Platforms:
- YouTube
- Vimeo  
- DailyMotion
- Twitch
- Facebook
- Instagram
- TikTok
- And many more...

#### Process:
1. Prompts for video URL
2. Extracts video metadata
3. Downloads in best available quality
4. Saves to `downloads/` directory

#### Code Integration:
```python
from movies import download_movie

# Download a video
video_path = download_movie("https://example.com/video")
print(f"Downloaded to: {video_path}")
```

## 💡 Usage Examples

### Example 1: Create Karaoke from Popular Song
```bash
# Download and create karaoke for a popular song
python3 karaoke_generator.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# Output: Rick_Astley_Never_Gonna_Give_You_Up_karaoke.mp4
```

### Example 2: Extract Audio for Remix
```bash
# Run the audio processor
python3 app.py
# Enter: https://www.youtube.com/watch?v=dQw4w9WgXcQ

# Files created:
# - downloads/Never_Gonna_Give_You_Up.mp3 (original)
# - downloads/voice.wav (vocals only)  
# - downloads/background.wav (instrumental)
```

### Example 3: Batch Processing
```python
# Create a batch processing script
import os
from karaoke_generator import main as generate_karaoke

urls = [
    "https://www.youtube.com/watch?v=VIDEO1",
    "https://www.youtube.com/watch?v=VIDEO2",
    "https://www.youtube.com/watch?v=VIDEO3"
]

for url in urls:
    try:
        os.system(f'python3 karaoke_generator.py "{url}"')
        print(f"✅ Processed: {url}")
    except Exception as e:
        print(f"❌ Failed: {url} - {e}")
```

### Example 4: Custom Audio Processing
```python
# Advanced audio processing workflow
from app import convert_to_audio, separate_voice
import librosa
import soundfile as sf

# Step 1: Convert video to audio
url = "https://www.youtube.com/watch?v=VIDEO_ID"
audio_file = convert_to_audio(url)

# Step 2: Separate vocals
separate_voice(audio_file)

# Step 3: Custom processing
y, sr = librosa.load('downloads/voice.wav')

# Apply noise reduction
y_reduced = librosa.effects.preemphasis(y)

# Save processed version
sf.write('downloads/voice_clean.wav', y_reduced, sr)
```

## ⚙️ Configuration

### Environment Variables
Create a `.env` file for custom settings:

```bash
# .env file
DOWNLOAD_PATH=/custom/path/downloads
TEMP_PATH=/custom/path/temp
OUTPUT_PATH=/custom/path/output
MAX_DOWNLOAD_SIZE=1000000000  # 1GB limit
WHISPER_MODEL=base  # tiny, base, small, medium, large
```

### Application Settings

#### app.py Configuration
```python
# Audio quality settings
AUDIO_QUALITY = '192'  # 96, 128, 192, 320
AUDIO_FORMAT = 'mp3'   # mp3, wav, flac

# Processing settings
USE_GPU = False  # Set to True if CUDA available
NOISE_REDUCTION = True
```

#### karaoke_generator.py Configuration
```python
# Video output settings
VIDEO_RESOLUTION = (1920, 1080)  # 4K: (3840, 2160)
VIDEO_FRAMERATE = 30
VIDEO_BITRATE = '5M'

# Whisper model selection
WHISPER_MODEL = 'base'  # Options: tiny, base, small, medium, large
# tiny: fastest, least accurate
# large: slowest, most accurate

# Subtitle styling
SUBTITLE_FONT = 'Arial'
SUBTITLE_SIZE = 60
SUBTITLE_COLOR = 'white'
SUBTITLE_OUTLINE = 2
```

### Directory Structure
```
Youtube DL/
├── app.py                 # Audio processor
├── karaoke_generator.py   # Karaoke creator
├── movies.py             # Video downloader
├── requirements.txt      # Python dependencies
├── .env                  # Environment settings (optional)
├── downloads/            # Downloaded files
├── temp/                 # Temporary processing files
├── output/              # Final karaoke videos
├── spleeter_env/        # Spleeter virtual environment
└── docs/                # Additional documentation
```

## 🔧 Advanced Configuration

### Custom Spleeter Models
```bash
# Download additional Spleeter models
source spleeter_env/bin/activate
pip install spleeter[tensorflow]

# Available models:
# - 2stems: vocals/accompaniment
# - 4stems: vocals/drums/bass/other  
# - 5stems: vocals/drums/bass/piano/other

# Use 4-stem separation
python3 -c "
from karaoke_generator import separate_vocals
separate_vocals('audio.mp3', model='spleeter:4stems')
"
```

### GPU Acceleration (NVIDIA)
```bash
# Install CUDA version of TensorFlow
pip install tensorflow-gpu

# Update karaoke_generator.py
import os
os.environ['CUDA_VISIBLE_DEVICES'] = '0'  # Use first GPU
```

### Memory Optimization
```python
# For large files, process in chunks
import librosa

def process_large_audio(file_path, chunk_size=30):
    """Process audio in chunks to reduce memory usage"""
    y, sr = librosa.load(file_path, duration=chunk_size)
    # Process chunk...
```

## 🐛 Troubleshooting

### Common Issues and Solutions

#### 1. FFmpeg Not Found
```bash
# Error: ffmpeg not found
# Solution:
sudo apt install ffmpeg  # Ubuntu
brew install ffmpeg      # macOS
choco install ffmpeg     # Windows
```

#### 2. Spleeter Installation Issues
```bash
# Error: TensorFlow compatibility
# Solution: Use specific versions
pip install tensorflow==2.8.0
pip install spleeter==2.3.0
```

#### 3. YouTube Download Failures
```bash
# Error: Unable to download
# Solution: Update yt-dlp
pip install --upgrade yt-dlp

# Or use alternative format
python3 -c "
import yt_dlp
ydl_opts = {'format': 'worst'}  # Try lower quality
"
```

#### 4. Memory Issues
```bash
# Error: Out of memory
# Solution: Reduce Whisper model size
# Edit karaoke_generator.py:
model = stable_whisper.load_model('tiny')  # Instead of 'base'
```

#### 5. Permission Errors
```bash
# Error: Permission denied
# Solution: Fix directory permissions
chmod 755 downloads temp output
mkdir -p downloads temp output
```

#### 6. Missing Audio in Karaoke Video
```bash
# Check audio file exists
ls -la temp/*/accompaniment.wav

# Verify audio format compatibility
ffprobe temp/*/accompaniment.wav

# Solution: Convert audio format
ffmpeg -i input.wav -ar 44100 -ac 2 output.wav
```

### Debug Mode

Enable detailed logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Add to script beginning for detailed output
import sys
sys.stdout.reconfigure(line_buffering=True)
```

### Performance Optimization

#### For Large Files
```python
# Process in chunks
CHUNK_DURATION = 30  # seconds
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB

# Use lower quality for testing
TEST_QUALITY = '96'  # kbps
PRODUCTION_QUALITY = '320'  # kbps
```

#### For Multiple Files
```bash
# Parallel processing
import multiprocessing
from concurrent.futures import ThreadPoolExecutor

def process_urls(urls):
    with ThreadPoolExecutor(max_workers=4) as executor:
        executor.map(generate_karaoke, urls)
```

## 📊 Performance Metrics

### Typical Processing Times

| Task | File Size | Processing Time | Hardware |
|------|-----------|----------------|----------|
| Audio Download | 4MB (3 min song) | 10-30 seconds | Standard Internet |
| Vocal Separation | 4MB audio | 30-60 seconds | CPU i5 |
| Lyrics Generation | 3 min song | 1-3 minutes | CPU + Whisper base |
| Video Creation | 1080p 3 min | 2-5 minutes | CPU i5 |
| **Total Pipeline** | **3 min song** | **4-9 minutes** | **Standard PC** |

### Hardware Requirements

| Component | Minimum | Recommended | Optimal |
|-----------|---------|-------------|---------|
| CPU | 2 cores, 2GHz | 4 cores, 3GHz | 8+ cores, 3.5GHz |
| RAM | 4GB | 8GB | 16GB+ |
| Storage | 5GB free | 20GB free | SSD 50GB+ |
| GPU | None | GTX 1060 | RTX 3070+ |

## 🔍 API Reference

### app.py Functions

```python
def convert_to_audio(url: str) -> str:
    """
    Convert YouTube video to audio file.
    
    Args:
        url (str): YouTube video URL
        
    Returns:
        str: Path to downloaded audio file
        
    Raises:
        yt_dlp.DownloadError: If download fails
        OSError: If file operations fail
    """

def separate_voice(audio_file: str) -> None:
    """
    Separate vocals from background music.
    
    Args:
        audio_file (str): Path to input audio file
        
    Side Effects:
        Creates voice.wav and background.wav in downloads/
        
    Raises:
        librosa.LibrosaError: If audio processing fails
    """
```

### karaoke_generator.py Functions

```python
def download_audio(youtube_url: str, output_path: str = "temp") -> tuple:
    """
    Download audio from YouTube video.
    
    Args:
        youtube_url (str): YouTube video URL
        output_path (str): Output directory path
        
    Returns:
        tuple: (audio_filename, song_title)
        
    Raises:
        subprocess.CalledProcessError: If yt-dlp fails
        FileNotFoundError: If output directory cannot be created
    """

def separate_vocals(audio_path: str, output_path: str = "temp") -> tuple:
    """
    Separate audio into vocals and instrumental tracks.
    
    Args:
        audio_path (str): Path to input audio file
        output_path (str): Output directory for separated files
        
    Returns:
        tuple: (instrumental_path, vocals_path)
        
    Raises:
        FileNotFoundError: If Spleeter not found or files missing
        subprocess.CalledProcessError: If separation fails
    """

def generate_timed_lyrics(vocals_path: str) -> list:
    """
    Generate time-synchronized lyrics from vocals.
    
    Args:
        vocals_path (str): Path to vocals audio file
        
    Returns:
        list: List of dicts with 'text', 'start', 'end' keys
        
    Raises:
        Exception: If Whisper processing fails
    """

def create_karaoke_video(instrumental_path: str, timed_lyrics: list, 
                        song_title: str, output_path: str = "output") -> None:
    """
    Create karaoke video with synchronized lyrics.
    
    Args:
        instrumental_path (str): Path to instrumental audio
        timed_lyrics (list): Time-synchronized lyrics data
        song_title (str): Title for output filename  
        output_path (str): Output directory
        
    Side Effects:
        Creates MP4 video file in output directory
        
    Raises:
        Exception: If video creation fails
    """
```

### movies.py Functions

```python
def download_movie(url: str) -> str:
    """
    Download video from supported platform.
    
    Args:
        url (str): Video URL from supported platform
        
    Returns:
        str: Path to downloaded video file
        
    Raises:
        yt_dlp.DownloadError: If download fails
        OSError: If file operations fail
    """
```

## 🤝 Contributing

We welcome contributions! Here's how to get started:

### Development Setup
```bash
# Fork the repository
git clone https://github.com/yourusername/youtube-dl-suite.git
cd youtube-dl-suite

# Create development environment
python3 -m venv dev_env
source dev_env/bin/activate

# Install development dependencies
pip install -r requirements.txt
pip install pytest black flake8 mypy

# Install pre-commit hooks
pip install pre-commit
pre-commit install
```

### Code Style
- Follow PEP 8 guidelines
- Use type hints where possible
- Add docstrings to all functions
- Maximum line length: 88 characters

### Testing
```bash
# Run tests
pytest tests/

# Run with coverage
pytest --cov=. tests/

# Type checking
mypy *.py

# Code formatting
black *.py

# Linting
flake8 *.py
```

### Submitting Changes
1. Create a feature branch: `git checkout -b feature/new-feature`
2. Make your changes with tests
3. Run the test suite: `pytest`
4. Submit a pull request with clear description

### Areas for Contribution
- [ ] Web interface (Flask/Django)
- [ ] Batch processing GUI
- [ ] Additional video platforms support
- [ ] Real-time karaoke mode
- [ ] Mobile app integration
- [ ] Docker containerization
- [ ] Cloud processing support

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### Third-Party Licenses
- **yt-dlp**: Public Domain (Unlicense)
- **FFmpeg**: LGPL v2.1+
- **Spleeter**: MIT License
- **Whisper**: MIT License
- **MoviePy**: MIT License
- **Librosa**: ISC License

## 🙏 Acknowledgments

- **yt-dlp team** for the excellent video downloading library
- **Deezer Research** for Spleeter audio source separation
- **OpenAI** for Whisper speech recognition
- **Librosa developers** for audio processing tools
- **MoviePy team** for video editing capabilities

## 📞 Support

### Getting Help
- 📖 Check this documentation first
- 🐛 [Report bugs](https://github.com/username/repo/issues)
- 💡 [Request features](https://github.com/username/repo/issues)
- 💬 [Join discussions](https://github.com/username/repo/discussions)

### Community
- Discord: [Join our server](https://discord.gg/invite)
- Reddit: [r/YouTubeDL](https://reddit.com/r/youtubedl)
- Stack Overflow: Tag with `youtube-dl-suite`

---

**Made with ❤️ by the YouTube DL Suite Team**

*Last updated: 2024*