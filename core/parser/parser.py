import base64
import re
from io import BytesIO
from pathlib import Path
from typing import Iterable

from PIL import Image
from rich.progress import track

from core.llm.mmclient import MMClient, convert_basemodel_to_xml_str

image_pattern_no_groups = r"(!\[.*?\]\(data:.*?;base64,.*?\))"
image_pattern_image_data = r"!\[.*?\]\(data:.*?;base64,(.*?)\)"
compiled_image_pattern_no_groups: re.Pattern[str] = re.compile(image_pattern_no_groups)
compiled_image_pattern_image_data: re.Pattern[str] = re.compile(image_pattern_image_data)


INSTRUCT = """
请结合上面的背景信息,用中文描述这张图片,用给定的json格式回复。
json格式对应的 python 的 pydantic 的 basemodel 为
class Description(BaseModel):
    descript: str
    type: Literal["流程图", "架构图", "示意图", "数据图表", "二维码"]
"""


def split_text_to_alternate_list(path: str | Path) -> list[str]:
    if isinstance(path, str):
        path = Path(path)
    results: list[str] = compiled_image_pattern_no_groups.split(path.read_text("utf-8"))
    texts = []
    assert len(results) % 2 == 1, "length of alternate list should be odd"
    for index in range(len(results)):
        if index % 2 == 0:
            texts.append(results[index])
    return texts


def extract_image_data_from_md(path: str | Path) -> list:
    if isinstance(path, str):
        path = Path(path)
    results: list[str] = compiled_image_pattern_image_data.split(path.read_text("utf-8"))
    images = []
    assert len(results) % 2 == 1, "length of alternate list should be odd"
    for index in range(len(results)):
        if index % 2:
            image_stream = BytesIO(base64.b64decode(results[index]))
            images.append(Image.open(image_stream))
    return images


def replace_image_with_descript(path: Path | str, client: MMClient) -> str:
    if not isinstance(path, Path):
        path = Path(path)
    texts: list[str] = split_text_to_alternate_list(path)
    images = extract_image_data_from_md(path)
    assert len(texts) == len(images) + 1, "parser result error"
    descriptions = []
    for index in range(len(images)):
        BACKGROUND_INFO: str = "".join(texts[max(index - 2,0) : index + 2])
        BACKGROUND_INFO = BACKGROUND_INFO + INSTRUCT
        discription = client.descript_image_with_text(images[index], BACKGROUND_INFO)
        xml_description = convert_basemodel_to_xml_str(discription)
        descriptions.append(xml_description)
    results = [texts[0]]
    for index in range(len(descriptions)):
        results.append(descriptions[index])
        results.append(texts[index + 1])
    return "".join(results)


def process_dir(path: Path | str, client: MMClient, target_dir:Path|str|None = None):
    if not isinstance(path, Path):
        path = Path(path)
    source_dir_path: Path = path
    if target_dir is None:
        target_dir = "results"
    target_dir_path: Path = source_dir_path.parent / target_dir
    target_dir_path.mkdir(exist_ok=True)
    source_files: list[Path] = list(source_dir_path.glob("*.md"))
    print(f"A total of {len(source_files)} files will be processed.")
    progress_bar: Iterable[Path] = track(source_files, description="Processing...")
    for source_file in progress_bar:
        target_file = target_dir_path / source_file.name
        content: str = replace_image_with_descript(source_file, client)
        target_file.write_text(content, encoding="utf-8")

if __name__ == "__main__":
    client = MMClient()
    process_dir("data/pdf.demo",client)