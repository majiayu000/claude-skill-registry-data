---
name: tmux
description: Terminal multiplexer.
metadata:
  trit: 0
---

# tmux

Terminal multiplexer.

## Sessions

```bash
tmux new -s name
tmux attach -t name
tmux ls
tmux kill-session -t name
```

## Keys (prefix: C-b)

```
d       Detach
c       New window
n/p     Next/prev window
0-9     Select window
%       Split vertical
"       Split horizontal
o       Next pane
z       Toggle zoom
x       Kill pane
[       Copy mode
]       Paste
```

## Copy Mode

```
Space   Start selection
Enter   Copy selection
q       Quit
/       Search forward
?       Search backward
```

## Config

```bash
# ~/.tmux.conf
set -g prefix C-a
set -g mouse on
set -g base-index 1
```
