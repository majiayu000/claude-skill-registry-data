---
name: badger-deploy
description: Deployment workflows, file management, and project organization for Universe 2025 (Tufty) Badge. Use when deploying apps to MonaOS, managing files on device, syncing projects, organizing code, or setting up deployment pipelines.
---

# Universe 2025 Badge Deployment and File Management

Efficient workflows for deploying applications to **MonaOS**, managing files, and organizing projects on the Universe 2025 (Tufty) Badge.

## Deploying to MonaOS

MonaOS apps are **directories** in `/system/apps/`, not single files. Each app directory must contain:
- `__init__.py` - Entry point with `update()` function
- `icon.png` - 24x24 PNG icon for the launcher
- `assets/` - Optional directory for app resources

### ⚠️ CRITICAL: USB Mass Storage Mode Required

**The `/system/apps/` directory is READ-ONLY via mpremote.** You MUST use USB Mass Storage Mode to install, update, or delete apps.

```bash
# Step 1: Enter USB Mass Storage Mode
# - Connect badge via USB-C
# - Press RESET button TWICE quickly (double-click)
# - Badge appears as "BADGER" drive at /Volumes/BADGER (macOS)

# Step 2: Copy your app to the badge
cp -r my_app /Volumes/BADGER/apps/

# Or manually via Finder:
# - Open BADGER drive
# - Navigate to apps/ folder
# - Drag my_app folder into apps/

# Step 3: Exit Mass Storage Mode
diskutil eject /Volumes/BADGER  # Or eject via Finder
# Press RESET button once to reboot into MonaOS

# Your app will now appear in the MonaOS launcher!
```

**File System Mapping**:
- `/Volumes/BADGER/apps/` → `/system/apps/` on badge (MonaOS apps)
- `/Volumes/BADGER/assets/` → `/system/assets/` on badge (system resources)
- `/Volumes/BADGER/main.py` → `/system/main.py` on badge (boot script)

**⚠️ Important**: Install the paginated menu to show unlimited apps (default shows only 6):
- Download: https://raw.githubusercontent.com/badger/home/refs/heads/main/badge/apps/menu/__init__.py
- Replace `/Volumes/BADGER/apps/menu/__init__.py` in Mass Storage Mode

## File Transfer Methods

### Using mpremote for Development (NOT for installing apps)

**⚠️ IMPORTANT**: You CANNOT use `mpremote` to install apps to `/system/apps/` because it's read-only. Use Mass Storage Mode for apps.

`mpremote` is useful for:
- **Testing**: Running code temporarily without saving
- **App Data**: Copying files to `/storage/` (writable partition)
- **Development**: Quick iteration and debugging

```bash
# Run app temporarily (doesn't save to badge)
mpremote run my_app/__init__.py

# Copy app data to writable storage
mpremote cp data.txt :/storage/data.txt

# Create directory in writable storage
mpremote mkdir :/storage/mydata

# Copy from badge to computer
mpremote cp :/storage/data.txt local_backup.txt

# List files on badge
mpremote ls              # Root directory
mpremote ls /system/apps # MonaOS apps (read-only)
mpremote ls /storage     # Writable storage

# Remove file from storage (NOT /system/)
mpremote rm :/storage/data.txt

# Remove directory from storage (NOT /system/)
mpremote rm -rf :/storage/mydata
```

**What you CANNOT do with mpremote**:
- ❌ Install apps to `/system/apps/` (read-only)
- ❌ Modify `/system/apps/menu/` (read-only)
- ❌ Edit files in `/system/` (read-only)
- ✅ Use USB Mass Storage Mode instead for these operations

### Using ampy

```bash
# Install ampy
pip install adafruit-ampy

# Set port (or use --port flag)
export AMPY_PORT=/dev/tty.usbmodem*

# Upload file
ampy put main.py
ampy put config.py /lib/config.py

# Upload directory
ampy put lib/

# Download file
ampy get main.py

# List files
ampy ls
ampy ls /lib

# Remove file
ampy rm old_file.py
```

### Using rshell

```bash
# Install rshell
pip install rshell

# Connect
rshell --port /dev/tty.usbmodem*

# Commands in rshell
/your/computer> boards               # List connected boards
/your/computer> connect serial /dev/tty.usbmodem*
/your/computer> cp main.py /pyboard/
/your/computer> cp -r lib /pyboard/
/your/computer> ls /pyboard
/your/computer> cat /pyboard/main.py
/your/computer> rm /pyboard/old.py
```

