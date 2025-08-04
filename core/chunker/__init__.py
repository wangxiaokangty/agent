from abc import ABC, abstractmethod


class Chunker(ABC):
    """Abstract base class for chunker implementations."""

    @abstractmethod
    def _chunk(self, contents: list[str], **kwargs) -> list[list[str]]:
        pass

    def chunk(self, contents: str | list[str], **kwargs) -> list[str] | list[list[str]]:
        batched = True
        if not isinstance(contents, list):
            batched = False
            contents = [contents]
        chunks = self._chunk(contents=contents, **kwargs)
        if not batched:
            return chunks[0]
        return chunks
