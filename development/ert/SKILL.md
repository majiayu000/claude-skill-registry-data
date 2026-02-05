---
name: ert
description: A guide to using ERT (Emacs Lisp Regression Testing) for testing Emacs Lisp code.
---

# ERT: Emacs Lisp Regression Testing

ERT is Emacs's built-in testing framework for automated testing of Emacs Lisp code. It provides facilities for defining tests, running them interactively or in batch mode, and debugging failures with integrated tooling.

## Overview

ERT (Emacs Lisp Regression Testing) is included with Emacs and requires no additional installation. It leverages Emacs's dynamic and interactive nature to provide powerful testing capabilities for unit tests, integration tests, and regression prevention.

**Key Characteristics:**
- Built into Emacs (available in Emacs 24+)
- Interactive debugging with backtrace inspection
- Flexible test selection and organization
- Batch mode for CI/CD integration
- Dynamic binding for easy mocking
- No external dependencies

## Core Concepts

### Test Definition

Tests are defined using `ert-deftest`, which creates a named test function:

```elisp
(ert-deftest test-name ()
  "Docstring describing what the test verifies."
  (should (= 2 (+ 1 1))))
```

### Assertions (Should Forms)

ERT provides three assertion macros:

- `should` - Assert that a form evaluates to non-nil
- `should-not` - Assert that a form evaluates to nil
- `should-error` - Assert that a form signals an error

Unlike `cl-assert`, these macros provide detailed error reporting including the form, evaluated subexpressions, and resulting values.

### Test Selectors

Selectors specify which tests to run:

- `t` - All tests
- `"regex"` - Tests matching regular expression
- `:tag symbol` - Tests tagged with symbol
- `:failed` - Tests that failed in last run
- `:passed` - Tests that passed in last run
- Combinations using `(and ...)`, `(or ...)`, `(not ...)`

## API Reference

### Defining Tests

#### `ert-deftest`
```elisp
(ert-deftest NAME () [DOCSTRING] [:tags (TAG...)] BODY...)
```

Define a test named NAME.

**Parameters:**
- `NAME` - Symbol naming the test
- `DOCSTRING` - Optional description of what the test verifies
- `:tags` - Optional list of tags for test organization
- `BODY` - Test code containing assertions

**Example:**
```elisp
(ert-deftest test-addition ()
  "Test basic arithmetic addition."
  :tags '(arithmetic quick)
  (should (= 4 (+ 2 2)))
  (should (= 0 (+ -1 1))))
```

### Assertion Macros

#### `should`
```elisp
(should FORM)
```

Assert that FORM evaluates to non-nil. On failure, displays the form and all evaluated subexpressions.

**Example:**
```elisp
(should (string-match "foo" "foobar"))
(should (< 1 2))
(should (member 'x '(x y z)))
```

#### `should-not`
```elisp
(should-not FORM)
```

Assert that FORM evaluates to nil.

**Example:**
```elisp
(should-not (string-match "baz" "foobar"))
(should-not (> 1 2))
```

#### `should-error`
```elisp
(should-error FORM [:type TYPE])
```

Assert that FORM signals an error. Optional `:type` specifies the expected error type.

**Example:**
```elisp
;; Any error accepted
(should-error (/ 1 0))

;; Specific error type required
(should-error (/ 1 0) :type 'arith-error)

;; Wrong error type would fail
(should-error (error "message") :type 'arith-error)  ; fails
```

### Running Tests Interactively

#### `ert` / `ert-run-tests-interactively`
```elisp
M-x ert RET SELECTOR RET
```

Run tests matching SELECTOR and display results in interactive buffer.

**Common selectors:**
- `t` - Run all tests
- `"^my-package-"` - Tests matching regex
- `:failed` - Re-run failed tests

**Interactive debugging commands:**
- `.` - Jump to test definition
- `d` - Re-run test with debugger enabled
- `b` - Show backtrace of failed test
- `r` - Re-run test at point
- `R` - Re-run all tests
- `l` - Show executed `should` forms
- `m` - Show messages from test
- `TAB` - Expand/collapse test details

