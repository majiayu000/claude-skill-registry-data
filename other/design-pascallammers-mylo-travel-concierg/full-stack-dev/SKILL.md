---
name: full-stack-dev
description: Guide for building fullstack applications with Vue 3, FastAPI, Docker, and MySQL. Use this skill when developing or debugging applications using this specific technology stack including frontend (Vue 3, Element Plus, Pinia, Vue Router, Axios, Vite), backend (FastAPI, SQLAlchemy, Pydantic, JWT), containerization (Docker, Docker Compose), database (MySQL 8.0+), RESTful API design, authentication, and deployment workflows.
license: MIT
---

# Vue 3 + FastAPI 全端開發技能

## 技能用途

This skill provides procedural knowledge and reusable resources for building fullstack applications with Vue 3 + FastAPI architecture. It covers project initialization, API development, frontend integration, database operations, authentication, and containerized deployment.

## 何時使用此技能

Use this skill when:
- Initializing a new Vue 3 + FastAPI project
- Implementing RESTful APIs with FastAPI
- Integrating Vue 3 frontend with FastAPI backend
- Setting up JWT authentication
- Configuring Docker containerization
- Designing database schemas with SQLAlchemy
- Troubleshooting stack-specific issues
- Deploying fullstack applications

## 技術堆疊概覽

### 前端
- **Vue 3** (Composition API)
- **Element Plus** (UI 組件庫)
- **Pinia** (狀態管理)
- **Vue Router** (路由管理)
- **Axios** (HTTP 客戶端)
- **Vite** (建置工具)
- **Port**: 9080 (開發), 80 (生產/容器)

### 後端
- **FastAPI** (Web 框架)
- **Python 3.11+**
- **SQLAlchemy 2.0** (ORM,支援 async)
- **Pydantic v2** (資料驗證)
- **JWT** (認證)
- **Port**: 9100 (開發), 8000 (容器)

### 資料庫
- **MySQL 8.0+**
- **Port**: 33306 (Docker 映射), 3306 (容器內)

### 部署
- **Docker** + **Docker Compose**
- **Nginx** (前端反向代理)

## 核心工作流程

### 1. 專案初始化

For new projects, use the bundled initialization script:

```bash
uv run /path/to/skill-stack/scripts/init_project.py <project-name>
```

This script creates a complete project structure with:
- Backend FastAPI application with proper directory structure
- Frontend Vue 3 application with Vite configuration
- Docker Compose setup for all services
- Basic configuration files and examples

After initialization:
```bash
cd <project-name>
docker-compose up -d  # Start all services
```

### 2. API 開發流程

#### 步驟 A: 定義 Pydantic Schema

Create data validation models in `backend/app/schemas/`:

```python
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True  # Pydantic v2
```

#### 步驟 B: 定義 SQLAlchemy 模型

Create database models in `backend/app/models/`:

```python
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(50), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
```

#### 步驟 C: 實現服務層

Create business logic in `backend/app/services/`:

```python
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User
from app.schemas.user import UserCreate

async def get_user(db: AsyncSession, user_id: int):
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()

async def create_user(db: AsyncSession, user: UserCreate):
    db_user = User(
        email=user.email,
        username=user.username,
        hashed_password=hash_password(user.password)
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user
```

#### 步驟 D: 創建 API 路由

Create endpoints in `backend/app/api/`:

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.user import UserCreate, UserResponse
from app.services import user_service

router = APIRouter(prefix="/api/users", tags=["users"])

@router.post("/", response_model=UserResponse, status_code=201)
async def create_user(
    user: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    return await user_service.create_user(db, user=user)

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    user = await user_service.get_user(db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
```

### 3. 前端整合流程

#### 步驟 A: 配置 Axios

Create `frontend/src/utils/request.ts`:

```typescript
import axios from 'axios'
import { useUserStore } from '@/stores/user'

const service = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:9100',
  timeout: 15000,
})

// 請求攔截器: 添加 Token
service.interceptors.request.use((config) => {
  const userStore = useUserStore()
  if (userStore.token) {
    config.headers.Authorization = `Bearer ${userStore.token}`
  }
  return config
})

// 響應攔截器: 錯誤處理
service.interceptors.response.use(
  (response) => response.data,
  (error) => {
    // Handle 401, 403, 404, 422, 500 errors
    return Promise.reject(error)
  }
)

export default service
```

#### 步驟 B: 封裝 API 服務

Create `frontend/src/api/user.ts`:

```typescript
import request from '@/utils/request'

export const getUserList = (params?: { skip?: number; limit?: number }) => {
  return request({
    url: '/api/users',
    method: 'get',
    params,
  })
}

