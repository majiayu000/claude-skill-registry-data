---
name: literate-programming
description: "CRITICAL: ALWAYS activate this skill BEFORE making ANY changes to .nw files. Use proactively when: (1) creating, editing, reviewing, or improving any .nw file, (2) planning to add/modify functionality in files with .nw extension, (3) user asks about literate quality, (4) user mentions noweb, literate programming, tangling, or weaving, (5) working in directories containing .nw files, (6) creating new modules/files that will be .nw format. Trigger phrases: 'create module', 'add feature', 'update', 'modify', 'fix' + any .nw file. Never edit .nw files directly without first activating this skill to ensure literate programming principles are applied. (project, gitignored)"
---

# Literate Programming Skill

**CRITICAL: This skill MUST be activated BEFORE making any changes to .nw files!**

You are an expert in literate programming using the noweb system. Apply these principles when writing or analyzing literate programs.

## WHEN TO USE THIS SKILL (Read This First!)

### ✅ CORRECT Workflow

**ALWAYS activate this skill FIRST when:**
1. Creating a new .nw file
2. Editing an existing .nw file
3. Reviewing any .nw file
4. User asks to modify anything in a .nw file
5. You notice a file has a .nw extension

**The correct order is:**
```
1. User asks to modify a .nw file
2. YOU ACTIVATE THIS SKILL IMMEDIATELY
3. You plan the changes with literate programming principles
4. You make the changes following the principles
5. You regenerate code with make/notangle
```

### ❌ INCORRECT Workflow (Anti-pattern)

**NEVER do this:**
```
1. User asks to modify a .nw file
2. You directly edit the .nw file
3. User asks you to review literate quality
4. You activate skill and find problems
5. You have to redo everything
```

### Examples of When to Activate

✅ "Can you fix the -M and -a options in assignments.nw?"
   → ACTIVATE SKILL IMMEDIATELY, then plan changes

✅ "Add a new feature to modules.nw"
   → ACTIVATE SKILL IMMEDIATELY, then design feature

✅ "I'm getting an error in the code generated from grades.nw"
   → ACTIVATE SKILL IMMEDIATELY to review before fixing

✅ Any task involving a .nw file
   → ACTIVATE SKILL IMMEDIATELY

### Remember

- .nw files are NOT regular source code files
- They are literate programs combining documentation and code
- Literate quality is AS IMPORTANT as code correctness
- Bad literate quality = failed task, even if code works
- ALWAYS think: "Is this a .nw file? Then activate skill FIRST!"

## Planning Changes to Literate Programs

**When you activate this skill to make changes to a .nw file, follow this process:**

1. **Read the existing .nw file** to understand the current structure and narrative
2. **Plan the changes with literate programming in mind:**
   - What is the "why" behind this change? (Explain in documentation)
   - How does this fit into the existing narrative?
   - Should I use contrast to explain the change? (old vs new approach)
   - What new chunks are needed? What are their meaningful names?
   - Where in the pedagogical order should this be explained?
3. **Design the documentation BEFORE writing code:**
   - Write prose explaining the problem and solution
   - Use subsections to structure complex explanations
   - Provide examples showing the new behavior
   - Explain design decisions and trade-offs
4. **Decompose code into well-named chunks:**
   - Each chunk = one coherent concept
   - Names describe purpose (like pseudocode), not syntax
   - Use the web structure effectively
5. **Write the code chunks referenced in documentation**
6. **Regenerate and test**

**Key principle:** If you find yourself writing code comments to explain logic, that explanation belongs in the TeX/documentation chunks instead!

## Reviewing Existing Literate Programs

When asked to review, improve, or analyze the literate quality of a .nw file, evaluate these aspects:

1. **Narrative flow**: Does the document tell a coherent story? Is the order pedagogical rather than compiler-dictated?
2. **Variation theory application**: Are contrasts used to highlight key concepts? Is the "whole, then parts, then back together" structure followed?
3. **Chunk quality**:
   - Are chunk names meaningful (describing purpose, not syntax)?
   - Are chunks appropriately sized (focused on single concepts)?
   - Is the web structure used effectively (defining chunks out of order when helpful)?
4. **Explanation quality**:
   - Does documentation explain "why" not just "what"?
   - Are design decisions and trade-offs explained?
   - Is technical context provided for non-obvious choices?
5. **Test organization** (if tests are present):
   - Do tests appear AFTER the functionality they verify?
   - Are tests distributed throughout the file, not all grouped at the beginning?
   - Is there pedagogical framing introducing each test section?
   - Are tests within ~10 lines of their implementation?
6. **Proper noweb syntax**:
   - Are code references using `[[code]]` notation?
   - Are chunk definitions properly formatted?
   - Would `noroots` find any unused chunks?

After analysis, provide specific, actionable improvements with rationale based on literate programming principles.

## Core Philosophy

Literate programming, as introduced by Donald Knuth, has two fundamental goals:

1. **Explaining to human beings what we want a computer to do** - Focus on human readers rather than compilers
2. **Striving for a program that is comprehensible because its concepts have been introduced in an order that is best for human understanding** - Write in psychological order, not computer-required order

We want to explain the "why" behind the code, not just the "how".

### Variation Theory in Literate Programming

**Apply the `variation-theory` skill** when structuring explanations in documentation chunks. Variation theory provides the pedagogical foundation for effective literate programs.

**The four patterns and how they apply:**

1. **Contrast** - Show what something IS vs what it is NOT
   - Compare two approaches to the same problem before choosing one
   - Show an anti-pattern alongside the correct pattern
   - Example: "We could use a list, but a dictionary provides O(1) lookup..."

2. **Separation** - Break the whole into parts, examine each independently
   - Start with the complete module structure, then explain each chunk
   - Show the high-level algorithm, then detail each step
   - Example: Module outline first, then individual functions

3. **Generalization** - Show the same pattern across different contexts
   - Demonstrate a pattern in multiple code chunks
   - Show how the same design decision applies throughout
   - Example: "This error handling pattern appears in all API calls..."

4. **Fusion** - Integrate parts back into a coherent whole
   - After explaining parts, show how they work together
   - Provide a summary that ties concepts together
   - Example: "With all pieces in place, the complete flow is..."

**Key principle for literate programs**: Start with the whole (module outline), separate into parts (individual chunks with explanations), and fuse back together (how chunks combine to form the complete program).

**CRITICAL - Examples before generalizations**: When explaining patterns or principles, show concrete code examples FIRST, then state the general principle. Readers cannot discern a pattern without first experiencing variation. See the `variation-theory` skill for detailed guidance on this common violation.

