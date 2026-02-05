---
name: emacs-buffer
description: Use when manipulating Emacs buffers - provides elisp patterns for listing, switching, creating, killing, and working with buffer contents
---

# Emacs Buffer Skill

## Display Guidelines

**E-ink Monitor Compatibility**: User uses an e-ink monitor that only supports black, white, and grey.
- NEVER use colors (`:foreground "red"`, `:foreground "cyan"`, etc.)
- Use `:weight bold`, `:weight light`, `:slant italic`, `:underline t` for differentiation
- Standard Emacs faces (font-lock-*-face) are acceptable as they adapt to themes

## Buffer Basics

### Get current buffer
```elisp
(current-buffer)      ; returns buffer object
(buffer-name)         ; returns buffer name string
(buffer-file-name)    ; returns file path or nil
```

### Switch to buffer
```elisp
(switch-to-buffer "buffer-name")
(set-buffer "buffer-name")  ; doesn't change window display
(pop-to-buffer "buffer-name")  ; shows in new window
```

### Create buffer
```elisp
(get-buffer-create "*my-buffer*")
(with-current-buffer (get-buffer-create "*my-buffer*")
  ;; work in buffer
  )
```

### Kill buffer
```elisp
(kill-buffer "buffer-name")
(kill-buffer (current-buffer))
```

## Buffer Contents

### Read buffer text
```elisp
(buffer-string)  ; entire buffer
(buffer-substring start end)  ; region
(buffer-substring-no-properties start end)  ; without text properties
```

### Insert text
```elisp
(insert "text")
(insert-buffer-substring other-buffer start end)
```

### Erase buffer
```elisp
(erase-buffer)
(delete-region start end)
```

## Buffer Properties

### Check buffer state
```elisp
(buffer-modified-p)  ; unsaved changes?
(buffer-live-p buf)  ; buffer exists?
(get-buffer "name")  ; returns buffer or nil
```

### Set buffer properties
```elisp
(set-buffer-modified-p nil)  ; mark as saved
(rename-buffer "new-name")
```

## Buffer Lists

### List all buffers
```elisp
(buffer-list)  ; all buffers
(mapcar #'buffer-name (buffer-list))  ; just names
```

### Filter buffers
```elisp
;; Get file-visiting buffers
(seq-filter #'buffer-file-name (buffer-list))

;; Get buffers matching pattern
(seq-filter (lambda (b)
              (string-match-p "\\*claude" (buffer-name b)))
            (buffer-list))
```

## Working with Buffer Positions

### Point operations
```elisp
(point)          ; current position
(point-min)      ; buffer start
(point-max)      ; buffer end
(goto-char pos)  ; move to position
```

### Save and restore position
```elisp
(save-excursion
  ;; point and buffer restored after body
  (goto-char (point-min))
  (search-forward "text"))
```

## Temporary Buffers

### with-temp-buffer
```elisp
(with-temp-buffer
  (insert "temporary content")
  (buffer-string))  ; returns content, buffer killed after
```

### Generate new buffer
```elisp
(generate-new-buffer "*unique-name*")
```

## Buffer-Local Variables

### Set buffer-local
```elisp
(setq-local my-var "value")
(make-local-variable 'my-var)
```

### Check if buffer-local
```elisp
(local-variable-p 'my-var)
(buffer-local-value 'my-var some-buffer)
```

## Common Patterns

### Process buffer safely
```elisp
(when-let ((buf (get-buffer "*my-buffer*")))
  (with-current-buffer buf
    ;; work with buffer
    ))
```

### Create output buffer
```elisp
(let ((buf (get-buffer-create "*output*")))
  (with-current-buffer buf
    (erase-buffer)
    (insert "Output:\n")
    (insert result))
  (display-buffer buf))
```

### Find buffer by mode
```elisp
(seq-find (lambda (b)
            (with-current-buffer b
              (derived-mode-p 'org-mode)))
          (buffer-list))
```
