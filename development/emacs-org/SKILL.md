---
name: emacs-org
description: Use when working with Emacs org-mode - provides elisp patterns for headings, properties, tables, links, and org-mode manipulation
---

# Emacs Org-Mode Skill

## Display Guidelines

**E-ink Monitor Compatibility**: User uses an e-ink monitor that only supports black, white, and grey.
- NEVER use colors (`:foreground "red"`, `:foreground "cyan"`, etc.)
- Use `:weight bold`, `:weight light`, `:slant italic`, `:underline t` for differentiation
- Standard Emacs faces (font-lock-*-face) are acceptable as they adapt to themes

## Org Properties

### Get property with inheritance
```elisp
(org-entry-get nil "PROPERTY_NAME" t)  ; t enables inheritance
```

### Get property without inheritance
```elisp
(org-entry-get nil "PROPERTY_NAME" nil)
```

### Set property
```elisp
(org-entry-put nil "PROPERTY_NAME" "value")
```

### Safe property access (for header-line, mode-line contexts)
```elisp
;; Wrap in ignore-errors when called from non-org-mode contexts
(ignore-errors
  (org-entry-get nil "PROPERTY_NAME" t))
```

## Headings Navigation

### Go to heading
```elisp
(org-back-to-heading t)  ; t means error if not at heading
```

### Walk up headings
```elisp
(while (org-up-heading-safe)
  ;; process each parent heading
  )
```

### Check if at heading
```elisp
(org-at-heading-p)
```

### Get current level
```elisp
(org-current-level)  ; returns integer
```

## Tags

### Get tags for current heading
```elisp
(org-get-tags nil t)  ; returns list of strings
```

### Check for specific tag
```elisp
(member "my_tag" (org-get-tags nil t))
```

## Subtree Operations

### Get subtree end
```elisp
(save-excursion
  (org-end-of-subtree t t)
  (point))
```

### Map over entries with tag
```elisp
(org-map-entries
 (lambda ()
   ;; body executed at each matching heading
   (org-entry-get nil "PROPERTY"))
 "+my_tag")
```

## File-Level Properties

### Get file keyword (#+PROPERTY: NAME value)
```elisp
(save-excursion
  (goto-char (point-min))
  (when (re-search-forward "^#\\+PROPERTY:\\s-+NAME\\s-+\\(.+\\)$" nil t)
    (match-string 1)))
```

## Tables

### Move in table
```elisp
(org-table-goto-column 2)  ; go to column 2
(org-table-next-row)       ; go to next row
```

### Get cell value
```elisp
(org-table-get-field)  ; current cell
(org-table-get-field 3)  ; column 3 of current row
```

## Links

### Parse link at point
```elisp
(org-element-context)  ; returns element with :path, :type properties
```

### Create link
```elisp
(org-link-make-string "https://example.com" "description")
```

## Common Patterns

### Safely get session info for mode-line
```elisp
(defun my-get-session-id ()
  "Get session ID safely from any context."
  (ignore-errors
    (save-excursion
      (org-entry-get nil "SESSION_ID" t))))
```

### Find heading with property value
```elisp
(save-excursion
  (goto-char (point-min))
  (catch 'found
    (while (re-search-forward "^\\*+ " nil t)
      (when (equal "target" (org-entry-get nil "MY_PROP"))
        (throw 'found (point))))
    nil))
```

### Insert property drawer
```elisp
(org-back-to-heading t)
(forward-line 1)
(insert ":PROPERTIES:\n")
(insert ":MY_PROP: value\n")
(insert ":END:\n")
```

## Error Prevention

Functions called from header-line or mode-line should wrap org-* calls:

```elisp
;; BAD - will error in non-org buffers
(defun my-header-line ()
  (org-entry-get nil "PROP" t))

;; GOOD - safe in any buffer
(defun my-header-line ()
  (ignore-errors
    (org-entry-get nil "PROP" t)))
```
