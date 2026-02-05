---
name: code-walk-thru
description: Use this when user wants you to walk through (code or text) files in a EDITOR to either explain how some code works, or to show the user what changes you made, etc. You would typically use this repeatedly to show the user your changes or code files one by one, sometimes with specific line-numbers. This way the user is easily able to follow along in their favorite EDITOR as you point at various files possibly at specific line numbers within those files. 
---

# code-walk-thru

## Instructions

Depending on which EDITOR the user says they are using, you will use a different
"show-file" cli command that shows (in the EDITOR) a specific file, optionally at 
specific line-number, as in examples below. If no editor specified, you must
ask the user which editor they are using.

IMPORTANT: you must walk thru the files ONE BY ONE, and you MUST wait for the user to say something before moving on to the next file, or to same file different line.

- VSCode:

```
code --goto <file_path>:<line_number>
```

- PyCharm:

```
pycharm --line <line_number> <file_path>
```

- IntelliJ:

```
intellij --line <line_number> <file_path>
```

- Zed:

```
zed path/to/file.md:43
```

- Vim/Neovim:

```
vim +42 blah.py
nvim +42 blah.py
```

If any of these fail tell the user to install the corresponding CLI tool for their editor.
