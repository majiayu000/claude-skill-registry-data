---
name: emacs
description: Interact with a running Emacs instance via MCP. Use this skill when the user asks to interact with Emacs buffers, set up automation, or coordinate between Claude Code and Emacs. Access Elisp documentation directly via (describe-function 'fn) or (describe-variable 'var).
---

# Emacs Integration

The `mcp__emacs__emacs_eval` tool evaluates Emacs Lisp in the running Emacs instance.

## When to Use Emacs vs CLI Tools

**Use Emacs (`emacs_eval`) for:**

1. **Semantic operations** (LSP-aware):
```elisp
(eglot-rename "new_name")          ; LSP knows scope, not just text
(xref-find-references "func")      ; Understands imports, aliases
(flymake-diagnostics)              ; Type errors, not just syntax
(project-find-file)                ; Project-aware file finding
```

2. **Elisp codebase exploration** (STRONGLY PREFERRED over grep/glob):
```elisp
;; Discover symbols matching a pattern
(apropos-internal "agent-shell.*hook" 'boundp)  ; Find variables
(apropos-internal "^gptel-make" 'fboundp)       ; Find functions

;; Get function/variable documentation instantly
(describe-function 'agent-shell-mcp-server-start)
(describe-variable 'agent-shell-mode-hook)

;; Check current runtime state
(agent-shell-mcp-server-running-p)              ; Live state check
(symbol-value 'some-variable)                   ; Current value

;; Find files
(directory-files-recursively "~/.emacs.d" "\\.el$")
```

**Use CLI tools (Bash/Grep) only for:**
```bash
grep -r "TODO" --include="*.py" .  # Bulk text search in non-Elisp
sed -i 's/old/new/g' *.py          # Global text replace
find . -name "*.test.js"           ; File finding by pattern
```

**Rule of thumb**: For Emacs/Elisp codebases, ALWAYS use `emacs_eval` first. It's more token-efficient (returns only what you need), provides live runtime state, and understands Elisp semantics. Only fall back to grep/glob for non-Elisp code or bulk text operations.

## Why Elisp is Powerful for Agents

1. **No access control** - Everything is public, agent can modify anything
2. **Advice system** - Wrap any function without modifying source: `(advice-add 'fn :before #'my-fn)`
3. **Instant eval** - No compilation step, immediate feedback
4. **Self-documenting** - `(describe-function 'fn)` at runtime
5. **Hooks everywhere** - Event-driven observation and intervention

## Documentation Discovery

Query Emacs directly for any Elisp documentation:

```elisp
(describe-function 'function-name)
(describe-variable 'variable-name)
(apropos "search-term")
```

## Current Context

The Claude Code session runs in an `agent-shell-mode` buffer. Get context:

```elisp
major-mode                        ; => agent-shell-mode
(buffer-name)                     ; => "Claude Code Agent @ project-name"
(agent-shell--current-shell)      ; Get the shell object
```

## Self-Prompting with Timers

Set up a timer to automatically queue a prompt after idle time:

```elisp
(defvar my-agent-idle-timer nil)

(defun my-agent-idle-prompt ()
  "Queue a nudge to the agent after idle timeout."
  (when-let ((shell-buf (get-buffer "Claude Code Agent @ .emacs.d")))
    (with-current-buffer shell-buf
      ;; Use enqueue - agent-shell-insert errors if agent is busy
      (agent-shell--enqueue-request
       :prompt "Continue working on the current task."))))

;; Start: prompt after 15 minutes (900 seconds) of no activity
(setq my-agent-idle-timer
      (run-with-idle-timer 900 t #'my-agent-idle-prompt))

;; Stop the timer
(when my-agent-idle-timer
  (cancel-timer my-agent-idle-timer)
  (setq my-agent-idle-timer nil))
```

**Edge case**: `agent-shell-insert` with `:submit t` returns "Busy" or "Not yet supported" errors while the agent is processing. Use `agent-shell--enqueue-request` instead - it queues the request to run after the current task completes.

## Queueing Requests

Queue prompts that execute when the agent is no longer busy:

```elisp
;; Queue a request (runs when current task completes)
(agent-shell--enqueue-request :prompt "Next task to do")

;; Check pending queue
(with-current-buffer (agent-shell--current-shell)
  (alist-get :pending-requests agent-shell--state))
```

## Response Size Limits

Large return values may exceed the MCP response limit. Strategies:

```elisp
;; Truncate long strings
(substring (buffer-string) 0 (min 10000 (length (buffer-string))))

;; Return counts instead of full lists
(length (buffer-list))

;; Filter before returning
(seq-take (buffer-list) 10)

;; Write to file, return path
(with-temp-file "/tmp/output.txt"
  (insert large-content))
"/tmp/output.txt"  ; Return just the path
```

## Buffer Context Gotcha

Evaluations run in the agent-shell buffer by default. To operate on other buffers:

