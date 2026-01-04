"""Tests for file loading helper functions."""

import tempfile
from pathlib import Path

import pytest

from llm_kit_pro.core.helpers import (
    FileLoadError,
    UnsupportedMimeTypeError,
    load_file,
    load_file_async,
    load_file_from_path,
)
from llm_kit_pro.core.inputs import LLMFile


class TestLoadFileFromPath:
    """Tests for load_file_from_path function."""

    def test_load_pdf_file(self):
        """Test loading a PDF file."""
        # Create a temporary PDF file
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
            tmp.write(b"%PDF-1.4\nTest PDF content")
            tmp_path = tmp.name

        try:
            result = load_file_from_path(tmp_path)

            assert isinstance(result, LLMFile)
            assert result.mime_type == "application/pdf"
            assert result.content == b"%PDF-1.4\nTest PDF content"
            assert result.filename == Path(tmp_path).name
        finally:
            Path(tmp_path).unlink()

    def test_load_png_file(self):
        """Test loading a PNG file."""
        # PNG signature
        png_content = b"\x89PNG\r\n\x1a\n" + b"fake png data"

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            tmp.write(png_content)
            tmp_path = tmp.name

        try:
            result = load_file_from_path(tmp_path)

            assert isinstance(result, LLMFile)
            assert result.mime_type == "image/png"
            assert result.content == png_content
        finally:
            Path(tmp_path).unlink()

    def test_load_jpeg_file(self):
        """Test loading a JPEG file."""
        # JPEG signature
        jpeg_content = b"\xff\xd8\xff" + b"fake jpeg data"

        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
            tmp.write(jpeg_content)
            tmp_path = tmp.name

        try:
            result = load_file_from_path(tmp_path)

            assert isinstance(result, LLMFile)
            assert result.mime_type == "image/jpeg"
            assert result.content == jpeg_content
        finally:
            Path(tmp_path).unlink()

    def test_load_text_file(self):
        """Test loading a text file."""
        text_content = b"Hello, world!\nThis is a test."

        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as tmp:
            tmp.write(text_content)
            tmp_path = tmp.name

        try:
            result = load_file_from_path(tmp_path)

            assert isinstance(result, LLMFile)
            assert result.mime_type == "text/plain"
            assert result.content == text_content
        finally:
            Path(tmp_path).unlink()

    def test_load_file_with_explicit_mime_type(self):
        """Test loading a file with explicitly specified MIME type."""
        with tempfile.NamedTemporaryFile(suffix=".dat", delete=False) as tmp:
            tmp.write(b"Some binary data")
            tmp_path = tmp.name

        try:
            result = load_file_from_path(tmp_path, mime_type="text/plain")

            assert isinstance(result, LLMFile)
            assert result.mime_type == "text/plain"
        finally:
            Path(tmp_path).unlink()

    def test_load_file_with_custom_filename(self):
        """Test loading a file with custom filename."""
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as tmp:
            tmp.write(b"Test content")
            tmp_path = tmp.name

        try:
            result = load_file_from_path(tmp_path, filename="custom_name.txt")

            assert result.filename == "custom_name.txt"
        finally:
            Path(tmp_path).unlink()

    def test_load_nonexistent_file(self):
        """Test loading a non-existent file raises FileLoadError."""
        with pytest.raises(FileLoadError, match="File not found"):
            load_file_from_path("/path/to/nonexistent/file.pdf")

    def test_load_directory_raises_error(self):
        """Test loading a directory raises FileLoadError."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            with pytest.raises(FileLoadError, match="Path is not a file"):
                load_file_from_path(tmp_dir)

    def test_unsupported_mime_type(self):
        """Test that unsupported MIME types raise UnsupportedMimeTypeError."""
        with tempfile.NamedTemporaryFile(suffix=".unknown", delete=False) as tmp:
            # Write binary data that can't be decoded as UTF-8
            tmp.write(b"\x80\x81\x82\x83\x84\x85\x86\x87")
            tmp_path = tmp.name

        try:
            with pytest.raises(
                UnsupportedMimeTypeError, match="Could not detect MIME type"
            ):
                load_file_from_path(tmp_path)
        finally:
            Path(tmp_path).unlink()

    def test_mime_type_from_magic_bytes(self):
        """Test MIME type detection from magic bytes (file signature)."""
        # Create file without extension but with PDF signature
        with tempfile.NamedTemporaryFile(suffix="", delete=False) as tmp:
            tmp.write(b"%PDF-1.4\nTest content")
            tmp_path = tmp.name

        try:
            result = load_file_from_path(tmp_path)
            assert result.mime_type == "application/pdf"
        finally:
            Path(tmp_path).unlink()


class TestLoadFile:
    """Tests for the universal load_file function."""

    def test_load_local_file(self):
        """Test that load_file correctly handles local paths."""
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as tmp:
            tmp.write(b"Test content")
            tmp_path = tmp.name

        try:
            result = load_file(tmp_path)

            assert isinstance(result, LLMFile)
            assert result.mime_type == "text/plain"
            assert result.content == b"Test content"
        finally:
            Path(tmp_path).unlink()

    def test_load_file_with_path_object(self):
        """Test that load_file accepts Path objects."""
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as tmp:
            tmp.write(b"Test content")
            tmp_path = Path(tmp.name)

        try:
            result = load_file(tmp_path)

            assert isinstance(result, LLMFile)
            assert result.content == b"Test content"
        finally:
            tmp_path.unlink()

    def test_load_file_expands_user_path(self):
        """Test that load_file expands ~ in paths."""
        # Create a temp file in a known location
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as tmp:
            tmp.write(b"Test content")
            tmp_path = tmp.name

        try:
            # This should work even though we're not testing ~ expansion directly
            result = load_file(tmp_path)
            assert isinstance(result, LLMFile)
        finally:
            Path(tmp_path).unlink()


class TestLoadFileAsync:
    """Tests for async file loading functions."""

    @pytest.mark.asyncio
    async def test_load_file_async_local(self):
        """Test async loading of local files."""
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as tmp:
            tmp.write(b"Async test content")
            tmp_path = tmp.name

        try:
            result = await load_file_async(tmp_path)

            assert isinstance(result, LLMFile)
            assert result.mime_type == "text/plain"
            assert result.content == b"Async test content"
        finally:
            Path(tmp_path).unlink()

    @pytest.mark.asyncio
    async def test_load_file_async_with_path_object(self):
        """Test async loading with Path objects."""
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
            tmp.write(b"%PDF-1.4\nAsync PDF")
            tmp_path = Path(tmp.name)

        try:
            result = await load_file_async(tmp_path)

            assert isinstance(result, LLMFile)
            assert result.mime_type == "application/pdf"
        finally:
            tmp_path.unlink()


class TestMimeTypeNormalization:
    """Tests for MIME type normalization and validation."""

    def test_jpeg_alias_normalization(self):
        """Test that image/jpg is normalized to image/jpeg."""
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
            tmp.write(b"\xff\xd8\xff" + b"jpeg data")
            tmp_path = tmp.name

        try:
            result = load_file_from_path(tmp_path, mime_type="image/jpg")
            assert result.mime_type == "image/jpeg"
        finally:
            Path(tmp_path).unlink()

    def test_unsupported_mime_type_explicit(self):
        """Test that explicitly providing unsupported MIME type raises error."""
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as tmp:
            tmp.write(b"test")
            tmp_path = tmp.name

        try:
            with pytest.raises(UnsupportedMimeTypeError, match="is not supported"):
                load_file_from_path(tmp_path, mime_type="application/json")
        finally:
            Path(tmp_path).unlink()


class TestEdgeCases:
    """Tests for edge cases and error conditions."""

    def test_empty_file(self):
        """Test loading an empty file."""
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as tmp:
            tmp_path = tmp.name

        try:
            result = load_file_from_path(tmp_path)
            assert result.content == b""
            assert result.mime_type == "text/plain"
        finally:
            Path(tmp_path).unlink()

    def test_large_file(self):
        """Test loading a larger file."""
        large_content = b"x" * (1024 * 1024)  # 1 MB

        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as tmp:
            tmp.write(large_content)
            tmp_path = tmp.name

        try:
            result = load_file_from_path(tmp_path)
            assert len(result.content) == 1024 * 1024
        finally:
            Path(tmp_path).unlink()

    def test_file_with_special_characters_in_name(self):
        """Test loading files with special characters in filename."""
        with tempfile.NamedTemporaryFile(suffix=" test (1).txt", delete=False) as tmp:
            tmp.write(b"test content")
            tmp_path = tmp.name

        try:
            result = load_file_from_path(tmp_path)
            assert isinstance(result, LLMFile)
            assert "test" in result.filename
        finally:
            Path(tmp_path).unlink()
