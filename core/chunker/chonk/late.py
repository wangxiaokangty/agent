from chonkie import LateChunker
from chonkie.types import RecursiveRules

from core.chunker import Chunker


class ChonkLateChunker(Chunker):
    def __init__(self, embedding_model: str = "all-MiniLM-L6-v2", chunk_size: int = 2048, rules: RecursiveRules | None = None, min_characters_per_chunk: int = 24) -> None:
        super().__init__()
        if rules is None:
            rules = RecursiveRules()
        self.chunker = LateChunker(embedding_model=embedding_model, chunk_size=chunk_size, rules=rules, min_characters_per_chunk=min_characters_per_chunk)

    def _chunk(self, contents: list[str], **kwargs) -> list[list[str]]:
        result = []
        for content in contents:
            result.append([chunk.text for chunk in self.chunker.chunk(content)])
        return result
