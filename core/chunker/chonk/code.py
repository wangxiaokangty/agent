from chonkie import CodeChunker

from core.chunker import Chunker


class ChonkCodeChunker(Chunker):
    def __init__(self, language: str = "auto", tokenizer_or_token_counter: str = "character", chunk_size: int = 2048, include_nodes: bool = False) -> None:
        super().__init__()
        self.chunker = CodeChunker(language=language, tokenizer_or_token_counter=tokenizer_or_token_counter, chunk_size=chunk_size, include_nodes=include_nodes)

    def _chunk(self, contents: list[str], **kwargs) -> list[list[str]]:
        result = []
        for content in contents:
            result.append([chunk.text for chunk in self.chunker.chunk(content)])
        return result
