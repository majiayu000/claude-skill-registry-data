---
name: companion-project-creator
description: Create complete runnable companion projects for articles - scaffolded projects, not snippets
---

# Companion Project Creator

Create **complete, executable companion projects** that readers can clone and run immediately.

## Core Principle

> **Companion projects must be COMPLETE and RUNNABLE, not snippets or partial code.**

A Laravel companion project is a full Laravel installation. A Node companion project is a full Node project. A document companion project is a complete, usable document.

## ⚠️ CRITICAL: Mandatory Verification

**Every code companion project MUST be verified by actually running it before it is considered complete.**

This is NOT optional. A companion project that hasn't been executed and tested is NOT complete.

### Verification Workflow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    COMPANION PROJECT CREATION FLOW                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  1. SCAFFOLD          Create base project (composer/npm/etc)                │
│         ↓                                                                   │
│  2. CUSTOMIZE         Add article-specific code                             │
│         ↓                                                                   │
│  3. VERIFY ⭐         ACTUALLY RUN THE CODE                                 │
│         │                                                                   │
│         ├── Install dependencies    → Must succeed                          │
│         ├── Run application         → Must start without errors             │
│         └── Run tests               → All tests must pass                   │
│         │                                                                   │
│         ├── ✅ All pass → Companion project complete                        │
│         └── ❌ Any fail → Fix code, return to step 3                        │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Verification Commands by Type

| Type | Install | Run | Test |
|------|---------|-----|------|
| **Laravel** | `composer install` | `php artisan serve` | `php artisan test` |
| **Node.js** | `npm install` | `npm start` or `node src/index.js` | `npm test` |
| **Python** | `pip install -r requirements.txt` | `python src/main.py` | `pytest` |
| **React** | `npm install` | `npm start` | `npm test` |
| **Vue** | `npm install` | `npm run dev` | `npm test` |
| **Go** | `go mod download` | `go run .` | `go test ./...` |

### What "Verify" Means

**You must actually execute these commands and confirm they succeed:**

```bash
# Example: Laravel verification
cd code

# 1. Install - MUST SUCCEED
composer install
# ✓ Check: No errors, vendor/ folder created

# 2. Setup - MUST SUCCEED  
cp .env.example .env
php artisan key:generate
touch database/database.sqlite
php artisan migrate
# ✓ Check: No errors, database has tables

# 3. Run - MUST START
php artisan serve &
# ✓ Check: Server starts on localhost:8000
# ✓ Check: Can access in browser (if web app)
# Then stop the server

# 4. Test - ALL MUST PASS
php artisan test
# ✓ Check: "Tests: X passed" with 0 failures
```

**If ANY step fails:**
1. Read the error message
2. Fix the code
3. Re-run verification from step 1
4. Repeat until ALL steps pass

### Verification Checklist

Before marking a companion project complete, confirm:

- [ ] `install_command` executed successfully (no errors)
- [ ] All dependencies installed (vendor/, node_modules/, etc. exists)
- [ ] `run_command` starts the application without errors
- [ ] Application is accessible (if web app, can load in browser)
- [ ] `test_command` executed successfully
- [ ] All tests pass (0 failures)
- [ ] No warnings that indicate missing functionality

**DO NOT proceed to the next phase until all boxes are checked.**

---

## Companion Project Types

### 1. Code Companion Projects (`code`)

Complete application installations that can be:
- Cloned/copied
- Installed with one command
- Run immediately
- Tested

#### Laravel Application

**Creation Process:**

```bash
# 1. Create full Laravel project
cd content/articles/YYYY_MM_DD_slug/
composer create-project laravel/laravel code --prefer-dist

# 2. Configure for SQLite (no external DB)
cd code
cp .env.example .env
sed -i 's/DB_CONNECTION=mysql/DB_CONNECTION=sqlite/' .env
touch database/database.sqlite
php artisan key:generate

# 3. Install Pest
composer require pestphp/pest --dev --with-all-dependencies
php artisan pest:install

# 4. Add article-specific code
# - Models, Controllers, Routes, Views
# - Migrations, Seeders
# - Tests

# 5. VERIFY - Run migrations and tests
php artisan migrate
php artisan test
# ⚠️ DO NOT CONTINUE IF TESTS FAIL
```

