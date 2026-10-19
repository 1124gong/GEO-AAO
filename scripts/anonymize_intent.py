# -*- coding: utf-8 -*-
import json

p = "/opt/park-mcp/data/intents.json"
d = json.load(open(p, encoding="utf-8"))
for r in d:
    if r["id"] == "df2acee75e1e":
        r["company"] = "律所（匿名登记）"
        r["contact"] = "不留存（委托方要求匿名）"
        r["description"] = "选址对接：律师事务所，需约2000平方米写字楼载体；联系方式由促进会专人线下掌握"
json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("已匿名化，当前台账：")
for r in d:
    print(" ", r["id"], "|", r["company"], "|", r["need_type"])
