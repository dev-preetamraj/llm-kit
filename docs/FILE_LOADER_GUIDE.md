# File Loader Helper Guide

## Overview

The `llm-kit-pro` library provides a comprehensive set of helper functions to load files from both local filesystem paths and remote URLs, automatically converting them to `LLMFile` objects that can be used with any LLM provider.

## Features

- ✅ **Universal Interface**: Single function handles both local files and URLs
- ✅ **Automatic MIME Type Detection**: Detects file types from extensions and magic bytes
- ✅ **Async Support**: Both synchronous and asynchronous APIs
- ✅ **Type Safety**: Full type hints and Pydantic integration
- ✅ **Robust Error Handling**: Clear, actionable error messages
- ✅ **Industry Standard**: Follows best practices for file handling and HTTP requests

## Supported File Types

- **PDF**: `application/pdf`
- **PNG Images**: `image/png`
- **JPEG Images**: `image/jpeg`
- **Plain Text**: `text/plain`

## Installation

The file loader utilities are included in the core `llm-kit-pro` package:

```bash
pip install llm-kit-pro
```

## Quick Start

### Basic Usage

```python
from llm_kit_pro.core.helpers import load_file

# Load from local path
file = load_file("/path/to/document.pdf")

# Load from URL
file = load_file("https://example.com/image.png")

# Use with any LLM provider
response = await client.generate_text(
    "Analyze this document",
    files=[file]
)
```

### Async Usage

```python
from llm_kit_pro.core.helpers import load_file_async

# Async loading (recommended for URLs)
file = await load_file_async("https://example.com/large-file.pdf")
```

## API Reference

### `load_file()`

Universal file loader (synchronous).

```python
def load_file(
    source: Union[str, Path],
    mime_type: Optional[str] = None,
    filename: Optional[str] = None,
    timeout: float = 30.0,
) -> LLMFile
```

