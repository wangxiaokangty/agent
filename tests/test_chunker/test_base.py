import pytest

from core.chunker import Chunker


class MockChunker(Chunker):
    """Mock chunker for testing purposes."""

    def __init__(self, chunk_size: int = 100, separator: str = "\n", encoding: str = "utf-8"):
        super().__init__()
        self.chunk_size = chunk_size
        self.separator = separator
        self.encoding = encoding

    def _chunk(self, contents: list[str], **kwargs) -> list[list[str]]:
        """Simple mock chunking implementation."""
        result = []
        for content in contents:
            # Simple chunking by splitting on separator and limiting size
            parts = content.split(self.separator)
            chunks = []
            current_chunk = ""
            for part in parts:
                if len(current_chunk) + len(part) + len(self.separator) <= self.chunk_size:
                    if current_chunk:
                        current_chunk += self.separator + part
                    else:
                        current_chunk = part
                else:
                    if current_chunk:
                        chunks.append(current_chunk)
                    current_chunk = part
            if current_chunk:
                chunks.append(current_chunk)
            result.append(chunks)
        return result


class TestChunkerRegistry:
    """Test the Registry functionality of the Chunker base class."""

    def test_init_subclass_registers_chunker(self):
        """Test that __init_subclass__ automatically registers chunkers."""
        # MockChunker should be automatically registered
        registry = Chunker.get_registry()
        assert "MockChunker" in registry
        assert registry["MockChunker"] is MockChunker

    def test_registry_contains_existing_chunkers(self):
        """Test that registry contains the existing chunker implementations."""
        # Import existing chunkers to trigger registration

        registry = Chunker.get_registry()
        assert "LengthChunker" in registry
        assert "SemanticChunker" in registry
        assert "ChonkCodeChunker" in registry
        assert "MockChunker" in registry

    def test_from_config_creates_chunker_instance(self):
        """Test that from_config creates a chunker instance from configuration."""
        config = {"type": "MockChunker", "chunk_size": 200, "separator": " ", "encoding": "ascii"}

        chunker = Chunker.from_config(config)

        assert isinstance(chunker, MockChunker)
        assert chunker.chunk_size == 200
        assert chunker.separator == " "
        assert chunker.encoding == "ascii"

    def test_from_config_missing_type_raises_error(self):
        """Test that from_config raises error when 'type' is missing."""
        config = {"chunk_size": 200, "separator": " "}

        with pytest.raises(ValueError, match="Configuration must include 'type' field"):
            Chunker.from_config(config)

    def test_from_config_unknown_type_raises_error(self):
        """Test that from_config raises error for unknown chunker type."""
        config = {"type": "UnknownChunker", "chunk_size": 200}

        with pytest.raises(ValueError, match="Unknown chunker type: UnknownChunker"):
            Chunker.from_config(config)

    def test_to_config_returns_configuration_dict(self):
        """Test that to_config returns a proper configuration dictionary."""
        chunker = MockChunker(chunk_size=150, separator="|", encoding="utf-16")
        config = chunker.to_config()

        assert config["type"] == "MockChunker"
        assert config["chunk_size"] == 150
        assert config["separator"] == "|"
        assert config["encoding"] == "utf-16"

    def test_to_config_excludes_internal_attributes(self):
        """Test that to_config excludes internal attributes and complex objects."""
        chunker = MockChunker()
        # Add some internal attributes that should be excluded
        chunker._internal_attr = "should_be_excluded"
        chunker.chunker = "complex_object_should_be_excluded"

        config = chunker.to_config()

        assert "_internal_attr" not in config
        assert "chunker" not in config
        assert "type" in config
        assert config["type"] == "MockChunker"

    def test_roundtrip_config_serialization(self):
        """Test that we can create a chunker, serialize it, and recreate it."""
        original_chunker = MockChunker(chunk_size=300, separator="||", encoding="latin-1")

        # Serialize to config
        config = original_chunker.to_config()

        # Recreate from config
        new_chunker = Chunker.from_config(config)

        # Verify they have the same configuration
        assert isinstance(new_chunker, MockChunker)
        assert new_chunker.chunk_size == original_chunker.chunk_size
        assert new_chunker.separator == original_chunker.separator
        assert new_chunker.encoding == original_chunker.encoding

        # Verify they produce the same output
        test_content = "This is a test content that should be chunked in the same way by both chunkers."
        original_chunks = original_chunker.chunk(test_content)
        new_chunks = new_chunker.chunk(test_content)
        assert original_chunks == new_chunks

    def test_get_registry_returns_copy(self):
        """Test that get_registry returns a copy of the registry, not the original."""
        registry1 = Chunker.get_registry()
        registry2 = Chunker.get_registry()

        # They should be equal but not the same object
        assert registry1 == registry2
        assert registry1 is not registry2

        # Modifying one shouldn't affect the other
        registry1["TestModification"] = None
        assert "TestModification" not in registry2

        # Original registry should not be affected
        original_registry = Chunker._registry
        assert "TestModification" not in original_registry
