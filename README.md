# TaskHub

一个基于 **FastAPI + MySQL + SQLAlchemy** 构建的任务管理后端项目，提供用户认证、JWT 鉴权、任务 CRUD、分页筛选、关键词搜索、排序、用户数据隔离、自动化测试与 Docker 部署能力。

> 当前版本：`v1.0.0`

---

## 项目简介

TaskHub 是一个用于练习和展示现代 Python 后端开发流程的 RESTful API 项目。

项目完整实现了：

- 用户注册与登录
- JWT Bearer Token 鉴权
- 当前用户信息查询
- Task 创建、查询、更新、删除
- 用户级数据隔离
- 分页、筛选、搜索与排序
- MySQL 数据持久化
- Alembic 数据库迁移
- pytest 自动化测试
- Docker Compose 一键启动

项目采用分层结构，将 API、业务逻辑、数据访问、Schema 与数据库模型分离，便于维护和扩展。

---

## 技术栈

| 分类 | 技术 |
| --- | --- |
| Web Framework | FastAPI |
| ASGI Server | Uvicorn |
| ORM | SQLAlchemy 2.x |
| Database | MySQL 8 |
| Migration | Alembic |
| Validation | Pydantic |
| Authentication | JWT + OAuth2 Bearer |
| Password Hashing | pwdlib + Argon2 |
| MySQL Driver | PyMySQL |
| Testing | pytest + FastAPI TestClient + HTTPX |
| Containerization | Docker + Docker Compose |
| Python | Python 3.13 |

---

## 功能特性

### 用户认证

- 用户注册
- 用户名 / Email 登录
- 密码安全哈希存储
- JWT Access Token
- OAuth2 Bearer Token 鉴权
- 获取当前登录用户
- 重复 Email 冲突处理
- 错误密码 / 缺失 Token 返回 401

### Task 管理

- 创建 Task
- 查询 Task 列表
- 查询单个 Task
- 更新 Task
- 删除 Task
- Task 状态：`todo` / `in_progress` / `done`
- Task 优先级：`low` / `medium` / `high`
- 截止时间 `due_date`
- 分页
- 状态筛选
- 优先级筛选
- 关键词搜索
- 多字段排序

### 权限与数据隔离

每个 Task 都归属于创建它的用户。

用户只能查看、修改和删除自己的 Task。即使知道其他用户的 `task_id`，也无法读取、修改或删除对应任务。

---

## 项目结构

```text
taskhub/
├── alembic/
│   └── versions/
├── app/
│   ├── api/
│   │   ├── deps.py
│   │   └── v1/
│   │       ├── auth.py
│   │       ├── health.py
│   │       ├── tasks.py
│   │       └── users.py
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   ├── db/
│   │   ├── base.py
│   │   └── session.py
│   ├── models/
│   │   ├── user.py
│   │   └── task.py
│   ├── repositories/
│   │   ├── task_repository.py
│   │   └── user_repository.py
│   ├── schemas/
│   │   ├── auth.py
│   │   ├── task.py
│   │   └── user.py
│   ├── services/
│   │   ├── task_service.py
│   │   └── user_service.py
│   └── main.py
├── tests/
│   ├── conftest.py
│   ├── test_auth.py
│   └── test_tasks.py
├── .dockerignore
├── .env.example
├── .env.test.example
├── .env.docker.example
├── .gitignore
├── alembic.ini
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## API 概览

### Health

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | `/health` | 服务健康检查 |

### Auth

| Method | Endpoint | Description |
| --- | --- | --- |
| POST | `/api/v1/auth/register` | 注册用户 |
| POST | `/api/v1/auth/login` | 登录并获取 JWT |

### Users

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | `/api/v1/users/me` | 获取当前用户 |

### Tasks

| Method | Endpoint | Description |
| --- | --- | --- |
| POST | `/api/v1/tasks` | 创建 Task |
| GET | `/api/v1/tasks` | 查询 Task 列表 |
| GET | `/api/v1/tasks/{task_id}` | 查询单个 Task |
| PATCH | `/api/v1/tasks/{task_id}` | 更新 Task |
| DELETE | `/api/v1/tasks/{task_id}` | 删除 Task |

### Task 列表查询参数

`GET /api/v1/tasks` 支持：

| Parameter | Description |
| --- | --- |
| `page` | 页码，最小为 1 |
| `page_size` | 每页数量，1～100 |
| `status` | `todo` / `in_progress` / `done` |
| `priority` | `low` / `medium` / `high` |
| `keyword` | 标题 / 描述关键词搜索 |
| `sort_by` | 排序字段 |
| `order` | `asc` / `desc` |

示例：

```http
GET /api/v1/tasks?status=todo&priority=high&keyword=FastAPI&page=1&page_size=20&sort_by=created_at&order=desc
```

---

## 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/yibanban0923/taskhub.git
cd taskhub
```

### 2. 创建 Python 虚拟环境

```bash
python3.13 -m venv .venv
source .venv/bin/activate
```

### 3. 安装依赖

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. 创建开发环境配置

```bash
cp .env.example .env
```

修改 `.env`：

