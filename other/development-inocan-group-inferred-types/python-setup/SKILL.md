---
name: python-setup
description: Python environment setup on your computer for Badger 2350 development. Use when installing Python, setting up virtual environments, installing development tools like mpremote or ampy, or configuring the computer-side development environment for Badger 2350 projects.
---

# Python Development Environment Setup

Complete guide to setting up Python on your computer for Universe 2025 (Tufty) Badge development, including virtual environments and all necessary tools.

## Quick Start (First Time Setup)

If you're brand new and just want to get started quickly:

```bash
# 1. Check if Python is installed
python3 --version
# If not installed, see "Install Python" section below

# 2. Create project directory
mkdir ~/badge-projects
cd ~/badge-projects

# 3. Create virtual environment
python3 -m venv venv

# 4. Activate it
source venv/bin/activate  # macOS/Linux
# venv\Scripts\Activate.ps1 # Windows

# 5. Install badge tools
pip install mpremote

# 6. Test badge connection
mpremote exec "print('Badge connected!')"
# Should print: Badge connected!

# ✓ You're ready! Continue to badger-quickstart skill
```

If any command fails, continue with the detailed instructions below.

## Prerequisites Check

Before starting detailed setup, check what you already have:

```bash
# Check Python version
python3 --version

# Check pip
pip3 --version

# Check if tools are installed
which mpremote
which ampy
which rshell
```

## Install Python

### macOS

**Option 1: Using Homebrew (Recommended)**

```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python3

# Verify installation
python3 --version
pip3 --version
```

**Option 2: Using python.org installer**

1. Download from https://www.python.org/downloads/
2. Run installer
3. Check "Add Python to PATH"
4. Complete installation

### Linux (Ubuntu/Debian)

```bash
# Update package list
sudo apt update

# Install Python 3 and pip
sudo apt install python3 python3-pip python3-venv

# Verify installation
python3 --version
pip3 --version
```

### Linux (Fedora/RHEL)

```bash
# Install Python 3
sudo dnf install python3 python3-pip

# Verify installation
python3 --version
pip3 --version
```

### Windows

**Option 1: Using winget (Windows 10/11)**

```powershell
# Install Python
winget install Python.Python.3.11

# Restart terminal, then verify
python --version
pip --version
```

**Option 2: Using python.org installer**

1. Download from https://www.python.org/downloads/
2. Run installer
3. **IMPORTANT**: Check "Add Python to PATH"
4. Check "Install pip"
5. Complete installation
6. Restart terminal

**Option 3: Using Microsoft Store**

1. Open Microsoft Store
2. Search for "Python 3.11"
3. Install
4. Verify in terminal

## Create Project Directory

Set up a dedicated directory for Badger 2350 projects:

```bash
# Create project directory
mkdir -p ~/badger-projects
cd ~/badger-projects

# Create your first project
mkdir my-badge-app
cd my-badge-app
```

## Set Up Virtual Environment

Virtual environments isolate project dependencies and prevent conflicts.

### Create Virtual Environment

```bash
# Create venv in project directory
python3 -m venv venv

# Alternative name
python3 -m venv .venv
```

### Activate Virtual Environment

**macOS/Linux:**

```bash
# Activate
source venv/bin/activate

# Your prompt should change to show (venv)
(venv) user@computer:~/badger-projects/my-badge-app$

# Deactivate when done
deactivate
```

**Windows (PowerShell):**

```powershell
# Enable script execution (first time only)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Activate
venv\Scripts\Activate.ps1

# Deactivate when done
deactivate
```

**Windows (Command Prompt):**

```cmd
# Activate
venv\Scripts\activate.bat

# Deactivate when done
deactivate
```

### Verify Virtual Environment

```bash
# Should show venv Python, not system Python
which python3  # macOS/Linux
where python   # Windows

# Should be venv location like:
# ~/badger-projects/my-badge-app/venv/bin/python3
```

## Install Badger Development Tools

With virtual environment activated:

### Core Tools

