---
name: solve-puzzle
description: Use this to solve the Advent of Code daily puzzles.
---

# Solving the Daily Puzzle

The following steps will guide you through solving the daily Advent of Code
puzzles. You must follow each and every step exactly to ensure a successful
completion. If you miss any step, you will fail the task. It is crucial to
succeed, so pay close attention to the instructions and follow them exactly.

**Create to-do items for each step below. Failure to follow these steps
exactly means you fail the task**:

- Ensure you are on a git branch for that specific day (e.g., `day05` for day
  5). Create it if necessary.
- Create the directory for that day's puzzle if it doesn't already exist,
  following the naming convention `dayXX` where `XX` is the zero-padded day
  number (e.g., `day05` for day 5).
- Inside that directory, create an empty file named `puzzle-partY.txt` where
  `Y` is the part number (1 or 2). Ask the user to provide the puzzle
  description by either providing it to you or pasting it directly into the
  file.
- Create another file named `input.txt` in the same directory and populate it
  with the provided input data in the same manner as above. Note that this
  file remains the same for both parts of the puzzle, so if it already exists,
  do not overwrite it.
- Commit these new files to a new branch named `dayXX` in preparation for
  solving the puzzle.
- Implement the solution code for the specified part of the puzzle in a file
  named `partY.py` within the same directory. There are sometimes choices of
  different algorithms to use. Choose one with algorithmic efficiency that is
  suitable for the problem constraints. Choosing a poor algorithm may lead to
  long runtimes or excessive memory usage. Make sure you consider the time and
  space complexity of your solution and monitor for performance issues.
- Use the examples from the puzzle description to create test cases in a file
  named `test_partY.py` to validate the solution.
- Write a README.md file documenting the approach, challenges, and
  explanations for the solution. This should include the algoriths used and
  any optimizations made.
- Commit the solution code and tests to the same branch.
- Run all tests to ensure correctness.
- Run the solution code with the main input data to obtain the final answer.

Once you think you have completed all the steps, use
superpowers:verification-before-completion to verify that you have finished
the task.
