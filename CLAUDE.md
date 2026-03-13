# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python-based photo resizing tool focused on certificate photo processing. The project uses `uv` as its package manager and build tool. The main functionality is contained in a single script (`photo_resizer.py`) that provides both CLI and Python API interfaces for resizing photos to standard certificate photo dimensions.

## Development Setup

### Environment Management
```bash
# Install dependencies and create virtual environment
uv sync

# Install with development tools
uv sync --extra dev

# Activate virtual environment
uv shell
```

### Running the Application
```bash
# Basic usage - resize to default 1寸 (600x840px)
uv run python photo_resizer.py input.jpg

# List available sizes
uv run python photo_resizer.py --list

# Specify size and processing method
uv run python photo_resizer.py input.jpg -s 2寸 -m smart

# Batch process directory
uv run python photo_resizer.py -b /path/to/photos -s 护照

# Custom dimensions
uv run python photo_resizer.py input.jpg --custom 400 600
```

### Code Quality Tools
```bash
# Format code
uv run black .
uv run isort .

# Type checking
uv run mypy photo_resizer.py

# Run tests (if available)
uv run pytest
```

## Architecture

### Core Components

1. **PhotoResizer Class**: The main processing engine that handles image resizing operations
   - Manages predefined certificate photo sizes (1寸, 2寸, 护照, etc.)
   - Implements three processing methods: `smart`, `crop`, `pad`
   - Handles both individual and batch processing

2. **Processing Methods**:
   - `smart`: Intelligent cropping combined with padding (default, recommended)
   - `crop`: Equal-ratio scaling followed by cropping
   - `pad`: Equal-ratio scaling followed by padding with white background

3. **Predefined Sizes**: Seven standard certificate photo dimensions:
   - 1寸 (600×840px) - Standard ID photo
   - 2寸 (708×1063px) - Large ID photo
   - 护照 (1134×1417px) - Passport photo
   - 签证 (1134×1134px) - Visa photo (square)
   - And others for specific use cases

### Image Processing Pipeline

1. **Input Validation**: Check file existence and format support
2. **Size Configuration**: Set target dimensions (predefined or custom)
3. **Processing Method Selection**: Apply chosen resize strategy
4. **Quality Enhancement**: Apply sharpening and contrast adjustments
5. **Output Generation**: Save as high-quality JPEG with 300 DPI

### Dependencies

- **Pillow**: Primary image processing library
- **argparse**: Command-line interface
- **pathlib**: Modern path handling
- No heavy dependencies like OpenCV - designed for simplicity and fast installation

### Configuration

The project uses `pyproject.toml` for configuration:
- Package metadata and dependencies
- Development tools configuration (black, isort, mypy)
- Command-line script entry point: `photo-resize`
- Python version requirement: >=3.8

### Input/Output

- **Supported Input**: JPG, JPEG, PNG, BMP, TIFF, WebP
- **Output Format**: JPEG with 95% quality, 300 DPI
- **Processing Algorithms**: Lanczos resampling for high quality
- **Enhancement**: UnsharpMask filter for sharpening

### API Usage

```python
from photo_resizer import PhotoResizer, batch_process

# Single file processing
resizer = PhotoResizer()
resizer.set_size("2寸")  # or resizer.set_custom_size(400, 600)
output_path = resizer.process_photo('input.jpg', method='smart')

# Batch processing
batch_process('./photos', size='护照', method='smart')
```

## Key Considerations

- The tool is designed to be lightweight with minimal dependencies
- All text output is in Chinese, reflecting the target user base
- The project prioritizes simplicity over advanced features like background removal
- Uses modern Python tooling (uv, pyproject.toml) for development efficiency
- Follows the Unix philosophy: "do one thing and do it well" - focused solely on resizing