```bash
# Install mpremote (recommended primary tool)
pip install mpremote

# Install ampy (alternative file management)
pip install adafruit-ampy

# Install rshell (interactive shell)
pip install rshell

# Install esptool (firmware flashing)
pip install esptool

# Verify installations
mpremote --version
ampy --version
rshell --version
esptool.py version
```

### Optional Development Tools

```bash
# Thonny IDE (beginner-friendly)
pip install thonny

# Code quality tools
pip install black      # Code formatter
pip install pylint     # Linter
pip install mypy       # Type checker

# Testing tools
pip install pytest     # Testing framework
pip install pytest-cov # Coverage reporting

# Documentation tools
pip install mkdocs     # Documentation generator
pip install sphinx     # Alternative documentation
```

### Save Dependencies

Create `requirements.txt` to track dependencies:

```bash
# Generate requirements.txt
pip freeze > requirements.txt
```

**Example requirements.txt:**

```
mpremote==1.20.0
adafruit-ampy==1.1.0
rshell==0.0.32
esptool==4.6.2
black==23.12.1
pylint==3.0.3
pytest==7.4.3
```

### Install from requirements.txt

```bash
# Install all dependencies at once
pip install -r requirements.txt

# Or upgrade existing
pip install -r requirements.txt --upgrade
```

## Configure Tools

### mpremote Configuration

Create alias for easier use:

**macOS/Linux (.bashrc or .zshrc):**

```bash
# Add to ~/.bashrc or ~/.zshrc
alias badge='mpremote connect /dev/tty.usbmodem*'

# Reload shell
source ~/.bashrc  # or source ~/.zshrc

# Usage
badge ls
badge cp main.py :main.py
```

**Windows (PowerShell profile):**

```powershell
# Open profile
notepad $PROFILE

# Add alias
function badge { mpremote connect COM3 @args }

# Reload
. $PROFILE

# Usage
badge ls
```

### ampy Configuration

Set default port to avoid typing it each time:

**macOS/Linux:**

```bash
# Add to ~/.bashrc or ~/.zshrc
export AMPY_PORT=/dev/tty.usbmodem*

# Reload
source ~/.bashrc
```

**Windows:**

```powershell
# Add to PowerShell profile
$env:AMPY_PORT = "COM3"

# Or set permanently
[Environment]::SetEnvironmentVariable("AMPY_PORT", "COM3", "User")
```

## Verify Complete Setup

Run this verification script:

```bash
# verify_setup.sh (macOS/Linux)
#!/bin/bash

echo "Verifying Badger 2350 Development Setup"
echo "========================================"

# Check Python
if command -v python3 &> /dev/null; then
    echo "✓ Python: $(python3 --version)"
else
    echo "✗ Python not found"
    exit 1
fi

# Check pip
if command -v pip3 &> /dev/null; then
    echo "✓ pip: $(pip3 --version)"
else
    echo "✗ pip not found"
    exit 1
fi

# Check virtual environment
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "✓ Virtual environment: active"
else
    echo "⚠ Virtual environment: not active"
fi

# Check tools
tools=(mpremote ampy rshell esptool.py)
for tool in "${tools[@]}"; do
    if command -v $tool &> /dev/null; then
        echo "✓ $tool: installed"
    else
        echo "✗ $tool: not installed"
    fi
done

echo "========================================"
echo "Setup verification complete!"
```

Make executable and run:

```bash
chmod +x verify_setup.sh
./verify_setup.sh
```

**Windows PowerShell version:**

