# 苏州产业园服务 MCP Server

把促进会产业园服务业务封装为 AI Agent 可调用的标准工具（AAO 层核心）。

## 工具清单

| 工具 | 功能 | 输入 |
|---|---|---|
| search_park | 检索园区 | 关键词 / 产业方向 |
| match_park | 需求匹配候选园区 + 选址要点 | 产业 + 需求描述 |
| get_service_system | 十大服务体系介绍 | 无 |
| submit_intent | 登记选址/入会/对接意向 | 企业、联系方式、类型、描述 |

## 数据说明

| 文件 | 内容 | 维护 |
|---|---|---|
| data/parks.json | 园区台账（当前为示例数据） | 替换为真实台账，字段结构保持不变 |
| data/intents.json | 意向登记（运行时自动生成） | 定期导出跟进 |

## 本机运行

| 步骤 | 操作 |
|---|---|
| 1 装依赖 | pip install -r requirements.txt（建议用隔离 venv） |
| 2 启动 | python server.py |
| 3 验证 | 浏览器访问 http://localhost:8000/mcp 返回 406/405 即为在线（MCP 端点不接受 GET 内容） |
| 4 测试工具 | 用 MCP 客户端（如 Cursor、Cherry Studio）连接 http://localhost:8000/mcp 调用 search_park |

## 正式部署（已上线）

| 项 | 值 |
|---|---|
| 公网端点 | http://119.45.16.249:8100/mcp |
| 部署位置 | 阿里云 VPS /opt/park-mcp（Docker 容器 park-mcp，restart unless-stopped） |
| 数据目录 | VPS /opt/park-mcp/data（挂载进容器，意向登记持久化） |
| 更新数据 | 替换 VPS 上的 data/parks.json 后执行 docker restart park-mcp |

容器运维命令（VPS 上）：sudo docker logs/restart/stop park-mcp

## 备选暴露方式

| 方式 | 命令/说明 | 适用 |
|---|---|---|
| localtunnel | lt --port 8000（注意 loca.lt 有密码页，Agent 平台直连可能被拦） | 本机临时调试 |
| 本机直跑 | venv 内 python server.py，端点 http://localhost:8000/mcp | 开发调试 |

## 接入 Agent 生态

| 平台 | 接入方式 |
|---|---|
| Coze 扣子 | 插件 → MCP → 填入 http://公网地址:8000/mcp |
| Dify | 工具 → MCP Server → 填端点地址 |
| 微信元器 | 插件市场支持 MCP 端点接入 |