## Noweb File Format

A noweb file (`.nw`) consists of two types of chunks:

### Documentation Chunks
- Begin with a line starting with `@` followed by a space or newline
- Contain explanatory text in the documentation language (LaTeX, Markdown, etc.)
- Have no names
- Are copied verbatim by noweave

### Code Chunks
- Begin with `<<chunk name>>=` on a line by itself (must start in column 1)
- End when another chunk begins or at end of file
- Can reference other code chunks using `<<chunk name>>`
- Multiple chunks with the same name are concatenated

### Syntax Rules
- Quote code in documentation using `[[code]]`, this escapes special characters 
  properly---so we don't need to escape underscores with `\_` in LaTeX, for 
  example.
- Escape special characters: `@<<` for literal `<<`, `@@` in column 1 for literal `@`
- Code chunks can reference other chunks, forming a "web" of code

## Writing Literate Programs

When writing literate programs:

1. **Start with the human story** - Explain the problem, approach, and design 
   decisions first, in terms of variation theory: the whole.
2. **Introduce concepts in pedagogical order** - Present ideas when they're easiest to understand, not when the compiler needs them
3. **Use meaningful chunk names** - Names should describe what the code does, 
   not its syntactic role, like pseudocode. They should be a 2--5 word summary 
   of the chunk's purpose.
4. **Decompose by concept, not syntax** - Break code into chunks based on logical units of thought
5. **Explain the "why"** - Don't just describe what the code does (that's visible), explain why you chose this approach
6. **Keep chunks focused** - Each chunk should represent a single, coherent idea
7. **Use the web structure** - Don't be afraid to define chunks out of order or
   to reuse chunks. However, use helper functions, don't replace those with
   chunks. We still want to do structured programming.
8. **Define constants for magic numbers** - Never use hardcoded numeric or
   string values scattered throughout code. Define named constants at the module
   level and reference them. This makes code self-documenting and ensures values
   stay synchronized. For example, define `DEFAULT_THRESHOLD = 5` once and use
   it everywhere, rather than repeating `5` in multiple places.
9. **Distinguish constants from imports** - Constants and enums are code you define,
   not external dependencies. They belong in `<<constants>>` chunks, not `<<imports>>`.
   Use multiple `<<constants>>=` chunks throughout the file to define constants near
   their first use (pedagogical order), and they will all be concatenated together.

   Example:
   ```noweb
   <<module.py>>=
   <<imports>>
   <<constants>>
   <<functions>>
   @

   \subsection{Configuration paths}
   We define a constant for the config key...
   <<constants>>=
   CONFIG_KEY = "module.config.path"
   @

   \subsection{Filter modes}
   We define an enum for filter modes...
   <<constants>>=
   class FilterMode(Enum):
       ALL = "all"
   @
   ```

10. **Co-locate dependencies with features** - When a module has multiple independent
    features (like multiple providers, handlers, or plugins), keep each feature's
    dependencies in a dedicated chunk defined within that feature's section.
    This ensures that if a feature is removed, its dependencies go with it.

    **Anti-pattern** (all imports in one place):
    ```noweb
    <<imports>>=
    from provider_a import ClientA
    from provider_b import ClientB
    from provider_c import ClientC
    @

    [... 500 lines later, Provider C is removed but import remains ...]
    ```

    **Good pattern** (dependencies co-located with features):
    ```noweb
    <<imports>>=
    from typing import Protocol
    from common import Paper
    <<provider a imports>>
    <<provider b imports>>
    <<provider c imports>>
    @

    \chapter{Provider A}
    ...implementation...

    \section{Dependencies}
    <<provider a imports>>=
    from provider_a import ClientA
    @

    \chapter{Provider B}
    ...implementation...

    \section{Dependencies}
    <<provider b imports>>=
    from provider_b import ClientB
    @
    ```

    **Benefits:**
    - Removing a feature removes its dependencies automatically
    - Easy to see what each feature depends on
    - Avoids orphaned imports when refactoring
    - Self-documenting: dependencies are explained near their use

    This pattern mirrors the `<<functions>>=` and `<<constants>>=` patterns where
    chunks are defined throughout the file and concatenated together.

## LaTeX Documentation Quality

**IMPORTANT**: Documentation chunks in .nw files are LaTeX. Apply the `latex-writing` skill best practices.

### Most Common Anti-Patterns in .nw Files

When writing documentation chunks, watch for these mistakes:

1. **Lists with bold labels**: Use `\begin{description}` with `\item[Label]`, NOT `\begin{itemize}` with `\item \textbf{Label}:`

   **Wrong:**
   ```latex
   \begin{itemize}
   \item \textbf{Feature A}: Description of feature A
   \item \textbf{Feature B}: Description of feature B
   \end{itemize}
   ```

   **Correct:**
   ```latex
   \begin{description}
   \item[Feature A] Description of feature A
   \item[Feature B] Description of feature B
   \end{description}
   ```

2. **Code with manual escaping**: Use `[[code]]` notation, NOT `\texttt{...\_...}`

3. **Manual quotes**: Use `\enquote{...}`, NOT `"..."` or `` ``...'' ``

4. **Manual cross-references**: Use `\cref{...}`, NOT `Section~\ref{...}`

See the `latex-writing` skill for complete guidelines.

## Progressive Disclosure: Abstract Placeholder Chunks

When introducing high-level structure early in a literate program, avoid exposing implementation details before the reader has sufficient context. Instead, use **abstract placeholder chunks** that defer specifics to pedagogically appropriate sections.

### The Pattern

**Core idea:** Define a conceptual chunk name at a high level, then use chunk concatenation to build it up incrementally as you explain each piece.

**Structure:**
1. **High-level reference**: Use an abstract chunk name describing the concept (e.g., `<<options for which contracts to show>>`)
2. **Later definitions**: Define that same chunk multiple times, once for each piece, as you explain them
3. **Concatenation builds it up**: Noweb concatenates all definitions in order

### Example: Function Parameters

Consider a function with multiple filtering options:

**Anti-pattern (too much detail too early):**
```noweb
def cli_amanuens_show(user_regex,
                      <<option [[all]] to show all contracts>>,
                      <<option [[next]] to show next contract>>,
                      <<option [[prev]] to show previous contract>>):
  """Shows stored amanuensis contracts for TAs."""
  <<implementation>>
@
```

At this point in the narrative, readers see three specific options but don't yet know:
- What contract filtering means
- Why these particular options exist
- How they interact with each other