**Required Files (auto-generated by Laravel):**
```
code/
├── app/
│   ├── Http/Controllers/
│   ├── Models/
│   └── Providers/
├── bootstrap/
├── config/
├── database/
│   ├── migrations/
│   ├── seeders/
│   └── database.sqlite
├── public/
├── resources/views/
├── routes/
│   ├── web.php
│   └── api.php
├── storage/
├── tests/
│   ├── Feature/
│   └── Unit/
├── .env
├── .env.example
├── artisan
├── composer.json
├── composer.lock
├── package.json
├── phpunit.xml
└── README.md          # Custom: explains the companion project
```

**Article-Specific Additions:**
- Custom models in `app/Models/`
- Custom controllers in `app/Http/Controllers/`
- Custom routes in `routes/web.php` or `routes/api.php`
- Custom views in `resources/views/`
- Custom migrations in `database/migrations/`
- Custom seeders in `database/seeders/`
- Feature tests in `tests/Feature/`

**README.md Template:**
```markdown
# Companion Project: [Article Topic]

Complete Laravel application demonstrating [concept].

## Requirements

- PHP 8.2+
- Composer

## Installation

\`\`\`bash
cd code
composer install
cp .env.example .env
php artisan key:generate
touch database/database.sqlite
php artisan migrate --seed
\`\`\`

## Run the Application

\`\`\`bash
php artisan serve
\`\`\`

Visit http://localhost:8000 to see the example.

## Run Tests

\`\`\`bash
php artisan test
\`\`\`

## What This Demonstrates

1. [Concept 1] - See `app/Models/Example.php`
2. [Concept 2] - See `app/Http/Controllers/ExampleController.php`
3. [Concept 3] - See `tests/Feature/ExampleTest.php`

## Key Files

| File | Description |
|------|-------------|
| `app/Models/Post.php` | Demonstrates [concept] |
| `routes/web.php` | Routes for [feature] |
| `tests/Feature/PostTest.php` | Tests for [feature] |

## Article Reference

This companion project accompanies: "[Article Title]"
```

#### Node.js Application

**Creation Process:**

```bash
# 1. Create project
cd content/articles/YYYY_MM_DD_slug/
mkdir code && cd code
npm init -y

# 2. Install dependencies
npm install express
npm install --save-dev jest

# 3. Configure package.json
# Add scripts: "start", "test", "dev"

# 4. Add article-specific code
# 5. Run tests
npm test
```

**Structure:**
```
code/
├── src/
│   ├── index.js
│   ├── routes/
│   └── controllers/
├── tests/
│   └── example.test.js
├── package.json
├── package-lock.json
└── README.md
```

#### Python Application

**Creation Process:**

```bash
# 1. Create project
cd content/articles/YYYY_MM_DD_slug/
mkdir code && cd code
python -m venv venv

# 2. Create requirements.txt
# 3. Add article-specific code
# 4. Add tests with pytest
```

**Structure:**
```
code/
├── src/
│   └── main.py
├── tests/
│   └── test_main.py
├── requirements.txt
├── setup.py
└── README.md
```

### 2. Document Companion Projects (`document`)

Complete, usable documents that readers can adapt.

**Types:**
- Project plans
- Technical specifications
- Process documents
- Meeting templates
- Report templates

**Structure:**
```
code/
├── templates/
│   ├── project-plan-template.md
│   └── sprint-planning-template.md
├── examples/
│   ├── project-plan-filled.md
│   └── sprint-planning-filled.md
└── README.md
```

**Each template must be:**
- Complete (all sections present)
- Well-commented (explain each section)
- Ready to use (just fill in the blanks)

### 3. Diagram Companion Projects (`diagram`)

Complete Mermaid diagrams that render correctly.

**Structure:**
```
code/
├── diagrams/
│   ├── architecture.mermaid
│   ├── sequence.mermaid
│   └── flowchart.mermaid
├── rendered/           # Optional: PNG exports
│   └── architecture.png
└── README.md
```

