from langchain_text_splitters import RecursiveCharacterTextSplitter

from core.chunker import Chunker


class RecursiveChunker(Chunker):
    def __init__(
        self,
        chunk_size: int = 200,
        chunk_overlap: int = 20,
        separators: list[str] | None = None,
    ) -> None:
        super().__init__()
        self.chunker: RecursiveCharacterTextSplitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=separators,
        )

    def _chunk(self, contents: list[str], **kwargs) -> list[list[str]]:
        results = []
        for content in contents:
            results.append(self.chunker.split_text(content))
        return results