### Running Tests in Batch Mode

#### `ert-run-tests-batch-and-exit`
```elisp
(ert-run-tests-batch-and-exit [SELECTOR])
```

Run tests in batch mode and exit with status code (0 for success, non-zero for failure).

**Command line usage:**
```bash
# Run all tests
emacs -batch -l ert -l my-tests.el -f ert-run-tests-batch-and-exit

# Run specific tests
emacs -batch -l ert -l my-tests.el \
  --eval '(ert-run-tests-batch-and-exit "^test-feature-")'

# Quiet mode (only unexpected results)
emacs -batch -l ert -l my-tests.el \
  --eval '(let ((ert-quiet t)) (ert-run-tests-batch-and-exit))'
```

#### `ert-run-tests-batch`
```elisp
(ert-run-tests-batch [SELECTOR])
```

Run tests in batch mode but do not exit. Useful when running tests is part of a larger batch script.

### Test Organization

#### Tags

Use `:tags` in `ert-deftest` to organize tests:

```elisp
(ert-deftest test-fast-operation ()
  :tags '(quick unit)
  (should (fast-function)))

(ert-deftest test-slow-integration ()
  :tags '(slow integration)
  (should (slow-integration-test)))
```

Run tagged tests:
```elisp
;; Run only quick tests
M-x ert RET :tag quick RET

;; Run integration tests
M-x ert RET :tag integration RET
```

#### Test Naming Conventions

Prefix test names with the package name:

```elisp
(ert-deftest my-package-test-feature ()
  "Test feature implementation."
  ...)

(ert-deftest my-package-test-edge-case ()
  "Test handling of edge case."
  ...)
```

This enables:
- Running all package tests: `M-x ert RET "^my-package-" RET`
- Clear test ownership and organization
- Avoiding name collisions

### Skipping Tests

#### `skip-unless`
```elisp
(skip-unless CONDITION)
```

Skip test if CONDITION is nil.

**Example:**
```elisp
(ert-deftest test-graphical-feature ()
  "Test feature requiring graphical display."
  (skip-unless (display-graphic-p))
  (should (graphical-operation)))
```

#### `skip-when`
```elisp
(skip-when CONDITION)
```

Skip test if CONDITION is non-nil.

**Example:**
```elisp
(ert-deftest test-unix-specific ()
  "Test Unix-specific functionality."
  (skip-when (eq system-type 'windows-nt))
  (should (unix-specific-function)))
```

### Programmatic Test Execution

#### `ert-run-tests`
```elisp
(ert-run-tests SELECTOR LISTENER)
```

Run tests matching SELECTOR, reporting results to LISTENER.

**Example:**
```elisp
;; Run all tests silently
(ert-run-tests t #'ert-quiet-listener)

;; Custom listener
(defun my-listener (event-type &rest data)
  (pcase event-type
    ('test-started ...)
    ('test-passed ...)
    ('test-failed ...)
    ('run-ended ...)))

(ert-run-tests "^my-" #'my-listener)
```

## Best Practices

### Test Structure

**1. Use descriptive test names:**

```elisp
;; Good
(ert-deftest my-package-parse-valid-json ()
  ...)

;; Poor
(ert-deftest test1 ()
  ...)
```

**2. Include clear docstrings:**

```elisp
(ert-deftest my-package-handle-empty-input ()
  "Verify that empty input returns nil without error."
  (should-not (my-package-process "")))
```

**3. One logical assertion per test:**

```elisp
;; Good - focused test
(ert-deftest my-package-parse-returns-alist ()
  "Parser returns result as alist."
  (should (listp (my-package-parse "data")))
  (should (eq 'cons (type-of (car (my-package-parse "data"))))))

;; Better - even more focused
(ert-deftest my-package-parse-returns-list ()
  "Parser returns a list."
  (should (listp (my-package-parse "data"))))

(ert-deftest my-package-parse-list-contains-alist-entries ()
  "Parser list contains alist entries."
  (should (eq 'cons (type-of (car (my-package-parse "data"))))))
```

