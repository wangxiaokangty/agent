import os
from typing import Literal

import outlines
import PIL
from dotenv import load_dotenv
from openai import OpenAI
from outlines.inputs import Image
from outlines.models.vllm import VLLM, AsyncVLLM
from pydantic import BaseModel
from pydantic_xml import BaseXmlModel, element


class Description(BaseModel):
    descript: str
    type: Literal["流程图", "架构图", "示意图", "数据图表", "二维码"]


class ImageDescription(BaseXmlModel, tag="Image"):
    descript: str = element(tag="Description")
    type: str = element(tag="Type")


def convert_basemodel_to_xml_str(data: BaseModel):
    return ImageDescription(**data.model_dump()).to_xml(pretty_print=True, encoding="UTF-8").decode("utf-8")  # type: ignore


class MMClient:
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

    def struct_generate(self, prompt: str | list, response_model: type[BaseModel]) -> BaseModel:
        result = self.model(prompt, response_model)
        return response_model.model_validate_json(result)  # type: ignore

    def descript_image_with_text(self, image: PIL.Image, prompt: str, response_model: type[BaseModel] = Description) -> BaseModel:  # type: ignore
        model_inputs = [prompt, Image(image)]
        result = self.model(model_inputs, response_model)
        return response_model.model_validate_json(result)  # type: ignore
