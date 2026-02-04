---
name: EmacsLisp
description: Emacs Lisp development with modern tooling and best practices. USE WHEN writing Emacs configuration, developing packages, testing, linting, publishing to MELPA/ELPA, or working with Emacs Lisp code.
---

# Emacs Lisp Development

Expert guidance on Emacs Lisp programming following modern best practices (2025), from configuration and scripting to package development and publishing.

## Purpose

Guide Emacs Lisp development using modern tooling and conventions:
- **Configuration**: use-package, straight.el, package.el best practices
- **Package development**: Structure, conventions, and tooling
- **Testing**: ERT (Emacs Lisp Regression Testing)
- **Code quality**: package-lint, checkdoc, byte-compilation
- **Publishing**: MELPA, GNU ELPA, NonGNU ELPA
- **Modern tools**: Eask, native compilation, package-vc

### Context Detection

**This skill activates when:**
- Working with `.el` files
- Directory contains `Eask`, `Cask`, or package headers
- User mentions Emacs configuration, packages, or MELPA
- Commands like `emacs`, `eask`, `package-lint` are mentioned
- Working in `.emacs.d/` or similar Emacs directories

## Workflow Routing

**When executing a workflow, output this notification directly:**

```
Running the **WorkflowName** workflow from the **EmacsLisp** skill...
```

| Workflow | Trigger | File |
|----------|---------|------|
| **Configure** | "emacs configuration", "use-package", "init.el" | `workflows/Configure.md` |
| **Package** | "create emacs package", "package structure", "elisp package" | `workflows/Package.md` |
| **Test** | "emacs tests", "ert", "test elisp", "buttercup" | `workflows/Test.md` |
| **Lint** | "lint elisp", "package-lint", "checkdoc", "byte compile" | `workflows/Lint.md` |
| **Publish** | "publish to melpa", "elpa", "submit package" | `workflows/Publish.md` |
| **Script** | "elisp script", "batch mode", "standalone elisp" | `workflows/Script.md` |
| **Debug** | "debug elisp", "edebug", "elisp debugger" | `workflows/Debug.md` |
| **Document** | "elisp documentation", "docstrings", "info manual" | `workflows/Document.md` |

## Core Principles

1. **Follow conventions**: Package naming, headers, docstrings
2. **Use modern Emacs**: Target Emacs 29+ for new packages
3. **Write tests**: Use ERT for all packages
4. **Lint before publishing**: package-lint, checkdoc, byte-compile
5. **Document thoroughly**: Every function, variable, and customization
6. **Use lexical binding**: Always use `;;; -*- lexical-binding: t -*-`
7. **Native compilation**: Support native-comp for performance

## Modern Emacs (2025)

### Emacs 29+ Features

- **use-package**: Built-in package configuration
- **package-vc**: Install packages directly from version control
- **Native compilation**: Faster Emacs Lisp execution
- **eglot**: Built-in LSP client
- **tree-sitter**: Fast syntax parsing

### Recommended Tooling

| Tool | Purpose | Status |
|------|---------|--------|
| **Eask** | Package development, testing, linting | Modern (2022+) |
| **package-lint** | Lint packages for MELPA | Essential |
| **checkdoc** | Check docstrings | Built-in |
| **ERT** | Testing framework | Built-in |
| **buttercup** | BDD testing (alternative) | Optional |
| **use-package** | Configuration management | Built-in (29+) |

## Package Structure

### Standard Package

```
my-package/
├── my-package.el          # Main package file
├── my-package-test.el     # Tests (ERT)
├── Eask                   # Package development tool
├── README.md              # Description and usage
├── CHANGELOG.md           # Version history
└── .github/
    └── workflows/
        └── test.yml       # CI testing
```

### Multi-file Package

```
my-package/
├── my-package.el          # Main entry point with autoloads
├── my-package-core.el     # Core functionality
├── my-package-ui.el       # UI components
├── my-package-utils.el    # Utilities
├── test/
│   ├── my-package-test.el
│   └── my-package-core-test.el
├── Eask
└── README.md
```

## Package Headers

Every Emacs Lisp package must start with standard headers:

