---
name: codecleanup
description: This should only be done if the user asks to "clean up code". At the end of a major change on a git branch this document describes the code clean up tasks that should be performed.
---

# Code Clean Up Guide

##  Overview
This document covers the type of work that should be performed when doing final code cleanup for a change.
This work should not be performed unless the user explicitly asks for a "code clean up" step at the end of a coding
session.

## Preparation
* Start by running `git diff` to see what changes were introduced
* Focus cleanup only on files/lines that appear in the diff

### General Rules
* Do not modify any code that wasn't introduced by the unstaged changes.
* Try to match existing styles you see in the code near the change that was introduced.
* Do not alter the behavior of the existing code
* Don't worry about markdown files.
* Refactorings should leave the code in an easier to understand and more maintainable state.
* You should use short and meaningful code comments.

### Comments

* Review all existing comments. Remove any comments that could be obvious based on a quick glance at the related code.
* Add comments for complex code blocks. 
* Add JSDoc, JavaDoc, or the doc format that is applicable for the given programming language. Only document public methods / functions
* Keep the comments short and to the point. Do not use emoji in comments. 

## Checklist
Work through these systematically:
- [ ] Review and update comments
- [ ] Format code to match project style
- [ ] Review variable naming
- [ ] Apply small refactorings
- [ ] Run linters/tests (with user approval)

### Code Clean up
* Review the overall formatting of the code and adjust it to match common accepted patterns or patterns found in the codebase.
* Review the naming of variables introduced or changed and update if needed for clarity.
* Try not to modify code which wasn't introduced by the unstaged changes

### Refactoring
* Small refactorings for code clarity
* Make sure refactoring optimizes for maintenance without introducing major changes
* If you see an opportunity for larger refactorings that will make things easier to understand or maintain propose a plan or design to the user and let them choose if you should do the work or not. 

### Project Automation
Once all tasks above are complete check the project setup and see if there are linting, compile, or test runners that should be executed. If you find any ask the user if you should execute them. Each project is different and we might not want to always execute these tasks but you should ask the user if you do find the tasks in the project.

## Completion Criteria
- All comments are clear and non-obvious
- Code follows project style conventions
- No linting errors (if linter was run)
- All tests pass (if tests were run) 
