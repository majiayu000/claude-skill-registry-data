---
name: explain-math
description: Explain a mathematical concept with full rigor, activating the /advanced-math skill, then write the explanation as a compilable-LaTeX markdown file to the current working directory. Use when the user wants a written-down, verifiable math explanation saved to a file.
argument-hint: <topic or concept to explain, e.g. "spectral theorem for compact operators">
---

# Explain Math to File

The user wants a rigorous mathematical explanation of: $ARGUMENTS

## Process

1. **Activate /advanced-math** — invoke the `advanced-math` skill with the topic to generate a rigorous, formally grounded explanation following its full methodology (foundational anchoring, abstraction mapping, modular proofs, no black boxes).

2. **Write the explanation** to a markdown file in the current working directory:
   - **Filename**: derive from the topic in kebab-case, e.g. `spectral-theorem-compact-operators.md`
   - **Location**: create a `math-explanations/` folder in the current working directory if it doesn't exist
   - **Full path**: `<cwd>/math-explanations/<topic-name>.md`

3. **LaTeX formatting requirements** — all math in the file must use proper, compilable LaTeX syntax:
   - Use `$$...$$` for display math and `$...$` for inline math
   - Use proper LaTeX commands: `\mathbb{R}`, `\langle`, `\rangle`, `\sum`, `\int`, `\inf`, `\sup`, `\lim`, `\to`, `\implies`, `\iff`, `\forall`, `\exists`, `\in`, `\subset`, `\subseteq`, `\cap`, `\cup`, `\setminus`, etc.
   - Use `\text{}` for words inside math environments
   - Use `\operatorname{}` for named operators (e.g., `\operatorname{ker}`, `\operatorname{span}`)
   - Use `\begin{aligned}...\end{aligned}` inside `$$` for multi-line equations
   - Use `\begin{cases}...\end{cases}` for piecewise definitions
   - Do NOT use Unicode math symbols (∈, ⊆, →, ⟨, ⟩, etc.) — always use LaTeX commands instead
   - Do NOT use plain text where a LaTeX command exists
   - Every equation must parse correctly if pasted into a LaTeX document with standard amsmath packages

4. **File structure**:
   ```markdown
   # <Topic Title>

   ## Prerequisites
   <What undergraduate concepts this builds on>

   ## Abstraction Mapping
   <Table mapping abstract objects to undergraduate analogues>

   ## Definitions
   <Formal definitions with Definition Bridges per /advanced-math methodology>

   ## Main Result
   <Theorem statement, then proof broken into labeled lemmas>

   ## Key Examples
   <Concrete examples and counterexamples>
   ```

5. **After writing**, inform the user of the file path and remind them to verify the LaTeX compiles correctly.
