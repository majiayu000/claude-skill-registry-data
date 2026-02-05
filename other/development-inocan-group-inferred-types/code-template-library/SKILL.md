---
name: Code Template Library
description: Maintain and organize a curated library of code templates, boilerplate, and scaffolds for rapid project initialization
---

# Code Template Library

## Purpose

Provide a comprehensive library of:
- Project scaffolds (starter templates)
- File templates (components, models, controllers)
- Configuration templates
- Common patterns and architectures
- Framework-specific boilerplate

## When to Use

Invoke this skill when:
- Starting a new project
- Adding a new feature/module
- Setting up development environment
- Creating standardized file structures
- Teaching project organization

## Instructions

### Step 1: Identify Template Need

Determine what template is required:
1. **Project Level**: Full project scaffold
2. **Module Level**: Feature module template
3. **File Level**: Single file template
4. **Config Level**: Configuration file
5. **Architecture Level**: Folder structure

### Step 2: Select Technology Stack

Identify the stack:
- **Frontend**: React, Vue, Angular, Svelte, Next.js
- **Backend**: Express, NestJS, Django, Flask, Spring Boot
- **Full Stack**: MERN, MEAN, JAMstack
- **Mobile**: React Native, Flutter
- **Desktop**: Electron, Tauri

### Step 3: Choose Template Complexity

Select appropriate level:
- **Minimal**: Bare bones, maximum flexibility
- **Standard**: Common features, best practices
- **Complete**: Full-featured, production-ready

### Step 4: Generate Template

Create template with:
- Proper folder structure
- Configuration files
- Example files
- Documentation (README)
- Setup instructions

## Project Templates

### React + TypeScript + Vite (Modern Frontend)

```
my-react-app/
├── public/
│   └── vite.svg
├── src/
│   ├── assets/
│   │   └── react.svg
│   ├── components/
│   │   ├── ui/
│   │   │   └── Button.tsx
│   │   └── layout/
│   │       ├── Header.tsx
│   │       └── Footer.tsx
│   ├── hooks/
│   │   └── useLocalStorage.ts
│   ├── lib/
│   │   └── utils.ts
│   ├── pages/
│   │   ├── Home.tsx
│   │   └── About.tsx
│   ├── services/
│   │   └── api.ts
│   ├── types/
│   │   └── index.ts
│   ├── App.tsx
│   ├── App.css
│   ├── main.tsx
│   └── vite-env.d.ts
├── .eslintrc.cjs
├── .gitignore
├── package.json
├── tsconfig.json
├── tsconfig.node.json
├── vite.config.ts
└── README.md
```

**Key Files**:

`vite.config.ts`:
```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    port: 3000,
    open: true,
  },
})
```

`tsconfig.json`:
```json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
```

---

### Express + TypeScript (Backend API)

```
my-api/
├── src/
│   ├── config/
│   │   ├── database.ts
│   │   └── environment.ts
│   ├── controllers/
│   │   └── user.controller.ts
│   ├── middleware/
│   │   ├── auth.middleware.ts
│   │   ├── error.middleware.ts
│   │   └── validation.middleware.ts
│   ├── models/
│   │   └── user.model.ts
│   ├── routes/
│   │   ├── index.ts
│   │   └── user.routes.ts
│   ├── services/
│   │   └── user.service.ts
│   ├── types/
│   │   └── express.d.ts
│   ├── utils/
│   │   ├── logger.ts
│   │   └── validators.ts
│   ├── app.ts
│   └── server.ts
├── tests/
│   ├── unit/
│   └── integration/
├── .env.example
├── .eslintrc.js
├── .gitignore
├── jest.config.js
├── package.json
├── tsconfig.json
└── README.md
```

**Key Files**:

`src/app.ts`:
```typescript
import express, { Application } from 'express';
import cors from 'cors';
import helmet from 'helmet';
import morgan from 'morgan';
import routes from './routes';
import { errorMiddleware } from './middleware/error.middleware';
import { logger } from './utils/logger';

const app: Application = express();

// Middleware
app.use(helmet());
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(morgan('combined', { stream: { write: message => logger.info(message.trim()) }}));

// Routes
app.use('/api', routes);

// Error handling
app.use(errorMiddleware);

export default app;
```

`src/server.ts`:
```typescript
import app from './app';
import { config } from './config/environment';
import { logger } from './utils/logger';

const PORT = config.port || 3000;

app.listen(PORT, () => {
  logger.info(`Server running on port ${PORT}`);
  logger.info(`Environment: ${config.env}`);
});
```

---

### Python FastAPI (Modern Python API)

```
my-fastapi-app/
├── app/
│   ├── api/
│   │   ├── v1/
│   │   │   ├── endpoints/
│   │   │   │   ├── __init__.py
│   │   │   │   └── users.py
│   │   │   └── router.py
│   │   └── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── security.py
│   │   └── dependencies.py
│   ├── db/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   └── session.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── user.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── user_service.py
│   ├── __init__.py
│   └── main.py
├── tests/
│   ├── __init__.py
│   └── test_users.py
├── .env.example
├── .gitignore
├── requirements.txt
├── pyproject.toml
└── README.md
```