**Each diagram must:**
- Be valid Mermaid syntax
- Include comments explaining components
- Render correctly in GitHub/VS Code

### 4. Configuration Companion Projects (`config`)

Complete, working configuration files.

**Structure:**
```
code/
├── docker/
│   ├── Dockerfile
│   ├── nginx.conf
│   └── php.ini
├── docker-compose.yml
├── .env.example
└── README.md
```

**Must be:**
- Complete (all required config present)
- Runnable (`docker-compose up` works)
- Well-commented

### 5. Script Companion Projects (`script`)

Complete, executable scripts.

**Structure:**
```
code/
├── scripts/
│   ├── deploy.sh
│   ├── backup.sh
│   └── setup.sh
├── lib/
│   └── helpers.sh
└── README.md
```

**Must be:**
- Executable (`chmod +x`)
- Include shebang (`#!/bin/bash`)
- Handle errors properly
- Include usage documentation

### 6. Data Companion Projects (`dataset`)

Complete datasets with schema.

**Structure:**
```
code/
├── data/
│   ├── sample-data.json
│   ├── sample-data.csv
│   └── seed.sql
├── schemas/
│   └── schema.json
└── README.md
```

### 7. Template Companion Projects (`template`)

Reusable file templates.

**Structure:**
```
code/
├── templates/
│   ├── component.tsx.template
│   ├── controller.php.template
│   └── model.php.template
├── generated/          # Example outputs
│   └── UserController.php
└── README.md
```

### 8. Spreadsheet Companion Projects (`spreadsheet`)

Complete spreadsheets with formulas.

**Structure:**
```
code/
├── spreadsheets/
│   ├── budget-tracker.xlsx
│   └── project-timeline.xlsx
├── csv/
│   └── raw-data.csv
└── README.md
```

## Creation Workflow

### Step 1: Determine Companion Project Type

Based on article content:

| Article Topic | Companion Project Type | What to Create |
|---------------|--------------|----------------|
| Laravel feature | `code` | Full Laravel app |
| API design | `code` | Full API server |
| Architecture | `diagram` | Mermaid diagrams |
| Project management | `document` | Complete templates |
| DevOps | `config` | Docker setup |
| Automation | `script` | Executable scripts |
| Data analysis | `dataset` + `code` | Data + analysis code |

### Step 2: Create Base Project

For code companion projects, ALWAYS start with proper project scaffolding:

```bash
# Laravel
composer create-project laravel/laravel code

# Node.js
mkdir code && cd code && npm init -y

# Python
mkdir code && cd code && python -m venv venv

# React
npx create-react-app code

# Vue
npm create vue@latest code
```

### Step 3: Add Article-Specific Code

After base project exists:
1. Add models/classes
2. Add controllers/routes
3. Add views/templates
4. Add tests
5. Add seeders/sample data

### Step 4: Verify Completeness

**Code Companion Projects Checklist:**
- [ ] Can be cloned fresh
- [ ] `composer install` / `npm install` works
- [ ] Application starts without errors
- [ ] Can be accessed in browser (if web app)
- [ ] All tests pass
- [ ] README explains setup and usage

**Document Companion Projects Checklist:**
- [ ] All sections are complete
- [ ] Placeholders are clearly marked
- [ ] At least one filled example exists
- [ ] README explains how to use

### Step 5: Document the Companion Project

Every companion project needs a README.md with:
1. What it demonstrates
2. Requirements
3. Installation steps
4. How to run
5. How to test
6. Key files explained
7. Article reference

## Integration with Article

### Referencing Companion Project in Article

```markdown
## Setting Up the Project

Clone the example and install dependencies:

\`\`\`bash
cd code
composer install
cp .env.example .env
php artisan key:generate
\`\`\`

See the complete working companion project in the `code/` folder.
```

### Code Snippets from Companion Project

When showing code in the article, reference actual files:

```markdown
Here's our Post model (`code/app/Models/Post.php`):

\`\`\`php
// From: code/app/Models/Post.php
<?php

namespace App\Models;

class Post extends Model
{
    // ... actual code from example
}
\`\`\`
```

## Settings Integration

**ALWAYS load settings.json before creating companion projects.**

