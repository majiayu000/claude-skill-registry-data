---
name: emacs-transient
description: Expert guide for building Emacs transient menus (keyboard-driven UI like Magit). Use when implementing or debugging transient-define-prefix, transient-define-suffix, or transient-define-infix commands.
---

# Emacs Transient Expert

This skill provides comprehensive guidance for building transient-based
interfaces in Emacs Lisp, based on the official transient library and
real-world implementations in Magit, Forge, and transient-showcase.

## When to Use This Skill

Invoke this skill when:
- Implementing new `transient-define-prefix` menus
- Creating `transient-define-suffix` or `transient-define-infix` commands
- Debugging transient menu layouts or behavior
- Understanding transient levels, groups, or conditional display
- Working on keyboard-driven UI similar to Magit
- Converting traditional Emacs commands to transient interfaces

## Core Concepts

### What is Transient?

Transient is a library for creating keyboard-driven, temporary menus
in Emacs. It's the foundation of Magit's interface and provides:
- **Display of current state** - Show active arguments and options
- **Modal bindings** - Temporary keymaps that disappear when done
- **Contextual UI** - Menus adapt based on state
- **Persistence** - Save and restore argument values across sessions
- **History** - Track previously used values

### Key Terminology

- **Prefix** - The main transient command that opens the menu
- **Suffix** - Commands invoked from the transient (actions)
- **Infix** - Special suffixes that set arguments/options without
  exiting
- **Groups** - Organizational units for layout (rows, columns,
  sections)
- **Levels** (1-7) - Control visibility based on user expertise
  (default: 4)
- **Scope** - Contextual value passed to suffixes (e.g., current
  branch)

## Three Core Macros

### 1. transient-define-prefix

Defines the main transient menu.

```elisp
(transient-define-prefix my-menu ()
  "Description of what this menu does."
  :man-page "git-commit"              ; Optional: link to man page
  :info-manual "(magit)Committing"    ; Optional: link to info manual
  :value '("--verbose")               ; Optional: default arguments

  ;; Groups define layout
  ["Arguments"                        ; Group header
   ("-v" "Verbose" "--verbose")       ; Switch (toggle)
   ("-a" "Author" "--author="         ; Option (takes value)
    :prompt "Author: ")
   (my-custom-infix)]                 ; Reference to defined infix

  [["Actions"                         ; Nested groups = columns
    ("c" "Commit" my-commit-cmd)
    ("a" "Amend" my-amend-cmd)]
   ["Other"
    ("q" "Quit" transient-quit)]])
```

**Key slots:**
- `:value` - Default arguments
- `:man-page` - Man page for help
- `:info-manual` - Info manual section
- `:transient-suffix` - Default transient behavior for suffixes
- `:transient-non-suffix` - Allow/forbid non-suffix commands
- `:refresh-suffixes` - When to refresh suffix state

### 2. transient-define-suffix

Defines action commands (suffixes).

```elisp
(transient-define-suffix my-commit-cmd (args)
  "Create a commit with ARGS."
  :description "Commit staged changes"  ; Optional: override in menu
  :transient t                          ; Stay transient after calling
  (interactive (list (transient-args 'my-menu)))
  (apply #'my-run-git "commit" args))
```

**Key slots:**
- `:key` - Key binding (can override menu binding)
- `:description` - Can be string or function returning string
- `:transient` - Control transient state (see below)
- `:if` / `:if-not` - Conditional visibility
- `:inapt-if` / `:inapt-if-not` - Show but disable

### 3. transient-define-infix (or transient-define-argument)

Defines argument commands (infixes).

```elisp
(transient-define-argument my-author-arg ()
  :description "Set author"
  :class 'transient-option              ; Option class (takes value)
  :shortarg "-a"                        ; Short form
  :argument "--author="                 ; Long form
  :reader #'my-read-author)             ; Custom reader function

(transient-define-infix my-verbose-switch ()
  :description "Verbose output"
  :class 'transient-switch              ; Switch class (boolean)
  :argument "--verbose")
```

## Infix/Suffix Classes

### Suffix Classes

