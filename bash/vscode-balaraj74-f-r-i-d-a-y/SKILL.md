---
name: vscode
description: "Control VS Code from the terminal. Open files, run commands, manage extensions, use the integrated terminal, interact with Copilot, and automate editor tasks. Use when a user asks FRIDAY to work with VS Code, edit files, or run VS Code commands."
homepage: https://code.visualstudio.com/docs/editor/command-line
metadata: {"friday":{"emoji":"💻","requires":{"bins":["code"]}}}
---

# VS Code Control Skill

Control Visual Studio Code from the command line. Open files, run commands, manage extensions, and automate editor tasks.

## Open Files and Folders

### Open a file
```bash
code /path/to/file.txt
code ~/project/src/main.py
```

### Open file at specific line
```bash
code --goto /path/to/file.txt:42
code -g /path/to/file.txt:42:10  # line 42, column 10
```

### Open folder/workspace
```bash
code /path/to/project
code .  # Current directory
```

### Open in new window
```bash
code -n /path/to/project
code --new-window /path/to/file.txt
```

### Open in existing window (reuse)
```bash
code -r /path/to/file.txt
code --reuse-window /path/to/project
```

### Open multiple files
```bash
code file1.py file2.py file3.py
```

### Compare/diff two files
```bash
code --diff file1.txt file2.txt
code -d original.py modified.py
```

## Create and Edit Files

### Create new untitled file
```bash
code --new-file
```

### Create file with content (using stdin)
```bash
echo "print('Hello World')" | code -
```

### Create file then open it
```bash
touch ~/project/newfile.py && code ~/project/newfile.py
```

### Create file with content and open
```bash
cat > /tmp/script.py << 'EOF'
#!/usr/bin/env python3
def main():
    print("Hello from Friday!")

if __name__ == "__main__":
    main()
EOF
code /tmp/script.py
```

### Quick edit with sed then open
```bash
sed -i 's/old_text/new_text/g' file.txt && code file.txt
```

## Run VS Code Commands

### Run any VS Code command
```bash
code --command "workbench.action.toggleSidebarVisibility"
code --command "editor.action.formatDocument"
code --command "workbench.action.files.save"
```

### Common commands
```bash
# File operations
code --command "workbench.action.files.save"
code --command "workbench.action.files.saveAll"
code --command "workbench.action.closeActiveEditor"
code --command "workbench.action.closeAllEditors"

# Editor actions
code --command "editor.action.formatDocument"
code --command "editor.action.commentLine"
code --command "editor.action.selectAll"

# View/UI
code --command "workbench.action.toggleSidebarVisibility"
code --command "workbench.action.togglePanel"
code --command "workbench.action.toggleZenMode"
code --command "workbench.action.toggleFullScreen"

# Search
code --command "workbench.action.findInFiles"
code --command "editor.action.startFindReplaceAction"

# Git
code --command "git.commit"
code --command "git.push"
code --command "git.pull"
code --command "git.sync"
```

## Integrated Terminal

### Open VS Code terminal
```bash
code --command "workbench.action.terminal.new"
```

### Run command in VS Code terminal
First open VS Code, then use xdotool to type in terminal:
```bash
code /path/to/project
sleep 2
# Open terminal
xdotool key ctrl+grave
sleep 0.5
# Type command
xdotool type "npm install"
xdotool key Return
```

### Run task
```bash
code --command "workbench.action.tasks.runTask"
```

## Extensions Management

### List installed extensions
```bash
code --list-extensions
```

### List with versions
```bash
code --list-extensions --show-versions
```

### Install extension
```bash
code --install-extension ms-python.python
code --install-extension esbenp.prettier-vscode
code --install-extension GitHub.copilot
```

### Install multiple extensions
```bash
code --install-extension ms-python.python \
     --install-extension ms-toolsai.jupyter \
     --install-extension GitHub.copilot
```

### Uninstall extension
```bash
code --uninstall-extension extension.id
```

### Disable all extensions (for troubleshooting)
```bash
code --disable-extensions
```

### Install extension from VSIX
```bash
code --install-extension /path/to/extension.vsix
```

## GitHub Copilot Integration

### Ensure Copilot is installed
```bash
code --list-extensions | grep -i copilot
# If not installed:
code --install-extension GitHub.copilot
code --install-extension GitHub.copilot-chat
```

### Open Copilot Chat
```bash
code --command "workbench.action.chat.open"
```

### Trigger inline suggestion
```bash
code --command "editor.action.inlineSuggest.trigger"
```

