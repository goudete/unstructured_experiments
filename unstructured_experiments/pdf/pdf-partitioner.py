from io import BytesIO
import json
import requests
from enum import Enum


from unstructured.partition.pdf import partition_pdf
from unstructured.partition.auto import partition
from unstructured.cleaners.core import clean
from unstructured.chunking.basic import chunk_elements


class PartitionStrategy(Enum):
    AUTO = "auto"
    FAST = "fast"
    HI_RES = "hi_res"
    OCR_ONLY = "ocr_only"


docs = [
    {
        "url": "https://athena-web-app-public-assets.s3.amazonaws.com/nux-tmp/523-dm-1.pdf",
        "id": "doc_18fa73fb-cb91-4d50-b3b5-1b5dd1ccd208",
    },
    {
        "url": "https://athena-web-app-public-assets.s3.amazonaws.com/nux-tmp/R46947.pdf",
        "id": "doc_82e80610-70ac-4b8d-826e-2a4d48a56db9",
    },
    {
        "url": "https://athena-web-app-public-assets.s3.amazonaws.com/nux-tmp/climate-change-policy.pdf",
        "id": "doc_5f92a142-ebe3-4f68-b9fb-3478058407f7",
    },
    {
        "url": "https://athena-web-app-public-assets.s3.amazonaws.com/nux-tmp/Global-Landscape-of-Climate-Finance-2021.pdf",
        "id": "doc_20d672f5-dc5a-46e0-a2b9-06476b0522e7",
    },
]


def partition(file_url: str):
  # get content
  response = requests.get(file_url)
  file_content = response.content

  # Convert bytes content to a file-like object
  file_like_object = BytesIO(file_content)
  partitions = partition_pdf(file=file_like_object, mode=PartitionStrategy.HI_RES)

  return partitions


def clean_text(text: str):
    clean_text = clean(text, bullets=True, extra_whitespace=True, dashes=True)
    print("🚀 ~ clean_text:", clean_text)
    return clean_text


def chunk(element):
    chunk_elements()


for doc in docs:
    print("processing url: ", doc["url"])
    partitions = partition(doc["url"])
    to_print = []
    for p in partitions:
        p = p.to_dict()
        p_obj = {
            "text": clean_text(p["text"]),
            "type": p["type"],
        }
        to_print.append(p_obj)

    filename = doc["url"].split("/")[-1]
    with open(
        f"{filename}-[{PartitionStrategy.HI_RES}].json", "w", encoding="utf-8"
    ) as f:
        json.dump(to_print, f, ensure_ascii=False, indent=4)