**Parameters:**
- `source`: File path (str or Path) or URL (http://, https://)
- `mime_type`: Optional explicit MIME type (auto-detected if not provided)
- `filename`: Optional custom filename
- `timeout`: Request timeout for URLs in seconds (default: 30.0)

**Returns:** `LLMFile` object

**Raises:**
- `FileLoadError`: If file cannot be loaded
- `UnsupportedMimeTypeError`: If MIME type is not supported

**Example:**
```python
from llm_kit_pro.core.helpers import load_file

# Auto-detect MIME type
file = load_file("/path/to/document.pdf")

# Explicit MIME type
file = load_file("/path/to/file", mime_type="text/plain")

# Custom filename
file = load_file("https://example.com/doc", filename="my_doc.pdf")
```

### `load_file_async()`

Universal file loader (asynchronous).

```python
async def load_file_async(
    source: Union[str, Path],
    mime_type: Optional[str] = None,
    filename: Optional[str] = None,
    timeout: float = 30.0,
) -> LLMFile
```

**Parameters:** Same as `load_file()`

**Returns:** `LLMFile` object

**Example:**
```python
from llm_kit_pro.core.helpers import load_file_async

# Async loading
file = await load_file_async("https://example.com/image.png")

# With custom settings
file = await load_file_async(
    "https://slow-server.com/file.pdf",
    timeout=60.0,
    filename="custom.pdf"
)
```

### `load_file_from_path()`

Load file from local filesystem (synchronous).

```python
def load_file_from_path(
    file_path: str,
    mime_type: Optional[str] = None,
    filename: Optional[str] = None,
) -> LLMFile
```

**Parameters:**
- `file_path`: Path to local file
- `mime_type`: Optional explicit MIME type
- `filename`: Optional custom filename

**Returns:** `LLMFile` object

**Example:**
```python
from llm_kit_pro.core.helpers import load_file_from_path

file = load_file_from_path("/home/user/document.pdf")
```

### `load_file_from_url()`

Download file from URL (synchronous).

```python
def load_file_from_url(
    url: str,
    mime_type: Optional[str] = None,
    filename: Optional[str] = None,
    timeout: float = 30.0,
) -> LLMFile
```

**Parameters:**
- `url`: URL to download from
- `mime_type`: Optional explicit MIME type
- `filename`: Optional custom filename
- `timeout`: Request timeout in seconds

**Returns:** `LLMFile` object

**Example:**
```python
from llm_kit_pro.core.helpers import load_file_from_url

file = load_file_from_url(
    "https://example.com/report.pdf",
    timeout=60.0
)
```

### `load_file_from_url_async()`

Download file from URL (asynchronous).

```python
async def load_file_from_url_async(
    url: str,
    mime_type: Optional[str] = None,
    filename: Optional[str] = None,
    timeout: float = 30.0,
) -> LLMFile
```

**Parameters:** Same as `load_file_from_url()`

**Returns:** `LLMFile` object

**Example:**
```python
from llm_kit_pro.core.helpers import load_file_from_url_async

file = await load_file_from_url_async("https://example.com/image.png")
```

## Advanced Usage

### MIME Type Detection

The library automatically detects MIME types using multiple strategies:

1. **File Extension**: Checks the file extension (`.pdf`, `.png`, etc.)
2. **Magic Bytes**: Examines file signatures (e.g., `%PDF` for PDFs)
3. **HTTP Headers**: Uses `Content-Type` header for URLs

```python
# Auto-detection from extension
file = load_file("document.pdf")  # Detects as application/pdf

# Auto-detection from magic bytes (no extension)
file = load_file("myfile")  # Checks file signature

# Manual override
file = load_file("data.bin", mime_type="text/plain")
```

### Error Handling

```python
from llm_kit_pro.core.helpers import (
    load_file,
    FileLoadError,
    UnsupportedMimeTypeError
)

try:
    file = load_file("https://example.com/document.pdf")
except FileLoadError as e:
    print(f"Failed to load file: {e}")
except UnsupportedMimeTypeError as e:
    print(f"Unsupported file type: {e}")
```

### Working with Different Providers

```python
from llm_kit_pro.core.helpers import load_file
from llm_kit_pro.providers.anthropic import AnthropicClient, AnthropicConfig
from llm_kit_pro.providers.openai import OpenAIClient, OpenAIConfig

# Load file once
document = load_file("report.pdf")

# Use with Anthropic
anthropic = AnthropicClient(AnthropicConfig(api_key="..."))
result1 = await anthropic.generate_text("Summarize", files=[document])

# Use with OpenAI
openai = OpenAIClient(OpenAIConfig(api_key="..."))
result2 = await openai.generate_text("Summarize", files=[document])
```

### Batch Loading

```python
from pathlib import Path
from llm_kit_pro.core.helpers import load_file_async

async def load_multiple_files(file_paths):
    """Load multiple files concurrently."""
    tasks = [load_file_async(path) for path in file_paths]
    return await asyncio.gather(*tasks)

# Usage
files = await load_multiple_files([
    "doc1.pdf",
    "https://example.com/doc2.pdf",
    "image.png"
])
```

### Custom Timeout for Slow Servers

```python
# Increase timeout for large files or slow servers
file = await load_file_async(
    "https://slow-server.com/large-file.pdf",
    timeout=120.0  # 2 minutes
)
```

### Path Expansion

The loader automatically expands user paths:

```python
# These all work
file = load_file("~/Documents/file.pdf")  # Expands ~
file = load_file("./relative/path.pdf")   # Resolves relative paths
file = load_file("/absolute/path.pdf")    # Absolute paths
```

## Best Practices

### 1. Use Async for URLs

When loading from URLs, prefer the async version for better performance:

```python
# Good: Non-blocking
file = await load_file_async("https://example.com/file.pdf")

# Okay: Blocking (use for local files)
file = load_file("/local/file.pdf")
```

### 2. Handle Errors Gracefully

Always wrap file loading in try-except blocks:

```python
try:
    file = load_file(user_provided_path)
except FileLoadError:
    # Handle missing/inaccessible files
    return "File not found"
except UnsupportedMimeTypeError:
    # Handle unsupported file types
    return "File type not supported"
```

### 3. Validate Input Sources

For user-provided URLs, consider validation:

```python
from urllib.parse import urlparse

def is_safe_url(url: str) -> bool:
    """Basic URL validation."""
    parsed = urlparse(url)
    return parsed.scheme in ('http', 'https') and bool(parsed.netloc)

if is_safe_url(user_url):
    file = await load_file_async(user_url)
```

### 4. Set Appropriate Timeouts

Adjust timeouts based on expected file sizes:

```python
# Small files
file = await load_file_async(url, timeout=10.0)

# Large files
file = await load_file_async(large_url, timeout=300.0)
```

### 5. Reuse Loaded Files

Load files once and reuse them:

```python
# Good: Load once
document = load_file("large-document.pdf")
result1 = await client1.generate_text("Task 1", files=[document])
result2 = await client2.generate_text("Task 2", files=[document])

# Bad: Load multiple times
result1 = await client1.generate_text("Task 1", files=[load_file("doc.pdf")])
result2 = await client2.generate_text("Task 2", files=[load_file("doc.pdf")])
```

## Common Use Cases

### 1. Document Analysis

```python
from llm_kit_pro.core.helpers import load_file
from llm_kit_pro.providers.anthropic import AnthropicClient, AnthropicConfig

# Load PDF invoice
invoice = load_file("invoice.pdf")

# Extract information
client = AnthropicClient(AnthropicConfig(api_key="..."))
data = await client.generate_json(
    "Extract invoice details",
    schema=InvoiceSchema,
    files=[invoice]
)
```

### 2. Image Analysis

```python
# Load image from URL
image = await load_file_async("https://example.com/photo.jpg")

# Analyze image
description = await client.generate_text(
    "Describe this image in detail",
    files=[image]
)
```

### 3. Multi-Document Processing

```python
# Load multiple documents
docs = [
    load_file("contract1.pdf"),
    load_file("contract2.pdf"),
    load_file("contract3.pdf")
]

# Process all together
summary = await client.generate_text(
    "Compare these contracts and highlight key differences",
    files=docs
)
```

### 4. Web Scraping Integration

```python
import httpx
from bs4 import BeautifulSoup

async def analyze_webpage_images(url: str):
    """Download and analyze all images from a webpage."""
    # Scrape page
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
    
    # Load all images
    image_urls = [img['src'] for img in soup.find_all('img')]
    images = await asyncio.gather(*[
        load_file_async(img_url) for img_url in image_urls
    ])
    
    # Analyze with LLM
    return await llm_client.generate_text(
        "Describe these images",
        files=images
    )
```

## Troubleshooting

### Issue: "File not found"

**Cause:** The file path doesn't exist or is inaccessible.

**Solution:**
```python
from pathlib import Path

# Check if file exists before loading
path = Path("document.pdf")
if path.exists():
    file = load_file(path)
else:
    print(f"File not found: {path}")
```

### Issue: "Could not detect MIME type"

**Cause:** File has no extension and no recognizable magic bytes.

**Solution:** Provide explicit MIME type:
```python
file = load_file("myfile", mime_type="text/plain")
```

### Issue: Timeout errors with URLs

**Cause:** Server is slow or file is large.

**Solution:** Increase timeout:
```python
file = await load_file_async(url, timeout=120.0)
```

### Issue: "MIME type is not supported"

**Cause:** File type is not supported by LLM providers.

**Solution:** Convert file to supported format or check supported types:
```python
# Supported types
SUPPORTED = ["application/pdf", "image/png", "image/jpeg", "text/plain"]
```

## Performance Considerations

### Memory Usage

Files are loaded entirely into memory. For very large files:

```python
import os

# Check file size before loading
file_size = os.path.getsize("large-file.pdf")
if file_size > 10 * 1024 * 1024:  # 10 MB
    print("Warning: Large file")

file = load_file("large-file.pdf")
```

### Network Performance

For multiple URLs, use async and gather:

```python
# Efficient: Parallel downloads
files = await asyncio.gather(*[
    load_file_async(url1),
    load_file_async(url2),
    load_file_async(url3)
])

# Inefficient: Sequential downloads
files = [
    await load_file_async(url1),
    await load_file_async(url2),
    await load_file_async(url3)
]
```

## Migration Guide

### From Manual File Loading

**Before:**
```python
from pathlib import Path
from llm_kit_pro.core.inputs import LLMFile

# Manual loading
with open("document.pdf", "rb") as f:
    content = f.read()
file = LLMFile(content=content, mime_type="application/pdf", filename="document.pdf")
```

**After:**
```python
from llm_kit_pro.core.helpers import load_file

# Automatic loading
file = load_file("document.pdf")
```

### From Other Libraries

**From `requests`:**
```python
# Before
import requests
response = requests.get(url)
file = LLMFile(content=response.content, mime_type="application/pdf")

# After
from llm_kit_pro.core.helpers import load_file
file = load_file(url)
```

**From `aiohttp`:**
```python
# Before
import aiohttp
async with aiohttp.ClientSession() as session:
    async with session.get(url) as response:
        content = await response.read()
file = LLMFile(content=content, mime_type="application/pdf")

# After
from llm_kit_pro.core.helpers import load_file_async
file = await load_file_async(url)
```

## Contributing

Found a bug or want to add support for more file types? See [CONTRIBUTION.md](../CONTRIBUTION.md) for guidelines.

## License

This library is licensed under the MIT License. See [LICENSE](../LICENSE) for details.