```elisp
;;; my-package.el --- Brief description  -*- lexical-binding: t -*-

;; Copyright (C) 2025 Your Name

;; Author: Your Name <your.email@example.com>
;; Version: 0.1.0
;; Package-Requires: ((emacs "29.1"))
;; Keywords: convenience, tools
;; URL: https://github.com/yourusername/my-package

;; This file is not part of GNU Emacs.

;; This program is free software; you can redistribute it and/or modify
;; it under the terms of the GNU General Public License as published by
;; the Free Software Foundation, either version 3 of the License, or
;; (at your option) any later version.

;; This program is distributed in the hope that it will be useful,
;; but WITHOUT ANY WARRANTY; without even the implied warranty of
;; MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
;; GNU General Public License for more details.

;; You should have received a copy of the GNU General Public License
;; along with this program.  If not, see <https://www.gnu.org/licenses/>.

;;; Commentary:

;; Longer description of what this package does.
;;
;; Usage:
;;
;;     (require 'my-package)
;;     (my-package-enable)

;;; Code:

(defgroup my-package nil
  "Customization group for my-package."
  :group 'tools
  :prefix "my-package-")

;; Package code here...

(provide 'my-package)
;;; my-package.el ends here
```

## Coding Conventions

### Naming

```elisp
;; Package prefix for all symbols
(defun my-package-do-something ()  ; Function
  ...)

(defvar my-package-mode-map       ; Variable
  (make-sparse-keymap))

(defcustom my-package-enable-feature nil  ; Customizable
  "Whether to enable feature."
  :type 'boolean
  :group 'my-package)

;; Private/internal (double dash)
(defun my-package--internal-helper ()
  "Internal helper function."
  ...)
```

### Docstrings

```elisp
(defun my-package-process-file (file &optional verbose)
  "Process FILE and return the result.

If VERBOSE is non-nil, print progress messages.

FILE should be a path to a readable file.  Returns a list
of processed items, or nil if FILE cannot be processed.

Example usage:

  (my-package-process-file \"/path/to/file.txt\" t)

See also `my-package-process-directory'."
  ...)

