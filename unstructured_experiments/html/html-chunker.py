from unstructured.chunking.basic import chunk_elements
from unstructured.staging.base import elements_from_json
import json


elements = elements_from_json(filename="./json/partition.json")
chunks = chunk_elements(elements=elements)

to_print = []
for chunk in chunks:
    to_print.append(chunk.to_dict())
    print(json.dumps(chunk.to_dict(), indent=4))

file_name = f"chunks.json"
with open(file_name, "w", encoding="utf-8") as f:
    json.dump(to_print, f, ensure_ascii=False, indent=4)