### Accept Copilot suggestion
```bash
code --command "editor.action.inlineSuggest.commit"
```

### Open Copilot panel/chat via keyboard simulation
```bash
# Open VS Code first, then:
xdotool key ctrl+shift+i  # Open Copilot Chat (may vary)
```

## Workspace and Settings

### Open settings
```bash
code --command "workbench.action.openSettings"
```

### Open settings JSON
```bash
code ~/.config/Code/User/settings.json
```

### Open keybindings
```bash
code ~/.config/Code/User/keybindings.json
```

### Export extensions list (for backup/sharing)
```bash
code --list-extensions > ~/vscode-extensions.txt
```

### Install extensions from list
```bash
cat ~/vscode-extensions.txt | xargs -L 1 code --install-extension
```

### Open workspace file
```bash
code project.code-workspace
```

## Search and Navigation

### Search in files (opens search panel)
```bash
code --command "workbench.action.findInFiles"
```

### Go to file (quick open)
```bash
code --command "workbench.action.quickOpen"
```

### Go to symbol
```bash
code --command "workbench.action.gotoSymbol"
```

### Go to line
```bash
code --command "workbench.action.gotoLine"
```

### Search with ripgrep from terminal, then open result
```bash
# Find and open first match
FILE=$(rg -l "search_term" | head -1) && code "$FILE"

# Find line number and open at that line
RESULT=$(rg -n "search_term" | head -1)
FILE=$(echo "$RESULT" | cut -d: -f1)
LINE=$(echo "$RESULT" | cut -d: -f2)
code -g "$FILE:$LINE"
```

## Debugging

### Start debugging
```bash
code --command "workbench.action.debug.start"
```

### Stop debugging
```bash
code --command "workbench.action.debug.stop"
```

### Toggle breakpoint
```bash
code --command "editor.debug.action.toggleBreakpoint"
```

### Step over/into/out
```bash
code --command "workbench.action.debug.stepOver"
code --command "workbench.action.debug.stepInto"
code --command "workbench.action.debug.stepOut"
```

## Git Integration

### Open source control view
```bash
code --command "workbench.view.scm"
```

### Stage all changes
```bash
code --command "git.stageAll"
```

### Commit
```bash
code --command "git.commit"
```

### Push/Pull/Sync
```bash
code --command "git.push"
code --command "git.pull"
code --command "git.sync"
```

### View git log
```bash
code --command "git.viewHistory"
```

## Advanced Automation

### Focus VS Code window
```bash
wmctrl -a "Visual Studio Code"
```

### Screenshot VS Code window
```bash
wmctrl -a "Visual Studio Code" && sleep 0.3 && scrot -u ~/Pictures/vscode-$(date +%Y%m%d-%H%M%S).png
```

### Type in VS Code (after focusing)
```bash
wmctrl -a "Visual Studio Code"
sleep 0.3
xdotool type "// This is a comment"
```

### Save current file via keyboard
```bash
wmctrl -a "Visual Studio Code"
xdotool key ctrl+s
```

### Open command palette
```bash
wmctrl -a "Visual Studio Code"
xdotool key ctrl+shift+p
sleep 0.3
xdotool type "Format Document"
xdotool key Return
```

### Create new file in project
```bash
PROJECT=~/myproject
mkdir -p "$PROJECT/src"
cat > "$PROJECT/src/utils.py" << 'EOF'
def helper():
    pass
EOF
code "$PROJECT/src/utils.py"
```

## Useful Workflows

### Open project and install deps
```bash
code ~/project && cd ~/project && npm install
```

### Create Python project structure
```bash
PROJECT=~/new-python-project
mkdir -p "$PROJECT"/{src,tests,docs}
touch "$PROJECT/src/__init__.py"
touch "$PROJECT/tests/__init__.py"
echo "# My Project" > "$PROJECT/README.md"
code "$PROJECT"
```

### Open project with terminal ready
```bash
code ~/project
sleep 2
code --command "workbench.action.terminal.new"
```

### Quick file from clipboard
```bash
xclip -selection clipboard -o > /tmp/from-clipboard.txt && code /tmp/from-clipboard.txt
```

## VS Code Server (Remote)

### Check if code-server is running
```bash
pgrep -f "code-server" && echo "Running" || echo "Not running"
```

### Status
```bash
code --status
```

### Version info
```bash
code --version
```

### Verbose logging (for debugging)
```bash
code --verbose --log debug
```
