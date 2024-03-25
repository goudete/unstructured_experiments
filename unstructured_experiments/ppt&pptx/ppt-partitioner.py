from unstructured.partition.pptx import partition_pptx

import json

elements = partition_pptx(filename="./sample.pptx")

to_print = []
for element in elements:
    to_print.append(element.to_dict())
    print(json.dumps(element.to_dict(), indent=4))

file_name = f"pptx.json"
with open(file_name, "w", encoding="utf-8") as f:
    json.dump(to_print, f, ensure_ascii=False, indent=4)