**Good pattern (progressive disclosure with concatenation):**
```noweb
def cli_amanuens_show(user_regex,
                      <<options for which contracts to show>>):
  """Shows stored amanuensis contracts for TAs."""
  <<implementation>>
@

[... 300 lines explaining contract filtering concepts ...]

\subsection{Options for filtering contracts by time}

Users can filter which contracts to display based on time periods.
We provide three options for different use cases.

\paragraph{The [[--all]] option}
This disables time filtering entirely, showing all valid contracts.
<<options for which contracts to show>>=
all: Annotated[bool, show_all_opt] = False,
@

\paragraph{The [[--next]] option}
This shows only upcoming contracts.
<<options for which contracts to show>>=
next: Annotated[bool, show_next_opt] = False,
@

\paragraph{The [[--prev]] option}
This shows only past contracts.
<<options for which contracts to show>>=
prev: Annotated[bool, show_prev_opt] = False
@
```

When the function definition expands, `<<options for which contracts to show>>` becomes all three concatenated definitions:
```python
def cli_amanuens_show(user_regex,
                      all: Annotated[bool, show_all_opt] = False,
                      next: Annotated[bool, show_next_opt] = False,
                      prev: Annotated[bool, show_prev_opt] = False):
```

### Benefits

1. **Readable high-level structure**: Function signature shows conceptual parameter groups, not individual details
2. **Pedagogical ordering**: Each option explained when reader has context to understand it
3. **Variation theory alignment**: Shows "whole" (filtering concept) before "parts" (specific options)
4. **Maintainability**: Easy to add new options by adding another concatenated definition
5. **Natural flow**: Each option introduced with motivation and explanation

### Relationship to Chunk Concatenation

This pattern **uses** chunk concatenation (multiple definitions of the same chunk name), but applies it specifically for progressive disclosure at high-level structure points.

**Key distinction:**
- **General concatenation**: Building up any chunk incrementally (e.g., `<<constants>>` defined multiple times)
- **This pattern**: Using concatenation specifically to defer details in high-level structure

Both use the same mechanism (concatenation) but this pattern focuses on the pedagogical benefit of abstraction early in the document.

### When to Use This Pattern

**Use abstract placeholder chunks when:**
- Defining high-level structure (module outlines, function signatures, class definitions)
- You have 3+ related pieces that form a conceptual unit
- Details aren't pedagogically relevant yet at this point in the narrative
- Each piece deserves its own explanation section

**Avoid when:**
- Only 1-2 pieces involved (direct reference may be clearer)
- All pieces should be introduced together
- The abstraction would be artificial or forced
- Pieces don't naturally form a conceptual group

### Naming Abstract Chunks

Good abstract chunk names describe **purpose**, not **syntax**:

✅ Good:
- `<<options for which contracts to show>>`
- `<<initialization parameters>>`
- `<<validation rules>>`
- `<<error handling cases>>`

❌ Avoid:
- `<<all options>>` (too vague)
- `<<option definitions>>` (describes syntax, not purpose)
- `<<parameters>>` (not specific enough)
- `<<stuff>>` (meaningless)

## Chunk Concatenation Patterns

Noweb allows multiple definitions of the same chunk name - they are concatenated in order of appearance. This feature can be used pedagogically to introduce concepts incrementally, but requires careful consideration of scope and context.

### When to Use Multiple Definitions (Pedagogical Building)

**Use multiple definitions** when building up a parameter list or configuration as you introduce each concept:

```noweb
\subsection{Adding the diff flag}
We introduce a [[--diff]] flag to show differences between versions.
<<args for diff option>>=
diff=args.diff,
@

[... 300 lines later ...]

\subsection{Fine-tuning diff matching with thresholds}
To handle edge cases in file matching, we add threshold parameters.
<<args for diff option>>=
diff_threshold_fixed=args.diff_threshold_fixed,
diff_threshold_percent=args.diff_threshold_percent
@
```

**Result:** When `<<args for diff option>>` is used, it expands to all three parameters. This pedagogical pattern:
- Introduces each concept at its natural point in the narrative
- Builds understanding incrementally
- Uses noweb's concatenation feature intentionally
- Makes the document more readable by not front-loading all parameters

**When this works well:**
- Parameters are being added to the same logical concept
- All uses of the chunk occur in the **same scope** (all have access to `args`)
- The incremental introduction aids understanding
- The chunk represents a single conceptual unit being built up over time

### When to Use Separate Chunks (Different Contexts)

**Use separate chunks** when the same parameters must be passed in different scopes:

```noweb
\subsection{Calling format\_submission from main}
The command function has access to [[args]]:
<<args for diff option>>=
diff=args.diff,
diff_threshold_fixed=args.diff_threshold_fixed,
diff_threshold_percent=args.diff_threshold_percent
@

\subsection{Recursive calls inside format\_submission}
Inside [[format_submission]], we don't have [[args]]---only parameters.
We need a separate chunk to pass these through:
<<diff params>>=
diff=diff,
diff_threshold_fixed=diff_threshold_fixed,
diff_threshold_percent=diff_threshold_percent
@
```

**Result:** Two distinct chunks for different scoping contexts. This pattern:
- Makes scope explicit through chunk naming
- Prevents `NameError` when `args` doesn't exist
- Clearly distinguishes external calls from internal recursion
- Improves code maintainability by making context visible

**When you need separate chunks:**
- The same logical parameters must be passed in **different scopes**
- One context has `args` object, another has only parameters
- External calls vs internal recursive calls
- Command-line processing vs function implementation

### Guidelines for Choosing

Ask these questions:

1. **Same scope?**
   - Yes → Consider concatenation for pedagogical building
   - No → Use separate chunks with descriptive names

2. **Same conceptual unit?**
   - Yes, building up one concept → Concatenation may be appropriate
   - No, different purposes → Separate chunks

3. **Will readers be confused?**
   - If a reader at the first definition won't know there's a second → Add forward reference
   - If scope differences aren't obvious → Use separate chunks with clear names

### Anti-Pattern: Confusing Concatenation

**Bad:** Using concatenation when contexts differ, causing scope errors:

```noweb
<<args for diff option>>=
diff=args.diff,
@

# Used both in command function AND inside format_submission
# This causes NameError inside format_submission where args doesn't exist!
```

**Good:** Recognize different contexts and use separate chunks:

```noweb
<<args for diff option>>=  # For command function (has args)
diff=args.diff,
@

<<diff params>>=  # For internal calls (no args)
diff=diff,
@
```

### Best Practices

