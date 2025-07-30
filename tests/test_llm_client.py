from datetime import date

from pydantic import BaseModel

from core.llm.client import LLMClient


class Character(BaseModel):
    name: str
    birth_date: date
    skills: dict | list[str]
    description: str


def test_client_initialize_from_dotenv():
    client = LLMClient()
    assert client is not None

def test_struct_output():
    client = LLMClient()
    result = client.struct_generate("请给我随机生成一个人物", Character)
    assert result is not None