### Test Environment

**1. Isolate tests from environment:**

```elisp
(ert-deftest my-package-test-configuration ()
  "Test respects custom configuration."
  ;; Save and restore configuration
  (let ((my-package-option 'custom-value))
    (should (eq 'custom-value (my-package-get-option)))))
```

**2. Use temporary buffers:**

```elisp
(ert-deftest my-package-buffer-manipulation ()
  "Test buffer manipulation functions."
  (with-temp-buffer
    (insert "test content")
    (my-package-process-buffer)
    (should (string= (buffer-string) "processed content"))))
```

**3. Clean up with `unwind-protect`:**

```elisp
(ert-deftest my-package-file-operation ()
  "Test file operations with cleanup."
  (let ((temp-file (make-temp-file "my-package-test-")))
    (unwind-protect
        (progn
          (my-package-write-file temp-file "data")
          (should (file-exists-p temp-file))
          (should (string= "data" (my-package-read-file temp-file))))
      ;; Cleanup always runs
      (when (file-exists-p temp-file)
        (delete-file temp-file)))))
```

### Fixtures with Higher-Order Functions

Instead of traditional fixture systems, use Lisp functions:

```elisp
(defun my-package-with-test-environment (body)
  "Execute BODY within test environment."
  (let ((my-package-test-mode t)
        (original-config (my-package-get-config)))
    (unwind-protect
        (progn
          (my-package-set-config 'test-config)
          (funcall body))
      (my-package-set-config original-config))))

(ert-deftest my-package-test-feature ()
  "Test feature in test environment."
  (my-package-with-test-environment
   (lambda ()
     (should (my-package-feature-works)))))
```

### Mocking with Dynamic Binding

Use `cl-letf` to override functions temporarily:

```elisp
(ert-deftest my-package-test-without-side-effects ()
  "Test function without filesystem access."
  (cl-letf (((symbol-function 'file-exists-p)
             (lambda (file) t))
            ((symbol-function 'insert-file-contents)
             (lambda (file) (insert "mock content"))))
    (should (my-package-load-config "config.el"))))
```

Traditional `flet` can also be used:

```elisp
(require 'cl)

(ert-deftest my-package-test-mocked ()
  "Test with mocked dependencies."
  (flet ((external-api-call (arg) "mocked response"))
    (should (string= "mocked response"
                     (my-package-use-api "data")))))
```

### Handling Preconditions

**Skip tests when preconditions aren't met:**

```elisp
(ert-deftest my-package-test-requires-feature ()
  "Test functionality requiring optional feature."
  (skip-unless (featurep 'some-feature))
  (should (my-package-use-feature)))

(ert-deftest my-package-test-requires-external-tool ()
  "Test requiring external program."
  (skip-unless (executable-find "tool"))
  (should (my-package-call-tool)))
```

### Testing for Side Effects

**1. Test buffer modifications:**

```elisp
(ert-deftest my-package-insert-text ()
  "Verify text insertion."
  (with-temp-buffer
    (my-package-insert-greeting)
    (should (string= (buffer-string) "Hello, World!\n"))
    (should (= (point) (point-max)))))
```

**2. Test variable changes:**

```elisp
(ert-deftest my-package-increment-counter ()
  "Counter increments correctly."
  (let ((my-package-counter 0))
    (my-package-increment)
    (should (= my-package-counter 1))
    (my-package-increment)
    (should (= my-package-counter 2))))
```

**3. Test message output:**

```elisp
(ert-deftest my-package-logs-message ()
  "Function logs expected message."
  (let ((logged-messages))
    (cl-letf (((symbol-function 'message)
               (lambda (fmt &rest args)
                 (push (apply #'format fmt args) logged-messages))))
      (my-package-operation)
      (should (member "Operation completed" logged-messages)))))
```

### Error Handling

**1. Test error conditions:**

```elisp
(ert-deftest my-package-invalid-input-signals-error ()
  "Invalid input signals appropriate error."
  (should-error (my-package-parse nil) :type 'wrong-type-argument)
  (should-error (my-package-parse "") :type 'user-error))
```

