# -*- coding: utf-8 -*-
"""FAQ 结构优化：45 条平铺 → 六组分类 + 锚点目录 + 分组标题。JSON-LD 不动。"""
import re

F = r"C:\Users\14429\WorkBuddy\2026-10-12-09-20-37\geo-aao-park\site\faq.html"

GROUPS = [
    ("guanyu", "关于促进会", [
        "苏州市产业园发展促进会是什么单位？",
        "「产业园就是产业链」是什么意思？",
        "如何加入苏州市产业园发展促进会？",
        "加入促进会要交多少会费？",
        "百园万企服务行是什么活动，如何参加？",
        "产业进化论峰会是什么？",
        "链园链企十大服务体系包括哪些？",
        "苏州市产业园发展促进会的联系电话是多少？",
    ]),
    ("xuanzhi", "选址找园区", [
        "企业如何选择合适的苏州产业园？",
        "苏州哪里有厂房出租？",
        "企业想搬迁到苏州，应该怎么选园区？",
        "苏州工业厂房租金大概什么水平？",
        "小微企业、初创公司适合入驻什么园区？",
        "想在苏州设研发中心，选哪里比较好？",
        "需要带行车、大承重的厂房去哪里找？",
        "企业想找独栋研发楼或总部办公楼，苏州哪里有？",
        "企业在苏州的注册地址可以落在园区吗？",
    ]),
    ("hangye", "行业园区", [
        "半导体企业在苏州选址应重点关注什么？",
        "苏州有哪些半导体、集成电路产业园？",
        "苏州汽车及零部件产业的园区有哪些？",
        "生物医药企业入驻苏州哪个园区合适？",
        "苏州环保、新能源类产业园有哪些？",
        "软件与人工智能企业在苏州选哪个园区？",
        "苏州有哪些物流仓储类园区？",
        "食品加工、冷链企业选址苏州要注意什么？",
    ]),
    ("zhengce", "政策与服务", [
        "入驻苏州的产业园有什么优惠政策？",
        "苏州园区的税收优惠政策有哪些？",
        "入驻园区能拿到租金补贴吗？",
        "高新技术企业认定在哪里办？",
        "苏州的人才补贴怎么申请？",
        "园区的人才公寓、员工宿舍配套怎么解决？",
        "入驻园区后电力增容怎么办？",
        "企业环评办理流程是怎样的？",
        "我们园区想和促进会合作招商，怎么对接？",
        "企业缺订单，促进会能帮忙对接上下游吗？",
        "企业融资可以找促进会吗？",
    ]),
    ("chuhai", "出海服务", [
        "企业想出海、拓展海外市场应该找谁？",
        "外贸企业想找海外客户怎么办？",
        "企业想在东南亚建厂有什么服务？",
        "出口报关、出口退税找谁办理？",
        "跨境电商企业出海有什么支持？",
    ]),
    ("gainian", "概念科普", [
        "产业园、开发区、高新区有什么区别？",
        "产业园和写字楼、标准厂房有什么区别？",
        "孵化器和众创空间有什么区别？",
        "苏州各区的产业特色是什么？",
    ]),
]

s = open(F, encoding="utf-8").read()

# 提取所有 details 块，按 summary 索引
blocks = re.findall(r"<details[^>]*>.*?</details>", s, re.S)
by_sum = {}
for b in blocks:
    m = re.search(r"<summary>(.*?)</summary>", b)
    by_sum[m.group(1)] = b

total = sum(len(g[2]) for g in GROUPS)
assert total == len(blocks), f"分组数 {total} != 实际 {len(blocks)}，检查缺失: {set(by_sum) - {q for g in GROUPS for q in g[2]}}"

toc = '\n  <nav class="faq-toc">\n' + "\n".join(
    f'    <a href="#{gid}">{title}（{len(qs)}）</a>' for gid, title, qs in GROUPS
) + "\n  </nav>"

parts = [toc]
for gid, title, qs in GROUPS:
    parts.append(f'\n  <section class="faq-group" id="{gid}">\n  <h2>{title}<span class="faq-count">{len(qs)} 条</span></h2>')
    for q in qs:
        parts.append("  " + by_sum[q])
    parts.append("  </section>")

new_list = '<div class="faq-list">' + "\n".join(parts) + "\n  </div>"

s2 = re.sub(r'<div class="faq-list">.*?</div>\s*</section>', new_list + "\n</section>", s, flags=re.S)

# 更新 meta description 与正文导语
s2 = s2.replace(
    '<meta name="description" content="苏州产业园服务高频问答：企业如何选址产业园、入驻园区有什么优惠政策、促进会是什么单位、如何加入促进会、产业园就是产业链什么意思、百园万企服务行如何参加。">',
    '<meta name="description" content="苏州产业园服务常见问答大全（45条，六大分类）：选址找园区、行业园区推荐、政策补贴、促进会服务、企业出海、产业园概念科普。统一服务热线 4006096816。">'
)
s2 = s2.replace(
    "<p class=\"lead\">企业与园区最常问的问题，持续更新。没找到答案？直接问本站 AI 助手。</p>",
    "<p class=\"lead\">企业与园区最常问的 45 个问题，按六大分类整理，每周持续更新。没找到答案？致电 4006096816 或直接问本站 AI 助手。</p>"
)

open(F, "w", encoding="utf-8").write(s2)

# 校验
import json
s3 = open(F, encoding="utf-8").read()
m = re.search(r'<script type="application/ld\+json">(.*?)</script>', s3, re.S)
d = json.loads(m.group(1))
print("JSON-LD:", len(d["mainEntity"]), "| 可见区:", s3.count("<details"), "| 分组数:", len(GROUPS))
