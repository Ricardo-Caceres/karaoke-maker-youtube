# 🤝 Contributing to YouTube DL Suite

Thank you for your interest in contributing to the YouTube DL Audio & Video Processing Suite! This document provides comprehensive guidelines for contributors.

## 📋 Table of Contents

- [Getting Started](#getting-started)
- [Development Environment](#development-environment)
- [Code Standards](#code-standards)
- [Contribution Workflow](#contribution-workflow)
- [Testing Guidelines](#testing-guidelines)
- [Documentation Standards](#documentation-standards)
- [Bug Reports](#bug-reports)
- [Feature Requests](#feature-requests)
- [Release Process](#release-process)
- [Community Guidelines](#community-guidelines)

## 🚀 Getting Started

### Prerequisites

Before contributing, ensure you have:
- Python 3.7+ installed
- Git configured with your credentials
- FFmpeg installed on your system
- Basic understanding of audio/video processing concepts
- Familiarity with the project structure

### Areas Where We Need Help

We welcome contributions in these areas:

#### 🎯 High Priority
- [ ] **Performance Optimization**: Improve processing speed and memory usage
- [ ] **Error Handling**: Better error messages and recovery mechanisms
- [ ] **Platform Support**: Add support for more video platforms
- [ ] **Documentation**: Improve and expand documentation
- [ ] **Testing**: Increase test coverage and add integration tests

#### 🎨 Medium Priority
- [ ] **Web Interface**: Create a web-based GUI using Flask/Django
- [ ] **Batch Processing**: Improve bulk operations and queue management
- [ ] **Configuration Management**: Better config file support
- [ ] **Logging**: Enhanced logging and debugging features
- [ ] **Internationalization**: Multi-language support

#### 🔮 Future Ideas
- [ ] **Mobile App**: React Native or Flutter mobile interface
- [ ] **Cloud Integration**: AWS/GCP processing support
- [ ] **Real-time Processing**: Live karaoke generation
- [ ] **Advanced AI**: Better lyrics detection and timing
- [ ] **Plugin System**: Extensible architecture for custom processors

## 🛠️ Development Environment

### 1. Fork and Clone

```bash
# Fork the repository on GitHub first, then:
git clone https://github.com/YOUR_USERNAME/youtube-dl-suite.git
cd youtube-dl-suite

# Add upstream remote
git remote add upstream https://github.com/ORIGINAL_OWNER/youtube-dl-suite.git
```

### 2. Set Up Development Environment

```bash
# Create virtual environment
python3 -m venv dev_env
source dev_env/bin/activate  # On Windows: dev_env\Scripts\activate

# Install development dependencies
pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Set up Spleeter environment
python3 -m venv spleeter_env
source spleeter_env/bin/activate
pip install spleeter[tensorflow]
deactivate
source dev_env/bin/activate
```

### 3. Install Development Tools

```bash
# Code formatting and linting
pip install black flake8 isort mypy

# Testing framework
pip install pytest pytest-cov pytest-mock

# Pre-commit hooks
pip install pre-commit
pre-commit install

# Documentation tools
pip install sphinx sphinx-rtd-theme
```

### 4. Verify Installation

```bash
# Run verification script
python scripts/verify_dev_setup.py

# Run basic tests
pytest tests/ -v

# Check code formatting
black --check .
flake8 .
mypy .
```

## 📝 Code Standards

### Python Style Guidelines

We follow **PEP 8** with some modifications:

```python
# Line length: 88 characters (Black's default)
# Use double quotes for strings
example_string = "Hello, world!"

# Type hints are required for public functions
def process_audio(file_path: str, quality: int = 192) -> str:
    """Process audio file with specified quality."""
    pass

# Use descriptive variable names
audio_file_path = "downloads/song.mp3"  # ✅ Good
f = "downloads/song.mp3"                # ❌ Bad

# Constants in UPPER_CASE
DEFAULT_AUDIO_QUALITY = 192
MAX_RETRIES = 3
```

### Code Organization

```python
# Import order (use isort)
# 1. Standard library imports
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Union

# 2. Third-party imports
import librosa
import moviepy
import yt_dlp
from moviepy.editor import VideoFileClip

# 3. Local imports
from .utils import clean_filename
from .config import AudioConfig
```

### Function Documentation

```python
def separate_vocals(
    audio_path: str, 
    output_path: str = "temp", 
    model: str = "spleeter:2stems"
) -> tuple[str, str]:
    """
    Separate vocals from instrumental using Spleeter.
    
    This function uses the Spleeter library to perform source separation
    on audio files, creating separate vocal and instrumental tracks.
    
    Args:
        audio_path (str): Path to input audio file. Must be a valid audio format.
        output_path (str, optional): Directory for output files. Defaults to "temp".
        model (str, optional): Spleeter model to use. Defaults to "spleeter:2stems".
            Available models:
            - "spleeter:2stems": vocals/accompaniment
            - "spleeter:4stems": vocals/drums/bass/other
            - "spleeter:5stems": vocals/drums/bass/piano/other
    
    Returns:
        tuple[str, str]: Paths to (instrumental_file, vocals_file)
    
    Raises:
        FileNotFoundError: If input audio file doesn't exist or Spleeter not installed.
        subprocess.CalledProcessError: If Spleeter processing fails.
        ValueError: If model parameter is invalid.
    
    Example:
        >>> instrumental, vocals = separate_vocals("song.mp3")
        >>> print(f"Instrumental: {instrumental}")
        >>> print(f"Vocals: {vocals}")
        
    Note:
        This function requires Spleeter to be installed and available in PATH
        or in the spleeter_env virtual environment.
        
        Processing time depends on audio length and system performance.
        Expect approximately 30-60 seconds per minute of audio.
    """
    # Implementation here...
```

### Error Handling

```python
# Use specific exceptions
def download_audio(url: str) -> str:
    """Download audio with proper error handling."""
    
    if not url.startswith(('http://', 'https://')):
        raise ValueError(f"Invalid URL format: {url}")
    
    try:
        # Download logic here
        return audio_path
    except subprocess.CalledProcessError as e:
        # Log the error with context
        logger.error(f"yt-dlp failed for URL {url}: {e.stderr}")
        raise DownloadError(f"Failed to download audio from {url}") from e
    except Exception as e:
        logger.exception(f"Unexpected error downloading {url}")
        raise ProcessingError(f"Unexpected download failure: {e}") from e
```

### Configuration Management

```python
# Use dataclasses for configuration
from dataclasses import dataclass
from typing import Optional

@dataclass
class ProcessingConfig:
    """Configuration for audio processing operations."""
    
    audio_quality: int = 192
    video_resolution: tuple[int, int] = (1280, 720)
    output_directory: str = "output"
    temp_directory: str = "temp"
    max_workers: int = 4
    
    def __post_init__(self):
        """Validate configuration after initialization."""
        if not (96 <= self.audio_quality <= 320):
            raise ValueError(f"Invalid audio quality: {self.audio_quality}")
        
        if self.video_resolution[0] < 640 or self.video_resolution[1] < 480:
            raise ValueError("Minimum resolution is 640x480")
```

### Logging

```python
import logging
from pathlib import Path

# Set up logging
def setup_logging(level: str = "INFO", log_file: Optional[str] = None):
    """Configure logging for the application."""
    
    # Create logs directory
    if log_file:
        Path(log_file).parent.mkdir(parents=True, exist_ok=True)
    
    # Configure formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    # File handler (if specified)
    handlers = [console_handler]
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        handlers.append(file_handler)
    
    # Configure root logger
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        handlers=handlers,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

# Use in functions
logger = logging.getLogger(__name__)

def process_video(url: str) -> str:
    logger.info(f"Starting video processing for: {url}")
    
    try:
        result = do_processing(url)
        logger.info(f"Successfully processed: {url}")
        return result
    except Exception as e:
        logger.error(f"Processing failed for {url}: {e}")
        raise
```

## 🔄 Contribution Workflow

### 1. Issue First Approach

Before making changes:

```bash
# Check existing issues
# Create a new issue if needed
# Discuss approach with maintainers
# Get approval for large changes
```

### 2. Branch Naming Convention

```bash
# Feature branches
git checkout -b feature/add-batch-processing
git checkout -b feature/web-interface

# Bug fix branches  
git checkout -b fix/memory-leak-in-processor
git checkout -b fix/unicode-handling

# Documentation branches
git checkout -b docs/api-reference-update
git checkout -b docs/installation-guide

# Hotfix branches (for urgent fixes)
git checkout -b hotfix/security-vulnerability
```

### 3. Development Process

```bash
# 1. Create feature branch
git checkout -b feature/new-feature

# 2. Make changes following code standards
# Edit files...

# 3. Run tests and linting
pytest tests/
black .
flake8 .
mypy .

# 4. Commit with descriptive messages
git add .
git commit -m "feat: add batch processing for multiple URLs

- Implement concurrent processing with ThreadPoolExecutor
- Add progress tracking and error handling
- Include configuration for max workers
- Add tests for batch functionality

Closes #123"

# 5. Push and create pull request
git push origin feature/new-feature
```

### 4. Commit Message Format

We use [Conventional Commits](https://www.conventionalcommits.org/):

```bash
# Format: type(scope): description
#
# [optional body]
#
# [optional footer(s)]

# Types:
feat:     # New feature
fix:      # Bug fix
docs:     # Documentation changes
style:    # Code style changes (formatting, etc.)
refactor: # Code refactoring
perf:     # Performance improvements
test:     # Adding or updating tests
chore:    # Maintenance tasks

# Examples:
feat(karaoke): add custom video styling options

fix(audio): resolve memory leak in voice separation

docs(api): update function signatures in reference

perf(processing): optimize audio loading for large files

test(integration): add end-to-end karaoke generation test
```

### 5. Pull Request Process

#### PR Title and Description Template

```markdown
## 📝 Summary
Brief description of changes made.

## 🎯 Type of Change
- [ ] Bug fix (non-breaking change that fixes an issue)
- [ ] New feature (non-breaking change that adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Code refactoring

## 🧪 Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed
- [ ] Added new tests for changes

## 📋 Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Comments added to hard-to-understand areas
- [ ] Documentation updated
- [ ] No new warnings introduced
- [ ] Backward compatibility maintained

## 🔗 Related Issues
Closes #123
Fixes #456
Related to #789

## 📸 Screenshots (if applicable)
Add screenshots for UI changes.

## 📝 Additional Notes
Any additional context or notes for reviewers.
```

#### Review Process

1. **Automated Checks**: CI/CD pipeline runs tests and linting
2. **Code Review**: At least one maintainer reviews the code
3. **Testing**: Manual testing of new features
4. **Documentation**: Ensure docs are updated
5. **Merge**: Squash and merge after approval

## 🧪 Testing Guidelines

### Test Structure

```
tests/
├── unit/                   # Unit tests
│   ├── test_app.py
│   ├── test_karaoke_generator.py
│   └── test_movies.py
├── integration/            # Integration tests
│   ├── test_full_pipeline.py
│   └── test_batch_processing.py
├── fixtures/               # Test data
│   ├── sample_audio.mp3
│   └── sample_video.mp4
└── conftest.py            # Shared fixtures
```

### Writing Tests

```python
# tests/unit/test_audio_processing.py
import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path

from app import convert_to_audio, separate_voice
from tests.fixtures import SAMPLE_AUDIO_URL, SAMPLE_AUDIO_FILE

class TestAudioProcessing:
    """Test suite for audio processing functions."""
    
    def setup_method(self):
        """Set up test fixtures before each test."""
        self.temp_dir = Path("test_temp")
        self.temp_dir.mkdir(exist_ok=True)
    
    def teardown_method(self):
        """Clean up after each test."""
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
    
    @patch('app.yt_dlp.YoutubeDL')
    def test_convert_to_audio_success(self, mock_ytdl):
        """Test successful audio conversion."""
        # Arrange
        mock_instance = MagicMock()
        mock_ytdl.return_value.__enter__.return_value = mock_instance
        mock_instance.extract_info.return_value = {'title': 'Test Song'}
        
        # Act
        result = convert_to_audio(SAMPLE_AUDIO_URL)
        
        # Assert
        assert result.endswith('.mp3')
        mock_instance.download.assert_called_once()
    
    @pytest.mark.parametrize("invalid_url", [
        "",
        "not_a_url",
        "https://invalid-site.com/video",
        None
    ])
    def test_convert_to_audio_invalid_url(self, invalid_url):
        """Test audio conversion with invalid URLs."""
        with pytest.raises((ValueError, TypeError)):
            convert_to_audio(invalid_url)
    
    def test_separate_voice_creates_files(self):
        """Test that voice separation creates expected output files."""
        # This test requires actual audio file
        if not Path(SAMPLE_AUDIO_FILE).exists():
            pytest.skip("Sample audio file not available")
        
        # Act
        separate_voice(SAMPLE_AUDIO_FILE)
        
        # Assert
        assert Path("downloads/voice.wav").exists()
        assert Path("downloads/background.wav").exists()
        
        # Clean up
        Path("downloads/voice.wav").unlink(missing_ok=True)
        Path("downloads/background.wav").unlink(missing_ok=True)
```

### Integration Tests

```python
# tests/integration/test_full_pipeline.py
import pytest
from pathlib import Path
import os

from karaoke_generator import main

class TestFullPipeline:
    """Integration tests for complete karaoke generation."""
    
    @pytest.mark.slow
    @pytest.mark.integration
    def test_full_karaoke_generation(self):
        """Test complete karaoke generation pipeline."""
        # Use a short, copyright-free test video
        test_url = "https://www.youtube.com/watch?v=TEST_VIDEO_ID"
        
        # Run the main pipeline
        with patch('sys.argv', ['karaoke_generator.py', test_url]):
            main()
        
        # Verify outputs exist
        output_dir = Path("output")
        karaoke_files = list(output_dir.glob("*_karaoke.mp4"))
        
        assert len(karaoke_files) > 0, "No karaoke video was created"
        
        # Verify file is not empty
        karaoke_file = karaoke_files[0]
        assert karaoke_file.stat().st_size > 1000, "Karaoke video file is too small"
```

### Test Configuration

```python
# conftest.py
import pytest
from pathlib import Path
import tempfile
import shutil

@pytest.fixture(scope="session")
def sample_audio_file():
    """Provide path to sample audio file for testing."""
    # Create or use existing sample file
    sample_path = Path("tests/fixtures/sample_audio.mp3")
    if not sample_path.exists():
        pytest.skip("Sample audio file not available")
    return str(sample_path)

@pytest.fixture
def temp_directory():
    """Provide temporary directory for test operations."""
    temp_dir = Path(tempfile.mkdtemp())
    yield temp_dir
    shutil.rmtree(temp_dir)

@pytest.fixture(autouse=True)
def setup_test_environment():
    """Set up clean test environment for each test."""
    # Create test directories
    for dir_name in ["downloads", "temp", "output"]:
        Path(dir_name).mkdir(exist_ok=True)
    
    yield
    
    # Clean up test files (optional)
    # Uncomment if you want automatic cleanup
    # for dir_name in ["downloads", "temp", "output"]:
    #     test_files = Path(dir_name).glob("test_*")
    #     for file in test_files:
    #         file.unlink()

# Pytest configuration
pytest_plugins = ["pytest_mock"]

# Custom markers
def pytest_configure(config):
    config.addinivalue_line("markers", "slow: marks tests as slow")
    config.addinivalue_line("markers", "integration: marks tests as integration tests")
    config.addinivalue_line("markers", "unit: marks tests as unit tests")
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test types
pytest -m unit          # Unit tests only
pytest -m integration   # Integration tests only
pytest -m "not slow"    # Skip slow tests

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/unit/test_app.py

# Run specific test function
pytest tests/unit/test_app.py::test_convert_to_audio_success

# Run tests in parallel (with pytest-xdist)
pip install pytest-xdist
pytest -n auto
```

## 📚 Documentation Standards

### Code Documentation

```python
# Use Google-style docstrings
def process_video(
    url: str,
    output_format: str = "mp4",
    quality: str = "best"
) -> str:
    """
    Process video from URL with specified parameters.
    
    This function downloads and processes video from supported platforms,
    applying the specified quality and format settings.
    
    Args:
        url: Video URL from supported platform. Must be a valid HTTP/HTTPS URL.
        output_format: Desired output format. Supported formats: 'mp4', 'mkv', 'avi'.
        quality: Quality setting. Options: 'best', 'worst', or specific resolution like '720p'.
    
    Returns:
        Path to processed video file as string.
    
    Raises:
        ValueError: If URL format is invalid or unsupported.
        DownloadError: If video cannot be downloaded from the platform.
        ProcessingError: If video processing fails.
    
    Example:
        Basic usage:
        >>> video_path = process_video("https://www.youtube.com/watch?v=VIDEO_ID")
        >>> print(f"Video saved to: {video_path}")
        
        With custom settings:
        >>> video_path = process_video(
        ...     "https://www.youtube.com/watch?v=VIDEO_ID",
        ...     output_format="mkv",
        ...     quality="1080p"
        ... )
    
    Note:
        Processing time varies based on video length and system performance.
        Large videos may require significant disk space and processing time.
        
        For best performance, ensure sufficient disk space (at least 2x video size)
        and close other resource-intensive applications.
    
    See Also:
        - download_audio(): For audio-only extraction
        - batch_process(): For processing multiple videos
    """
```

### README Updates

When adding new features, update the main README.md:

```markdown
# Add to features section
## ✨ New Feature: Batch Processing

Process multiple videos simultaneously with configurable concurrency:

```python
from batch_processor import BatchProcessor

processor = BatchProcessor(max_workers=4)
results = processor.process_urls([
    "https://youtube.com/watch?v=VIDEO1",
    "https://youtube.com/watch?v=VIDEO2"
])
```

# Add to installation section if new dependencies
pip install new-dependency>=1.0.0

# Add to usage examples
### Batch Processing Example
```bash
python batch_process.py --input urls.txt --workers 4 --format mp4
```

# Update table of contents if adding new sections
```

### API Documentation

Update API_REFERENCE.md for new functions:

```markdown
#### `batch_process(urls: List[str], max_workers: int = 2) -> Dict[str, str]`

Process multiple URLs concurrently with controlled parallelism.

**Parameters:**
- `urls` (List[str]): List of video URLs to process
- `max_workers` (int, optional): Maximum concurrent workers. Defaults to 2.

**Returns:**
- `Dict[str, str]`: Mapping of URLs to processing results

**Example:**
```python
results = batch_process([
    "https://youtube.com/watch?v=VIDEO1",
    "https://youtube.com/watch?v=VIDEO2"
], max_workers=4)

for url, result in results.items():
    print(f"{url}: {result}")
```
```

## 🐛 Bug Reports

### Bug Report Template

When reporting bugs, use this template:

```markdown
## 🐛 Bug Report

### Description
A clear description of what the bug is.

### Expected Behavior
What you expected to happen.

### Actual Behavior
What actually happened.

### Steps to Reproduce
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

### Environment
- OS: [e.g. macOS 12.0, Ubuntu 20.04, Windows 11]
- Python Version: [e.g. 3.9.7]
- Project Version: [e.g. 1.2.3]
- FFmpeg Version: [output of `ffmpeg -version`]

### Error Output
```
Paste error messages, stack traces, or log output here
```

### Additional Context
Add any other context about the problem here.

### Possible Solution
If you have ideas about what might be causing the issue or how to fix it.
```

### Bug Investigation Process

1. **Reproduce the Issue**: Try to reproduce the bug locally
2. **Check Existing Issues**: Search for similar reported issues
3. **Gather Information**: Collect logs, system info, and error details
4. **Create Minimal Example**: Reduce the problem to its simplest form
5. **Document Findings**: Include all relevant details in the bug report

## 💡 Feature Requests

### Feature Request Template

```markdown
## 🚀 Feature Request

### Summary
Brief description of the feature you'd like to see.

### Motivation
Why is this feature needed? What problem does it solve?

### Detailed Description
Provide a detailed description of the feature and how it should work.

### Use Cases
- Use case 1: [description]
- Use case 2: [description]
- Use case 3: [description]

### Proposed Implementation
If you have ideas about how this could be implemented.

### Alternatives Considered
What other approaches have you considered?

### Additional Context
Any other context, mockups, or examples.
```

### Feature Development Process

1. **Discussion**: Engage with maintainers about the feature
2. **Design**: Create detailed design documents for complex features
3. **Implementation**: Develop the feature following coding standards
4. **Testing**: Add comprehensive tests for the new functionality
5. **Documentation**: Update all relevant documentation
6. **Review**: Submit PR for review and feedback

## 🚀 Release Process

### Version Numbering

We use [Semantic Versioning](https://semver.org/):

- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

Examples:
- `1.0.0` → `1.0.1` (bug fix)
- `1.0.1` → `1.1.0` (new feature)
- `1.1.0` → `2.0.0` (breaking change)

### Release Checklist

```markdown
## Pre-Release
- [ ] All tests passing
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] Version bumped in setup.py
- [ ] No known critical bugs
- [ ] Performance regression testing completed

## Release
- [ ] Create release branch
- [ ] Final testing on release branch
- [ ] Create and push version tag
- [ ] Build and upload to PyPI
- [ ] Create GitHub release with notes
- [ ] Update documentation website

## Post-Release
- [ ] Announce on social media/forums
- [ ] Monitor for issues
- [ ] Update project roadmap
- [ ] Plan next release cycle
```

### Changelog Format

```markdown
# Changelog

## [1.2.0] - 2024-01-15

### Added
- Batch processing functionality for multiple URLs
- Custom video styling options
- Progress tracking for long operations
- Support for additional video platforms

### Changed
- Improved error handling with more descriptive messages
- Updated dependencies to latest stable versions
- Optimized memory usage for large files

### Fixed
- Memory leak in audio processing pipeline
- Unicode handling in filenames
- Crash when processing very short videos

### Deprecated
- Old configuration format (will be removed in 2.0.0)

### Removed
- Support for Python 3.6 (EOL)

### Security
- Updated vulnerable dependencies
```

## 🤝 Community Guidelines

### Code of Conduct

We are committed to providing a welcoming and inclusive experience for everyone. We expect all contributors to:

- **Be Respectful**: Treat everyone with respect and kindness
- **Be Collaborative**: Work together towards common goals
- **Be Inclusive**: Welcome newcomers and help them learn
- **Be Professional**: Maintain professional communication
- **Be Patient**: Help others learn and grow

### Communication Channels

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: General questions and community chat
- **Discord**: Real-time chat and voice discussions
- **Email**: Direct contact with maintainers for sensitive issues

### Getting Help

If you need help:

1. **Check Documentation**: README, API reference, and guides
2. **Search Issues**: Look for similar questions or problems
3. **Ask in Discussions**: Post in GitHub Discussions
4. **Join Discord**: Get real-time help from the community
5. **Contact Maintainers**: Email for urgent or sensitive issues

### Recognition

We recognize contributors in several ways:

- **Contributors List**: Listed in README.md and repository
- **Release Notes**: Major contributions mentioned in releases
- **Hall of Fame**: Special recognition for significant contributions
- **Swag**: Stickers and t-shirts for active contributors

### Mentorship

New contributors can get mentorship through:

- **Good First Issues**: Labeled beginner-friendly issues
- **Mentorship Program**: Pairing with experienced contributors
- **Code Review**: Learning through the review process
- **Pair Programming**: Real-time collaboration sessions

---

## 📞 Contact

For questions about contributing:

- 📧 **Email**: maintainers@youtube-dl-suite.com
- 💬 **Discord**: [Join our server](https://discord.gg/INVITE_LINK)
- 📱 **Twitter**: [@YouTubeDLSuite](https://twitter.com/YouTubeDLSuite)
- 🐙 **GitHub**: [Open a discussion](https://github.com/OWNER/REPO/discussions)

Thank you for contributing to the YouTube DL Suite! 🎉

---

*Last updated: 2024-01-15*