**2. Test error recovery:**

```elisp
(ert-deftest my-package-recovers-from-error ()
  "Function recovers gracefully from error condition."
  (let ((result (my-package-safe-operation 'invalid-input)))
    (should (eq result 'fallback-value))
    (should (my-package-error-logged-p))))
```

### Testing Asynchronous Code

**Use timers and `accept-process-output`:**

```elisp
(ert-deftest my-package-async-operation ()
  "Test asynchronous operation completion."
  (let ((callback-called nil)
        (callback-result nil))
    (my-package-async-call
     (lambda (result)
       (setq callback-called t
             callback-result result)))
    ;; Wait for async operation
    (with-timeout (5 (error "Async operation timeout"))
      (while (not callback-called)
        (accept-process-output nil 0.1)))
    (should callback-called)
    (should (string= "expected" callback-result))))
```

### Debugging Failed Tests

**1. Use detailed assertions:**

```elisp
;; Less helpful
(should (my-package-valid-p data))

;; More helpful
(should (listp data))
(should (= 3 (length data)))
(should (stringp (car data)))
```

**2. Add messages for context:**

```elisp
(ert-deftest my-package-complex-test ()
  "Test complex operation."
  (let ((data (my-package-prepare-data)))
    (message "Prepared data: %S" data)
    (should (my-package-valid-p data))
    (let ((result (my-package-process data)))
      (message "Processing result: %S" result)
      (should (my-package-expected-result-p result)))))
```

**3. Break complex tests into steps:**

```elisp
(ert-deftest my-package-pipeline ()
  "Test processing pipeline."
  (let* ((input "raw data")
         (parsed (progn
                   (should (stringp input))
                   (my-package-parse input)))
         (validated (progn
                      (should (listp parsed))
                      (my-package-validate parsed)))
         (processed (progn
                      (should validated)
                      (my-package-process validated))))
    (should (my-package-expected-output-p processed))))
```

## Common Patterns

### Testing Mode Definitions

```elisp
(ert-deftest my-mode-initialization ()
  "Major mode initializes correctly."
  (with-temp-buffer
    (my-mode)
    (should (eq major-mode 'my-mode))
    (should (local-variable-p 'my-mode-variable))
    (should (keymapp my-mode-map))))

(ert-deftest my-mode-font-lock ()
  "Font lock keywords defined correctly."
  (with-temp-buffer
    (my-mode)
    (insert "keyword other-keyword")
    (font-lock-ensure)
    (should (eq (get-text-property 1 'face) 'my-mode-keyword-face))))
```

### Testing Interactive Commands

```elisp
(ert-deftest my-package-interactive-command ()
  "Interactive command behaves correctly."
  (with-temp-buffer
    (insert "initial text")
    (goto-char (point-min))
    ;; Simulate command execution
    (call-interactively 'my-package-command)
    (should (string= (buffer-string) "modified text"))
    (should (= (point) 14))))
```

### Testing with Mock Data

```elisp
(ert-deftest my-package-parse-json ()
  "JSON parsing produces expected structure."
  (let ((json-data "{\"name\": \"test\", \"value\": 42}"))
    (cl-letf (((symbol-function 'url-retrieve-synchronously)
               (lambda (url)
                 (with-temp-buffer
                   (insert json-data)
                   (current-buffer)))))
      (let ((result (my-package-fetch-data "https://api.example.com")))
        (should (string= "test" (alist-get 'name result)))
        (should (= 42 (alist-get 'value result)))))))
```

### Testing Regular Expressions

```elisp
(ert-deftest my-package-regex-matches ()
  "Regular expression matches expected patterns."
  (let ((re (my-package-build-regex)))
    ;; Positive cases
    (should (string-match re "valid-input-123"))
    (should (string-match re "another_valid_case"))
    ;; Negative cases
    (should-not (string-match re "invalid input"))
    (should-not (string-match re "123-invalid"))))
```

### Testing Hooks

