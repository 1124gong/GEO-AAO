# GEO + AAO · 苏州产业园服务业务门户

以促进会「产业园服务」业务为核心的 GEO（内容信任地基）+ AAO（Agent 交易引擎）双线工程，个人账号 + 台式机起步版。

## 目录结构

| 目录 | 内容 | 作用 |
|---|---|---|
| site/ | 纯静态站（无构建依赖，4 页 + SEO 文件） | GEO 层，发布到 GitHub Pages |
| mcp-server/ | Python MCP Server + 示例园区数据 | AAO 层，本机/VPS 运行 |
| docs/ | 部署上线手册 | 从上线到监测的完整操作路径 |

## 快速开始

| 步骤 | 动作 | 详见 |
|---|---|---|
| 1 | site/ 推到 GitHub，开 Pages | docs/部署上线手册.md 第二节 |
| 2 | mcp-server/ 本机启动 + localtunnel 穿透 | 手册第三节 |
| 3 | Coze/元器 发布 Agent 挂 MCP 端点 | 手册第三节 |
| 4 | 每周跑 GEO 监测清单 | 手册第五节 |
| 5 | 验证通过后迁阿里云 VPS | 手册第四节 |

## 核心逻辑

GEO 让 AI 在答案里提到你（信任地基），AAO 让 Agent 直接调用你（交易引擎）；Agent 调用前会核验 GEO 内容做信源校验，两条线缺一不可。AAO 意向登记（intents.json）里的真实提问反哺 FAQ 内容，形成增长飞轮。
