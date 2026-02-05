---
name: emacs-navigation
description: Use when navigating files and positions in Emacs - provides elisp patterns for finding files, searching, and position management
---

# Emacs Navigation Skill

## Display Guidelines

**E-ink Monitor Compatibility**: User uses an e-ink monitor that only supports black, white, and grey.
- NEVER use colors (`:foreground "red"`, `:foreground "cyan"`, etc.)
- Use `:weight bold`, `:weight light`, `:slant italic`, `:underline t` for differentiation
- Standard Emacs faces (font-lock-*-face) are acceptable as they adapt to themes

## File Navigation

### Open file
```elisp
(find-file "/path/to/file")
(find-file-noselect "/path/to/file")  ; open without switching
```

### Find file in project
```elisp
(project-find-file)  ; interactive
(project-root (project-current))  ; get project root
```

### Recent files
```elisp
recentf-list  ; list of recent files
(recentf-open-files)  ; interactive
```

## Position Navigation

### Line navigation
```elisp
(goto-line 42)
(forward-line n)  ; move n lines (negative goes backward)
(beginning-of-line)
(end-of-line)
```

### Character navigation
```elisp
(goto-char position)
(forward-char n)
(backward-char n)
```

### Word navigation
```elisp
(forward-word)
(backward-word)
```

## Search Navigation

### Search forward
```elisp
(search-forward "text" nil t)  ; returns nil if not found
(re-search-forward "regex" nil t)
```

### Search backward
```elisp
(search-backward "text" nil t)
(re-search-backward "regex" nil t)
```

### Search with bounds
```elisp
(re-search-forward "pattern" limit-pos t)  ; stop at limit-pos
```

## Save/Restore Positions

### save-excursion
```elisp
(save-excursion
  (goto-char (point-min))
  (search-forward "target")
  ;; point restored after body
  )
```

### save-restriction
```elisp
(save-restriction
  (narrow-to-region start end)
  ;; work with narrowed buffer
  )  ; narrowing restored
```

### Markers
```elisp
(point-marker)  ; marker at current point
(set-marker marker position)
(marker-position marker)
(goto-char marker)
```

## Window Navigation

### Switch windows
```elisp
(other-window 1)  ; next window
(select-window window)
```

### Find window
```elisp
(get-buffer-window "*buffer*")
(selected-window)
```

### Split windows
```elisp
(split-window-right)
(split-window-below)
(delete-window)
```

## Match Data

### After successful search
```elisp
(re-search-forward "\\(group1\\).*\\(group2\\)")
(match-string 1)  ; first group
(match-string 2)  ; second group
(match-beginning 0)  ; start of full match
(match-end 0)  ; end of full match
```

## Common Patterns

### Find and process all matches
```elisp
(save-excursion
  (goto-char (point-min))
  (while (re-search-forward "pattern" nil t)
    ;; process each match
    (let ((matched (match-string 0)))
      ;; do something
      )))
```

### Navigate to specific file and line
```elisp
(let ((file "/path/to/file")
      (line 42))
  (find-file file)
  (goto-char (point-min))
  (forward-line (1- line)))  ; lines are 1-indexed
```

### Narrow to function/section
```elisp
(save-restriction
  (org-narrow-to-subtree)  ; or narrow-to-defun
  ;; work within narrowed region
  (point-min)  ; now returns subtree start
  )
```

### Visit file at point
```elisp
(find-file-at-point)  ; interactive
(ffap-file-at-point)  ; get filename at point
```

## Directory Navigation

### Default directory
```elisp
default-directory  ; current directory
(cd "/new/path")
```

### List directory
```elisp
(directory-files "/path")
(directory-files "/path" t "\\.el$")  ; full paths, only .el files
```

### Walk directory tree
```elisp
(directory-files-recursively "/path" "\\.org$")
```
