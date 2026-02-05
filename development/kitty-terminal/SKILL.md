---
name: kitty-terminal
description: Configure and control kitty terminal emulator using kitten commands, kitty.conf settings, remote control, and session automation. Use when working with kitty terminal, kittens, kitty.conf, terminal automation, or debugging kitty sessions.
---

# Kitty Terminal Usage and Commands

kitty - The fast, feature rich terminal emulator

## About

The kitty terminal is run as GUI and controlled through a config file at `~/.config/kitty/kitty.conf`. This config file can include additional files (often in the same directory for ease, but absolute paths are supported). The config file is a custom, but simple format, and most functionality is exposed via mappings to kitty 'actions' or from the cli via the `kitty` cli and self contained actions known as `kittens`.

For example `kitten @ ls` will list all current os-windows, tabs and windows, with their foreground processes, ids etc. In fact all kitty behaviour can be controlled programmatically from `kitten` commands. See manpages and debugging below for more details.

Kitty's windowing model follows the hierarchy of 'os-window' > 'tabs' > 'windows', where the user may be running multiple 'os-windows' which maps to actual GUI instances managed by the operating system, and then each 'os-window' contains one or more tabs, which in turn has one or more 'windows' (which appear as 'splits' in the ui, allowing for side-by-side views within the same tab).

IMPORTANT: The 'os-windows' are managed by the operating system and so it is not possible (on macos) to programmatically move focus between os-windows, this means in practice the user will always have a single 'os-window' (though more may be spawned to create test instances or quick temporary views like viewing a config file).

## Manpages

Kitty has local `man` pages and these can be searched faster by focusing the manpath:

```sh
man -M "/Applications/kitty.app/Contents/Resources/man" kitty
```

This can be combined with `-k` for 'apropos' search:

```sh
man -k -M "/Applications/kitty.app/Contents/Resources/man" kitty
# =>
# kitten(1)                - Fast, statically compiled implementations of various kittens (command line tools for use with kitty)
# kitten-@(1)              - Control kitty remotely
# kitten-@-run(1)          - Run a program on the computer in which kitty is running and get the output
#    ...

man -k -M "/Applications/kitty.app/Contents/Resources/man" remote
# =>
# kitten-@(1)              - Control kitty remotely
# kitten-remote-file(1)    - kitten Documentation
```

### Manpage list

The full list of pages is as follows:

`$ man -k -M "/Applications/kitty.app/Contents/Resources/man" "." | sort`:

!`man -k -M "/Applications/kitty.app/Contents/Resources/man" "." | sort`

## Key Commands and Remote Control

### Essential kitten @ commands:

- `kitten @ ls` - List all os-windows, tabs, windows with IDs, processes, user variables
- `kitten @ launch --type=tab --cwd=/path` - Create new tab in specific directory
- `kitten @ launch --type=window --cwd=/path` - Create new window (split)
- `kitten @ set-user-vars VAR=value` - Set user variables on windows
- `kitten @ close-window --match all` - Close windows
- `kitten @ focus-tab --match id:123` - Focus specific tab by ID
- `kitten @ set-tab-title "title"` - Set tab title

### Remote control with sockets:

```bash
# Target specific kitty instance
kitten @ --to unix:/path/to/socket command

# Find existing sockets
ls /tmp/mykitty-* 2>/dev/null
```

### Matching windows and tabs

Most kittens and kitty actions support a `--match` flag (and sometimes a `--match-tab` flag) which is documented as:

The window to match. Match specifications are of the form: `field:query`. Where field can be one of: id, title, pid, cwd, cmdline, num, env, var, state, neighbor, and recent. query is the expression to match. Expressions can be either a number or a regular expression, and can be combined using Boolean operators.

The special value all matches all windows.

For numeric fields: id, pid, num and recent, the expression is interpreted as a number, not a regular expression. Negative values for id match from the highest id number down, in particular, -1 is the most recently created window.

The field num refers to the window position in the current tab, starting from zero and counting clockwise (this is the same as the order in which the windows are reported by the kitten @ ls command).

The window id of the current window is available as the `KITTY_WINDOW_ID` environment variable.

The field recent refers to recently active windows in the currently active tab, with zero being the currently active window, one being the previously active window and so on.

The field neighbor refers to a neighbor of the active window in the specified direction, which can be: left, right, top or bottom.

