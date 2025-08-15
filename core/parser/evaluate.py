import base64
import re
from io import BytesIO
from pathlib import Path

from PIL import Image
from PIL.ImageFile import ImageFile

image_pattern: re.Pattern[str] = re.compile(r"!\[.*?\]\(data:.*?;base64,(.*?)\)")
desciption_pattern: re.Pattern[str] = re.compile("(<Image>.*?</Image>)", re.DOTALL)


def find_images_list(dir_path: str | Path) -> list:
    dir_path = Path(dir_path)
    files = sorted(dir_path.glob("*.md"))
    res = []
    for file in files:
        content = file.read_text(encoding="utf-8")
        images = image_pattern.findall(content)
        res.append(images)
    return res


def find_description_list(dir_path: str | Path) -> list:
    dir_path = Path(dir_path)
    files = sorted(dir_path.glob("*.md"))
    res = []
    for file in files:
        content = file.read_text(encoding="utf-8")
        images = desciption_pattern.findall(content)
        res.append(images)
    return res


if __name__ == "__main__":
    images = find_images_list("data/pdf.demo")
    desciptions = find_description_list("data/qwen-results")
    result_path = Path("data/sample")
    result_path.mkdir(exist_ok=True)

    target_picture_dir: Path = result_path / "picture"
    target_descrip_dir: Path = result_path / "descrip"
    target_picture_dir.mkdir(exist_ok=True)
    target_descrip_dir.mkdir(exist_ok=True)

    index = 1
    for image_list, desciption_list in zip(images, desciptions):
        for image_str, description in zip(image_list, desciption_list):
            image: ImageFile = Image.open(BytesIO(base64.b64decode(image_str)))
            target_picture_file = target_picture_dir / f"{index}.png"
            target_descrip_file = target_descrip_dir / f"{index}.txt"
            image.save(target_picture_file)
            target_descrip_file.write_text(description, encoding="utf-8")
            index = index + 1
