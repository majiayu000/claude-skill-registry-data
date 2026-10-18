---
name: laravel-nova
description: "Build custom administration panels using Laravel Nova with advanced fields, lenses, actions, and cards."
category: backend
tags: [laravel, php, nova, admin, dashboard]
complexity: advanced
risk: low
compatibility: [claude-code, antigravity, gemini-cli, cursor, copilot, codex-cli, autohand, kiro]
source: antigravity-official
version: "1.0.0"
date_added: "2026-07-10"
last_updated: "2026-07-10"
---

# Laravel Nova Expert

## Purpose
Manage and implement Laravel Nova Expert requirements efficiently within enterprise applications.

## Core Concepts
Detailed operational framework for Laravel Nova Expert:

### 1️⃣ Overview and Strategy
Understanding boundaries, rules, and best practices for the laravel-nova feature domain.

### 2️⃣ Code Implementation Reference
```javascript
// App/Nova/User.php
public function fields(NovaRequest $request)
{
    return [
        ID::make()->sortable(),
        Text::make('Name')->rules('required', 'max:255'),
        Email::make('Email')->rules('required', 'email', 'unique:users,email,{{resourceId}}'),
        Avatar::make('Avatar')->disk('s3'),
    ];
}
```

### 3️⃣ Checklist & Validation Rules
- [ ] Integration validation checklist completed.
- [ ] Code conventions and naming rules followed.
- [ ] Strict type safety constraints verified.
- [ ] Security standards checked.

## Outputs
1. System integration pattern definitions.
2. Code templates and examples.
3. Test validation checklists.