When using the env field to match on environment variables, you can specify only the environment variable name or a name and value, for example, env:MY_ENV_VAR=2.

Similarly, the var field matches on user variables set on the window. You can specify name or name and value as with the env field.

The field state matches on the state of the window. Supported states are: active, focused, needs_attention, parent_active, parent_focused, self, overlay_parent. Active windows are the windows that are active in their parent tab. There is only one focused window and it is the window to which keyboard events are delivered. If no window is focused, the last focused window is matched. The value self matches the window in which the remote control command is run. The value overlay_parent matches the window that is under the self window, when the self window is an overlay.

Note that you can use the `kitten @ ls` command to get a list of windows.

## Watcher System

Kitty supports Python watcher scripts that respond to observable events:

- `on_load`, `on_resize`, `on_focus_change`, `on_close`, `on_set_user_var`, `on_title_change`, `on_cmd_startstop`, `on_color_scheme_preference_change`

Enable via: `watcher script.py` in config or `--override watcher=script.py`

## Debugging

To debug session state from command line (non-TTY contexts):

#### Basic Session Inspection

```bash
# Find the kitty socket (has PID suffix)
ls -la /tmp/ | grep mykitty

# Use the socket to query kitty state
kitten @ --to unix:/tmp/mykitty-<PID> ls

# Example with dynamic socket discovery
KITTY_SOCKET=$(ls /tmp/mykitty-* 2>/dev/null | head -1)
kitten @ --to unix:$KITTY_SOCKET ls | jq '.[] | .tabs[] | .windows[] | .user_vars'
```

#### Testing with Fresh Kitty Instance

When debugging, create a separate test instance to ensure the latest config is loaded:

```bash
# 1. Create test kitty instance with test config and optionally override any specific settings
kitty --listen-on unix:/tmp/test-kitty-watcher --detach \
      --config=/path/to/test/config.conf \
      --override allow_remote_control=yes \
      --override watcher=mywatcher.py &

# 2. Wait for startup then test tab creation
sleep 2
kitten @ --to unix:/tmp/test-kitty-watcher launch --type=tab --cwd=/path/to/test

# 3. Inspect variables or other ls information
kitten @ --to unix:/tmp/test-kitty-watcher ls | \
  jq '.[] | .tabs[] | .windows[] | {id: .id, cwd: .cwd, user_vars: .user_vars}'

# 4. Manipulate the terminal with various launch commands
kitten @ --to unix:/tmp/test-kitty-watcher launch --type=tab --cwd=/tmp
kitten @ --to unix:/tmp/test-kitty-watcher launch --type=tab --cwd=/Users/username

# 5. Clean up test instance when done
kitten @ --to unix:/tmp/test-kitty-watcher close-window --match all
rm /tmp/test-kitty-watcher
```

## Data Structures and JSON Output

### kitten @ ls output structure:

```json
[
  {
    "id": 1,
    "is_focused": true,
    "tabs": [
      {
        "id": 1,
        "is_focused": true,
        "title": "bash",
        "windows": [
          {
            "id": 1,
            "is_focused": true,
            "title": "user@hostname",
            "pid": 12345,
            "cwd": "/Users/username/project",
            "user_vars": {
              "SESSION": "project"
            },
            "foreground_processes": [...]
          }
        ]
      }
    ]
  }
]
```

### Common jq queries:

```bash
# Get all user variables
kitten @ ls | jq '.[] | .tabs[] | .windows[] | .user_vars'

# Get CWD and other info
kitten @ ls | jq '.[] | .tabs[] | .windows[] | {id, cwd, user_vars}'

# Find tabs with a specific user_var
kitten @ ls | jq '.[] | .tabs[] | select(.windows[].user_vars.SESSION == "project")'
```

## Instructions

When users ask about kitty terminal, terminal configuration, automating terminal sessions, or debugging terminal issues:

1. **Provide specific commands** - Give exact kitten @ commands with proper flags
2. **Use man pages** - Reference the built-in man pages with the restricted path for quick lookups
3. **Show debugging techniques** - Use socket-based debugging when appropriate
4. **Explain windowing model** - Clarify the os-window > tab > window hierarchy when relevant
5. **Provide jq examples** - Show how to parse JSON output from `kitten @ ls`
