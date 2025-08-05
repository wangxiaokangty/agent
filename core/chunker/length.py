from langchain_text_splitters import CharacterTextSplitter

from core.chunker import Chunker


class LengthChunker(Chunker):
    def __init__(
        self,
        chunk_size: int = 200,
        chunk_overlap: int = 0,
        encoding_name: str = "cl100k_base",
    ) -> None:
        super().__init__()
        self.chunker: CharacterTextSplitter = (
            CharacterTextSplitter.from_tiktoken_encoder(
                encoding_name=encoding_name,
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
            )
        )

    def _chunk(self, contents: list[str], **kwargs) -> list[list[str]]:
        results = []
        for content in contents:
            results.append(self.chunker.split_text(content))
        return results
