from typing import Literal

import torch
from langchain_experimental.text_splitter import SemanticChunker as SeChunker
from langchain_huggingface import HuggingFaceEmbeddings

from core.chunker import Chunker


class SemanticChunker(Chunker):
    def __init__(
        self,
        model_name: str = "moka-ai/m3e-base",
        breakpoint_threshold_type: str = "percentile",
        breakpoint_threshold_amount: float = 0.95,
    ) -> None:
        super().__init__()
        device: Literal["cuda"] | Literal["cpu"] = "cuda" if torch.cuda.is_available() else "cpu"
        model_kwargs: dict[str, str] = {"device": device}
        encode_kwargs: dict[str, bool] = {"normalize_embeddings": True}
        self.embeddings = HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs=model_kwargs,
            encode_kwargs=encode_kwargs,
        )
        self.chunker = SeChunker(
            self.embeddings,
            breakpoint_threshold_type=breakpoint_threshold_type,  # type: ignore
            breakpoint_threshold_amount=breakpoint_threshold_amount,
        )

    def _chunk(self, contents: list[str], **kwargs) -> list[list[str]]:
        results = []
        for content in contents:
            results.append(self.chunker.split_text(content))
        return results