```powershell
# verify_setup.ps1
Write-Host "Verifying Badger 2350 Development Setup"
Write-Host "========================================"

# Check Python
if (Get-Command python -ErrorAction SilentlyContinue) {
    $version = python --version
    Write-Host "✓ Python: $version"
} else {
    Write-Host "✗ Python not found"
    exit 1
}

# Check pip
if (Get-Command pip -ErrorAction SilentlyContinue) {
    Write-Host "✓ pip: installed"
} else {
    Write-Host "✗ pip not found"
    exit 1
}

# Check virtual environment
if ($env:VIRTUAL_ENV) {
    Write-Host "✓ Virtual environment: active"
} else {
    Write-Host "⚠ Virtual environment: not active"
}

# Check tools
$tools = @("mpremote", "ampy", "rshell", "esptool.py")
foreach ($tool in $tools) {
    if (Get-Command $tool -ErrorAction SilentlyContinue) {
        Write-Host "✓ $tool: installed"
    } else {
        Write-Host "✗ $tool: not installed"
    }
}

Write-Host "========================================"
Write-Host "Setup verification complete!"
```

## Test Badge Connection

Once tools are installed, test connection to badge:

```bash
# List serial ports (macOS/Linux)
ls /dev/tty.usb*

# List serial ports (Windows PowerShell)
[System.IO.Ports.SerialPort]::getportnames()

# Test connection with mpremote
mpremote connect /dev/tty.usbmodem* exec "print('Hello from Badger!')"

# Or on Windows
mpremote connect COM3 exec "print('Hello from Badger!')"

# If successful, you should see: Hello from Badger!
```

## Project Template

Create a standard project structure:

```bash
# Create structure
mkdir -p my-badge-app/{lib,assets,data,tests}
cd my-badge-app

# Create files
touch main.py config.py README.md requirements.txt
touch lib/__init__.py
touch tests/test_main.py

# Create .gitignore
cat > .gitignore <<EOF
# Virtual environment
venv/
.venv/
env/

# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Local config
config.local.py
.env
EOF

# Initialize git
git init
```

**Project structure:**

```
my-badge-app/
├── venv/                # Virtual environment (gitignored)
├── main.py              # Main application
├── config.py            # Configuration
├── requirements.txt     # Python dependencies
├── README.md
├── .gitignore
├── lib/                 # Reusable modules
│   └── __init__.py
├── assets/              # Images, fonts, etc.
├── data/                # Runtime data
└── tests/               # Test files
    └── test_main.py
```

## IDE Setup

### VS Code (Recommended)

```bash
# Install VS Code
# macOS
brew install --cask visual-studio-code

# Linux
sudo snap install code --classic

# Windows
winget install Microsoft.VisualStudioCode
```

**Recommended Extensions:**

1. Python (Microsoft)
2. Pylance
3. Python Debugger
4. MicroPython (for syntax)
5. GitLens

**VS Code Settings (.vscode/settings.json):**

```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/venv/bin/python",
  "python.formatting.provider": "black",
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,
  "editor.formatOnSave": true,
  "files.exclude": {
    "**/__pycache__": true,
    "**/*.pyc": true
  }
}
```

### PyCharm

1. Download from https://www.jetbrains.com/pycharm/
2. Open project directory
3. Configure interpreter: Settings → Project → Python Interpreter
4. Select existing venv or create new one

### Thonny (Beginner-Friendly)

```bash
# Install Thonny
pip install thonny

# Or download from https://thonny.org

# Run
thonny
```

**Configure Thonny for Badger:**

1. Tools → Options → Interpreter
2. Select "MicroPython (RP2040)"
3. Select correct port
4. Click OK

## Workflow Scripts

### Activate Script

Create `activate.sh` in project root:

```bash
#!/bin/bash
# activate.sh - Quick project activation

# Activate virtual environment
source venv/bin/activate

# Set badge port
export BADGE_PORT="/dev/tty.usbmodem*"

# Show status
echo "Badge development environment activated!"
echo "Python: $(which python3)"
echo "Badge port: $BADGE_PORT"

# Quick commands
alias badge='mpremote connect $BADGE_PORT'
alias deploy='./deploy.sh'

echo "Ready to develop!"
```

Usage:

```bash
source activate.sh
# Now you're ready to work!
```

### Quick Deploy Script

Create `deploy.sh`:

```bash
#!/bin/bash
# deploy.sh - Quick deploy to badge

if [ -z "$BADGE_PORT" ]; then
    BADGE_PORT="/dev/tty.usbmodem*"
fi

echo "Deploying to badge..."
mpremote connect $BADGE_PORT cp main.py :main.py
mpremote connect $BADGE_PORT cp config.py :config.py
echo "Deployment complete!"
```

Make executable:

```bash
chmod +x deploy.sh activate.sh
```

## Common Setup Issues

### "command not found: python"

**macOS/Linux:**
```bash
# Use python3 instead of python
python3 --version  # This should work

# If python3 also not found, install Python (see Install Python section above)

# Optional: Create alias for convenience
alias python=python3
alias pip=pip3
# Add to ~/.bashrc or ~/.zshrc to make permanent
```

**Windows:**
```powershell
# Use python instead of python3
python --version

# If not found, reinstall Python with "Add to PATH" checked
```

**Important**: On macOS/Linux, always use `python3` and `pip3` (not `python` and `pip`).

### Python not in PATH

**macOS/Linux:**
```bash
# Add to PATH in ~/.bashrc or ~/.zshrc
export PATH="/usr/local/bin:$PATH"
export PATH="/opt/homebrew/bin:$PATH"  # For M1/M2 Macs

# Reload shell
source ~/.bashrc  # or source ~/.zshrc
```

**Windows:**
- Reinstall Python with "Add to PATH" checked
- Or manually add to PATH:
  - System Properties → Environment Variables
  - Add `C:\Python311` and `C:\Python311\Scripts`

### pip install fails with permissions error

```bash
# Don't use sudo! Use virtual environment instead
python3 -m venv venv
source venv/bin/activate
pip install mpremote
```

### Virtual environment activation fails (Windows)

```powershell
# Enable scripts (run as Administrator)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then activate normally
venv\Scripts\Activate.ps1
```

### Badge not detected

**macOS:**
```bash
# Check if driver needed (usually automatic)
ls /dev/tty.usb*

# Grant permissions
sudo chmod 666 /dev/tty.usbmodem*
```

**Linux:**
```bash
# Add user to dialout group
sudo usermod -a -G dialout $USER

# Logout and login for changes to take effect

# Or use sudo temporarily
sudo mpremote connect /dev/ttyACM0
```

**Windows:**
- Install USB driver if needed
- Check Device Manager for COM port
- Try different USB ports

### mpremote connection fails

```bash
# Try explicit port
mpremote connect /dev/tty.usbmodem14201

# List available ports
mpremote connect list

# Auto-detect port (usually works)
mpremote exec "print('Hello')"

# Check if badge is in bootloader mode
# (Hold BOOTSEL button while connecting)
```

### "can't open file" or "No such file" errors

If you see errors like `can't open file 'test_connection.py'`:

```bash
# This means the script doesn't exist yet

# Option 1: Use basic verification instead
mpremote exec "print('Badge connected!')"

# Option 2: Create the missing script (see badger-diagnostics skill)

# Option 3: Use direct mpremote commands instead of scripts
mpremote run my_app/__init__.py  # Instead of make commands
```

**Common missing files on first setup**:
- `test_connection.py` - Use `mpremote exec` for basic testing instead
- `deploy.sh` - Use direct `mpremote cp` commands instead
- Apps/examples - Create them as you go

**Don't let missing scripts block you** - use the direct mpremote commands shown in CLAUDE.md and skills.

## Update Tools

Keep tools updated:

```bash
# Activate virtual environment first
source venv/bin/activate

# Update pip itself
pip install --upgrade pip

# Update all packages
pip install --upgrade mpremote ampy rshell esptool

# Or update from requirements.txt
pip install -r requirements.txt --upgrade
```

## ⚠️ Verify Your Setup

**CRITICAL**: Always verify your setup is working correctly before starting development.

### Complete Verification Checklist

Run through this checklist every time you start a new session:

```bash
# 1. Verify Python installation
python3 --version
# Should show: Python 3.8.0 or higher

# 2. Verify virtual environment is activated
which python3
# Should show path to venv/bin/python3 (not system Python)

# 3. Verify tools are installed
mpremote --version
ampy --version
# Both should show version numbers

# 4. Verify badge is connected
ls /dev/tty.usb*        # macOS/Linux
# OR
# [System.IO.Ports.SerialPort]::getportnames()  # Windows

# 5. Test badge connection
mpremote connect /dev/tty.usbmodem* exec "print('Hello from Badge!')"
# Should print: Hello from Badge!

# 6. Verify badgeware module
mpremote connect /dev/tty.usbmodem* exec "import badgeware; print('badgeware OK')"
# Should print: badgeware OK
```

### Automated Verification Script

Create `verify_setup.sh` in your project:

```bash
#!/bin/bash
# verify_setup.sh - Complete environment verification

echo "=========================================="
echo "Badger 2350 Environment Verification"
echo "=========================================="

errors=0

# Check Python
if command -v python3 &> /dev/null; then
    version=$(python3 --version)
    echo "✓ Python: $version"
else
    echo "✗ Python not found"
    ((errors++))
fi

# Check virtual environment
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "✓ Virtual environment: active ($VIRTUAL_ENV)"
else
    echo "⚠ Virtual environment: not active"
    echo "  Run: source venv/bin/activate"
    ((errors++))
fi

# Check mpremote
if command -v mpremote &> /dev/null; then
    echo "✓ mpremote: installed"
else
    echo "✗ mpremote: not installed"
    echo "  Run: pip install mpremote"
    ((errors++))
fi

# Check badge connection
if mpremote connect list 2>&1 | grep -q "usb"; then
    echo "✓ Badge: detected"

    # Test REPL
    if mpremote exec "print('OK')" 2>&1 | grep -q "OK"; then
        echo "✓ Badge REPL: working"
    else
        echo "✗ Badge REPL: not responding"
        ((errors++))
    fi

    # Test badgeware module
    if mpremote exec "import badgeware" 2>&1; then
        echo "✓ badgeware module: available"
    else
        echo "✗ badgeware module: not found"
        ((errors++))
    fi
else
    echo "✗ Badge: not detected"
    echo "  Check USB connection"
    ((errors++))
fi

echo "=========================================="
if [ $errors -eq 0 ]; then
    echo "✓ ALL CHECKS PASSED - Ready for development!"
    exit 0
else
    echo "✗ $errors ERROR(S) FOUND - Fix issues before proceeding"
    exit 1
fi
```

Make executable: `chmod +x verify_setup.sh`

**Run this script before every development session**: `./verify_setup.sh`

### What to Do If Verification Fails

| Issue | Solution |
|-------|----------|
| Python not found | Reinstall Python, check PATH |
| venv not active | Run `source venv/bin/activate` |
| Tools not installed | Run `pip install -r requirements.txt` |
| Badge not detected | Check USB cable, try different port |
| REPL not responding | Restart badge, check for other programs using port |
| badgeware missing | Badge firmware may need reflashing |

**Never skip verification** - It catches 90% of issues before they become problems.

## Best Practices

1. **Always verify setup first** - Run verification script at start of session
2. **Always use virtual environments** - Isolate project dependencies
3. **Keep requirements.txt updated** - `pip freeze > requirements.txt`
4. **Use version control (git)** - Track changes
5. **Document your setup** - Update README.md
6. **Test on clean environment** - Verify requirements.txt is complete
7. **Don't commit venv/** - Add to .gitignore
8. **Pin versions** - Avoid "works on my machine" issues

## Next Steps

After setup is complete:

1. ✓ Python installed
2. ✓ Virtual environment created
3. ✓ Tools installed (mpremote, ampy, etc.)
4. ✓ Badge connected and detected
5. ✓ Project structure created

Now you're ready to:
- Flash firmware to badge (see `badger-2350-dev` skill)
- Create your first app (see `badger-app-creator` skill)
- Connect sensors (see `badger-hardware` skill)

Your development environment is ready! 🎉
