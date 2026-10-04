---
name: evoagentx
version: 1.0.1
description: EvoAgentX - Self-evolving AI agents framework integration
metadata: {"openclaw": {"emoji": "🧬", "category": "ai", "requires": {"bins": ["python3.12"], "pip": ["evoagentx"], "python_path": "C:\\Users\\z\\AppData\\Local\\Programs\\Python\\Python312\\python.exe"}, "homepage": "https://github.com/EvoAgentX/EvoAgentX"}}
---

# EvoAgentX Skill

Integration with EvoAgentX framework for self-evolving AI agents.

## ⚠️ Important: Python Version

**This skill uses Python 3.12** (not default Python)
- Path: `C:\Users\z\AppData\Local\Programs\Python\Python312\python.exe`

## What it does

- **Install** - Install EvoAgentX framework  
- **Status** - Check EvoAgentX installation and API keys
- **Docs** - Open documentation links
- **Run** - Run an EvoAgentX workflow

## Installation

```powershell
# Check status first
.\evoagentx.ps1 -Action status

# Install (if needed)
.\evoagentx.ps1 -Action install
```

## Usage

### Check Status

```powershell
.\evoagentx.ps1 -Action status
```

### Install

```powershell
.\evoagentx.ps1 -Action install
```

### Open Documentation

```powershell
.\evoagentx.ps1 -Action docs
```

## Requirements

- Python 3.12 (already installed)
- evoagentx package (already installed!)
- OpenAI API key (or Claude, DeepSeek, etc)

## Setup

1. Set API key:
   ```powershell
   $env:OPENAI_API_KEY = "sk-..."
   ```
2. Run: `.\evoagentx.ps1 -Action run -Goal "your goal"`

## What is EvoAgentX?

EvoAgentX is a framework for building self-evolving AI agents:
- Auto-constructs workflows from goals
- Self-evolution based on feedback
- Multi-model support (OpenAI, Claude, DeepSeek, Qwen)
- Memory (short-term + long-term)
- Human-in-the-loop

**Links:**
- Website: https://evoagentx.org
- GitHub: https://github.com/EvoAgentX/EvoAgentX

## License

MIT
