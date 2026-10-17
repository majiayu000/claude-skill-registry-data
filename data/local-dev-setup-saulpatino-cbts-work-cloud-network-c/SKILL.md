---
name: local-dev-setup
description: Set up and manage local development environment for the Cloud FinOps Assessment platform
---

# Local Development Setup

Use this skill to:
- Start the full stack (API, Web, Database) locally
- Set up environment variables
- Initialize Docker containers
- Run migrations
- Verify all services are running

## Common Tasks

### Start Development Stack
```bash
docker-compose up -d
npm install
npm run dev:api
npm run dev:web
```

### Initialize Database
```bash
docker exec -it cfa-sql npm run migrate:up
```

### Check Service Status
```bash
docker ps
curl http://localhost:3000/health
```

### Stop All Services
```bash
docker-compose down
```