### Manual File Sync via REPL

```python
# In REPL - create/edit file directly
f = open('config.py', 'w')
f.write('''
CONFIG = {
    'wifi_ssid': 'MyNetwork',
    'wifi_password': 'password123',
    'version': '1.0.0'
}
''')
f.close()
```

## Project Organization

### MonaOS App Structure

Each MonaOS app is a **directory** with this structure:

```
my_app/                  # Your app directory
├── __init__.py          # Entry point with update() function (required)
├── icon.png             # 24x24 PNG icon for launcher (required)
├── assets/              # Optional: app resources (auto-added to path)
│   ├── sprites.png
│   ├── font.ppf
│   └── config.json
└── README.md            # Optional: app documentation
```

### Local Development Structure

Your development directory on your computer:

```
badge-project/
├── my_app/              # MonaOS app directory
│   ├── __init__.py      # App entry point
│   ├── icon.png         # 24x24 icon
│   └── assets/          # App assets
│       └── sprites.png
├── another_app/         # Another MonaOS app
│   ├── __init__.py
│   └── icon.png
├── requirements.txt     # Python dependencies for development
├── venv/                # Virtual environment
└── deploy.sh            # Deployment script
```

### Deploy Script for MonaOS Apps

**⚠️ IMPORTANT**: Since `/system/apps/` is read-only via mpremote, this script uses USB Mass Storage Mode.

Create `deploy.sh`:

```bash
#!/bin/bash
# deploy.sh - Deploy MonaOS app to badge via USB Mass Storage Mode

if [ -z "$1" ]; then
    echo "Usage: ./deploy.sh <app_name>"
    echo "Example: ./deploy.sh my_app"
    exit 1
fi

APP_NAME=$1
BADGE_MOUNT="/Volumes/BADGER"

if [ ! -d "$APP_NAME" ]; then
    echo "Error: App directory '$APP_NAME' not found"
    exit 1
fi

# Check if badge is in Mass Storage Mode
if [ ! -d "$BADGE_MOUNT" ]; then
    echo "⚠️  Badge not found in Mass Storage Mode"
    echo ""
    echo "Please enter Mass Storage Mode:"
    echo "  1. Connect badge via USB-C"
    echo "  2. Press RESET button TWICE quickly"
    echo "  3. Wait for BADGER drive to appear"
    echo "  4. Run this script again"
    exit 1
fi

echo "Deploying $APP_NAME to MonaOS..."

# Verify required files exist
if [ ! -f "$APP_NAME/__init__.py" ]; then
    echo "Error: __init__.py not found in $APP_NAME/"
    exit 1
fi

if [ ! -f "$APP_NAME/icon.png" ]; then
    echo "Warning: icon.png not found (required for launcher display)"
fi

# Remove old version if it exists
if [ -d "$BADGE_MOUNT/apps/$APP_NAME" ]; then
    echo "Removing old version..."
    rm -rf "$BADGE_MOUNT/apps/$APP_NAME"
fi

# Copy app to badge
echo "Copying app to badge..."
cp -r "$APP_NAME" "$BADGE_MOUNT/apps/"

echo "✓ Deployment complete!"
echo ""
echo "Next steps:"
echo "  1. Eject BADGER drive: diskutil eject /Volumes/BADGER"
echo "  2. Press RESET once on badge to reboot"
echo "  3. Your app will appear in MonaOS launcher"
echo ""
echo "Note: Install paginated menu for unlimited apps:"
echo "https://raw.githubusercontent.com/badger/home/refs/heads/main/badge/apps/menu/__init__.py"
```

Make executable: `chmod +x deploy.sh`

Usage:
```bash
./deploy.sh my_app
```

## Deployment Workflows

### Development Workflow

Quick iteration during development:

```bash
# 1. Edit code locally
vim my_app/__init__.py

# 2. Test app temporarily (doesn't save to badge)
mpremote run my_app/__init__.py

# 3. Deploy to MonaOS launcher (use Mass Storage Mode)
# - Press RESET twice on badge
# - Copy updated files: cp -r my_app /Volumes/BADGER/apps/
# - Eject and press RESET once

# 4. Verify deployment
mpremote ls /system/apps/my_app

# 5. Launch from badge
# Use physical buttons to navigate MonaOS menu and select your app
```