**Key Files**:

`app/main.py`:
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.router import api_router
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
```

---

## File Templates

### React Component Template

```typescript
import { FC } from 'react';
import styles from './${ComponentName}.module.css';

interface ${ComponentName}Props {
  ${prop1}: ${Type1};
  ${prop2}?: ${Type2};
}

/**
 * ${ComponentName} - ${description}
 */
export const ${ComponentName}: FC<${ComponentName}Props> = ({
  ${prop1},
  ${prop2} = ${defaultValue}
}) => {
  return (
    <div className={styles.${componentName}}>
      {/* Component content */}
    </div>
  );
};
```

### Express Controller Template

```typescript
import { Request, Response, NextFunction } from 'express';
import { ${Service} } from '../services/${service}';

export class ${Controller}Controller {
  /**
   * Get all ${resources}
   */
  async getAll(req: Request, res: Response, next: NextFunction): Promise<void> {
    try {
      const ${resources} = await ${Service}.findAll();
      res.json({ success: true, data: ${resources} });
    } catch (error) {
      next(error);
    }
  }

  /**
   * Get ${resource} by ID
   */
  async getById(req: Request, res: Response, next: NextFunction): Promise<void> {
    try {
      const { id } = req.params;
      const ${resource} = await ${Service}.findById(id);
      if (!${resource}) {
        res.status(404).json({ success: false, error: '${Resource} not found' });
        return;
      }
      res.json({ success: true, data: ${resource} });
    } catch (error) {
      next(error);
    }
  }

  /**
   * Create new ${resource}
   */
  async create(req: Request, res: Response, next: NextFunction): Promise<void> {
    try {
      const ${resource} = await ${Service}.create(req.body);
      res.status(201).json({ success: true, data: ${resource} });
    } catch (error) {
      next(error);
    }
  }

  /**
   * Update ${resource}
   */
  async update(req: Request, res: Response, next: NextFunction): Promise<void> {
    try {
      const { id } = req.params;
      const ${resource} = await ${Service}.update(id, req.body);
      res.json({ success: true, data: ${resource} });
    } catch (error) {
      next(error);
    }
  }

  /**
   * Delete ${resource}
   */
  async delete(req: Request, res: Response, next: NextFunction): Promise<void> {
    try {
      const { id } = req.params;
      await ${Service}.delete(id);
      res.status(204).send();
    } catch (error) {
      next(error);
    }
  }
}
```

## Configuration Templates

### package.json (Node.js)

```json
{
  "name": "${project-name}",
  "version": "1.0.0",
  "description": "${description}",
  "main": "dist/index.js",
  "scripts": {
    "dev": "tsx watch src/server.ts",
    "build": "tsc",
    "start": "node dist/server.js",
    "test": "jest",
    "test:watch": "jest --watch",
    "test:coverage": "jest --coverage",
    "lint": "eslint src --ext .ts",
    "lint:fix": "eslint src --ext .ts --fix",
    "format": "prettier --write \"src/**/*.ts\""
  },
  "keywords": [],
  "author": "${author}",
  "license": "MIT",
  "devDependencies": {
    "@types/node": "^20.0.0",
    "@typescript-eslint/eslint-plugin": "^6.0.0",
    "@typescript-eslint/parser": "^6.0.0",
    "eslint": "^8.0.0",
    "jest": "^29.0.0",
    "prettier": "^3.0.0",
    "tsx": "^4.0.0",
    "typescript": "^5.0.0"
  },
  "dependencies": {
    "${dependency}": "${version}"
  }
}
```

### .gitignore (Comprehensive)

```
# Dependencies
node_modules/
vendor/
__pycache__/
*.pyc
.venv/
venv/
env/

# Build outputs
dist/
build/
*.egg-info/
target/

# Environment variables
.env
.env.local
.env.*.local

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Logs
logs/
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Testing
coverage/
.nyc_output/
.pytest_cache/

# Misc
.cache/
*.tmp
```

## Best Practices

1. **Modularity**: Keep templates modular and composable
2. **Documentation**: Always include README with setup instructions
3. **Environment**: Use .env files for configuration
4. **Types**: Include TypeScript types/interfaces
5. **Testing**: Include test setup and examples
6. **Linting**: Include linter and formatter configs
7. **Git**: Proper .gitignore from the start
8. **Security**: Don't commit secrets or credentials

## Output Format

When providing a template:

```
## ${TemplateName}

**Purpose**: ${purpose}

**Technology**: ${stack}

**Folder Structure**:
```
${structure}
```

**Setup Instructions**:
1. ${step1}
2. ${step2}

**Key Files**:
- `${file1}`: ${description}
- `${file2}`: ${description}

**Usage**:
```bash
${commands}
```
```

## Related Skills

- `snippet-generator`: For individual code snippets
- `project-scaffolder`: For generating full projects
- `config-generator`: For creating configuration files
- `boilerplate-cleaner`: For removing unnecessary boilerplate