```elisp
(ert-deftest my-package-hook-executes ()
  "Hook functions execute in correct order."
  (let ((execution-order nil))
    (unwind-protect
        (progn
          (add-hook 'my-package-hook
                    (lambda () (push 'first execution-order)))
          (add-hook 'my-package-hook
                    (lambda () (push 'second execution-order)))
          (run-hooks 'my-package-hook)
          (should (equal '(second first) execution-order)))
      (setq my-package-hook nil))))
```

## Performance Considerations

### Keep Tests Fast

```elisp
;; Tag slow tests
(ert-deftest my-package-slow-integration-test ()
  :tags '(slow integration)
  ...)

;; Run only fast tests during development
M-x ert RET (not :tag slow) RET

;; Mock slow operations
(ert-deftest my-package-test-with-mock ()
  (cl-letf (((symbol-function 'slow-network-call)
             (lambda () "instant mock result")))
    (should (my-package-feature))))
```

### Avoid Redundant Setup

```elisp
;; Inefficient - recreates data in each test
(ert-deftest test-1 ()
  (let ((data (expensive-data-creation)))
    (should (test-aspect-1 data))))

(ert-deftest test-2 ()
  (let ((data (expensive-data-creation)))
    (should (test-aspect-2 data))))

;; Better - use fixture function
(defun with-test-data (body)
  (let ((data (expensive-data-creation)))
    (funcall body data)))

(ert-deftest test-1 ()
  (with-test-data
   (lambda (data)
     (should (test-aspect-1 data)))))

(ert-deftest test-2 ()
  (with-test-data
   (lambda (data)
     (should (test-aspect-2 data)))))
```

## Integration with Development Workflow

### Key Bindings for Quick Testing

```elisp
;; In your init.el
(global-set-key (kbd "C-c t") #'ert)

;; Run tests for current package
(defun my/ert-run-package-tests ()
  "Run all tests for current package."
  (interactive)
  (let ((prefix (file-name-base (buffer-file-name))))
    (ert (concat "^" prefix "-"))))

(global-set-key (kbd "C-c C-t") #'my/ert-run-package-tests)
```

### File Organization

```
my-package/
├── my-package.el          ; Main package code
├── my-package-utils.el    ; Utility functions
└── test/
    ├── my-package-test.el       ; Tests for main package
    └── my-package-utils-test.el ; Tests for utilities
```

### Test File Template

```elisp
;;; my-package-test.el --- Tests for my-package -*- lexical-binding: t -*-

;;; Commentary:
;; Test suite for my-package functionality.

;;; Code:

(require 'ert)
(require 'my-package)

(ert-deftest my-package-test-basic ()
  "Test basic functionality."
  (should (my-package-function)))

(provide 'my-package-test)
;;; my-package-test.el ends here
```

### Makefile Integration

```makefile
.PHONY: test
test:
	emacs -batch -l ert \
	  -l my-package.el \
	  -l test/my-package-test.el \
	  -f ert-run-tests-batch-and-exit

.PHONY: test-interactive
test-interactive:
	emacs -l my-package.el \
	  -l test/my-package-test.el \
	  --eval "(ert t)"
```

### CI/CD Integration

```yaml
# .github/workflows/test.yml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        emacs-version: ['27.2', '28.2', '29.1']
    steps:
      - uses: actions/checkout@v2
      - uses: purcell/setup-emacs@master
        with:
          version: ${{ matrix.emacs-version }}
      - name: Run tests
        run: |
          emacs -batch -l ert \
            -l my-package.el \
            -l test/my-package-test.el \
            -f ert-run-tests-batch-and-exit
```

## Common Pitfalls

### 1. Tests Depend on External State

```elisp
;; Bad - depends on file system
(ert-deftest bad-test ()
  (should (file-exists-p "~/.emacs")))

;; Good - controls environment
(ert-deftest good-test ()
  (let ((temp-file (make-temp-file "test-")))
    (unwind-protect
        (should (file-exists-p temp-file))
      (delete-file temp-file))))
```

### 2. Tests Interfere with Each Other

