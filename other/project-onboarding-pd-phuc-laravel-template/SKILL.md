---
name: project-onboarding
description: >-
  Use when starting a new project from this template. Interviews the user to gather project
  requirements (domain, features, project mode, auth strategy, models), then auto-generates
  updated CLAUDE.md, AGENTS.md, and docs/architecture.md with project-specific information.
  Trigger keywords: "onboard", "setup project", "new project", "initialize", "bắt đầu dự án",
  "khởi tạo", "cấu hình dự án".
---

# Project Onboarding Skill

## Purpose

Automate the initial project setup by interviewing the user and generating all necessary
documentation so that AI agents understand the project's domain, architecture, and conventions
from the very first interaction.

## When to Use

- Starting a new project from this Laravel template
- Joining an existing project that lacks AI documentation
- Major architectural pivot requiring documentation refresh

## Workflow

### Phase 1: Project Mode Interview

Ask the user these questions **one group at a time**. Do NOT dump all questions at once.

#### Group 1 — Basics
1. **Tên dự án** là gì? (ví dụ: "E-commerce Platform", "CRM System")
2. **Mô tả ngắn** dự án (1-2 câu, domain chính)?
3. **Frontend mode**:
   - `blade-ssr` — Laravel render HTML (Blade + Tailwind + Alpine.js)
   - `react-spa` — React app riêng, Laravel chỉ làm API
   - `undecided` — Chưa quyết định (mặc định blade-ssr, chuyển sau được)

#### Group 2 — Domain & Models
4. **Các model/entity chính** là gì? (ví dụ: User, Product, Order, Category)
5. **Relationships chính** giữa các model? (ví dụ: User hasMany Order, Order belongsTo Product)
6. Có **status workflow** nào không? (ví dụ: Order: pending → paid → shipped → delivered)

#### Group 3 — Auth & Access
7. **Auth strategy**: Session only? Sanctum API? Cả hai? Google OAuth?
8. **Roles/permissions**: Có phân quyền không? (admin, moderator, user, etc.)
9. **Rate limiting**: Có cần giới hạn gì không? (IP-based, user-based)

#### Group 4 — Technical
10. **Database**: MySQL (default)? PostgreSQL? SQLite?
11. **Queue/Jobs**: Có cần xử lý background không? (email, file processing, etc.)
12. **Caching strategy**: Database? Redis? File?
13. **Third-party integrations**: Payment? Email? SMS? Cloud storage?

### Phase 2: Generate Documentation

After gathering answers, generate/update these files:

#### 1. Update `CLAUDE.md`

Replace the template content with project-specific information:

```markdown
# CLAUDE.md

## Stack
[Stack description based on answers — include project mode]

## Project Mode: [blade-ssr | react-spa]

## Commands
[Keep existing commands, add project-specific ones if needed]

## Architecture
### Core Domain: [Domain Name]
[Model descriptions, relationships, status workflows]

### Request Flow
[Based on project mode — Blade views OR JSON API]

### Authentication
[Based on auth strategy answers]

### Models & Relationships
| Model | Key Relations |
|-------|--------------|
[Table from interview answers]

## Key Files
[Update with project-specific key files]

## Conventions
[Keep template conventions, add project-specific ones]
```

#### 2. Update `AGENTS.md`

Add project-specific section:

```markdown
## Project: [Name]
[Description]

## Project Mode: [blade-ssr | react-spa]

## Domain Models
[From interview]

## Business Rules
[Key rules and constraints from interview]
```

#### 3. Create/Update `docs/architecture.md`

Add detailed architecture based on project mode:

- If `blade-ssr`: Document Blade layouts, component structure, view hierarchy
- If `react-spa`: Document API endpoints, React app structure, Sanctum SPA config

#### 4. Create `docs/features/` stubs

For each major feature identified in the interview, create a stub file:

```markdown
# Feature: [Name]

## Status: Planning

## Description
[From interview]

## Models Involved
[List]

## Routes
[To be defined]

## Notes
[Any constraints or requirements mentioned]
```

### Phase 3: Verify & Report

After generating all files:

1. List all files created/updated
2. Show a summary table of project configuration
3. Suggest next steps:
   - "Run `php artisan make:model [Model] -mfc` for each model"
   - "Create migrations based on the relationships defined"
   - "Set up `.env` with your database credentials"

## Output Format

After completing onboarding, present this summary:

```markdown
## ✅ Project Onboarding Complete

| Setting | Value |
|---------|-------|
| Project | [name] |
| Mode | [blade-ssr / react-spa] |
| Models | [list] |
| Auth | [strategy] |
| Database | [type] |

### Files Updated
- ✏️ CLAUDE.md — Project-specific agent instructions
- ✏️ AGENTS.md — Project-specific agent rules
- ✏️ docs/architecture.md — Architecture documentation
- 🆕 docs/features/[feature].md — Feature stubs

### Suggested Next Steps
1. ...
2. ...
3. ...
```

## Rules

1. **Ask, don't assume** — If the user says "e-commerce", still ask about specific models
2. **One group at a time** — Don't overwhelm with 13 questions at once
3. **Allow "skip"** — If user skips a question, use sensible defaults
4. **Vietnamese-friendly** — Respond in the user's language
5. **Don't touch code** — This skill only generates documentation, never source code
6. **Preserve existing content** — If CLAUDE.md already has project info, merge, don't overwrite