export const createUser = (data: any) => {
  return request({
    url: '/api/users',
    method: 'post',
    data,
  })
}
```

#### 步驟 C: 使用 Pinia Store

Create `frontend/src/stores/user.ts`:

```typescript
import { defineStore } from 'pinia'
import { ref } from 'vue'
import { login, getUserInfo } from '@/api/user'

export const useUserStore = defineStore('user', () => {
  const token = ref<string>('')
  const userInfo = ref<any>(null)

  async function loginAction(credentials: any) {
    const data = await login(credentials)
    token.value = data.access_token
    userInfo.value = data.user
  }

  return { token, userInfo, loginAction }
})
```

### 4. 認證實現

#### JWT Token 生成 (後端)

```python
from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=30))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)
```

#### 依賴注入保護 API

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
):
    # Decode JWT and get user from database
    # Raise HTTPException if invalid
    pass

@router.get("/me")
async def get_me(current_user = Depends(get_current_user)):
    return current_user
```

### 5. Docker 部署

#### 開發環境 (熱重載)

```bash
# 啟動所有服務
docker-compose up -d

# 查看日誌
docker-compose logs -f backend

# 重啟特定服務
docker-compose restart backend
```

#### 生產環境建置

```bash
# 建置映像
docker-compose build

# 啟動 (不使用開發模式掛載)
docker-compose -f docker-compose.prod.yml up -d
```

### 6. 資料庫遷移

Use Alembic for database migrations:

```bash
# 初始化 Alembic
cd backend
uv run alembic init alembic

# 創建遷移
uv run alembic revision --autogenerate -m "Create users table"

# 執行遷移
uv run alembic upgrade head

# 回退遷移
uv run alembic downgrade -1
```

## 參考資源

For detailed information, consult the bundled reference files:

1. **`references/tech-stack-details.md`**
   - 深入的技術細節和配置
   - 效能優化策略
   - 安全性最佳實踐
   - 測試策略
   - 監控與維護

2. **`references/api-design-guide.md`**
   - RESTful API 設計規範
   - 完整的 CRUD 範例
   - 錯誤處理模式
   - 前端 Axios 整合
   - OpenAPI 文件撰寫

Use Grep to search these files when specific information is needed:
```bash
# 搜尋特定主題
grep -i "jwt" references/*.md
grep -i "pydantic" references/*.md
grep -i "docker" references/*.md
```

## 常見問題解決

### CORS 錯誤
確認 FastAPI CORS 中間件已正確配置,並包含前端 URL。

### 資料庫連線失敗
檢查:
1. MySQL 容器是否正常運行
2. DATABASE_URL 環境變數是否正確
3. 連線池配置 (pool_pre_ping=True)

### JWT Token 無效
驗證:
1. SECRET_KEY 是否一致
2. Token 是否過期
3. 前端是否正確在 Header 中傳送

### 前端 API 請求失敗
檢查:
1. Axios baseURL 配置
2. 請求攔截器中的 Token 添加
3. 後端 API 端點是否正確

## 開發命令速查

```bash
# 後端
cd backend
uv venv                              # 創建虛擬環境
source .venv/bin/activate            # 啟用虛擬環境
uv pip install -r requirements.txt   # 安裝依賴
uvicorn main:app --reload --port 9100  # 啟動開發伺服器

# 前端
cd frontend
npm install    # 安裝依賴
npm run dev    # 啟動開發伺服器
npm run build  # 生產建置

# Docker
docker-compose up -d              # 啟動所有服務
docker-compose ps                 # 查看服務狀態
docker-compose logs -f [service]  # 查看日誌
docker-compose down               # 停止所有服務
docker-compose exec backend bash  # 進入容器
```

## 服務端口配置

| 服務 | 開發端口 | Docker 映射 | 容器內端口 |
|------|---------|------------|----------|
| 前端 | 9080 | 9080:80 | 80 |
| 後端 | 9100 | 9100:8000 | 8000 |
| MySQL | - | 33306:3306 | 3306 |
| API 文件 | http://localhost:9100/docs | - | - |

## 專案結構範例

```
my-project/
├── backend/
│   ├── app/
│   │   ├── api/           # API 路由
│   │   ├── core/          # 配置
│   │   ├── db/            # 資料庫
│   │   ├── models/        # SQLAlchemy 模型
│   │   ├── schemas/       # Pydantic schemas
│   │   └── services/      # 業務邏輯
│   ├── main.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── api/          # API 服務
│   │   ├── components/   # Vue 組件
│   │   ├── router/       # 路由
│   │   ├── stores/       # Pinia stores
│   │   ├── utils/        # 工具
│   │   └── views/        # 頁面
│   ├── package.json
│   └── Dockerfile
└── docker-compose.yml
```

---

**提示**: 使用 `uv run scripts/init_project.py <project-name>` 快速生成完整專案結構。
