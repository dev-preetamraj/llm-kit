"""
Advanced file loading examples demonstrating real-world use cases.
"""

import asyncio
from pathlib import Path
from typing import List, Optional

from llm_kit_pro.core.helpers import (
    FileLoadError,
    UnsupportedMimeTypeError,
    load_file,
    load_file_async,
)
from llm_kit_pro.core.inputs import LLMFile


# Example 1: Safe file loader with validation
def safe_load_file(source: str) -> Optional[LLMFile]:
    """
    Safely load a file with comprehensive error handling.

    Args:
        source: File path or URL

    Returns:
        LLMFile if successful, None otherwise
    """
    try:
        file = load_file(source)
        print(f"✓ Loaded: {file.filename} ({len(file.content):,} bytes)")
        return file
    except FileLoadError as e:
        print(f"✗ File error: {e}")
        return None
    except UnsupportedMimeTypeError as e:
        print(f"✗ Unsupported type: {e}")
        return None
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return None


# Example 2: Batch file loader with progress
async def load_files_batch(
    sources: List[str], show_progress: bool = True
) -> List[LLMFile]:
    """
    Load multiple files concurrently with optional progress reporting.

    Args:
        sources: List of file paths or URLs
        show_progress: Whether to show progress messages

    Returns:
        List of successfully loaded LLMFile objects
    """
    if show_progress:
        print(f"Loading {len(sources)} files...")

    # Load all files concurrently
    results = await asyncio.gather(
        *[load_file_async(source) for source in sources],
        return_exceptions=True,  # Don't fail on individual errors
    )

    # Filter out errors and collect successful loads
    loaded_files = []
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            if show_progress:
                print(f"✗ Failed to load {sources[i]}: {result}")
        else:
            loaded_files.append(result)
            if show_progress:
                print(f"✓ Loaded {result.filename}")

    if show_progress:
        print(f"Successfully loaded {len(loaded_files)}/{len(sources)} files")

    return loaded_files


# Example 3: File loader with size validation
def load_file_with_size_limit(source: str, max_size_mb: float = 10.0) -> Optional[LLMFile]:
    """
    Load a file with size validation.

    Args:
        source: File path or URL
        max_size_mb: Maximum file size in megabytes

    Returns:
        LLMFile if successful and within size limit, None otherwise
    """
    try:
        # For local files, check size before loading
        if not source.startswith(("http://", "https://")):
            file_path = Path(source).expanduser().resolve()
            size_bytes = file_path.stat().st_size
            size_mb = size_bytes / (1024 * 1024)

            if size_mb > max_size_mb:
                print(
                    f"✗ File too large: {size_mb:.2f}MB (limit: {max_size_mb}MB)"
                )
                return None

        # Load the file
        file = load_file(source)

        # Verify loaded size
        size_mb = len(file.content) / (1024 * 1024)
        if size_mb > max_size_mb:
            print(f"✗ File too large: {size_mb:.2f}MB (limit: {max_size_mb}MB)")
            return None

        print(f"✓ Loaded {file.filename} ({size_mb:.2f}MB)")
        return file

    except Exception as e:
        print(f"✗ Error: {e}")
        return None


# Example 4: Retry logic for network files
async def load_file_with_retry(
    url: str, max_retries: int = 3, timeout: float = 30.0
) -> Optional[LLMFile]:
    """
    Load a file from URL with retry logic.

    Args:
        url: URL to download from
        max_retries: Maximum number of retry attempts
        timeout: Timeout per attempt in seconds

    Returns:
        LLMFile if successful, None otherwise
    """
    for attempt in range(1, max_retries + 1):
        try:
            print(f"Attempt {attempt}/{max_retries}: Downloading {url}")
            file = await load_file_async(url, timeout=timeout)
            print(f"✓ Successfully downloaded {file.filename}")
            return file
        except FileLoadError as e:
            if attempt < max_retries:
                wait_time = 2**attempt  # Exponential backoff
                print(f"✗ Failed: {e}. Retrying in {wait_time}s...")
                await asyncio.sleep(wait_time)
            else:
                print(f"✗ Failed after {max_retries} attempts: {e}")
                return None
        except Exception as e:
            print(f"✗ Unexpected error: {e}")
            return None

    return None


# Example 5: File type validator
def validate_file_type(file: LLMFile, allowed_types: List[str]) -> bool:
    """
    Validate that a loaded file has an allowed MIME type.

    Args:
        file: The loaded LLMFile
        allowed_types: List of allowed MIME types

    Returns:
        True if file type is allowed, False otherwise
    """
    if file.mime_type in allowed_types:
        print(f"✓ File type {file.mime_type} is allowed")
        return True
    else:
        print(f"✗ File type {file.mime_type} not in allowed types: {allowed_types}")
        return False