### Production Deployment

Full deployment with verification:

```bash
#!/bin/bash
# production-deploy.sh

set -e  # Exit on error

BADGE_PORT="/dev/tty.usbmodem*"

echo "Starting production deployment..."

# Backup existing files
echo "Creating backup..."
mpremote connect $BADGE_PORT cp :main.py :main.py.backup
mpremote connect $BADGE_PORT cp :config.py :config.py.backup

# Deploy new files
echo "Deploying new version..."
mpremote connect $BADGE_PORT cp main.py :main.py
mpremote connect $BADGE_PORT cp config.py :config.py
mpremote connect $BADGE_PORT cp -r lib/ :/lib/

# Verify deployment
echo "Verifying deployment..."
mpremote connect $BADGE_PORT exec "
import sys
print('MicroPython version:', sys.version)

# Import and verify main module
try:
    import main
    print('✓ main.py imports successfully')
except Exception as e:
    print('✗ Error importing main.py:', e)
    sys.exit(1)
"

# Restart with new code
echo "Restarting badge..."
mpremote connect $BADGE_PORT exec "import machine; machine.soft_reset()"

echo "Production deployment complete!"
```

### Staged Deployment

Test on one badge before deploying to multiple:

```bash
#!/bin/bash
# staged-deploy.sh

# Stage 1: Deploy to test badge
echo "Stage 1: Deploying to test badge..."
./deploy.sh --port /dev/tty.usbmodem1

# Stage 2: Run automated tests
echo "Stage 2: Running tests..."
python test_suite.py --badge /dev/tty.usbmodem1

# Stage 3: Deploy to production badges
echo "Stage 3: Deploying to all badges..."
for port in /dev/tty.usbmodem*; do
    echo "Deploying to $port..."
    ./deploy.sh --port $port
done

echo "Staged deployment complete!"
```

## File Management

### Sync Local and Badge Files

```python
# sync.py - Sync files between computer and badge
import os
import subprocess
import hashlib

def get_local_files(path='.'):
    """Get list of local .py files"""
    files = []
    for root, dirs, filenames in os.walk(path):
        # Skip test directories
        if 'test' in root:
            continue
        for filename in filenames:
            if filename.endswith('.py'):
                filepath = os.path.join(root, filename)
                files.append(filepath)
    return files

def sync_to_badge(port='/dev/tty.usbmodem*'):
    """Sync all Python files to badge"""
    files = get_local_files()

    print(f"Syncing {len(files)} files to badge...")
    for filepath in files:
        # Determine badge path
        if filepath.startswith('./lib/'):
            badge_path = f":/{filepath[2:]}"
        elif filepath.startswith('./'):
            badge_path = f":/{filepath[2:]}"
        else:
            badge_path = f":/{filepath}"

        # Upload file
        cmd = f"mpremote connect {port} cp {filepath} {badge_path}"
        print(f"  {filepath} -> {badge_path}")
        subprocess.run(cmd, shell=True, check=True)

    print("Sync complete!")

if __name__ == '__main__':
    sync_to_badge()
```

### Clean Up Badge Files

```python
# cleanup.py - Remove unused files from badge

def cleanup_badge():
    """Remove temporary and cache files from badge"""
    import os

    # Files to remove
    patterns = [
        '.pyc',      # Compiled Python
        '.backup',   # Backup files
        '.tmp',      # Temporary files
        'debug_',    # Debug files
    ]

    removed = []

    for path in ['/', '/lib']:
        try:
            files = os.listdir(path)
            for file in files:
                # Check if file matches cleanup pattern
                if any(file.endswith(p) or file.startswith(p) for p in patterns):
                    filepath = f"{path}/{file}".replace('//', '/')
                    os.remove(filepath)
                    removed.append(filepath)
        except:
            pass

    print(f"Cleanup complete! Removed {len(removed)} files:")
    for f in removed:
        print(f"  {f}")

# Run on badge via mpremote:
# mpremote exec "$(cat cleanup.py)"
```

### List Badge Files