```elisp
;; Bad - modifies global state
(defvar my-package-state nil)

(ert-deftest bad-test-1 ()
  (setq my-package-state 'value1)
  (should (eq my-package-state 'value1)))

(ert-deftest bad-test-2 ()
  ;; May fail if bad-test-1 ran first
  (should-not my-package-state))

;; Good - isolates state
(ert-deftest good-test-1 ()
  (let ((my-package-state 'value1))
    (should (eq my-package-state 'value1))))

(ert-deftest good-test-2 ()
  (let ((my-package-state nil))
    (should-not my-package-state)))
```

### 3. Overly Broad Assertions

```elisp
;; Bad - unclear what failed
(ert-deftest bad-test ()
  (should (and (condition-1)
               (condition-2)
               (condition-3))))

;; Good - each assertion is explicit
(ert-deftest good-test ()
  (should (condition-1))
  (should (condition-2))
  (should (condition-3)))
```

### 4. Missing Cleanup

```elisp
;; Bad - leaves processes running
(ert-deftest bad-test ()
  (let ((proc (start-process "test" nil "sleep" "10")))
    (should (process-live-p proc))))
;; Process keeps running after test

;; Good - ensures cleanup
(ert-deftest good-test ()
  (let ((proc (start-process "test" nil "sleep" "10")))
    (unwind-protect
        (should (process-live-p proc))
      (when (process-live-p proc)
        (kill-process proc)))))
```

### 5. Not Testing Error Cases

```elisp
;; Incomplete - only tests success path
(ert-deftest incomplete-test ()
  (should (= 5 (my-package-divide 10 2))))

;; Complete - tests both success and failure
(ert-deftest complete-test ()
  (should (= 5 (my-package-divide 10 2)))
  (should-error (my-package-divide 10 0) :type 'arith-error))
```

## Advanced Topics

### Custom Should Forms

Create domain-specific assertions:

```elisp
(defun should-match-regex (string regex)
  "Assert that STRING matches REGEX."
  (declare (indent 1))
  (should (string-match regex string)))

(ert-deftest test-with-custom-should ()
  (should-match-regex "foobar" "^foo"))
```

### Test Statistics

```elisp
(defun my-package-test-stats ()
  "Display statistics about test suite."
  (interactive)
  (let* ((all-tests (ert-select-tests t t))
         (total (length all-tests))
         (tagged (length (ert-select-tests '(tag slow) t)))
         (quick (- total tagged)))
    (message "Total: %d, Quick: %d, Slow: %d" total quick tagged)))
```

### Running Specific Test Programmatically

```elisp
;; Run single test
(ert-run-tests 'my-package-specific-test #'ert-quiet-listener)

;; Run tests matching pattern
(ert-run-tests "^my-package-feature-" #'ert-batch-listener)

;; Run tests with custom listener
(defvar my-test-results nil)

(defun my-test-listener (event-type &rest args)
  (pcase event-type
    ('test-started (push (car args) my-test-results))
    ('test-ended (message "Finished: %s" (car args)))))

(ert-run-tests t #'my-test-listener)
```

## Resources

- **Official Manual:** https://www.gnu.org/software/emacs/manual/html_mono/ert.html
- **Info in Emacs:** `C-h i m ert RET`
- **Source Code:** `lisp/emacs-lisp/ert.el` in Emacs repository
- **ERT Reference Card:** https://github.com/fniessen/refcard-ERT

## Summary

ERT provides a comprehensive testing framework fully integrated with Emacs:

1. Define tests with `ert-deftest` and assertions with `should` forms
2. Run tests interactively for rapid development feedback
3. Use batch mode for automated testing in CI/CD
4. Leverage dynamic binding for easy mocking
5. Debug failures interactively with integrated tooling
6. Organize tests with tags and selectors
7. Follow best practices: isolation, cleanup, clear assertions
8. Keep tests fast and focused for quick feedback cycles

ERT's integration with Emacs's interactive environment makes it uniquely powerful for developing and debugging Emacs Lisp code.