- **`transient-suffix`** - Base class for all suffixes
- **`transient-infix`** - Base for all infixes (auto-stays transient)

### Infix Classes (derive from transient-infix)

**For command-line arguments:**
- **`transient-switch`** - Boolean flag (e.g., `--verbose`)
- **`transient-option`** - Argument with value (e.g., `--author=NAME`)
- **`transient-switches`** - Mutually exclusive options
- **`transient-files`** - File arguments (`--` separator)

**For variables:**
- **`transient-variable`** - Base for variable infixes
- **`transient-lisp-variable`** - Set Emacs Lisp variables

**Display only:**
- **`transient-information`** - Display info (no command/key)
- **`transient-information*`** - Info aligned with descriptions

## Suffix Specification Syntax

Three ways to specify suffixes:

### 1. Inline (shorthand)
```elisp
("key" "description" command)
("-s" "switch" "--switch")              ; Auto-creates transient-switch
("-o" "option" "--option=")             ; Auto-creates transient-option
```

### 2. With keyword arguments
```elisp
("key" "description" command
 :transient t                           ; Stay transient
 :if (lambda () (my-condition)))        ; Conditional

("-a" "author" "--author="
 :prompt "Author name: "
 :reader #'my-custom-reader
 :always-read t)                        ; Always prompt, don't toggle
```

### 3. Reference to separately defined command
```elisp
(my-custom-suffix)                      ; Uses suffix's own key/desc
```

## Group Specification Syntax

```elisp
[{LEVEL} {DESCRIPTION} {KEYWORD VALUE}... ELEMENT...]
```

**Common patterns:**

```elisp
["Group Title"                          ; Simple group with title
 ("k" "desc" cmd)]

[:description "Dynamic"                 ; Dynamic description
 :description (lambda () (format "Time: %s" (current-time-string)))
 ("k" "desc" cmd)]

[:if some-predicate                     ; Conditional group
 ("k" "desc" cmd)]

[:class transient-row                   ; Explicit layout class
 ("k" "desc" cmd)]

[["Column 1"                            ; Nested groups = columns
  ("a" "cmd a" cmd-a)]
 ["Column 2"
  ("b" "cmd b" cmd-b)]]
```

**Group classes:**
- **`transient-column`** - Stack items vertically (default)
- **`transient-row`** - Arrange items horizontally
- **`transient-columns`** - Contains column groups side-by-side
- **`transient-subgroups`** - Contains subgroups

## The :transient Slot (Controlling State)

Controls whether transient stays active after invoking a command.

**For suffixes (default: exit transient):**
- `nil` or `:transient nil` - Exit transient (default for suffixes)
- `t` or `:transient t` - Stay transient
- `:transient 'transient--do-call` - Export args and stay
- `:transient 'transient--do-return` - Return to parent prefix

**For infixes (default: stay transient):**
- Infixes always use `transient--do-stay` by default
- Rarely need to override

**For sub-prefixes (nested transients):**
- `nil` - Exit all transients when sub-prefix exits
- `t` - Return to parent when sub-prefix exits
- `:transient 'transient--do-recurse` - Enable return behavior
- `:transient 'transient--do-replace` - Replace parent (no return)

**Common pre-commands:**
- `transient--do-exit` - Exit and export args
- `transient--do-stay` - Stay, don't export args
- `transient--do-call` - Stay and export args
- `transient--do-return` - Exit to parent prefix

## Layout Patterns

### Stacked Groups (Vertical)
```elisp
(transient-define-prefix my-menu ()
  ["Top Group" ...]
  ["Bottom Group" ...])
```

### Columns (Side-by-side)
```elisp
(transient-define-prefix my-menu ()
  [["Left Column" ...]
   ["Right Column" ...]])
```

### Mixed (Stacked + Columns)
```elisp
(transient-define-prefix my-menu ()
  ["Top Group (full width)" ...]

  [["Left Column" ...]
   ["Right Column" ...]])
```

### Grid Layout
```elisp
(transient-define-prefix my-menu ()
  [:description "The Grid"
   ["Left Column"
    ("tl" "top-left" cmd)
    ("bl" "bottom-left" cmd)]
   ["Right Column"
    ("tr" "top-right" cmd)
    ("br" "bottom-right" cmd)]])
```