```bash
# list_files.sh - Comprehensive file listing

echo "Files on badge:"
echo "==============="

echo -e "\nRoot directory:"
mpremote ls

echo -e "\n/lib directory:"
mpremote ls /lib 2>/dev/null || echo "  (not found)"

echo -e "\n/assets directory:"
mpremote ls /assets 2>/dev/null || echo "  (not found)"

echo -e "\n/data directory:"
mpremote ls /data 2>/dev/null || echo "  (not found)"
```

## Backup and Restore

### Backup Badge to Computer

```bash
#!/bin/bash
# backup.sh - Backup all files from badge

BACKUP_DIR="backup_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

echo "Backing up badge to $BACKUP_DIR..."

# Backup root Python files
for file in $(mpremote ls | grep '.py'); do
    echo "  Backing up $file..."
    mpremote cp ":$file" "$BACKUP_DIR/$file"
done

# Backup lib directory
mkdir -p "$BACKUP_DIR/lib"
for file in $(mpremote ls /lib 2>/dev/null | grep '.py'); do
    echo "  Backing up /lib/$file..."
    mpremote cp ":/lib/$file" "$BACKUP_DIR/lib/$file"
done

echo "Backup complete: $BACKUP_DIR"
```

### Restore Badge from Backup

```bash
#!/bin/bash
# restore.sh - Restore files to badge from backup

if [ -z "$1" ]; then
    echo "Usage: ./restore.sh <backup_directory>"
    exit 1
fi

BACKUP_DIR=$1

echo "Restoring from $BACKUP_DIR..."

# Restore root files
for file in "$BACKUP_DIR"/*.py; do
    if [ -f "$file" ]; then
        filename=$(basename "$file")
        echo "  Restoring $filename..."
        mpremote cp "$file" ":$filename"
    fi
done

# Restore lib directory
if [ -d "$BACKUP_DIR/lib" ]; then
    mpremote mkdir /lib 2>/dev/null || true
    for file in "$BACKUP_DIR/lib"/*.py; do
        if [ -f "$file" ]; then
            filename=$(basename "$file")
            echo "  Restoring /lib/$filename..."
            mpremote cp "$file" ":/lib/$filename"
        fi
    done
fi

echo "Restore complete!"
```

## Version Management

### Version File

Create `version.py` on badge:

```python
# version.py
VERSION = '1.2.3'
BUILD_DATE = '2024-01-15'
COMMIT = 'abc123f'

def show():
    print(f"Version: {VERSION}")
    print(f"Build: {BUILD_DATE}")
    print(f"Commit: {COMMIT}")
```

### Auto-generate Version

```bash
#!/bin/bash
# generate_version.sh - Auto-generate version file

VERSION=$(git describe --tags --always)
BUILD_DATE=$(date +%Y-%m-%d)
COMMIT=$(git rev-parse --short HEAD)

cat > version.py <<EOF
# Auto-generated version file
VERSION = '$VERSION'
BUILD_DATE = '$BUILD_DATE'
COMMIT = '$COMMIT'
EOF

echo "Generated version.py: $VERSION ($BUILD_DATE)"
```

Add to deploy script:

```bash
# Generate version before deploy
./generate_version.sh
mpremote cp version.py :version.py
```

## Multi-Badge Deployment

### Deploy to Multiple Badges

```bash
#!/bin/bash
# multi-deploy.sh - Deploy to multiple connected badges

echo "Scanning for connected badges..."
BADGES=$(ls /dev/tty.usbmodem* 2>/dev/null)

if [ -z "$BADGES" ]; then
    echo "No badges found!"
    exit 1
fi

echo "Found badges:"
echo "$BADGES"
echo

read -p "Deploy to all? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    exit 0
fi

for PORT in $BADGES; do
    echo "================================"
    echo "Deploying to $PORT..."
    echo "================================"

    mpremote connect $PORT cp main.py :main.py
    mpremote connect $PORT cp config.py :config.py
    mpremote connect $PORT cp -r lib/ :/lib/

    echo "✓ Deployed to $PORT"
    echo
done

echo "All badges updated!"
```

## CI/CD Integration

### GitHub Actions Example

```yaml
# .github/workflows/deploy.yml
name: Deploy to Badge

on:
  push:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install mpremote pytest

      - name: Run tests
        run: |
          pytest tests/

  deploy:
    needs: test
    runs-on: self-hosted  # Runner with badge connected
    steps:
      - uses: actions/checkout@v3

      - name: Deploy to badge
        run: |
          ./generate_version.sh
          ./deploy.sh
```

