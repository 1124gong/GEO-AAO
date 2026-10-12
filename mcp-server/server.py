# -*- coding: utf-8 -*-
"""
苏州产业园服务 MCP Server（AAO 层核心）
=========================================
把促进会的「产业园服务」业务封装为 AI Agent 可调用的标准工具：

  1. search_park      按关键词/产业方向检索园区
  2. match_park       按企业需求智能匹配候选园区
  3. get_service_system  返回链园链企十大服务体系
  4. submit_intent    登记企业选址/入会/对接意向（落盘 data/intents.json）

运行方式（本机验证）:
    python server.py            # streamable-http 模式，监听 0.0.0.0:8000/mcp

外部 Agent 生态（Coze/元器/Dify）通过以下地址接入:
    http://<你的公网地址>:8000/mcp
    本机验证可用 localtunnel: lt --port 8000
"""
import json
import os
import uuid
from datetime import datetime
from pathlib import Path

from mcp.server.fastmcp import FastMCP

BASE = Path(__file__).parent
DATA_FILE = BASE / "data" / "parks.json"
INTENT_FILE = BASE / "data" / "intents.json"

mcp = FastMCP(
    "suzhou-park-service",
    host="0.0.0.0",
    port=8000,
)


def _load_db() -> dict:
    with open(DATA_FILE, encoding="utf-8") as f:
        return json.load(f)


def _save_intent(record: dict) -> None:
    intents = []
    if INTENT_FILE.exists():
        try:
            with open(INTENT_FILE, encoding="utf-8") as f:
                intents = json.load(f)
        except (json.JSONDecodeError, OSError):
            intents = []
    intents.append(record)
    with open(INTENT_FILE, "w", encoding="utf-8") as f:
        json.dump(intents, f, ensure_ascii=False, indent=2)


@mcp.tool()
def search_park(keyword: str = "", industry: str = "") -> str:
    """检索苏州地区产业园。

    Args:
        keyword: 园区名称关键词，如 "纳米"、"高铁新城"，留空则不过滤
        industry: 产业方向，如 "半导体"、"智能制造"、"生物医药"，留空则不过滤

    Returns:
        匹配的园区列表（名称、板块、产业方向、载体类型、特色）
    """
    db = _load_db()
    kw = keyword.strip().lower()
    ind = industry.strip()
    results = []
    for p in db["parks"]:
        if kw and kw not in (p["名称"] + p.get("板块", "") + p.get("地址", "")).lower():
            continue
        if ind and not any(ind in d for d in p["产业方向"]):
            continue
        results.append(p)
    if not results:
        return json.dumps(
            {"count": 0, "msg": "未匹配到园区，可提交意向由促进会人工匹配",
             "hint": "调用 submit_intent 登记需求"},
            ensure_ascii=False,
        )
    return json.dumps({"count": len(results), "parks": results},
                      ensure_ascii=False, indent=2)


@mcp.tool()
def match_park(industry: str, requirement: str = "") -> str:
    """按企业需求匹配候选园区（选址第一步）。

    Args:
        industry: 企业所属产业，如 "半导体"、"智能制造"、"生物医药"
        requirement: 具体需求描述，如 "需要5000平米洁净厂房，关注政策补贴"

    Returns:
        按产业方向匹配的候选园区列表与选址要点提示
    """
    db = _load_db()
    matched = [p for p in db["parks"]
               if any(industry in d for d in p["产业方向"])]
    tips = {
        "半导体": "关注洁净厂房等级、危化品许可、超纯水与电力稳定性、封测配套半径",
        "智能制造": "关注层高、地面承重、货梯吨位、用电容量",
        "生物医药": "关注环评、动物房、GMP 改造条件、注册检验配套",
        "人工智能": "关注算力资源、人才社区、政策补贴力度",
    }
    return json.dumps(
        {
            "industry": industry,
            "requirement": requirement,
            "candidates": matched,
            "选址要点": tips.get(industry, "建议从产业方向、载体硬件、政策资源、配套半径四维评估"),
            "next_step": "调用 submit_intent 登记意向，促进会出具正式比选报告",
        },
        ensure_ascii=False, indent=2,
    )


@mcp.tool()
def get_service_system() -> str:
    """获取苏州市产业园发展促进会「链园链企」十大服务体系与品牌项目介绍。"""
    db = _load_db()
    return json.dumps(db["service_system"], ensure_ascii=False, indent=2)


@mcp.tool()
def submit_intent(company: str, contact: str, need_type: str,
                  description: str) -> str:
    """登记企业意向（选址/入会/资源对接），促进会跟进。

    Args:
        company: 企业或园区名称
        contact: 联系人与方式
        need_type: 意向类型，可选：选址对接 / 入会咨询 / 资源对接 / 其他
        description: 需求描述
    """
    record = {
        "id": uuid.uuid4().hex[:12],
        "company": company,
        "contact": contact,
        "need_type": need_type,
        "description": description,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "待跟进",
    }
    _save_intent(record)
    return json.dumps(
        {"ok": True, "msg": "意向已登记，促进会将通过留存的联系方式跟进",
         "record_id": record["id"]},
        ensure_ascii=False,
    )


if __name__ == "__main__":
    print("苏州产业园服务 MCP Server 启动中 ... 端点: http://0.0.0.0:8000/mcp")
    mcp.run(transport="streamable-http")