### Spacing
```elisp
["Group"
 ""                                     ; Empty line
 ("k" "first" cmd)
 ("l" "second" cmd)
 ""                                     ; Another gap
 ("m" "third" cmd)]
```

## Accessing Transient Values

### In suffix commands

```elisp
(transient-define-suffix my-suffix (args)
  "Do something with ARGS."
  (interactive (list (transient-args 'my-prefix)))
  ;; Now use args...
  (message "Args: %S" args))
```

### Getting specific argument values

```elisp
(let* ((args (transient-args 'my-prefix))
       (author (transient-arg-value "--author=" args))
       (verbose-p (transient-arg-value "--verbose" args)))
  ;; Use values...
  )
```

### Using scope (contextual value)

```elisp
(transient-define-prefix my-menu (scope)
  "Menu with scope."
  ["Actions"
   ("a" "Action" my-action)]
  (interactive "P")  ; Can take prefix arg as scope
  (transient-setup 'my-menu nil nil :scope scope))

(transient-define-suffix my-action ()
  (interactive)
  (let ((scope (transient-scope)))
    (message "Scope: %S" scope)))
```

## Conditional Display (Predicates)

### Visibility predicates (if suffix should appear)

```elisp
("k" "desc" cmd
 :if (lambda () (file-exists-p "Makefile")))      ; Show if true

("k" "desc" cmd
 :if-not some-mode                                ; Show if not in mode
 :if-non-nil some-variable                        ; Show if var non-nil
 :if-mode 'emacs-lisp-mode                        ; Show in mode
 :if-derived 'prog-mode)                          ; Show if derived
```

### Inapt predicates (show but grayed out)

```elisp
("k" "desc" cmd
 :inapt-if (lambda () (not (magit-anything-staged-p)))) ; Gray if true

("k" "desc" cmd
 :inapt-if-not some-function                      ; Gray if false
 :inapt-if-nil some-variable)                     ; Gray if var nil
```

### On groups

```elisp
[:if magit-rebase-in-progress-p         ; Whole group conditional
 ("a" "abort" magit-rebase-abort)
 ("c" "continue" magit-rebase-continue)]
```

## Important Suffix Slots

**Required/Common:**
- `:key` - Key binding
- `:description` - String or function returning string
- `:command` - The command to invoke

**Behavioral:**
- `:transient` - Stay transient? (t/nil/pre-command)
- `:level` - Visibility level (1-7, default 4)

**Conditional:**
- `:if`, `:if-not`, `:if-mode`, `:if-derived` - Visibility
- `:inapt-if`, `:inapt-if-not` - Enable/disable

**Display:**
- `:format` - Custom display format (`%k` `%d` `%v`)
- `:face` - Face for description
- `:summary` - Echo area/tooltip text

**Help:**
- `:show-help` - Custom help function

## Important Infix Slots

**All suffix slots, plus:**

**Argument-related:**
- `:argument` - Long form (e.g., `--verbose`)
- `:shortarg` - Short form (e.g., `-v`)
- `:class` - Infix class (switch/option/etc.)