### Pre-commit Hook

```bash
# .git/hooks/pre-commit
#!/bin/bash
# Run tests before allowing commit

echo "Running tests..."
python -m pytest tests/

if [ $? -ne 0 ]; then
    echo "Tests failed! Commit aborted."
    exit 1
fi

echo "Tests passed!"
exit 0
```

Make executable: `chmod +x .git/hooks/pre-commit`

## Hot Reload Development

### Watch and Auto-deploy

```python
# watch.py - Watch for file changes and auto-deploy
import time
import os
import subprocess
from pathlib import Path

def get_file_hash(filepath):
    """Get hash of file contents"""
    import hashlib
    with open(filepath, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()

def watch_and_deploy(watch_files, port='/dev/tty.usbmodem*'):
    """Watch files and deploy on change"""
    print(f"Watching {len(watch_files)} files for changes...")

    file_hashes = {f: get_file_hash(f) for f in watch_files}

    try:
        while True:
            time.sleep(1)  # Check every second

            for filepath in watch_files:
                current_hash = get_file_hash(filepath)

                if current_hash != file_hashes[filepath]:
                    print(f"\n{filepath} changed! Deploying...")

                    # Deploy changed file
                    badge_path = f":/{filepath}"
                    cmd = f"mpremote connect {port} cp {filepath} {badge_path}"
                    subprocess.run(cmd, shell=True)

                    # Soft reset badge
                    cmd = f"mpremote connect {port} exec 'import machine; machine.soft_reset()'"
                    subprocess.run(cmd, shell=True)

                    # Update hash
                    file_hashes[filepath] = current_hash

                    print("Deploy complete!")
    except KeyboardInterrupt:
        print("\nStopped watching.")

if __name__ == '__main__':
    watch_files = ['main.py', 'config.py', 'lib/display.py']
    watch_and_deploy(watch_files)
```

## Best Practices

### Pre-deployment Checklist

- [ ] Test code locally (if possible)
- [ ] Update version number
- [ ] Run linter/formatter
- [ ] Commit changes to git
- [ ] Backup current badge code
- [ ] Deploy to test badge first
- [ ] Verify deployment success
- [ ] Test on badge
- [ ] Deploy to production badges

### File Organization Tips

1. **Keep main.py simple** - Import from modules
2. **Use /lib for reusable code** - Separate concerns
3. **Store data in /data** - Keep code and data separate
4. **Version control everything** - Except secrets
5. **Use .gitignore** - Don't commit badge-specific configs

### Deployment Optimization

```bash
# Minimize deployment time

# Deploy only changed files
git diff --name-only HEAD~1 | grep '.py$' | while read file; do
    mpremote cp "$file" ":/$file"
done

# Compress files before transfer (if network-based)
# gzip files, transfer, decompress on badge

# Parallel deployment to multiple badges
parallel -j 4 ./deploy.sh --port ::: /dev/tty.usbmodem*
```

## Troubleshooting Deployment

**Files not updating**: Verify file was actually copied, check paths with `mpremote ls /system/apps/my_app`

**Permission denied**: Badge may be in use by another process, close other connections

**Deployment fails silently**: Check disk space on badge, verify file syntax, ensure `__init__.py` and `icon.png` exist

**App doesn't appear in MonaOS menu**:
- Verify files uploaded to `/system/apps/my_app/`
- Check icon is exactly 24x24 PNG
- Default menu shows only 6 apps - enable pagination: https://badger.github.io/hack/menu-pagination/

**Changes not reflected**: Restart badge to reload app code

**Slow transfers**: USB cable quality matters, try different cable/port

## Official Examples

For inspiration on what to deploy to your badge:
- **Hacks**: https://badger.github.io/hacks/ - Step-by-step customization tutorials
- **Apps**: https://badger.github.io/apps/ - Loadable MonaOS apps (Commits, Snake)
- **Source Code**: https://github.com/badger/home/tree/main/badgerware - Browse official MonaOS app code and API docs

With these deployment workflows, you can efficiently manage and deploy applications to your Universe 2025 Badge's MonaOS launcher!