### Step 1: Load Settings

```bash
# View settings for your example type
bun run "${CLAUDE_PLUGIN_ROOT}"/scripts/show.ts settings code
```

**Or read directly:**
```javascript
const settings = JSON.parse(fs.readFileSync('.article_writer/settings.json'));
const defaults = settings.companion_project_defaults.code;
```

### Step 2: Get Values from Settings

```json
// .article_writer/settings.json → companion_project_defaults.code
{
  "technologies": ["Laravel 12", "Pest 4", "SQLite"],
  "scaffold_command": "composer create-project laravel/laravel code --prefer-dist",
  "post_scaffold": [
    "cd code",
    "composer require pestphp/pest pestphp/pest-plugin-laravel --dev --with-all-dependencies",
    "php artisan pest:install",
    "sed -i 's/DB_CONNECTION=.*/DB_CONNECTION=sqlite/' .env",
    "touch database/database.sqlite"
  ],
  "run_command": "php artisan serve",
  "test_command": "php artisan test"
}
```

### Step 3: Merge with Article Overrides

If the article task has a `companion_project` field, those values override settings:

```
settings.json defaults    +    article.companion_project    =    final config
──────────────────────         ────────────────        ────────────
scaffold_command: X            scaffold_command: Y      Y (article wins)
technologies: [A, B]           (not set)                [A, B] (use default)
has_tests: true                has_tests: false         false (article wins)
```

### Step 4: Execute Commands

```bash
# 1. Run scaffold_command
composer create-project laravel/laravel code --prefer-dist

# 2. Run each post_scaffold command
cd code
composer require pestphp/pest pestphp/pest-plugin-laravel --dev --with-all-dependencies
php artisan pest:install
# ... etc
```

### Step 5: Verify with test_command

```bash
# From settings.companion_project_defaults.code.test_command
php artisan test
```

---

Global defaults from `settings.json`:

```json
{
  "companion_project_defaults": {
    "code": {
      "technologies": ["Laravel 12", "Pest 4", "SQLite"],
      "scaffold_command": "composer create-project laravel/laravel code",
      "post_scaffold": [
        "cd code",
        "composer require pestphp/pest --dev",
        "php artisan pest:install"
      ]
    }
  }
}
```

Article can override:
```json
{
  "companion_project": {
    "type": "code",
    "technologies": ["Laravel 11", "PHPUnit", "MySQL"],
    "scaffold_command": "composer create-project laravel/laravel:^11.0 code"
  }
}
```

## Common Mistakes to Avoid

### ❌ Wrong: Partial Code

```
code/
├── app/Models/Post.php      # Just one file!
└── README.md
```

### ✅ Correct: Complete Project

```
code/
├── app/                     # Full Laravel structure
├── bootstrap/
├── config/
├── database/
├── public/
├── resources/
├── routes/
├── storage/
├── tests/
├── .env.example
├── artisan
├── composer.json
└── README.md
```

### ❌ Wrong: Untested Code

```php
// Example that might not work
class PostController {
    public function index() {
        return Post::all(); // Is Post even defined?
    }
}
```

### ✅ Correct: Tested, Working Code

```php
// Tested with: php artisan test
class PostController extends Controller
{
    public function index()
    {
        return Post::with('comments')->paginate(10);
    }
}

// tests/Feature/PostTest.php exists and passes
```

## Companion Project Task Recording

After creating companion project, update article_tasks.json:

```json
{
  "companion_project": {
    "type": "code",
    "path": "code/",
    "description": "Complete Laravel app with rate limiting",
    "technologies": ["Laravel 12", "Pest 4", "SQLite"],
    "has_tests": true,
    "scaffold_command": "composer create-project laravel/laravel code",
    "files": [
      "app/Http/Controllers/ApiController.php",
      "app/Http/Middleware/RateLimitMiddleware.php",
      "routes/api.php",
      "tests/Feature/RateLimitTest.php"
    ],
    "run_instructions": "composer install && php artisan serve",
    "test_command": "php artisan test",
    "verified": true,
    "verified_at": "2025-01-15T14:00:00Z"
  }
}
```