# Example 6: Document collection loader
class DocumentCollection:
    """Load and manage a collection of documents."""

    def __init__(self):
        self.documents: List[LLMFile] = []

    async def add_from_directory(self, directory: Path, pattern: str = "*.pdf"):
        """Load all matching files from a directory."""
        print(f"Scanning {directory} for {pattern}...")

        files = list(directory.glob(pattern))
        print(f"Found {len(files)} files")

        loaded = await load_files_batch([str(f) for f in files])
        self.documents.extend(loaded)

        print(f"Collection now contains {len(self.documents)} documents")

    async def add_from_urls(self, urls: List[str]):
        """Load documents from URLs."""
        print(f"Downloading {len(urls)} files from URLs...")

        loaded = await load_files_batch(urls)
        self.documents.extend(loaded)

        print(f"Collection now contains {len(self.documents)} documents")

    def filter_by_type(self, mime_type: str) -> List[LLMFile]:
        """Filter documents by MIME type."""
        filtered = [doc for doc in self.documents if doc.mime_type == mime_type]
        print(f"Found {len(filtered)} documents of type {mime_type}")
        return filtered

    def get_total_size(self) -> int:
        """Get total size of all documents in bytes."""
        total = sum(len(doc.content) for doc in self.documents)
        print(f"Total collection size: {total:,} bytes ({total / 1024 / 1024:.2f}MB)")
        return total


# Demo functions
async def demo_safe_loading():
    """Demonstrate safe file loading."""
    print("\n" + "=" * 60)
    print("Demo 1: Safe File Loading")
    print("=" * 60)

    # Try to load existing file
    bill_path = Path(__file__).parent.parent / "bill.pdf"
    safe_load_file(str(bill_path))

    # Try to load non-existent file
    safe_load_file("/nonexistent/file.pdf")


async def demo_batch_loading():
    """Demonstrate batch file loading."""
    print("\n" + "=" * 60)
    print("Demo 2: Batch File Loading")
    print("=" * 60)

    sources = [
        str(Path(__file__).parent.parent / "bill.pdf"),
        "https://httpbin.org/image/png",
        "/nonexistent/file.pdf",  # This will fail
    ]

    files = await load_files_batch(sources)
    print(f"\nSuccessfully loaded {len(files)} files")


async def demo_size_validation():
    """Demonstrate file size validation."""
    print("\n" + "=" * 60)
    print("Demo 3: File Size Validation")
    print("=" * 60)

    bill_path = Path(__file__).parent.parent / "bill.pdf"

    # With generous limit
    load_file_with_size_limit(str(bill_path), max_size_mb=10.0)

    # With strict limit
    load_file_with_size_limit(str(bill_path), max_size_mb=0.1)


async def demo_retry_logic():
    """Demonstrate retry logic for network files."""
    print("\n" + "=" * 60)
    print("Demo 4: Retry Logic")
    print("=" * 60)

    # Try to download a file (use a reliable URL)
    url = "https://httpbin.org/image/jpeg"
    await load_file_with_retry(url, max_retries=3, timeout=10.0)


async def demo_type_validation():
    """Demonstrate file type validation."""
    print("\n" + "=" * 60)
    print("Demo 5: File Type Validation")
    print("=" * 60)

    bill_path = Path(__file__).parent.parent / "bill.pdf"
    file = load_file(str(bill_path))

    # Validate against allowed types
    validate_file_type(file, ["application/pdf", "text/plain"])
    validate_file_type(file, ["image/png", "image/jpeg"])


async def demo_document_collection():
    """Demonstrate document collection management."""
    print("\n" + "=" * 60)
    print("Demo 6: Document Collection")
    print("=" * 60)

    collection = DocumentCollection()

    # Add local file
    bill_path = Path(__file__).parent.parent / "bill.pdf"
    await collection.add_from_urls([str(bill_path)])

    # Add from URL
    await collection.add_from_urls(["https://httpbin.org/image/png"])

    # Get statistics
    collection.filter_by_type("application/pdf")
    collection.filter_by_type("image/png")
    collection.get_total_size()


async def main():
    """Run all demonstrations."""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 8 + "ADVANCED FILE LOADING DEMONSTRATIONS" + " " * 14 + "║")
    print("╚" + "=" * 58 + "╝")

    await demo_safe_loading()
    await demo_batch_loading()
    await demo_size_validation()
    await demo_retry_logic()
    await demo_type_validation()
    await demo_document_collection()

    print("\n" + "=" * 60)
    print("All demonstrations completed!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())

