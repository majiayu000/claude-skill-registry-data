---
name: document-python-component
description: Write or upgrade conventional Python docstrings for public modules, classes, functions, methods, and properties. Docstrings must be user-facing, mkdocstrings-friendly, include runnable examples, and must not repeat type hints.
metadata:
  short-description: Google-style docstrings for public Python APIs (mkdocstrings-ready)
  keywords:
    - python
    - docstrings
    - google-style
    - mkdocs
    - mkdocstrings
    - mkdocs-material
---

# Python docstrings (Google style)

## Mission
When editing or creating Python code, write **high-quality Google-style docstrings** for:
- Modules (top-of-file docstring)
- Public classes
- Public functions
- Public methods and properties

Docstrings must render well in **mkdocs + mkdocs-material + mkdocstrings**.

## Trigger conditions
Use this skill when you:
- Add or modify a public module/class/function/method/property
- See missing, vague, outdated, or inconsistent docstrings
- Prepare code for API docs (mkdocstrings pages)
- Introduce non-obvious behavior, edge cases, or side effects

## Definitions (for this repo)
- **Public API**: no leading underscore (e.g., `fetch_prices`, `Client.get`). Private/internal objects (leading underscore) are optional unless behavior is non-obvious.
- **Type hints are the source of truth**: do **not** repeat types in docstrings when type hints exist.

## Authoring workflow
1. Identify public objects changed/created.
2. For each object, draft:
   - A one-line summary (what it does)
   - What matters to callers: constraints, invariants, side effects
3. Add only the sections that apply (e.g., include `Raises:` only when callers should care).
4. Add at least one runnable `Examples:` snippet for every public callable.
5. Read it like a user: “Can I use this without opening the source?”

## Output requirements
For every **public** object, add/upgrade a docstring that:
1. Follows **Google style**
2. Is **clear, concrete, and non-marketing**
3. Does **not** repeat type hints
4. Includes runnable `Examples:` for every public callable

## Google docstring structure (standard)
Include sections only when meaningful:
- Short summary (1 line)
- Optional extended summary (1–3 short paragraphs)
- `Args:`
- `Returns:`
- `Raises:`
- `Attributes:` (classes, when useful)
- `Examples:`
- `Notes:` (optional)
- `Warning:` (rare)

## Formatting rules
- Use triple double quotes: `"""Docstring..."""`
- Summary line ends with a period.
- Wrap lines roughly ~88–100 chars when reasonable (don’t force ugly wrapping).
- Prefer imperative/active voice (“Fetch prices…”, “Validate payload…”).
- Examples must be **copy-pastable** (no pseudocode).

## Markdown in docstrings (mkdocstrings-friendly)
- Prefer fenced code blocks with language identifiers in `Examples:` (e.g., ```py).
- You may use mkdocs-material **admonitions** and **content tabs** where they add clarity.
- Avoid nesting admonitions inside each other.
- Keep function/method docstrings simple; put richer narrative/context in module/class docstrings.

## Content rules
### 1) Keep it user-facing
Explain what it does, what matters, and any side effects (I/O, network, mutation, caching).

### 2) Don’t repeat types in docstrings
Describe meaning, not types. The user will see type hints.

✅ Do
```py
Args:
  ticker: Stock ticker symbol (e.g., "AAPL").
  period: Time period to fetch. Defaults to "1y".

Returns:
  A DataFrame containing historical stock prices.
```

❌ Don’t
```py 
Args:
  ticker (str): ...
  period (str, optional): ...

Returns:
  pd.DataFrame: ...
```

## Object-specific rules
### Module docstrings
Every module should start with a module docstring that answers:
- What the module provides/contains/implements
- Typical usage
- Important constraints (timezone assumptions, caching, side effects)

### Class docstrings
Class docstrings should describe:
- What the class represents/does/implements
- Lifecycle/ownership (resources, caches)
- Key invariants
- Constructor expectations (especially if non-obvious)

If the class is primarily a data container, document fields in `Attributes:`. Otherwise, document the public attributes that matter to callers.

### Method/property docstrings
- For obvious getters/setters, keep it brief but still include an example (even a tiny one).
- Mention side effects (writes to disk, network calls, mutates internal state).
- In `Raises:`, document meaningful error conditions (don’t list every low-level exception).

## `Examples:` rules (important)
Every public callable must have `Examples:` with at least one runnable example.

Examples should:
- Use realistic values (`"AAPL"`, `"1d"`, etc.)
- Show the most common happy path first
- Avoid network calls in examples unless the module is literally a client library
- Prefer tiny examples that won’t rot quickly
- Don’t use `>>>` prompts; use standard script-style code blocks so users can copy-paste directly.

If a function is async, example must use `asyncio.run(...)`.

## Quality checklist (must pass)
- [ ] Module has a top-quality docstring following software engineering best practices
- [ ] Every public function/class/method/property has a docstring
- [ ] Every public callable has `Examples:` with runnable code
- [ ] Args/Attributes describe meaning but **no types**
- [ ] Returns describes meaning (and shape if non-obvious)
- [ ] Raises lists meaningful exceptions + when they occur
- [ ] No fluff; no internal implementation narration unless it affects use
