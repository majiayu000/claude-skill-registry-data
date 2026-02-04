---
name: sinatra-setup-for-beginners
description: Set up Ruby Sinatra development environment for beginners with step-by-step guidance, Bundler setup, and troubleshooting
license: Complete terms in LICENSE.txt
---

# Sinatra Setup for Beginners
**Version:** 0.17.0

## When to Use
- User wants Sinatra web application
- Beginner needs Sinatra environment setup
- User asks "How do I set up Sinatra?"

## Instructions for ASSISTANT
**Format ALL instructions as Claude Code copy/paste blocks.**

**DO NOT:** Manual instructions like "Open File Explorer", "Navigate to folder"
**ALWAYS:** Single code block with TASK, STEPs, and report request

## Setup Steps

### 1. Verify Ruby
```bash
ruby --version
```
**Expected:** Ruby 3.0+ | **If missing:**
- **Windows:** RubyInstaller from rubyinstaller.org
- **Mac:** `brew install ruby`
- **Linux:** `sudo apt-get install ruby-full`

### 2. Install Bundler
```bash
gem install bundler
```
**What:** Ruby's package manager
**Verify:** `bundler --version` shows 2.X.X

### 3. Create Gemfile
File: `Gemfile` (no extension, capital G) in project root
```ruby
source 'https://rubygems.org'
gem 'sinatra'
```

### 4. Install Dependencies
```bash
bundle install
```
**Wait:** 30-90 seconds
**Creates:** `Gemfile.lock`

### 5. Create app.rb
```
my-project/
├── Gemfile
├── Gemfile.lock
└── app.rb  ← Create here
```

### 6. Verify Installation
```bash
ruby --version
bundle --version
bundle list
ruby -e "require 'sinatra'; puts 'Sinatra works!'"
```

## Project Structure
```
my-project/
├── Gemfile        ← Dependencies
├── Gemfile.lock   ← Version lock
├── app.rb         ← Main code
├── views/         ← Templates (.erb)
└── public/        ← Static files
```

## Troubleshooting
| Issue | Solution |
|-------|----------|
| `gem: command not found` | Ruby not installed |
| `Could not locate Gemfile` | Wrong directory |
| Permission denied | `bundle install --path vendor/bundle` |
| Old Ruby version | Update to 3.0+ |

## Next Steps
After setup: Create first route, start server, build first page.

**Remember:** Run `bundle exec ruby app.rb` to start (ensures correct gem versions).

---

**End of Skill**
