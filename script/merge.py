from pathlib import Path
import re
from typing import Literal
from rich.pretty import pprint
from core.llm.client import LLMClient
from pydantic import BaseModel
from rich.progress import track

desciption_pattern: re.Pattern[str] = re.compile("(<Image>.*?</Image>)",re.DOTALL)

class Answer(BaseModel):
    reason: str
    answer: Literal["是","不是"]


def get_prompt(begin:str,end:str):
    return f"""
        请问下面的两段话在逻辑上是一体的吗？如果这两局话拼在一起语意顺畅则这两段话在逻辑上就是一体的。
        这是第一段话：{begin}
        这是第二段话：{end}
        请首先回复我原因，然后再回答“是”或者“不是”,
        用下面的 python 的 pydantic 库的 basemodel 对应的 json 回答我
        class Answer(BaseModel):
            reason: str
            answer: Literal["是","不是"]
    """

def get_page_number(path) -> int:
    match: re.Match[str] | None = re.search(r'_page_(\d+)_nohf\.md$', str(path))
    assert match
    return int(match.group(1))


def remove_discription(content:str) -> str:
    return desciption_pattern.sub('',content)


def extract_file_begin_and_end(path:Path|str,length:int = 100) -> tuple[str, str]:
    if not isinstance(path,Path):
        path = Path(path)
    content: str = path.read_text(encoding="utf-8")
    content = remove_discription(content)
    return content[:length],content[-length:]


def get_begins_ends_list(dir_path:Path|str):
    if not isinstance(dir_path,Path):
        dir_path = Path(dir_path)
    begins_list = []
    ends_list = []
    files: list[Path] = list(dir_path.glob("*.md"))
    files = sorted(files,key=get_page_number)
    for file in files:
        begin,end = extract_file_begin_and_end(file)
        begins_list.append(begin)
        ends_list.append(end)
    return begins_list,ends_list

if __name__ == "__main__":
    client = LLMClient()
    begin_list,end_list = get_begins_ends_list("data/qwen-results")
    logs_path = Path("data") / "logs"
    logs_path.mkdir(exist_ok=True)
    progress_bar = track(enumerate(begin_list),description="processing...")
    for index,begin in progress_bar:
        if index == 0:
            continue
        prompt = get_prompt(end_list[index-1],begin)
        answer: str = client.struct_generate(prompt,Answer)
        log_file = logs_path / f"{index}.txt"
        log_file.write_text(answer,encoding="utf-8")