1. **Document concatenation intent**: If using multiple definitions, mention it in the prose (e.g., "we'll extend this chunk later")
2. **Use forward references**: If split is large, note "see Section X.Y for threshold parameters"
3. **Check for scope issues**: Before reusing a chunk name, verify all usage sites have access to the same variables
4. **Prefer separate chunks when in doubt**: Clear, explicit chunk names beat clever reuse
5. **Name chunks for context**: `<<args for X>>` vs `<<X params>>` makes scope immediately visible

## Organizing Tests in Literate Programs

When embedding tests in literate programs (common for modules using pytest, unittest, etc.), follow these principles to maintain pedagogical clarity:

### Test Placement: After Implementation, Not Before

**CRITICAL PRINCIPLE:** Tests should appear AFTER the functionality they verify, not before.

**Pedagogical flow:**
1. **Explain** the problem and approach
2. **Implement** the solution
3. **Verify** it works with tests

This ordering allows readers to:
- Understand what's being built before seeing verification
- See tests as proof/validation rather than mysterious code
- Follow a natural learning progression

### Pattern: Distributed Test Organization

**DO NOT** group all tests at the beginning of the file. Instead, distribute tests throughout the document, placing each test section immediately after its corresponding implementation.

**Example structure:**
```noweb
\section{Feature Implementation}

We need to implement feature X...

<<implementation>>=
def feature_x():
    # implementation code
@

Now let's verify this works correctly...

<<test feature>>=
def test_feature_x():
    assert feature_x() == expected
@
```

### Main Test File Structure Pattern

Define the main test file structure early (imports, test file skeleton), then reference a single `<<test functions>>` chunk that gets built up throughout the document:

```noweb
\section{Testing Overview}

Tests are distributed throughout this document, appearing after
each implementation section.

<<test [[module.py]]>>=
"""Tests for module functionality"""
import pytest
from module import *

<<test functions>>
@

\section{Feature A Implementation}
<<implementation of feature a>>=
...
@

\subsection{Verifying Feature A}
<<test functions>>=
class TestFeatureA:
    def test_basic_case(self):
        ...
@

\section{Feature B Implementation}
<<implementation of feature b>>=
...
@

\subsection{Verifying Feature B}
<<test functions>>=
class TestFeatureB:
    def test_another_case(self):
        ...
@
```

**Key principles:**

1. **Use `from module import *`** - Import everything from the module being tested. This allows freely adding to `<<test functions>>` without updating imports. The test setup should not need modification when adding new tests.

2. **Single `<<test functions>>` chunk** - All test chunks use the same name. Noweb concatenates them in order of appearance, building up the complete test file.

3. **Tests stay close to implementations** - Each `<<test functions>>=` chunk appears immediately after the implementation it verifies, maintaining pedagogical proximity.

### Anti-Pattern: Tests Before Implementation

**BAD** (Tests appear 300 lines before implementation):
```noweb
\section{Testing}
<<test module.py>>=
import module

<<test equality>>=    ← Reader doesn't know what this tests yet!
def test_users_equal():
    ...
@

[300 lines of other content]

\section{Make Classes Comparable}  ← Implementation finally appears!
<<implementation>>=
def make_comparable(cls):
    ...
@
```

**Reader confusion:**
- "What does `test_users_equal` test? I haven't seen the code yet!"
- Must scroll back hundreds of lines to understand tests
- Tests feel unmotivated and disconnected

**GOOD** (Tests appear after implementation):
```noweb
\section{Make Classes Comparable}
<<implementation>>=
def make_comparable(cls):
    ...
@

\subsection{Verifying Comparability}

Now let's verify the decorator works correctly...

<<test functions>>=
def test_users_equal():
    ...
@
```

**Reader clarity:**
- Sees implementation first
- Understands what's being tested
- Tests serve as proof/verification
- Natural pedagogical flow

### Framing Test Sections

Use pedagogical framing to introduce test sections:

**Good framing language:**
- "Now let's verify this works correctly..."
- "Let's prove this implementation handles edge cases..."
- "We can demonstrate correctness with these tests..."
- "To ensure reliability, we test..."

**Avoid:**
- Starting tests with no context
- Separating tests completely from what they test
- Grouping unrelated tests together

### Test Organization Roadmap

For files with many test sections, provide a roadmap early:

```latex
\subsection{Test Organization}

Tests are distributed throughout this file:
\begin{description}
\item[Feature A tests] Appear after implementation (Section~\ref{sec:featureA})
\item[Feature B tests] Appear after implementation (Section~\ref{sec:featureB})
\item[Integration tests] Appear after all features (Section~\ref{sec:integration})
\end{description}
```

### When to Use This Pattern

**Use distributed test placement when:**
- Tests verify specific implementations in the same file
- Pedagogical clarity is important
- Tests serve as proof/examples of correctness
- File is meant to be read by humans (documentation-oriented)

**Consider grouped tests when:**
- Tests are integration tests spanning multiple modules
- Test file is separate from implementation (.nw file just for tests)
- Tests don't directly correspond to specific code sections

### Benefits of This Approach

1. **Pedagogical clarity**: Readers learn before they see verification
2. **Proximity**: Tests next to implementation (easier maintenance)
3. **Motivation**: Tests feel natural, not arbitrary
4. **Flow**: Natural progression from problem → solution → proof
5. **Findability**: Easy to locate tests for specific functionality

### Testing Dependencies to Detect Breaking Changes

While testing functionality is essential, it's not sufficient on its own. Tests should also verify assumptions about dependencies—the functions used within your implementation. This helps detect errors when implementations change elsewhere in the codebase.

**Why this matters**: When a dependency changes its behavior (e.g., returning a generator instead of a list), your code may break in subtle ways. Tests that verify dependency contracts catch these breaking changes immediately.

#### The Problem: Silent Breaking Changes

Consider a function that filters objects based on regex patterns. Initially, it might return a list, but later be refactored to return a generator for efficiency. Code that depends on list-specific behavior (like indexing) will break, but the breakage might not be obvious.

Here's a concrete example:

**Initial implementation** (returns list implicitly):
```noweb
<<functions>>=
def filter_by_regex(objects, attributes, require_all=False):
    """
    Filters objects based on regex patterns.
    """
    results = []
    for object in objects:
        # ... matching logic ...
        if match:
            results.append(object)
    return results
@
```

**Refactored implementation** (returns generator):
```noweb
<<functions>>=
def filter_by_regex(objects, attributes, require_all=False):
    """
    Filters objects based on regex patterns.
    """
    for object in objects:
        <<search [[object]] for [[regex]] in its [[attributes]] and yield matches>>
@
```

