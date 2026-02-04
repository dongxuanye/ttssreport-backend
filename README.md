# TTSS Report 后端服务 - 已迁移

## ⚠️ 重要通知

此仓库已**停止维护**，代码已整合到统一仓库：

## 新仓库地址

https://github.com/immarkfu/ttssreport

## 迁移详情

### 为什么迁移？

为了简化项目管理和部署，前后端代码已整合到一个仓库：

- **前端**：React + Vite + TailwindCSS
- **后端**：FastAPI + Tushare + MySQL
- **Docker 配置**：docker-compose.yml
- **CI/CD**：GitHub Actions

### 新仓库结构

```
ttssreport/
├── client/          # 前端代码
├── server/          # 后端代码（原此仓库内容）
├── docker-compose.yml
├── Dockerfile
├── Dockerfile.backend
└── .github/workflows/
    └── ci.yml
```

## 后续操作

1. 所有新代码提交到：https://github.com/immarkfu/ttssreport
2. CI/CD 已在新仓库配置
3. Docker 部署请使用新仓库

---

**迁移日期**：2026-02-04  
**迁移者**：Mark + OpenClaw
