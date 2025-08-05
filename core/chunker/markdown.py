from langchain_text_splitters import MarkdownHeaderTextSplitter

from core.chunker import Chunker


class MarkdownChunker(Chunker):
    def __init__(
        self,
        headers_to_split_on: list[tuple[str, str]] | None = None,
        return_each_line: bool = False,
    ) -> None:
        super().__init__()
        if headers_to_split_on is None:
            headers_to_split_on = [
                ("#", "Header 1"),
                ("##", "Header 2"),
                ("###", "Header 3"),
            ]
        self.chunker: MarkdownHeaderTextSplitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=headers_to_split_on,
            return_each_line=return_each_line,
        )

    def _chunk(self, contents: list[str], **kwargs) -> list[list[str]]:
        results = []
        for content in contents:
            chunks = self.chunker.split_text(content)
            results.append([chunk.page_content for chunk in chunks])
        return results

    def _meta(self, contents: list[str], **kwargs) -> list[list[str]]:
        metas = []
        for content in contents:
            chunks = self.chunker.split_text(content)
            metas.append([chunk.metadata for chunk in chunks])
        return metas

    def meta(self, contents: str | list[str], **kwargs) -> list[str] | list[list[str]]:
        batched = True
        if not isinstance(contents, list):
            batched = False
            contents = [contents]
        chunks = self._meta(contents=contents, **kwargs)
        if not batched:
            return chunks[0]
        return chunks