**Reading values:**
- `:reader` - Function to read value (PROMPT, INITIAL, HISTORY)
- `:prompt` - Prompt string or function
- `:choices` - List of valid values
- `:always-read` - Always prompt (don't toggle for options)
- `:allow-empty` - Allow empty string

**Multi-value:**
- `:multi-value` - `'rest` or `'repeat` for multiple values

**Other:**
- `:init-value` - Function to set initial value
- `:history-key` - Symbol for history (share across infixes)
- `:unsavable` - Don't save with prefix value

## Levels (1-7)

Control visibility based on user preference:
- **1-3**: Essential commands (always visible)
- **4**: Default level
- **5-6**: Advanced/rarely used
- **7**: Experimental/debug
- **0**: Never show (effectively disabled)

```elisp
("k" "advanced" cmd :level 6)           ; Only show at level 6+

["Arguments" :level 5                   ; Whole group at level 5
 ("-v" "verbose" "--verbose")]
```

Users can change levels interactively with `C-x l`.

## Dynamic Content

### Dynamic descriptions

```elisp
("k" my-cmd
 :description (lambda ()
                (format "Branch: %s" (magit-get-current-branch))))
```

### Dynamic groups (:setup-children)

```elisp
[:class transient-column
 :setup-children
 (lambda (_)
   (transient-parse-suffixes
    'my-prefix
    (mapcar (lambda (file)
              (list (substring file 0 1) file
                    (lambda () (interactive) (find-file file))))
            (directory-files "."))))]
```

### Information display

```elisp
["Info"
 (:info "Static information")
 (:info (lambda () (format "Dynamic: %s" (current-time-string))))
 (:info my-info-function :format " %d")]  ; Custom format
```

## Common Patterns from Magit

### Context-aware suffixes

```elisp
(transient-define-suffix my-cmd (args)
  (interactive
   (if (derived-mode-p 'my-list-mode)
       (list (my-get-args-from-buffer))
     (list (transient-args 'my-prefix))))
  ...)
```

### Shared argument groups

```elisp
(transient-define-group my-common-args ()
  ["Common Arguments"
   ("-v" "Verbose" "--verbose")
   ("-q" "Quiet" "--quiet")])

(transient-define-prefix my-menu-1 ()
  [my-common-args]                      ; Include by reference
  ["Actions" ...])

(transient-define-prefix my-menu-2 ()
  [my-common-args]                      ; Reuse in another menu
  ["Other Actions" ...])
```

### Validation before execution

```elisp
(transient-define-suffix my-create (title desc)
  (interactive
   (list (read-string "Title: ")
         (read-string "Description: ")))
  (when (string-empty-p title)
    (user-error "Title cannot be empty"))
  (my-create-thing title desc))
```

## Best Practices

### 1. Use appropriate classes
- Use `transient-switch` for boolean flags
- Use `transient-option` for value-taking arguments
- Use `transient-switches` for mutually exclusive options

### 2. Leverage levels effectively
- Put common operations at level 3-4
- Put advanced features at level 5-6
- Use level 7 for debug/experimental

### 3. Provide good descriptions
- Keep descriptions concise (fits in menu)
- Use dynamic descriptions to show state
- Use `:summary` for longer explanations

### 4. Handle state properly
- Use `:transient t` for commands that should stay in menu
- Use `:if` predicates instead of manual state checking
- Use `:inapt-if` to show unavailable options

### 5. Organize logically
- Group related items together
- Use columns for parallel choices
- Put common actions on left, advanced on right

### 6. Share history
- Use `:history-key` to share history between similar infixes
```elisp
(transient-define-argument my-author ()
  :argument "--author="
  :history-key 'my-package-author-history)
```

### 7. Provide help
- Set `:man-page` or `:info-manual` on prefix
- Use descriptive docstrings
- Implement custom `:show-help` if needed

### 8. Test interactively
- Use `C-h` while transient is active to see help
- Use `C-x l` to experiment with levels
- Use `C-x s` / `C-x C-s` to test persistence

## Common Gotchas

1. **Don't quote in transient definitions** - The macro handles it
   ```elisp
   ;; WRONG:
   ["Group" '("k" "desc" 'cmd)]

   ;; RIGHT:
   ["Group" ("k" "desc" cmd)]
   ```

2. **Use :transient t for iterative commands**
   ```elisp
   ("n" "next" my-next :transient t)    ; Can press 'n' repeatedly
   ```

3. **Remember infixes stay transient by default**
   - Don't need `:transient t` on infixes
   - They automatically use `transient--do-stay`

4. **:if vs :inapt-if**
   - `:if` - completely hide the suffix
   - `:inapt-if` - show but grayed out

5. **Accessing args in interactive**
   ```elisp
   (interactive (list (transient-args 'my-prefix)))  ; Correct
   ```

6. **Sub-prefix returns**
   ```elisp
   ("s" "sub-menu" my-sub-prefix :transient t)  ; Returns to parent
   ```

## Complete Example

```elisp
;; Custom argument
(transient-define-argument my-pkg:--author ()
  :description "Override author"
  :class 'transient-option
  :shortarg "-a"
  :argument "--author="
  :reader #'my-read-author)

;; Suffix that stays transient
(transient-define-suffix my-pkg-preview ()
  "Preview current settings."
  :transient t
  (interactive)
  (message "Args: %S" (transient-args 'my-pkg-create)))

;; Main suffix
(transient-define-suffix my-pkg-execute (args)
  "Execute with ARGS."
  (interactive (list (transient-args 'my-pkg-create)))
  (apply #'my-pkg-run args))

;; Main menu
(transient-define-prefix my-pkg-create ()
  "Create something with options."
  :man-page "my-tool"
  :value '("--verbose")

  ["Arguments"
   ("-v" "Verbose" "--verbose")
   ("-q" "Quiet" "--quiet")
   ("-n" "Dry run" "--dry-run" :level 5)
   (my-pkg:--author)]

  [["Actions"
    ("p" "Preview" my-pkg-preview)
    ("c" "Create" my-pkg-execute)]
   ["Other"
    ("q" "Quit" transient-quit)]])
```

## Reference Materials

For deeper understanding, refer to:
- **transient-reference/transient/** - Core library documentation
- **transient-reference/magit/** - Real-world usage in Magit
- **transient-reference/forge/** - Additional patterns in Forge
- **transient-reference/transient-showcase/** - Examples showcase

## Testing Transient Menus

### Why Test Transients?

Transient menus have complex state management involving:
- Infix commands that set state variables
- Suffix commands that read those states
- Pre/post-command hooks for state transitions
- Display refreshes and keybinding resolution

Testing only suffix commands (by mocking `transient-args`) skips
testing the **entire UI layer**.

### Two Testing Approaches

#### 1. Unit Testing (Mocked Args) - Fast but Limited

Test suffix commands directly by mocking `transient-args`:

```elisp
(defmacro my-test-with-transient-args (prefix args &rest body)
  "Execute BODY with transient-args mocked for PREFIX to return ARGS."
  (declare (indent 2))
  `(cl-letf (((symbol-function 'transient-args)
              (lambda (p)
                (when (eq p ,prefix)
                  ,args))))
     ,@body))

(ert-deftest my-test-suffix-execution ()
  "Test suffix command with mocked args."
  (my-test-with-transient-args 'my-prefix
      '("--title=Test" "--priority=1")
    (let ((result (call-interactively #'my-suffix-execute)))
      (should (string-match-p "Created" result)))))
```

**Pros:**
- Fast (~0.5s per test)
- Simple to write
- Good for testing suffix logic

**Cons:**
- ❌ Doesn't test infix commands
- ❌ Doesn't test transient UI
- ❌ Doesn't test user workflow
- ❌ Won't catch binding errors

#### 2. Integration Testing (execute-kbd-macro) - Slower but Complete

Test the full user interaction with keyboard macros:

```elisp
(ert-deftest my-test-full-ui-interaction ()
  "Test complete user workflow through transient UI."
  :tags '(:integration :ui)
  (my-test-with-project ()  ; Setup test environment
    ;; Invoke the transient menu
    (funcall-interactively #'my-prefix)

    ;; Set title via infix (key + input in ONE macro!)
    (execute-kbd-macro (kbd "t Test SPC Title RET"))

    ;; Set priority via infix
    (execute-kbd-macro (kbd "- p 1 RET"))

    ;; Execute the suffix
    (execute-kbd-macro (kbd "x"))

    ;; Verify results
    (let ((result (my-get-created-item)))
      (should (equal (plist-get result :title) "Test Title"))
      (should (equal (plist-get result :priority) 1)))))
```

**Pros:**
- ✅ Tests infix commands
- ✅ Tests transient UI
- ✅ Tests real user workflow
- ✅ No mocking needed
- ✅ Works in batch mode (CI-friendly!)
- ✅ Catches binding errors, UI bugs

**Cons:**
- Slower (~2.3s per test, +0.65s overhead)
- More complex to write
- Need to know key sequences

**Performance breakdown:**
- Transient infrastructure: ~0.15s
- Multiple kbd macro calls: ~0.20s
- Minibuffer interactions: ~0.20s
- Display refreshes: ~0.10s
- **Total overhead: ~0.65s per test**

### Critical Rule for execute-kbd-macro

**You MUST combine transient key + input in a SINGLE kbd macro:**

```elisp
;; ✅ CORRECT - Key + input in one macro
(execute-kbd-macro (kbd "t Bug SPC Title RET"))

;; ❌ WRONG - Splitting key and input
(execute-kbd-macro (kbd "t"))              ; Opens minibuffer
(execute-kbd-macro (kbd "Bug Title RET"))  ; Fails! Tries to invoke
                                           ; transient keys B, u, g
```

**Why?** When you split the macro, the second call doesn't go to the
minibuffer - it's interpreted as more transient commands.

### Testing Patterns

#### Pattern 1: Minimal workflow (title only)

```elisp
(ert-deftest my-test-minimal-workflow ()
  "Test simplest possible workflow."
  (my-test-setup ()
    (funcall-interactively #'my-create)
    (execute-kbd-macro (kbd "t Minimal SPC Test RET"))
    (execute-kbd-macro (kbd "x"))
    ;; Verify...
    ))
```

#### Pattern 2: Full workflow (multiple fields)

```elisp
(ert-deftest my-test-full-workflow ()
  "Test complete workflow with all fields."
  (my-test-setup ()
    (funcall-interactively #'my-create)

    ;; Set all fields
    (execute-kbd-macro (kbd "t Full SPC Test RET"))
    (execute-kbd-macro (kbd "- t feature RET"))
    (execute-kbd-macro (kbd "- p 2 RET"))
    (execute-kbd-macro (kbd "- a john@example.com RET"))

    ;; Execute
    (execute-kbd-macro (kbd "x"))

    ;; Verify all fields were set correctly
    ))
```

#### Pattern 3: Testing switches (toggle flags)

```elisp
(ert-deftest my-test-switches ()
  "Test boolean switch toggling."
  (my-test-setup ()
    (funcall-interactively #'my-prefix)

    ;; Toggle switch on
    (execute-kbd-macro (kbd "- v"))  ; --verbose

    ;; Toggle switch off
    (execute-kbd-macro (kbd "- v"))

    ;; Toggle back on
    (execute-kbd-macro (kbd "- v"))

    (execute-kbd-macro (kbd "x"))
    ;; Verify switch state...
    ))
```

#### Pattern 4: Testing transient navigation

```elisp
(ert-deftest my-test-navigation ()
  "Test moving between transient levels."
  (my-test-setup ()
    (funcall-interactively #'my-prefix)

    ;; Change transient level to show advanced options
    (execute-kbd-macro (kbd "C-x l 6 RET"))

    ;; Now advanced options should be visible
    (execute-kbd-macro (kbd "- n"))  ; Advanced option

    (execute-kbd-macro (kbd "x"))
    ;; Verify...
    ))
```

### Helper Functions

```elisp
(defun my-test-kbd-do (keys)
  "Execute keyboard macro from KEYS list.
KEYS is a list of key sequence strings that will be joined
and executed as a keyboard macro."
  (execute-kbd-macro (kbd (string-join keys " "))))

;; Usage:
(my-test-kbd-do '("t" "Title" "RET"))  ; Cleaner than raw kbd
```

### When to Use Each Approach

**Use mocked approach when:**
- Testing suffix logic in isolation
- Testing error handling
- Speed is critical (large test suite)
- Don't need to test UI interaction

**Use execute-kbd-macro approach when:**
- Testing end-to-end user workflows
- Validating infix commands work
- Testing transient state management
- Need confidence in the full UI
- Testing for a critical user path

**Recommended strategy:**
- Use mocked tests for most unit tests
- Use execute-kbd-macro for key integration tests
- At least one full UI test per transient menu

### Example: Complete Test Suite

```elisp
;;; Unit Tests (Mocked - Fast)

(ert-deftest my-create-test-parse-args ()
  "Test argument parsing."
  ;; Fast unit test, no UI
  )

(ert-deftest my-create-test-validation ()
  "Test validation logic."
  (my-test-with-transient-args 'my-create
      '("--title=")  ; Empty title
    (should-error (call-interactively #'my-create-execute)
                  :type 'user-error)))

;;; Integration Tests (Full UI - Comprehensive)

(ert-deftest my-create-test-full-ui-basic ()
  "Test basic creation workflow through UI."
  :tags '(:integration :ui)
  (my-test-setup ()
    (funcall-interactively #'my-create)
    (execute-kbd-macro (kbd "t Basic SPC Test RET"))
    (execute-kbd-macro (kbd "x"))
    ;; Verify creation...
    ))

(ert-deftest my-create-test-full-ui-all-fields ()
  "Test creation with all fields through UI."
  :tags '(:integration :ui :slow)
  (my-test-setup ()
    (funcall-interactively #'my-create)
    (execute-kbd-macro (kbd "t Full SPC Test RET"))
    (execute-kbd-macro (kbd "- t feature RET"))
    (execute-kbd-macro (kbd "- p 2 RET"))
    (execute-kbd-macro (kbd "x"))
    ;; Verify all fields...
    ))
```

### Debugging Tips

**When tests fail:**

1. **Check key bindings** - Use `C-h` in transient to see actual keys
2. **Test interactively first** - Run the transient manually
3. **Add debug messages**:
   ```elisp
   (execute-kbd-macro (kbd "t Test RET"))
   (message "After title: %S" (transient-args 'my-prefix))
   ```
4. **Check transient buffer** - Look at `*transient*` buffer state
5. **Use edebug** - Step through suffix execution

**Common issues:**

- **"Unbound suffix"** - Wrong key binding in test
- **"Wrong type argument"** - Reader function got nil/wrong type
- **Macro fails silently** - Split key + input across macros
- **Args not set** - Forgot to call `funcall-interactively` on prefix

### Testing Multiline Editor Fields

Fields that open dedicated editor buffers for multiline input (description,
notes, comments) **DO work** with `execute-kbd-macro` using the same principle
as simple fields: **combine everything in a SINGLE macro**.

**Pattern:**

```elisp
(funcall-interactively #'my-create)

;; ✅ CORRECT - Combine infix + text + commit in ONE macro
(execute-kbd-macro (kbd "- d Full SPC description SPC text C-c C-c"))
(execute-kbd-macro (kbd "- A Acceptance SPC criteria C-c C-c"))
```

**Why this works:**
1. `- d` opens the editor buffer
2. `Full SPC description SPC text` types into that buffer (it's now active)
3. `C-c C-c` commits and returns to transient menu
4. All happens in single macro execution, so context is preserved

**What DOESN'T work (split across macros):**

```elisp
;; ❌ WRONG - Split into separate macros
(execute-kbd-macro (kbd "- d"))               ; Opens editor
(execute-kbd-macro (kbd "My description"))     ; Fails! Wrong context
(execute-kbd-macro (kbd "C-c C-c"))           ; Fails! Wrong context
```

When you split into multiple `execute-kbd-macro` calls, each call starts from
the current buffer context, which may not be the editor buffer that was opened.

**Summary:**
- ✅ Simple minibuffer prompts work (combine key + input + RET)
- ✅ Switches/toggles work (just the key)
- ✅ **Multiline editor fields work** (combine key + text + C-c C-c)
- ❌ Splitting any interaction across multiple macro calls fails

### Comparison to Other Testing Approaches

**with-simulated-input package:**
- ❌ Adds complexity without clear benefits for transient testing
- ❌ Our pattern (mock transient-args + call-interactively) is simpler
- ✅ execute-kbd-macro works natively in batch mode

**Casual project approach:**
- Tests only binding structure (overrides commands with stubs)
- ❌ Doesn't test actual command execution
- ✅ Our approach tests REAL commands with REAL execution

**Result:** Our execute-kbd-macro approach gives superior coverage!

## Version History

- v1.1.0 (2025-11-19): Added comprehensive testing section with
  execute-kbd-macro patterns and performance analysis
- v1.0.0 (2025-11-06): Initial skill created from research of
  transient, Magit, Forge, and transient-showcase repositories
