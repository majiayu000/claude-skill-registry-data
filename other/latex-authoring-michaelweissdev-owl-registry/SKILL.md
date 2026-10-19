---
name: latex-authoring
description: >
  Draft, structure, format, and debug scientific documents, technical papers,
  and mathematical manuscripts using LaTeX. Use when typesetting complex equations,
  formatting professional multi-column tables, managing BibTeX/Biber references,
  resolving LaTeX compilation errors, or structuring modular book and thesis projects.
compatibility: >
  Agent Skills-compatible coding agents authoring or debugging LaTeX documents
  with pdflatex, xelatex, or lualatex engines.
metadata:
  author: michaelweissdev
  version: "1.0.0"
  tags: "latex, bibtex, math, scientific-writing, pdf, typesetting, academic"
  topics: "documentation, office, devtools"
---

# Professional LaTeX Authoring and Typesetting

LaTeX is the gold standard for scientific, mathematical, and academic document preparation. Writing robust LaTeX requires clean modular file structures, proper mathematical environments (`amsmath`), book-quality tables (`booktabs`), modern bibliography management (`biblatex`/`biber`), and disciplined resolution of compilation errors and warnings.

## Core Rules

1. **Always use modern math environments**: Use `amsmath` environments (`align*`, `equation`, `gather`) rather than obsolete TeX primitives (`$$ ... $$`, `\eqnarray`).
2. **Never use vertical rules in tables**: Follow professional typography guidelines (`booktabs`: `\toprule`, `\midrule`, `\bottomrule`). Never use `|` vertical lines in tables.
3. **Use consistent labeling conventions**: Prefix cross-reference labels by type: `fig:` for figures, `tab:` for tables, `sec:` for sections, and `eq:` for equations (`\label{eq:navier-stokes}`).
4. **Compile twice for cross-references**: LaTeX requires multiple compilation passes (or `latexmk`) to resolve forward citations, references, and table of contents numbering.
5. **Protect special characters in text**: Characters like `%`, `_`, `&`, `#`, `$`, `{`, `}` must be escaped (`\%`, `\_`, `\&`) when not intended as syntax tokens.

---

## 1. Canonical Article Template

```latex
\documentclass[11pt,a4paper]{article}

% --- Essential Packages ---
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{amsmath,amssymb,amsfonts}  % Advanced mathematics
\usepackage{booktabs}                  % Professional quality tables
\usepackage{graphicx}                  % External images
\usepackage{microtype}                 % Typographic micro-adjustments
\usepackage[hidelinks]{hyperref}       % Hyperlinks and PDF metadata

% --- Page Geometry ---
\usepackage[margin=1.0in]{geometry}

% --- Document Metadata ---
\title{\textbf{Distributed Consensus in Asynchronous Peer Networks}}
\author{Michael Weiss \and Distributed Systems Laboratory}
\date{October 15, 2026}

\begin{document}

\maketitle

\begin{abstract}
We present a formal analysis of consensus stability under network partition conditions, demonstrating bounded latency convergence bounds.
\end{abstract}

\section{Introduction}
\label{sec:introduction}
Distributed coordination under asynchronous timing models presents fundamental trade-offs formalized by the CAP theorem. As demonstrated in Section~\ref{sec:methods}, our approach minimizes message complexity while ensuring Byzantine fault tolerance.

\section{Mathematical Formulation}
\label{sec:methods}
Let $G = (V, E)$ represent a network graph where nodes $v_i \in V$ exchange state vectors. The convergence metric $\Phi(t)$ is defined as:

\begin{equation}
\label{eq:convergence}
\Phi(t) = \sum_{i=1}^{n} \left\| x_i(t) - \bar{x}(t) \right\|^2 + \int_{0}^{t} \lambda e^{-\gamma \tau} \, d\tau
\end{equation}

Notice that Equation~\eqref{eq:convergence} decays exponentially when the spectral gap satisfies $\lambda_2(L) > 0$.

\section{Experimental Results}
\label{sec:results}
Table~\ref{tab:benchmarks} summarizes throughput across varying cluster scales.

\begin{table}[htbp]
\centering
\caption{Throughput and Latency Across Cluster Topologies}
\label{tab:benchmarks}
\begin{tabular}{lrrr}
\toprule
\textbf{Nodes ($N$)} & \textbf{Throughput (tx/s)} & \textbf{Mean Latency (ms)} & \textbf{Loss Rate (\%)} \\
\midrule
5   & 14,200 & 1.8 & 0.00 \\
25  & 11,850 & 4.5 & 0.02 \\
100 &  8,400 & 14.2 & 0.15 \\
\bottomrule
\end{tabular}
\end{table}

\section{Conclusion}
The experimental results validate our analytical convergence boundaries.

\end{document}
```

---

## 2. Compiling with `latexmk`

Avoid manual multi-pass invocations of `pdftotext`, `bibtex`, and `pdflatex`. Use `latexmk` for automated dependency resolution:

```bash
# Automated compilation to PDF (runs pdflatex and biber until all references resolve)
latexmk -pdf -synctex=1 -interaction=nonstopmode document.tex

# Clean temporary compilation artifacts (.aux, .log, .out, .bbl)
latexmk -c
```

---

## 3. Diagnosing Common Compilation Errors

- **`! Undefined control sequence`**: Typo in command name or missing `\usepackage{...}` in the preamble.
- **`! Missing $ inserted`**: An underscore `_` or math symbol was used in standard text mode without escaping (`\_`).
- **`! LaTeX Error: Environment ... undefined`**: Missing package (e.g. using `align` without `\usepackage{amsmath}`).
- **`LaTeX Warning: Reference '...' on page X undefined`**: Document needs an additional compilation pass to resolve cross-references.

---

## 4. Common Mistakes and Anti-Patterns

| Anti-Pattern | Typographic / Build Bug | Correct Practice |
| :--- | :--- | :--- |
| `\begin{tabular}{|l|c|r|}` with vertical bars | Visually amateurish tables that violate academic typography | Use `\usepackage{booktabs}` with horizontal rules only |
| Using `$$ ... $$` for display math | Deprecated TeX primitive; breaks vertical spacing | Use `\begin{equation}` or `\[ ... \]` |
| Using standard quotes `"word"` | Yields identical closing quotes on both sides: ''word'' | Use backticks for opening quotes: `` `word' `` or `` ``word'' `` |
| Hardcoding figure numbers: `as seen in Figure 2` | Breaks numbering when figures are inserted/reordered | Use `Figure~\ref{fig:label}` with non-breaking tilde |

---

## 5. Verification Checklist

- [ ] Clean compilation with zero fatal errors (`latexmk -pdf`).
- [ ] No undefined reference warnings (`LaTeX Warning: Reference ... undefined`).
- [ ] Tables use `booktabs` (`\toprule`, `\midrule`, `\bottomrule`) without vertical lines.
- [ ] Special characters (`%`, `_`, `&`, `#`) escaped in text mode.
- [ ] Equations numbered and referenced via `\eqref{...}`.