(defcustom my-package-timeout 30
  "Timeout in seconds for operations.

This value controls how long to wait before giving up on
long-running operations.  Set to 0 to disable timeout."
  :type 'integer
  :group 'my-package)
```

### Lexical Binding

Always use lexical binding (modern Emacs standard):

```elisp
;;; my-package.el --- Description  -*- lexical-binding: t -*-
```

Benefits:
- Better performance
- Proper closures
- Catches more errors

## Configuration Best Practices

### use-package (Built-in since Emacs 29)

```elisp
;; In init.el or early-init.el
(require 'package)
(add-to-list 'package-archives '("melpa" . "https://melpa.org/packages/"))
(package-initialize)

;; Configure packages with use-package
(use-package magit
  :ensure t
  :bind ("C-x g" . magit-status)
  :config
  (setq magit-display-buffer-function
        #'magit-display-buffer-same-window-except-diff-v1))

(use-package org
  :ensure t
  :defer t
  :custom
  (org-directory "~/org")
  (org-agenda-files '("~/org/agenda.org"))
  :config
  (org-babel-do-load-languages
   'org-babel-load-languages
   '((emacs-lisp . t)
     (python . t))))
```

### straight.el (Alternative package manager)

```elisp
;; Bootstrap straight.el
(defvar bootstrap-version)
(let ((bootstrap-file
       (expand-file-name "straight/repos/straight.el/bootstrap.el"
                         user-emacs-directory))
      (bootstrap-version 6))
  (unless (file-exists-p bootstrap-file)
    (with-current-buffer
        (url-retrieve-synchronously
         "https://raw.githubusercontent.com/radian-software/straight.el/develop/install.el"
         'silent 'inhibit-cookies)
      (goto-char (point-max))
      (eval-print-last-sexp)))
  (load bootstrap-file nil 'nomessage))

;; Use packages
(straight-use-package 'use-package)
(use-package magit
  :straight t)
```

## Testing with ERT

### Basic Test

```elisp
;;; my-package-test.el --- Tests for my-package  -*- lexical-binding: t -*-

(require 'ert)
(require 'my-package)

(ert-deftest my-package-test-addition ()
  "Test that addition works correctly."
  (should (= (my-package-add 2 3) 5))
  (should (= (my-package-add -1 1) 0))
  (should (= (my-package-add 0 0) 0)))

(ert-deftest my-package-test-error ()
  "Test that errors are raised correctly."
  (should-error (my-package-divide 10 0)))

(ert-deftest my-package-test-buffer ()
  "Test buffer operations."
  (with-temp-buffer
    (insert "test content")
    (should (= (point-max) 13))
    (goto-char (point-min))
    (should (looking-at "test"))))

(provide 'my-package-test)
;;; my-package-test.el ends here
```

### Run Tests

```bash
# Using Emacs batch mode
emacs -batch -l my-package.el -l my-package-test.el -f ert-run-tests-batch-and-exit

# Using Eask
eask test ert my-package-test.el

# In Emacs interactively
M-x ert RET t RET
```

## Eask (Modern Development Tool)

### Eask File

```elisp
;; Eask
(package "my-package"
         "0.1.0"
         "Brief description of my package")

(website-url "https://github.com/yourusername/my-package")
(keywords "convenience" "tools")

(package-file "my-package.el")

(script "test" "echo \"Run tests..\" && eask ert-runner")
(script "lint" "echo \"Linting..\" && eask lint package")

(source "gnu")
(source "melpa")

(depends-on "emacs" "29.1")

(development
 (depends-on "ert-runner")
 (depends-on "package-lint"))
```

### Eask Commands

```bash
# Install dependencies
eask install-deps

# Run tests
eask test

# Lint package
eask lint package
eask lint checkdoc
eask lint elisp-lint

# Byte compile
eask compile

# Package for distribution
eask package

# Clean build artifacts
eask clean all
```

## Publishing to MELPA

### Requirements

1. **Package structure**: Follow conventions
2. **Tests**: Include tests
3. **Documentation**: Complete docstrings
4. **License**: GPL-compatible license
5. **Git repository**: Public Git repo (GitHub, GitLab, etc.)

### MELPA Recipe

Create a recipe in MELPA repository:

```elisp
;; In melpa/recipes/my-package
(my-package :fetcher github
            :repo "yourusername/my-package"
            :files ("*.el"))
```

### Submission Process

1. **Prepare package**:
   ```bash
   eask lint package
   eask lint checkdoc
   eask compile
   eask test
   ```

2. **Fork MELPA**: https://github.com/melpa/melpa

3. **Add recipe**: Create `recipes/my-package`

4. **Test locally**:
   ```bash
   make recipes/my-package
   make sandbox INSTALL=my-package
   ```

5. **Submit PR**: Create pull request to MELPA

6. **Wait for review**: MELPA maintainers will review

## Publishing to GNU ELPA

### Requirements

- **Copyright assignment**: Assign copyright to FSF (for packages >300 lines)
- **License**: GPL-compatible
- **No external dependencies**: Prefer built-in Emacs features

### Submission

1. Email `emacs-devel@gnu.org` with package proposal
2. Provide Git repository URL
3. Complete copyright assignment if needed
4. Maintainers will add to GNU ELPA

## Code Quality Tools

### package-lint

```bash
# Install
M-x package-install RET package-lint RET

# Run
M-x package-lint-current-buffer

# Or with Eask
eask lint package
```

### checkdoc

```bash
# Interactive
M-x checkdoc

# Batch mode
emacs -batch -l checkdoc -f checkdoc-file my-package.el
```

### Byte Compilation

```bash
# Interactive
M-x byte-compile-file

# Batch
emacs -batch -f batch-byte-compile my-package.el

# Eask
eask compile
```

## Common Patterns

### Minor Mode

```elisp
(defvar my-package-mode-map
  (let ((map (make-sparse-keymap)))
    (define-key map (kbd "C-c m") #'my-package-command)
    map)
  "Keymap for `my-package-mode'.")

;;;###autoload
(define-minor-mode my-package-mode
  "Toggle My Package mode.

When enabled, provides enhanced features for working with files."
  :lighter " MyPkg"
  :keymap my-package-mode-map
  :group 'my-package
  (if my-package-mode
      (my-package--enable)
    (my-package--disable)))

(defun my-package--enable ()
  "Enable My Package mode."
  (add-hook 'before-save-hook #'my-package--before-save nil t))

(defun my-package--disable ()
  "Disable My Package mode."
  (remove-hook 'before-save-hook #'my-package--before-save t))
```

### Autoloads

```elisp
;;;###autoload
(defun my-package-enable ()
  "Enable my-package globally."
  (interactive)
  (my-package-mode 1))
```

### Customization

```elisp
(defgroup my-package nil
  "Customization group for my-package."
  :group 'tools
  :prefix "my-package-")

(defcustom my-package-auto-save t
  "Whether to automatically save files."
  :type 'boolean
  :safe #'booleanp
  :group 'my-package)

(defcustom my-package-file-extensions '("txt" "md")
  "List of file extensions to process."
  :type '(repeat string)
  :group 'my-package)
```

## Performance

### Lazy Loading

```elisp
;; Defer loading until needed
(use-package my-package
  :defer t
  :commands (my-package-enable my-package-do-something))

;; Load on file type
(use-package my-package
  :mode "\\.mypkg\\'")

;; Load on hook
(use-package my-package
  :hook (prog-mode . my-package-mode))
```

### Byte Compilation

Always byte-compile packages for distribution:
- Faster execution
- Catches some errors
- Smaller file size

### Native Compilation

Support native compilation (Emacs 28+):
- Automatically compiles to native code
- Significantly faster execution
- No code changes needed

## Best Practices

1. **Use lexical binding**: `;;; -*- lexical-binding: t -*-`
2. **Follow naming conventions**: Use package prefix
3. **Write complete docstrings**: Every public function/variable
4. **Include tests**: Use ERT for all functionality
5. **Lint before publishing**: package-lint, checkdoc
6. **Use autoloads**: Mark entry points with `;;;###autoload`
7. **Avoid global state**: Use buffer-local variables
8. **Handle errors**: Use `condition-case` appropriately
9. **Check Emacs version**: Use `(when (version< emacs-version "29.1") ...)`
10. **Keep dependencies minimal**: Prefer built-in features

## Resources

### Official Documentation

- [Emacs Lisp Manual](https://www.gnu.org/software/emacs/manual/html_node/elisp/)
- [Emacs Lisp Intro](https://www.gnu.org/software/emacs/manual/html_node/eintr/)
- [MELPA Contributing](https://github.com/melpa/melpa/blob/master/CONTRIBUTING.org)

### Tools

- [Eask](https://emacs-eask.github.io/) - Modern package development
- [package-lint](https://github.com/purcell/package-lint) - Lint for packages
- [elisp-lint](https://github.com/gonewest818/elisp-lint) - Comprehensive linting
- [buttercup](https://github.com/jorgenschaefer/emacs-buttercup) - BDD testing

### Style Guides

- [Emacs Lisp Style Guide](https://github.com/bbatsov/emacs-lisp-style-guide)
- [Naming Conventions](https://www.gnu.org/software/emacs/manual/html_node/elisp/Coding-Conventions.html)

## Examples

**Example 1: Create a new package**
```
User: "Create an Emacs package for managing bookmarks"
→ Invokes Package workflow
→ Creates package structure with Eask
→ Sets up tests and CI
→ Generates package headers and boilerplate
```

**Example 2: Publish to MELPA**
```
User: "How do I publish my package to MELPA?"
→ Invokes Publish workflow
→ Checks package quality with linters
→ Creates MELPA recipe
→ Guides through PR submission
```

**Example 3: Configure Emacs**
```
User: "Set up my Emacs with use-package"
→ Invokes Configure workflow
→ Shows modern use-package patterns
→ Demonstrates package installation
→ Explains performance optimization
```

---

**Philosophy**: Modern Emacs Lisp development emphasizes testing, documentation, and code quality. Use modern tooling (Eask, package-lint) and follow conventions to create packages that integrate seamlessly with the Emacs ecosystem.
