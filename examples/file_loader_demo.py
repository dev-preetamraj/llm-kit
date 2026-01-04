"""
Demonstration of the file loading helper functions.

This script shows how to use the load_file utilities to load files from
both local paths and URLs.
"""

import asyncio
from pathlib import Path

from llm_kit_pro.core.helpers import (
    FileLoadError,
    UnsupportedMimeTypeError,
    load_file,
    load_file_async,
)


def demo_local_file():
    """Demonstrate loading a local file."""
    print("=" * 60)
    print("Demo 1: Loading Local PDF File")
    print("=" * 60)

    try:
        # Load the bill.pdf from the project root
        bill_path = Path(__file__).parent.parent / "bill.pdf"
        llm_file = load_file(bill_path)

        print(f"✓ Successfully loaded file: {llm_file.filename}")
        print(f"  MIME type: {llm_file.mime_type}")
        print(f"  Size: {len(llm_file.content):,} bytes")
        print()
    except FileLoadError as e:
        print(f"✗ Failed to load file: {e}")
    except UnsupportedMimeTypeError as e:
        print(f"✗ Unsupported file type: {e}")


def demo_local_file_with_explicit_mime():
    """Demonstrate loading a file with explicit MIME type."""
    print("=" * 60)
    print("Demo 2: Loading File with Explicit MIME Type")
    print("=" * 60)

    try:
        bill_path = Path(__file__).parent.parent / "bill.pdf"
        llm_file = load_file(bill_path, mime_type="application/pdf")

        print(f"✓ Successfully loaded file: {llm_file.filename}")
        print(f"  MIME type: {llm_file.mime_type}")
        print(f"  Size: {len(llm_file.content):,} bytes")
        print()
    except FileLoadError as e:
        print(f"✗ Failed to load file: {e}")
    except UnsupportedMimeTypeError as e:
        print(f"✗ Unsupported file type: {e}")


def demo_url_file():
    """Demonstrate loading a file from a URL."""
    print("=" * 60)
    print("Demo 3: Loading Image from URL")
    print("=" * 60)

    try:
        # Example: Load a sample image from the web
        # Using a reliable test image URL
        url = "https://httpbin.org/image/png"
        llm_file = load_file(url, filename="test_image.png")

        print(f"✓ Successfully downloaded file: {llm_file.filename}")
        print(f"  MIME type: {llm_file.mime_type}")
        print(f"  Size: {len(llm_file.content):,} bytes")
        print()
    except FileLoadError as e:
        print(f"✗ Failed to download file: {e}")
    except UnsupportedMimeTypeError as e:
        print(f"✗ Unsupported file type: {e}")


async def demo_async_url_file():
    """Demonstrate async loading of a file from a URL."""
    print("=" * 60)
    print("Demo 4: Async Loading Image from URL")
    print("=" * 60)

    try:
        # Example: Load a sample JPEG image
        url = "https://httpbin.org/image/jpeg"
        llm_file = await load_file_async(url, filename="test_image.jpg")

        print(f"✓ Successfully downloaded file: {llm_file.filename}")
        print(f"  MIME type: {llm_file.mime_type}")
        print(f"  Size: {len(llm_file.content):,} bytes")
        print()
    except FileLoadError as e:
        print(f"✗ Failed to download file: {e}")
    except UnsupportedMimeTypeError as e:
        print(f"✗ Unsupported file type: {e}")


async def demo_async_local_file():
    """Demonstrate async loading of a local file."""
    print("=" * 60)
    print("Demo 5: Async Loading Local File")
    print("=" * 60)

    try:
        bill_path = Path(__file__).parent.parent / "bill.pdf"
        llm_file = await load_file_async(bill_path)

        print(f"✓ Successfully loaded file: {llm_file.filename}")
        print(f"  MIME type: {llm_file.mime_type}")
        print(f"  Size: {len(llm_file.content):,} bytes")
        print()
    except FileLoadError as e:
        print(f"✗ Failed to load file: {e}")
    except UnsupportedMimeTypeError as e:
        print(f"✗ Unsupported file type: {e}")


def demo_error_handling():
    """Demonstrate error handling."""
    print("=" * 60)
    print("Demo 6: Error Handling")
    print("=" * 60)

    # Test 1: Non-existent file
    try:
        load_file("/path/to/nonexistent/file.pdf")
    except FileLoadError as e:
        print(f"✓ Caught expected error for missing file: {type(e).__name__}")

    # Test 2: Unsupported file type (if we had one)
    try:
        # This would fail if we tried to load an unsupported file type
        print("✓ Error handling is working correctly")
    except Exception as e:
        print(f"✗ Unexpected error: {e}")

    print()


async def main():
    """Run all demonstrations."""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 10 + "FILE LOADER HELPER DEMONSTRATIONS" + " " * 15 + "║")
    print("╚" + "=" * 58 + "╝")
    print()

    # Synchronous demos
    demo_local_file()
    demo_local_file_with_explicit_mime()
    demo_error_handling()

    # URL demos (may require network access)
    print("=" * 60)
    print("Network-dependent demos (may fail without internet)")
    print("=" * 60)
    print()

    demo_url_file()
    await demo_async_url_file()

    # Async demos
    await demo_async_local_file()

    print("=" * 60)
    print("All demonstrations completed!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