```env
APP_NAME=TaskHub
APP_ENV=development
APP_HOST=0.0.0.0
APP_PORT=8000

MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_USER=taskhub_user
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=taskhub_dev

SECRET_KEY=your_random_secret_key_at_least_32_bytes
ACCESS_TOKEN_EXPIRE_MINUTES=60
JWT_ALGORITHM=HS256
```

> `.env` 包含真实数据库密码和密钥，不应提交到 Git。

### 5. 准备数据库

请确保 MySQL 已启动，并创建：

```text
Database: taskhub_dev
User:     taskhub_user
```

数据库账号需要拥有 `taskhub_dev` 的读写权限。

### 6. 执行数据库迁移

```bash
alembic upgrade head
```

### 7. 启动 API

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

启动后：

```text
API:      http://127.0.0.1:8000
Swagger:  http://127.0.0.1:8000/docs
ReDoc:    http://127.0.0.1:8000/redoc
Health:   http://127.0.0.1:8000/health
```

Health Check：

```bash
curl http://127.0.0.1:8000/health
```

预期返回：

```json
{
  "status": "ok",
  "app": "TaskHub",
  "environment": "development"
}
```

---

## Docker 启动

项目支持使用 Docker Compose 同时启动 FastAPI 与 MySQL。

### 1. 创建 Docker 环境配置

```bash
cp .env.docker.example .env.docker
```

修改其中的真实密码和密钥。

### 2. 构建并启动

```bash
docker compose --env-file .env.docker up --build -d
```

### 3. 查看状态

```bash
docker compose --env-file .env.docker ps
```

默认端口：

```text
FastAPI       -> host :8000
Docker MySQL  -> host :3307
```

API 容器会在启动时先执行：

```bash
alembic upgrade head
```

随后启动 Uvicorn。

### 4. 查看 API 日志

```bash
docker compose --env-file .env.docker logs -f api
```

### 5. 停止服务

```bash
docker compose --env-file .env.docker down
```

> `docker compose down -v` 会同时删除 MySQL 数据卷，请谨慎使用。

---

## 自动化测试

测试使用独立数据库 `taskhub_test`，避免污染开发数据库。

### 1. 创建测试配置

```bash
cp .env.test.example .env.test
```

填写测试数据库账号，并确保：

```env
APP_ENV=test
MYSQL_DATABASE=taskhub_test
```

### 2. 运行测试

```bash
pytest -q
```

当前测试覆盖：

- 注册 → 登录 → 当前用户认证链路
- 重复 Email
- 错误密码
- 未登录访问受保护接口
- Task CRUD
- Task 分页与筛选
- 用户无法访问其他用户的 Task

测试启动时会检查数据库名；如果不是 `taskhub_test`，测试会直接终止。

---

## 使用示例

### 注册

```http
POST /api/v1/auth/register
Content-Type: application/json
```

```json
{
  "username": "alice",
  "email": "alice@example.com",
  "password": "password123"
}
```

### 登录

登录接口使用 `application/x-www-form-urlencoded`：

```text
username=alice
password=password123
```

成功后返回：

```json
{
  "access_token": "<JWT>",
  "token_type": "bearer"
}
```

### 访问受保护接口

```http
Authorization: Bearer <JWT>
```

例如：

```http
GET /api/v1/users/me
```

### 创建 Task

```http
POST /api/v1/tasks
Authorization: Bearer <JWT>
Content-Type: application/json
```

```json
{
  "title": "Learn FastAPI",
  "description": "Complete TaskHub backend",
  "status": "todo",
  "priority": "high"
}
```

---

## 数据模型

### User

主要字段：

```text
id
username
email
hashed_password
created_at
updated_at
```

### Task

主要字段：

```text
id
title
description
status
priority
due_date
user_id
created_at
updated_at
```

关系：

```text
User 1 -------- N Task
```

---

## 架构设计

```text
HTTP Request
     ↓
API / Router
     ↓
Service
     ↓
Repository
     ↓
SQLAlchemy ORM
     ↓
MySQL
```

各层职责：

- **API**：HTTP 请求、参数校验与依赖注入
- **Service**：业务规则与流程编排
- **Repository**：数据库查询与持久化
- **Schema**：请求 / 响应数据结构与校验
- **Model**：SQLAlchemy ORM 映射
- **Core**：配置、安全等基础能力

---

## 安全设计

当前版本包含：

- 密码仅保存哈希值
- JWT 设置过期时间
- 受保护接口要求 Bearer Token
- Task 查询绑定当前用户 ID
- 真实环境配置通过 `.gitignore` 排除
- pytest 强制使用独立测试数据库

---

## 后续计划

- 补充更多 401 / 404 / 409 / 422 边界测试
- 增加 GitHub Actions CI
- 锁定依赖版本
- 改进统一异常响应
- 增加日志与可观测性
- Docker 非 root 用户运行
- 发布 `v1.0.0` Release

---

## Repository

https://github.com/yibanban0923/taskhub

---

## Author

**yibanban0923**

TaskHub 是一个用于学习、实践和展示 Python Web 后端工程化流程的项目。
