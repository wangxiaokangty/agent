import os

import outlines
from dotenv import load_dotenv
from openai import OpenAI
from outlines.models.vllm import VLLM, AsyncVLLM
from pydantic import BaseModel


class LLMClient:
    def __init__(self, model_name: str = None, base_url: str = None):  # type: ignore
        if base_url is None:
            load_dotenv()

            base_url = os.getenv("OPENAI_BASE_URL")
            if not base_url:
                raise ValueError("please fill OPENAI_BASE_URL in .env file in the project's root")
        if model_name is None:
            model_name = os.getenv("MODEL_NAME")
            if not model_name:
                raise ValueError("please fill MODEL_NAME in .env file in the project's root")
        openai_client = OpenAI(base_url=base_url)
        self.model: VLLM | AsyncVLLM = outlines.from_vllm(openai_client, model_name)  # type: ignore

    def struct_generate(self, prompt: str, response_model: type[BaseModel]) -> str:
        result = self.model(prompt, response_model)
        return result
