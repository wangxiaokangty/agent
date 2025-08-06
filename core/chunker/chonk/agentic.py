from dotenv import load_dotenv
from core.chunker import Chunker
import os
from chonkie import SlumberChunker
from chonkie.genie import OpenAIGenie


class AgenticChunker(Chunker):
    def __init__(self, model_name: str | None = None, base_url: str | None = None) -> None:
        super().__init__()
        if base_url is None:
            load_dotenv()
            base_url = os.getenv("OPENAI_BASE_URL")
            if not base_url:
                raise ValueError("please fill OPENAI_BASE_URL in .env file in the project's root")
        if model_name is None:
            model_name = os.getenv("MODEL_NAME")
            if not model_name:
                raise ValueError("please fill MODEL_NAME in .env file in the project's root")
            
        self.genie = OpenAIGenie(model=model_name,base_url=base_url)
        self.chunker = SlumberChunker(
            genie=self.genie,                        # Genie interface to use
            tokenizer_or_token_counter="character",  # Default tokenizer (or use "gpt2", etc.)
            chunk_size=1024,                    # Maximum chunk size
            candidate_size=128,                 # How many tokens Genie looks at for potential splits
            min_characters_per_chunk=24,        # Minimum number of characters per chunk
            verbose=True                        # See the progress bar for the chunking process
        )

    def _chunk(self, contents: list[str], **kwargs) -> list[list[str]]:
        result = []
        for content in contents:
            result.append([chunk.text for chunk in self.chunker.chunk(content)])
        return result