Now consider code that uses this function and assumes list behavior:

```noweb
<<functions>>=
def get_filtered_objects_from_api(api_url, attributes, require_all=False):
    """
    Fetches objects from API and filters them.
    """
    <<get [[data]] from [[api_url]]>>
    objects = [TestObject(item['name'], item['description']) for item in data]
    return filter_by_regex(objects, attributes, require_all)
@
```

**The test that catches the problem**:
```noweb
<<test functions>>=
def test_get_filtered_objects_from_api(monkeypatch):
    sample_api_data = [
        {"name": "apple", "description": "A fruit"},
        {"name": "banana", "description": "Another fruit"},
        {"name": "carrot", "description": "A vegetable"},
        {"name": "apricot", "description": "A tasty vegetable fruit"},
    ]
    def mock_get(url):
        class MockResponse:
            def raise_for_status(self):
                pass
            def json(self):
                return sample_api_data
        return MockResponse()
    monkeypatch.setattr(requests, "get", mock_get)

    attributes = {
        "name": r"^a",
        "description": r"vegetable",
    }
    results = get_filtered_objects_from_api(api_url, attributes)

    # These assertions assume list behavior (indexing)
    assert len(results) == 3
    assert results[0].name == "apple"
    assert results[1].name == "carrot"
    assert results[2].name == "apricot"
@
```

**What happens**: After the refactoring to use generators, this test will fail because:
1. `results` is now a generator object, not a list
2. You cannot call `len()` on a generator
3. You cannot index into a generator with `results[0]`

**This is exactly what we want**: The test catches that `get_filtered_objects_from_api` (or code calling it) assumes list-like behavior from `filter_by_regex`. The test documents this dependency assumption and fails when the contract changes.

#### Core Principle: Test Assumptions About Dependencies

Tests should verify not just that your code produces the right output, but that dependencies behave as your code expects them to. When you use a function in a certain way, test that it supports that usage pattern.

**Test the contract, not just the outcome**:
- If your code indexes into a result: test that the dependency returns something indexable
- If your code iterates multiple times: test that the dependency returns something re-iterable
- If your code catches specific exceptions: test that the dependency raises those exceptions

This makes implicit contracts explicit and documents assumptions for future maintainers.

#### Types of Dependency Changes to Catch

**1. Return type changes** (primary concern):
- List vs generator (as in the example above)
- List vs iterator vs iterable
- Concrete type vs abstract protocol
- Single value vs collection
- None vs empty collection

**2. Behavior changes**:
- Raising exceptions vs returning None/default values
- Eager vs lazy evaluation
- Mutable vs immutable returns
- Side effects vs pure functions

**3. Interface/protocol changes**:
- Available methods or attributes
- Parameter signatures
- Expected protocols (iterator, context manager, etc.)
- State requirements (must call setup(), etc.)

#### Pattern: Structure Dependency Tests

Place dependency verification tests close to where dependencies are used, following the same proximity principle as other tests (~10 lines from usage).

**Frame tests pedagogically**:
```noweb
We also want to test that [[filter_by_regex]] fulfils our expectations.
The calling code assumes the result is indexable, so let's verify that:

<<test functions>>=
def test_filter_returns_indexable():
    results = filter_by_regex(sample_objects, {"name": r"^a"})
    # Verify we can index into results
    first = results[0]
    assert first.name == "apple"
@
```

**Test the assumption explicitly**, not just indirectly through higher-level behavior. This makes it clear what contract you're depending on.

#### Best Practices