```elisp
;; WRONG: operates on agent-shell buffer
(buffer-string)

;; RIGHT: explicitly target a buffer
(with-current-buffer "target-buffer"
  (buffer-string))

;; Or use a temp buffer for scratch work
(with-temp-buffer
  (insert-file-contents "/path/to/file")
  (buffer-string))
```

## Periodic Background Tasks

Use `run-at-time` for scheduled operations:

```elisp
;; Run once after 5 minutes
(run-at-time 300 nil #'my-function)

;; Run every 60 seconds
(run-at-time t 60 #'my-repeating-function)

;; Cancel a timer
(cancel-timer timer-object)
```

## Coordinating Multiple Agents

If multiple agent-shell sessions exist:

```elisp
;; List all agent buffers
(agent-shell-buffers)

;; Get project-specific buffers  
(agent-shell-project-buffers)

;; Queue request to a specific shell (safe even if busy)
(with-current-buffer "Claude Code Agent @ other-project"
  (agent-shell--enqueue-request :prompt "message"))
```

## Inspecting Agent State

Access internal state for debugging or coordination:

```elisp
(with-current-buffer (agent-shell--current-shell)
  ;; Available state keys
  (mapcar #'car agent-shell--state)
  ;; => (:agent-config :buffer :client :request-count :pending-requests ...)
  
  ;; Check request count
  (alist-get :request-count agent-shell--state)
  
  ;; Check if authenticated
  (alist-get :authenticated agent-shell--state))
```

## Error Handling

Errors return with `isError: true`. To handle gracefully in Elisp:

```elisp
(condition-case err
    (potentially-failing-operation)
  (error (format "Failed: %s" (error-message-string err))))
```

## Event-Driven Agent Behavior (Hooks)

Emacs's hook system enables event-driven agent behavior:

```elisp
;; OBSERVE user actions
(add-hook 'after-save-hook #'agent-on-file-saved)
(add-hook 'compilation-finish-functions #'agent-on-compile-done)
(add-hook 'flymake-diagnostic-functions #'agent-on-diagnostics)
(add-hook 'buffer-list-update-hook #'agent-on-focus-change)

;; INTERVENE at key moments  
(add-hook 'before-save-hook #'agent-maybe-format)
(add-hook 'find-file-hook #'agent-setup-buffer)

;; ADVICE any function non-invasively
(advice-add 'compile :before #'agent-log-compile-command)
(advice-add 'save-buffer :after #'agent-notify-save)
```

This enables proactive assistance without polling - the agent becomes an event-driven observer that reacts to user actions in real-time.

## Key Insight: Dynamic Modification

Unlike static languages, Elisp lets agents modify behavior at runtime:

```elisp
;; Add logging to ANY function, instantly, no rebuild
(advice-add 'some-function :before 
  (lambda (&rest args) (message "Called with: %S" args)))

;; Remove it just as easily
(advice-remove 'some-function #'my-advice-fn)
```

This is the core advantage over TypeScript/VS Code extensions - no compilation, no packaging, no restart. The agent can experiment and iterate in real-time.

## Repository Structure

This is a **literate Emacs configuration** using Org-Babel. Assumes Emacs 30+ as baseline.

### Configuration Hierarchy

All modules are loaded at startup via `org-babel-load-file`:

```
init.org (2,288 lines) - MAIN ENTRY POINT
├── emacs24.helm.org - Helm completion
├── emacs24.smartparens.org - Structural editing
├── emacs24.hacky.org - Misc utilities
├── emacs24.python.org - Python dev
├── emacs24.eshell.org - Shell with Git prompt
├── emacs24.ess.org - R/statistics
├── emacs24.elisp.org - Elisp dev
├── emacs24.js2.org - JavaScript
├── emacs24.sql.org - SQL (5 formatters, sqlfluff preferred)
├── emacs24.scheme.org - Scheme
├── emacs29.llm.org - LLM/AI integration
└── private.org - API keys (external, not in repo)
```

Note: "emacs24" naming is historical, not version-specific.

### Key Sections in init.org

| Lines | Purpose |
|-------|---------|
| 1-150 | Core setup: GC, keybindings, platform detection, straight.el |
| 150-450 | Org mode configuration |
| 374-450 | External module loading |
| 450-2100 | Language modes, UI, navigation |
| 2100+ | Themes, finalization, auto-tangle |

### Runtime Data (do not commit)

- `bookmarks` - Emacs bookmark locations
- `keyfreq` - Key frequency statistics
- `prompts/` - LLM prompt templates
- `snippets/` - Yasnippet templates
- `elpa/`, `straight/repos/` - Package caches
- `eln-cache/` - Native compilation cache

### Package Management

Uses `straight.el` with `use-package` for declarative configuration. ~116 packages configured.

### Known Issues (documented for cleanup)

- **emacs24.eshell.org**: Git status runs shell commands on every keystroke (performance)
- **emacs24.hacky.org**: `date2unix` defined twice; legacy keyboard macros
- **emacs24.scheme.org**: xscheme is ancient/unmaintained
- **emacs24.js2.org**: js2-mode superseded by js-ts-mode
