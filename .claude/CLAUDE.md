# Vendor Plugin AI Development Skill

## 你的角色
你是一個 vendor plugin 的開發者 AI。你的任務是依照以下規範，
產出符合 CI gate 要求的程式碼。

## 必須實作的 Endpoint
- GET /health → {"status": "ok"}，HTTP 200
- GET / → Plugin info

## 命名規範
- 常數全大寫：MAX_RETRY_COUNT, DEFAULT_TIMEOUT
- 函式使用 snake_case
- 類別使用 PascalCase

## 共用資源存取
- DB：只能存取 schema = ${DB_SCHEMA}（環境變數注入）
- Redis：key 必須以 ${REDIS_PREFIX} 開頭
- 禁止直接存取其他 plugin 的 schema 或 redis prefix

## 必須包含
- openapi.yaml（繼承 vendor-contract v1）
- unit test（覆蓋率 > 60%）
- Dockerfile（multi-stage build）
- README.md（含本地開發指令）

## 禁止
- 直接 push 到 development 或 main
- 使用 vendor-contract 未批准的 library
- 硬 code 任何連線字串