1. **Test contracts when you depend on them**: If your code uses `results[0]`, test that the dependency returns something indexable
2. **Test iteration behavior**: If you iterate twice, test that the dependency supports it (generators don't)
3. **Test exception contracts**: If you catch `ValueError`, test that the dependency actually raises it
4. **Place tests near usage**: Keep dependency tests within ~10 lines of where the dependency is used
5. **Frame pedagogically**: Explain why you're testing this assumption ("We need to verify that X returns Y because...")
6. **Make implicit contracts explicit**: If your code assumes something, document it with a test

#### Connection to Literate Programming

Testing dependencies serves the literate programming goal of clarity and documentation:

**Makes contracts explicit**: Your code may implicitly assume a function returns a list. The test makes this explicit: "This code requires filter_by_regex to return an indexable collection."

**Documents assumptions**: Future maintainers see not just what your code does, but what it expects from dependencies. This prevents subtle bugs when refactoring.

**Pedagogical value**: Readers understand the relationship between components. The test shows: "get_filtered_objects_from_api depends on filter_by_regex returning something indexable."

**Prevents confusion**: Without dependency tests, readers might wonder: "Can I refactor filter_by_regex to return a generator?" The test answers: "No, because get_filtered_objects_from_api (and its tests) assume indexable behavior."

**Supports refactoring**: Want to change filter_by_regex to return a generator? The dependency tests immediately show what calling code needs updating: any code that indexes into results must convert to a list first.

#### When to Apply This Pattern

**Always test dependency assumptions when**:
- Your code uses specific behaviors (indexing, multiple iteration, exception catching)
- Dependencies might reasonably be refactored (internal functions you control)
- The contract is implicit rather than enforced by types
- Breaking the contract would cause subtle bugs rather than immediate errors

**Consider skipping when**:
- The dependency is external and stable (standard library, major framework)
- The contract is enforced by the type system (strict typing makes behavior guaranteed)
- The dependency is trivial (one-line helper that obviously won't change)

**Balance**: Test important contracts, especially for internal dependencies. Don't test every function call, but do test assumptions that would cause subtle bugs if broken.

## Noweb Commands

### Tangling (Extracting Code)

```bash
# Extract a specific root chunk
notangle -Rchunkname file.nw > output.ext

# With line number directives for debugging
notangle -L -Rchunkname file.nw > output.ext

# Default root is <<*>>
notangle file.nw > output.ext

# List all root chunks (not used in other chunks)
noroots file.nw
```

Common flags:
- `-R<name>`: Specify root chunk to extract (can be repeated)
- `-L`: Emit line number directives (`#line` for C, etc.)
- `-L'format'`: Custom line number format
- `-t<n>`: Preserve tabs, with stops every n columns
- `-filter cmd`: Filter through command before tangling

### Weaving (Creating Documentation)

```bash
# Generate LaTeX
noweave -latex file.nw > output.tex

# Generate with cross-references
noweave -latex -x file.nw > output.tex

# Generate with index and autodefs for language
noweave -latex -index -autodefs lang file.nw > output.tex

# Generate HTML
noweave -html -index -autodefs lang file.nw > output.html

# No wrapper (for inclusion in larger document)
noweave -n -latex file.nw > output.tex

# Delay preamble (for custom \documentclass)
noweave -delay -latex file.nw > output.tex
```

Common flags:
- `-latex`: Emit LaTeX (default)
- `-html`: Emit HTML
- `-tex`: Emit plain TeX
- `-n`: No wrapper (no document structure)
- `-delay`: Delay file info until after first doc chunk
- `-x`: Add cross-references and chunk definitions
- `-index`: Build identifier index
- `-autodefs lang`: Auto-detect definitions in language
- `-t<n>`: Expand tabs to n columns

## Example Structure

```noweb
This is the documentation explaining what we're doing.
We'll implement a function to compute [[factorial]].

<<factorial.py>>=
"""
<<module docstring>>
"""

<<imports>>
<<factorial function>>
<<test code>>
@

The factorial function uses recursion:
<<factorial function>>=
def factorial(n):
    """Compute n factorial."""
    <<base case>>
    return n * factorial(n - 1)
@

For the base case, we check if n is 0 or 1:
<<base case>>=
if n <= 1:
    return 1
@
```

## Best Practices

1. **Write documentation first** - Start with explanation, then add code
2. **Keep lines under 80 characters** - Both in documentation and code chunks.
   This improves readability and follows traditional Unix conventions. Break
   long lines at natural points (after commas, before operators, etc.)
3. **Use the -L flag for debugging** - Line directives help debuggers point to
   .nw file, however: this doesn't work for Python (among others).
4. **Check for unused chunks** - Run `noroots` to find typos in chunk names
5. **Mix languages freely** - Noweb is language-agnostic; include Makefiles, configs, etc.
6. **Consider your audience** - Write for someone learning the code, not just maintaining it
7. **Use cross-references** - The `-x` and `-index` flags help readers navigate
8. **Keep tangled code in gitignore** - The .nw file is the source of truth
9. **NEVER commit generated files** - .py and .tex files generated from .nw sources are build artifacts and must NEVER be committed to git. Only commit the .nw source files.
10. **Test your tangles** - Ensure extracted code actually compiles/runs
11. **Keep docstrings independent from LaTeX** - Docstrings are for code users (rendered with pydoc/help()), not maintainers. Never include LaTeX commands (like `\cref`, `\section`, etc.) in docstrings. The literate source documentation is for maintainers who read the compiled PDF; docstrings are runtime documentation.
12. **Include a table of contents** - Add `\tableofcontents` after `\maketitle` in the document preamble. This helps readers navigate the documentation, especially for larger literate programs with multiple sections.

## Language-Specific Notes

### C/C++
- Use `-L` flag for `#line` directives
- Put headers and implementation in same .nw file
- Extract with: `notangle -L -Rfile.cpp file.nw > file.cpp`

### Python
- No special flags needed
- Keep lines under 80 characters in .nw files (both prose and code)
- Break long lines in Python code:
  - Function calls: break after commas, indent continuation
  - String literals: use implicit string concatenation or parentheses
  - Long expressions: use parentheses and break at logical points
- Consider using formatters on output: `notangle -Rfile.py file.nw | black - > file.py`
- Note: Black may reformat to different line lengths, but keep source readable

**Docstring Anti-Pattern**: Never include LaTeX commands in Python docstrings

**Why**: Docstrings serve two different audiences:
- **Literate source (LaTeX)**: For maintainers who read the compiled PDF
- **Python docstrings**: For code users who run `help()` or `pydoc`

**Bad** - LaTeX in docstring causes Python syntax warnings:
```python
def is_submission_ungraded(submission):
    """
    Returns True if submission is ungraded.

    See \cref{SubmissionsFiltering} for details.  # ← WARNING: invalid escape
    """
    return submission.submitted_at and ...
```

**Good** - LaTeX reference in literate source, plain docstring:
```noweb
\subsection{Helper function}

This function implements the filtering strategy described above
(\cref{SubmissionsFiltering}), encapsulating the logic...

<<functions>>=
def is_submission_ungraded(submission):
    """
    Returns True if submission is ungraded.

    A submission is ungraded if submitted but not graded,
    or if grade doesn't match current submission.
    """
    return submission.submitted_at and ...
@
```

The cross-reference `\cref{SubmissionsFiltering}` belongs in the LaTeX documentation (for maintainers), not in the docstring (for users)

### Haskell
- Use `-L` flag (GHC understands line pragmas)
- Note: Haskell also has native `.lhs` literate format

### Make
- Use `-t2` to convert spaces to tabs: `notangle -t2 -RMakefile file.nw > Makefile`

### Shell scripts
- No special flags needed
- Remember to `chmod +x` the output

## Common Patterns

### Multiple outputs from one file
```bash
notangle -Rprogram.c file.nw > program.c
notangle -Rprogram.h file.nw > program.h
notangle -RMakefile file.nw > Makefile
```

### Building with Make
```makefile
%.py: %.nw
    notangle -R$@ $< > $@

%.tex: %.nw
    noweave -n -latex $< > $@

%.pdf: %.tex
    pdflatex $<
```

### Documentation with tests
Interleave test code with implementation to show correctness:
```noweb
Here's our sort function:
<<sort function>>=
def sort(lst):
    <<sorting implementation>>
@

Let's verify it works:
<<test code>>=
assert sort([3,1,2]) == [1,2,3]
@
```

## Multi-Directory Project Organization

For large literate programming projects spanning multiple modules, use hierarchical organization patterns. This section provides an overview; see `references/multi-directory-projects.md` for detailed examples.

### When to Use Multi-Directory Organization

**Use three-directory separation when:**
- Project has 5+ .nw files across multiple modules
- Documentation needs different organization than code structure
- Tests should be cleanly separated for CI/CD
- Multiple developers need clear separation of concerns

**Use flat structure when:**
- Single-file or small projects (1-3 .nw files)
- Documentation and code naturally align
- Simplicity is more important

### Repository Structure Pattern

Separate literate sources, documentation builds, and tests:

```
project/
├── src/           # .nw source files (mirror package structure)
│   └── package/
│       ├── Makefile
│       ├── module.nw → module.py + module.tex
│       └── subpackage/
│           └── module2.nw
├── doc/           # Documentation build directory
│   ├── Makefile
│   ├── main.tex   # Master document (includes .tex from src)
│   └── main.pdf   # Generated documentation
├── tests/         # Extracted test files
│   ├── Makefile
│   └── test_*.py  # Generated from test chunks in .nw
└── makefiles/     # Shared build infrastructure
    ├── noweb.mk   # Tangle/weave rules
    └── subdir.mk  # Recursive build rules
```

**Key insight**: .nw files in `/src` generate:
- **Code** tangled back into `/src`
- **Documentation** woven to .tex in `/src`, then included in `/doc`
- **Tests** extracted to `/tests`

### Hierarchical Build Systems

Use recursive Makefiles with shared rules:

**Each directory Makefile:**
```makefile
# Declare modules to build
MODULES+= module.py

# Declare subdirectories
SUBDIR+= subpackage

# Include shared rules (adjust path depth)
INCLUDE_MAKEFILES=../../makefiles
include ${INCLUDE_MAKEFILES}/noweb.mk
include ${INCLUDE_MAKEFILES}/subdir.mk
```

**The noweb.mk provides:**
- Suffix rules: `.nw.tex` (weaving), `.nw.py` (tangling)
- Language-specific post-processing (e.g., Black for Python)
- Common flags and customization points

**The subdir.mk provides:**
- Recursive traversal to subdirectories
- Propagation of make goals (all, clean, etc.)

**Python __init__.py pattern:**
```makefile
.INTERMEDIATE: init.py
__init__.py: init.py
    ${MV} $< $@
```

**LaTeX-safe chunk naming pattern:**

When chunk names contain underscores (common in Python), LaTeX will interpret them
as math subscripts outside of code blocks, causing compilation errors. The solution
is to use noweb's `[[...]]` notation, which automatically escapes all LaTeX special
characters.

```noweb
# In your .nw file, use [[...]] notation for ALL Python chunks:
<<[[module_name.py]]>>=
def my_function():
    pass
@
```

**Makefile integration:**

The `noweb.mk` makefile infrastructure automatically handles `[[...]]` notation
when extracting chunks:

```makefile
# In makefiles/noweb.mk - extraction uses [[...]] notation
%.py: %.nw
    ${NOTANGLE} -R"[[$(notdir $@)]]" $< > $@

# In module Makefiles - just list the files
MODULES = module_name.py another_module.py
```

**Why this works:**
- `[[...]]` tells noweb to escape all LaTeX special characters automatically
- Works for underscores, hashes, ampersands, and other special characters
- Chunk name matches filename exactly (no renaming needed)
- Simpler Makefiles (no intermediate file renaming)
- Consistent pattern for all Python modules

**Example from canvaslms project:**
```noweb
# attachment_cache.nw
<<[[attachment_cache.py]]>>=
"""Caching for Canvas attachment downloads"""
import os
import hashlib
<<imports>>
<<functions>>
@
```

**When to use this pattern:**
- **ALL Python chunks should use `[[...]]` notation** for consistency
- Required for any filename with underscores, hashes, or special characters
- Projects that weave documentation to LaTeX format

**Alternatives and why they were rejected:**
- **Escaping with `\_`**: Requires escaping everywhere `\_` characters appear, unmaintainable
- **Hyphens + Makefile renaming** (old approach): Adds complexity, extra build steps, intermediate files
- **Renaming files to avoid underscores**: Breaks Python import conventions

### Documentation Composition

Create a master document in `/doc` that includes .tex from `/src`:

**Directory structure:**
```
project/
├── src/package/
│   ├── module1.nw → module1.py + module1.tex
│   └── module2.nw → module2.py + module2.tex
└── doc/
    ├── Makefile
    ├── main.tex       # Master document (committed to git)
    ├── preamble.tex   # Shared LaTeX preamble (committed to git)
    └── main.pdf       # Generated (gitignored)
```

**Key principle**: The master document (`main.tex`) and preamble (`preamble.tex`) in `/doc`
are **source files** that get committed to git. They are NOT generated from .nw files.
Only the woven .tex files in `/src` are generated.

### The Separate Preamble Pattern

**ALWAYS use a separate preamble.tex file** that the main document inputs. This provides:
- Consistent formatting across all literate programming projects
- Easy updates to packages and settings
- Clean separation of document structure from formatting

**Master document** (`doc/main.tex`):
```latex
\documentclass[a4paper,oneside]{memoir}
\input{preamble}

\usepackage{noweb}
\noweboptions{shift,breakcode,longxref,longchunks}

\title{Project Name}
\author{Author Name}
\date{\today}

\begin{document}
\frontmatter
\maketitle

\begin{abstract}
Brief description of the project.
\end{abstract}

\tableofcontents

\mainmatter

\part{Core Functionality}
\input{../src/package/module1.tex}
\input{../src/package/module2.tex}

\part{Extensions}
\input{../src/package/subpackage/module3.tex}

\backmatter
\end{document}
```

**Standard preamble** (`doc/preamble.tex`):

Copy the standard preamble from `references/preamble.tex` in this skill directory.
This preamble is used consistently across all literate programming projects and includes:
- Language support (babel with swedish,british)
- Bibliography (biblatex with alphabetic style)
- Code highlighting (minted, pythontex)
- Mathematics (amsmath, amssymb, mathtools, amsthm)
- Cross-references (cleveref with custom question labels)
- Various utilities (enumitem, csquotes, acro, etc.)

### .nw Files as Chapters

Each .nw file should be structured as a **chapter** (not a complete document):

```noweb
\chapter{Module Name}
\label{module-name}

\section{Introduction}

This module provides...

<<[[module_name.py]]>>=
<<imports>>
<<functions>>
@

\section{Implementation}
...
```

**Key points:**
- Start with `\chapter{...}` and `\label{...}`
- NO `\documentclass`, `\begin{document}`, `\end{document}`
- NO `\input{preamble}` or `\maketitle`
- Use `\section`, `\subsection` for internal structure
- The main document provides the document wrapper

### Weaving for Inclusion

Use the `-n -delay` flags when weaving to produce includable .tex files:

```makefile
# In src/package/Makefile
NOWEAVEFLAGS.tex?= -x -n -delay -t2

module.tex: module.nw
    noweave ${NOWEAVEFLAGS.tex} $< > $@
```

The flags mean:
- `-x`: Add cross-references
- `-n`: No wrapper (no `\documentclass`, etc.)
- `-delay`: Delay file info until after first doc chunk
- `-t2`: Expand tabs to 2 spaces

### Documentation Makefile Pattern

**Documentation Makefile** (`doc/Makefile`):
```makefile
DOC+=       main.pdf

SRC_TEX+=   ../src/package/module1.tex
SRC_TEX+=   ../src/package/module2.tex
SRC_TEX+=   ../src/package/subpackage/module3.tex

.PHONY: all clean

all: ${DOC}

main.pdf: main.tex preamble.tex
main.pdf: ${SRC_TEX}

# Pattern rule: build .tex files in src if they don't exist or are outdated
../src/%::
    ${MAKE} -C $(dir $@) $(notdir $@)

INCLUDE_MAKEFILES=../makefiles
include ${INCLUDE_MAKEFILES}/tex.mk

clean:
    latexmk -C ${DOC}
```

**How it works:**
1. `main.pdf` depends on `main.tex`, `preamble.tex`, and all `SRC_TEX` files
2. If any `.tex` in `/src` is missing or outdated, the pattern rule builds it
3. The pattern rule calls `make` in the source directory to weave the .nw file
4. Once all dependencies exist, latexmk compiles the main document

This allows reorganizing documentation pedagogically without changing code structure.

### Test Organization

Define tests in .nw files, extract to `/tests`:

**In your .nw file:**
```noweb
<<test [[modulename.py]]>>=
import pytest
from package.modulename import feature

def test_feature():
    assert feature() == expected
@
```

**Note**: Use `[[...]]` notation for test chunks: `<<test [[modulename.py]]>>` to handle
filenames with underscores or other LaTeX special characters consistently.

**Tests Makefile** (`tests/Makefile`):
```makefile
# Auto-discover test chunks in all .nw files
define find_tests
find ../src -name "*.nw" | \
    xargs grep "<<test \[\[[^]]*\]\]>>" | \
    sed -En "s/^(.*):.*<<test \[\[([^]]*)\]\]>>.*/test_\2:\1/p"
endef

# Extract each test file from its source .nw
test_modulename.py: ../src/package/modulename.nw
    notangle -R"test [[modulename.py]]" $< > $@

# Run tests
test: all
    pytest
```

**Important for Poetry-managed projects:** If your project uses Poetry for dependency management, test dependencies (pytest, pytest-cov, etc.) are installed in Poetry's virtual environment. You must run tests with `poetry run pytest`:

```makefile
# Run tests with poetry
test: all
    poetry run pytest -v --cov=packagename --cov-report=term-missing
```

Without `poetry run`, pytest won't be found or will use a system-wide installation that lacks your test dependencies.

Benefits: tests stay with implementation documentation, but cleanly separated for pytest.

### Navigating Multi-Directory Projects

**Finding source code:**
```bash
grep -r "function_name" src/**/*.nw
```

**Reading documentation:**
```bash
cd doc && make all && open main.pdf
```

**Running tests:**
```bash
cd tests && make test
```

**Tracing bugs in generated code:**
1. Find corresponding .nw: `module.py` → `module.nw`
2. Fix the .nw source (NOT generated file)
3. Regenerate: `make` in the directory

**Understanding what gets built:**
```bash
cat src/package/Makefile  # Check MODULES+= lines
make -n all               # Dry-run shows commands
```

### Multi-Output from Single .nw

One .nw file can generate multiple artifacts:

```makefile
# Regular outputs
MODULES+= module.py

# Additional outputs from same .nw
EXTRAS+= script.sh
EXTRAS+= config.yaml

${EXTRAS}: module.nw
    notangle -R$(notdir $@) $< > $@

all: ${MODULES} ${EXTRAS}
```

### Self-Documenting Build Systems

The build infrastructure itself can be literate:

```
makefiles/
├── noweb.mk.nw → noweb.mk + noweb.tex
├── subdir.mk.nw → subdir.mk + subdir.tex
└── makefiles.pdf  # Documentation of build system
```

See `references/multi-directory-projects.md` for complete examples including the nytid repository.

## When to Use Literate Programming

Literate programming is especially valuable for:

- Complex algorithms requiring detailed explanation
- Educational code where understanding is paramount
- Code that will be maintained by others
- Programs where design decisions need documentation
- Projects combining multiple languages/tools
- Code that serves as documentation (like TeX itself)

## Troubleshooting

- **"chunk not defined" error**: Check chunk name spelling with `noroots`
- **Line numbers wrong in debugger**: Use `-L` flag with notangle
- **Formatting broken**: Check that `<<` starts in column 1
- **Chunks in wrong order**: Remember, notangle assembles them correctly
- **Documentation not rendering**: Verify `@` markers for documentation chunks

## Integration with Development Tools

- **Version control**:
  - **CRITICAL**: Only commit .nw files to git. Generated .py and .tex files are build artifacts.
  - Add generated files to .gitignore immediately when setting up a literate project
  - If generated files are already tracked, use `git rm --cached` to untrack them
  - Regenerate code with make after checkout/pull
- **IDEs**: Configure to run notangle on save, or use file watchers
- **CI/CD**: Add tangle step before build/test
- **Documentation**: Weave to HTML or PDF for readable docs
- **Code review**: Review .nw files for both code and explanation quality

## Git Workflow for Literate Programming Projects

**CRITICAL RULE**: Generated .py and .tex files from .nw sources must NEVER be committed to version control.

### Setting Up .gitignore

When starting a literate programming project:

1. Create .gitignore patterns for all generated files
2. Pattern examples:
   ```
   # Generated from literate programming (.nw files)
   src/**/*.py
   src/**/*.tex

   # Exceptions for hand-written files (if any)
   !src/specific_file.py
   ```

### Removing Accidentally Tracked Files

If generated files are already in git:

```bash
# Untrack but keep in working directory
git rm --cached path/to/generated.py
git rm --cached path/to/generated.tex

# Add to .gitignore
echo "path/to/generated.py" >> .gitignore
echo "path/to/generated.tex" >> .gitignore

# Regenerate fresh files from .nw source
make

# Commit the .gitignore changes
git add .gitignore
git commit -m "Remove generated files from version control"
```

### Pre-commit Checks

Before committing, verify:
1. No .py files with corresponding .nw sources are staged
2. No .tex files with corresponding .nw sources are staged
3. Only .nw files and other hand-written sources are being committed

### Identifying Generated vs Hand-Written Files

A .py or .tex file is **generated** (should NOT be committed) if:
- A corresponding .nw file exists with the same base name
- The file is listed as a target in a Makefile that uses notangle/noweave
- The file contains patterns typical of noweb output

A .py file is **hand-written** (OK to commit) if:
- No .nw source file exists
- It's explicitly marked as an exception in .gitignore
- It's a special file like `__init__.py` that's not generated from .nw
