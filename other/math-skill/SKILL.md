---
name: math-skill
description: A comprehensive mathematical reasoning skill for AI assistants — handles arithmetic to research-level problems with rigorous step-by-step reasoning, systematic verification, and transparent uncertainty handling
---

# Math.skill

## Skill Name

**Math.skill** — A comprehensive mathematical reasoning skill for AI assistants.

## Skill Purpose

Enable AI assistants to handle mathematical tasks across all difficulty levels — from basic arithmetic to research-level problems — with rigorous, step-by-step reasoning, systematic verification, and transparent uncertainty handling.

This skill enforces a disciplined mathematical workflow: every problem is parsed, modeled, solved with justifications, verified through multiple independent checks, and only then delivered as a final answer. The verification engine (see **Verification Engine** section) is the core differentiator — no answer is output without passing at least two verification methods.

## Scope of Application

This skill covers the following mathematical domains:

- **Foundations**: Arithmetic, number sense, order of operations, unit conversions
- **Algebra**: Algebraic expressions, polynomial operations, factoring, completing the square, rational expressions, radical expressions, exponents and logarithms
- **Equations**: Linear, quadratic, polynomial, rational, radical, exponential, logarithmic, absolute value equations
- **Inequalities**: Linear, quadratic, rational, absolute value, exponential, logarithmic inequalities; systems of inequalities
- **Functions**: Domain/range, composition, inverse, monotonicity, parity, periodicity, graphing, transformations, piecewise functions
- **Geometry**: Plane geometry, solid geometry, coordinate geometry, vector geometry, geometric transformations
- **Trigonometry**: Trigonometric functions, identities, equations, triangle solving, inverse trigonometric functions
- **Sequences and Series**: Arithmetic, geometric, recursive sequences; series convergence, summation formulas
- **Combinatorics**: Permutations, combinations, inclusion-exclusion, pigeonhole principle, generating functions
- **Probability and Statistics**: Classical probability, conditional probability, Bayes' theorem, distributions, expectation, variance, hypothesis testing, confidence intervals
- **Limits**: Limits of sequences and functions, one-sided limits, limits at infinity, epsilon-delta definitions, L'Hôpital's rule
- **Differentiation**: Derivative rules, implicit differentiation, logarithmic differentiation, higher-order derivatives, applications (tangents, rates, optimization, curve sketching)
- **Integration**: Indefinite and definite integrals, substitution, integration by parts, partial fractions, trigonometric integrals, improper integrals, applications (area, volume, arc length, work)
- **Multivariable Calculus**: Partial derivatives, gradients, directional derivatives, double/triple integrals, line integrals, surface integrals, divergence, curl, Green's/Stokes'/divergence theorems
- **Linear Algebra**: Matrices, determinants, vector spaces, linear transformations, eigenvalues/eigenvectors, diagonalization, inner product spaces, quadratic forms
- **Ordinary Differential Equations**: First-order, second-order linear, systems, Laplace transforms, series solutions, qualitative analysis
- **Complex Analysis**: Complex numbers, analytic functions, contour integration, residue theorem, conformal mapping
- **Real Analysis**: Completeness, sequences and series of functions, continuity, differentiation, Riemann integration, measure theory basics
- **Abstract Algebra**: Groups, rings, fields, homomorphisms, isomorphisms, quotient structures, Galois theory basics
- **Topology**: Metric spaces, topological spaces, continuity, compactness, connectedness, fundamental group basics
- **Number Theory**: Divisibility, congruences, prime numbers, Diophantine equations, modular arithmetic, cryptography basics
- **Discrete Mathematics**: Graph theory, recurrence relations, Boolean algebra, automata theory basics
- **Optimization**: Linear programming, nonlinear optimization, constrained optimization, Lagrange multipliers, convex optimization
- **Mathematical Modeling**: Model formulation, parameter estimation, model validation, sensitivity analysis
- **Proofs**: Direct proof, induction, contradiction, contrapositive, construction, exhaustion, epsilon-delta, combinatorial proofs
- **Counterexamples**: Systematic search for counterexamples to disprove conjectures or verify solution uniqueness
- **Solution Checking**: Verifying existing solutions, identifying errors, providing corrections
- **Problem Generation**: Creating well-posed problems with verified solutions at specified difficulty levels
- **Research-Level Problems**: Engaging with open or partially solved problems, clearly distinguishing known results from conjectures

## Out of Scope

This skill should NOT be invoked for:

- **Pure opinion questions**: "Is math beautiful?" — not a mathematical task
- **Non-mathematical creative writing**: Generating poems, stories, or essays not centered on mathematical reasoning
- **Factual lookup without reasoning**: "What is the capital of France?" — no mathematical reasoning required (use general knowledge or web search directly)
- **Pure code generation without math**: Writing a web server, a database query, or a UI component where no mathematical reasoning is needed
- **Conversational chat unrelated to math**: General small talk, emotional support, scheduling, etc.

Boundary cases: If a user asks "Explain the math behind RSA encryption," invoke this skill. If a user asks "Write a Python script to calculate prime numbers," invoke this skill (the core task is mathematical reasoning; code is implementation).

## Language Matching Rules

This skill adapts its language to the user's context:

- **Explicit specification**: If the user specifies an output language (e.g., "Answer in English"), use that language
- **Default**: If not specified, match the user's primary input language throughout the response
- **Mixed Chinese-English input**: Respond in the user's dominant language; keep mathematical terms in their standard form (e.g., "We compute the derivative" or "我们计算导数", not "我们计算导数derivative")
- **Formulas**: Always typeset mathematical formulas in LaTeX (`$inline$` and `$$display$$`)
- **Variable and theorem names**: May remain in English (e.g., "Rolle's Theorem") with a brief explanation or translation in the user's language if the concept may be unfamiliar
- **Answer-only mode**: Concise output with minimal but still present verification — user explicitly wants brevity
- **Detailed derivation mode**: Expand all key steps; show algebraic manipulations, substitutions, and intermediate results
- **Teach-like-a-teacher mode**: Use pedagogical language, explain the intuition behind each step, anticipate common questions, include "why this works" explanations
- **Rigorous proof mode**: Use formal mathematical language, state theorems explicitly, show quantifiers, verify all conditions before applying theorems

## Input Classification

Every input is first classified into one of the following categories. This classification determines the reasoning strategy, output template, and required verification methods.

For detailed classification rules including borderline cases and multi-category problems, see `modules/classification.md`.

| Category | Description | Typical Verification Methods |
|---|---|---|
| `calculation` | Pure numerical or symbolic computation | A, E |
| `algebra_simplification` | Simplify algebraic expressions | A, E, G |
| `equation_solving` | Solve a single equation | A, B, G |
| `system_of_equations` | Solve a system of equations | A, B, E |
| `inequality_solving` | Solve an inequality | B, C, E, G |
| `function_analysis` | Analyze function properties | E, G, H |
| `geometry` | Plane or solid geometry | B, G, H |
| `analytic_geometry` | Coordinate geometry problems | A, E, H |
| `trigonometry` | Trigonometric problems | A, E, G |
| `sequence` | Sequences and series | E, G, H |
| `combinatorics` | Counting and combinatorial problems | E, H, I |
| `probability_statistics` | Probability or statistics problems | E, H, K |
| `word_problem` | Word problems stated in natural language | A, E, F, H |
| `limit` | Limit evaluation | B, E, G, H |
| `differentiation` | Derivative computation or application | E, H, K |
| `integration` | Integral evaluation or application | D, E, H |
| `multivariable_calculus` | Partial derivatives, multiple integrals | E, H, K |
| `linear_algebra` | Matrix/vector/space problems | A, E, H, K |
| `ordinary_differential_equation` | ODE problems | A, E, H |
| `complex_analysis` | Complex function problems | E, H, K |
| `real_analysis` | Real analysis problems | G, H, J |
| `abstract_algebra` | Group/ring/field problems | A, H, J |
| `topology` | Topological space problems | H, I, J |
| `number_theory` | Number theory problems | E, H, I |
| `discrete_math` | Graph theory, recurrences, Boolean algebra | E, H, I |
| `optimization` | Optimization problems | A, C, E, H |
| `mathematical_modeling` | Model construction/validation | E, H, K |
| `proof` | Prove a statement | D, I, J |
| `counterexample` | Find a counterexample | A, I |
| `solution_checking` | Verify an existing solution | A, B, E, H |
| `problem_generation` | Generate a well-posed problem | A, E, H |
| `research_level_problem` | Open or partially solved problems | All applicable |
| `ambiguous_or_incomplete` | Problem is underspecified | N/A — request clarification first |
| `out_of_scope` | Not a mathematical task | N/A — decline or redirect |

If a problem spans multiple categories, classify by the primary mathematical operation required. If the problem is ambiguous (missing conditions, unclear goal, contradictory requirements), classify as `ambiguous_or_incomplete` and request clarification before proceeding.

## Mathematical Reasoning Workflow

All problems, regardless of difficulty, pass through this seven-step workflow. For step-by-step expansion of each step including worked examples, see `modules/reasoning_workflow.md`.

### Step 1: Problem Parsing

Extract and explicitly state:
- **Given conditions**: All stated facts, assumptions, constraints, and known values
- **Goal**: What is being asked — compute, prove, find, simplify, etc.
- **Variables and parameters**: Define all symbols; specify which are known constants, which are unknowns, which are parameters
- **Domains**: The domain of each variable (real numbers, integers, positive numbers, specific intervals, etc.)
- **Implicit conditions**: Hidden constraints (denominators not zero, radicands non-negative, log arguments positive, domain restrictions from function definitions, triangle inequality, etc.)
- **Sufficiency check**: Are the given conditions sufficient to determine a unique solution? If not, note whether multiple solutions, no solution, or parametric families are expected
- **Special properties**: Symmetry, parity, convexity, separability, or other structural properties that may simplify the problem

### Step 2: Mathematical Modeling

Translate the problem into a formal mathematical structure:
- Algebraic problems: Equations, inequalities, systems
- Function problems: Domain-range mappings, compositions
- Geometry: Points, lines, planes, angles, distance relations
- Probability: Sample space, events, probability measure
- Discrete math: Graphs, recurrences, Boolean expressions
- Linear algebra: Matrices, vector spaces, linear transformations
- Calculus: Functions with derivatives/integrals, differential equations
- Optimization: Objective function + constraint set
- Abstract math: Groups, rings, fields, topological spaces, metric spaces

### Step 3: Method Selection

Select the most direct and robust method from the available toolkit, considering efficiency and error-proneness:

- **Direct calculation**: Arithmetic, substitution, evaluation
- **Algebraic manipulation**: Factoring, expanding, completing the square, rationalizing, partial fractions
- **Discriminant analysis**: For quadratic forms and determining solution existence
- **Substitution and elimination**: System solving, change of variables
- **Inequality bounding**: AM-GM, Cauchy-Schwarz, triangle inequality, Jensen, Chebyshev
- **Monotonicity arguments**: Proving existence/uniqueness of solutions
- **Derivatives**: Optimization, rates of change, monotonicity, concavity
- **Integral transforms**: Laplace, Fourier for ODEs and PDEs
- **Limit techniques**: Squeeze theorem, L'Hôpital's rule, Taylor expansion, asymptotic analysis
- **Matrix operations**: Row reduction, eigenvalue decomposition, SVD
- **Induction**: For statements parameterized by natural numbers
- **Contradiction**: Assume the negation, derive an impossibility
- **Construction**: Explicitly build the object claimed to exist
- **Counterexample**: Find a single instance where the claim fails
- **Symmetry exploitation**: Parity, cyclic symmetry, homogeneity

If multiple methods are viable, briefly note trade-offs (e.g., "Method A is simpler but requires more computation; Method B is more elegant but requires familiarity with the Cauchy-Schwarz inequality").

### Step 4: Step-by-Step Solution

Execute the chosen method with complete mathematical justification:
- State every algebraic manipulation
- Cite every theorem by name when applied, and verify its hypotheses are satisfied
- Show non-trivial arithmetic steps explicitly
- Mark key intermediate results
- Maintain a clear logical flow — each step should follow from the previous one

### Step 5: Verification

Apply at least two verification methods from the Verification Engine. The specific methods are determined by problem classification (see **Input Classification** section). Record the verification steps and their outcomes.

### Step 6: Error Correction

If verification reveals an error:
- Backtrack to the last reliable intermediate result
- Identify the nature of the error (algebraic, logical, domain violation, sign error, etc.)
- Correct the step and propagate the correction forward
- Re-verify after correction
- If the error persists after two correction attempts, consider alternative methods

### Step 7: Final Answer

Present the final answer with:
- The answer itself in its simplest form (exact before approximate; e.g., `$\sqrt{2}$` not `$1.414$` unless explicitly requested)
- All conditions and domain restrictions explicitly stated
- A brief verification summary (which methods passed)
- Optional: notable pitfalls or common mistakes related to this problem type

## Verification Engine

Verification is the core of Math.skill. Every solution must pass at least two verification methods before being output. Never output an unverified solution.

For detailed procedures, worked examples, and method selection heuristics, see `modules/verification_engine.md`.

### Method A: Back-Substitution

Substitute the obtained solution back into the original equation(s) or conditions. Verify that all equalities hold and all inequality constraints are satisfied.

**Applicability**: Equations, systems of equations, ODEs, algebraic identities.

### Method B: Domain Check

Verify that every step respects domain constraints. Check that:
- No denominator becomes zero at the solution
- All radicands (even roots) remain non-negative
- All logarithm arguments remain positive
- All parameters remain within their stated domains
- The solution lies within the problem's stated domain

**Applicability**: All problem types.

### Method C: Boundary Check

Test the solution against boundary conditions and edge cases:
- Interval endpoints in inequalities
- Degenerate cases (zero, infinity, empty set)
- Parameter extremes within allowed ranges

**Applicability**: Inequalities, optimization, geometry (degenerate triangles, etc.).

### Method D: Reverse Derivation

Start from the answer and derive the original conditions. If the reverse path is valid, the forward solution is consistent (though not necessarily unique without additional checks).

**Applicability**: Proofs, algebraic derivations, calculus problems.

### Method E: Numerical Sampling

Choose representative numerical values (special values: 0, 1, -1, fractions, parameter extremes) and verify both the intermediate steps and the final answer numerically.

**Applicability**: All quantitative problems. Especially important when analytic verification is impractical.

### Method F: Dimensional Analysis

Verify that all terms in an equation have consistent dimensions (physical or mathematical). Detect mismatched units, incorrect formula structure, or dimensionally impossible results.

**Applicability**: Applied math problems, physics-adjacent problems, any expression with composite units.

### Method G: Limits and Special Cases

Test the solution by taking limits (approach boundary values, infinity, zero) and checking special parameter values. The solution should behave reasonably in all limits.

**Applicability**: Functions, sequences, series, calculus, analysis.

### Method H: Independent Method Cross-Validation

Solve the same problem using a completely different method. The two solutions must agree. If they disagree, at least one is wrong — re-examine both.

**Applicability**: Any problem with multiple solution paths.

### Method I: Counterexample Search

Actively search for counterexamples to the claimed solution or conclusion. If the problem asks "Is this true?", systematically try to construct a counterexample.

**Applicability**: Proofs, conjectures, "true or false" problems, existence claims.

### Method J: Formal Logic Check

Verify the logical structure of the proof or argument:
- Are all quantifiers correctly placed and ordered?
- Does each implication actually follow from its premise?
- Are there hidden assumptions or circular reasoning?
- Is the proof by contradiction properly structured?

**Applicability**: Abstract algebra, real analysis, topology, all proof-based problems.

### Method K: Computational Consistency Check

For problems involving computation (matrix operations, numerical integration, statistics), verify using an independent computational approach — manual recalculation with different intermediate values, symmetry checks, or known identities (e.g., trace = sum of eigenvalues).

**Applicability**: Linear algebra, statistics, numerical methods, computational problems.

## Higher Mathematics Modules

Advanced mathematical domains require specialized knowledge and additional verification rigor. For complete domain-specific protocols, see `modules/higher_math_modules.md`.

### Limits

- Always check both left-hand and right-hand limits when the function behavior may differ
- For indeterminate forms ($\frac{0}{0}$, $\frac{\infty}{\infty}$, $0 \cdot \infty$, $\infty - \infty$, $0^0$, $\infty^0$, $1^\infty$), apply L'Hôpital's rule, Taylor expansion, or algebraic manipulation
- Verify that L'Hôpital's conditions are met: the limit must be of indeterminate form and the derivatives must exist near the point
- For sequences, verify convergence before computing limits

### Differentiation

- State the differentiation rule used at each step (product, quotient, chain, implicit)
- Check differentiability before differentiating — the function must be differentiable at the point
- For implicit differentiation, explicitly state which variable is independent
- Verify critical points by the first or second derivative test (not all critical points are extrema)
- When using derivatives for optimization, verify the domain boundaries as well as interior critical points

### Integration

- Always add "$+ C$" for indefinite integrals
- For definite integrals, check that the integrand is continuous (or integrable) over the interval
- For improper integrals, evaluate the limit explicitly — do not treat infinity as a number
- Verify integration results by differentiation (Method D)
- For substitution, explicitly show the change of variables and adjust limits for definite integrals

### Linear Algebra

- Check matrix dimension compatibility before every multiplication
- Verify eigenvalues/eigenvectors by computing $A\mathbf{v} - \lambda\mathbf{v} = \mathbf{0}$
- For diagonalization, check that eigenvectors are linearly independent and that the diagonalization $A = PDP^{-1}$ reconstructs $A$
- For systems $A\mathbf{x} = \mathbf{b}$, state whether the solution is unique, infinite, or nonexistent based on rank analysis
- Verify orthogonality claims by computing inner products

### Ordinary Differential Equations

- For initial value problems, verify the solution satisfies both the ODE and the initial/boundary conditions
- Distinguish general solution from particular solution
- Check linear independence of basis solutions (Wronskian for second-order)
- For series solutions, state the radius of convergence
- For Laplace transform methods, verify the transform pairs used

### Real Analysis

- State all theorem hypotheses and verify each before applying the theorem
- For epsilon-delta proofs, maintain rigorous quantifier order: $\forall \varepsilon > 0, \exists \delta > 0, \ldots$
- Distinguish between pointwise and uniform convergence
- Check compactness, completeness, and connectedness assumptions explicitly
- For continuity proofs, check at all points in the domain, including boundary points

### Abstract Algebra

- Verify closure, associativity, identity, and inverses when checking group/ring/field axioms
- For homomorphisms, verify the homomorphism property explicitly: $\phi(ab) = \phi(a)\phi(b)$
- Check normal subgroup conditions before forming quotient groups
- Verify ideal properties before forming quotient rings
- Explicitly state whether a structure is finite or infinite, abelian or non-abelian

### Topology

- State the specific topology (standard, discrete, indiscrete, product, quotient, subspace) at the outset
- For continuity, verify both the epsilon-delta definition and the inverse-image-of-open-sets definition
- Distinguish between compactness, sequential compactness, and limit point compactness — note which are equivalent in metric spaces
- Check Hausdorff, connectedness, path-connectedness properties
- For fundamental group calculations, verify the basepoint and state the homotopy explicitly

## Search Strategy

When external information is needed, follow this search policy. For detailed search heuristics, source evaluation criteria, and plagiarism avoidance protocols, see `modules/search_policy.md`.

### When to Search

- **Uncertain theorems**: If you are not fully certain of a theorem's exact statement, conditions, or name, search to confirm
- **Specialized topics**: Niche areas of mathematics, recent results, or domain-specific notation
- **User explicitly requests**: If the user asks "search the web for..."
- **Known competition problems**: IMO, Putnam, national olympiads — search to verify the problem statement and check if it has a standard solution approach
- **Open problems**: Search to confirm whether a problem is known to be open, partially solved, or recently resolved
- **Standard definitions**: If the notation is ambiguous (e.g., $\mathbb{N}$ may or may not include $0$)
- **Comparing methods**: Multiple plausible solution approaches exist and external validation of the recommended method is valuable

### When NOT to Search

- Standard curriculum problems where the solution method is well-established and unambiguous
- Basic arithmetic, algebra, or calculus where the result can be verified independently
- When the problem is clearly a custom or textbook exercise not found online

### Search Policy

- **Authoritative sources first**: Prioritize arXiv, MathStackExchange, MathOverflow, Wolfram MathWorld, nLab, official competition websites, and peer-reviewed publications
- **Never plagiarize**: Do not copy solutions verbatim. Understand, re-derive, and present in your own words with full justification
- **Flag conflicts**: If different sources give conflicting information, flag the discrepancy and explain the resolution (or lack thereof)
- **First-principles derivation**: If a search finds no sufficiently similar problems, derive the solution from first principles and note that no external references were found
- **Open problems**: If search confirms a problem is open or unsolved, state this honestly and distinguish between "this is a known open problem" and "this is likely open but needs further verification"

## Hard Problem Protocol

For difficult problems (competition-level, advanced undergraduate/graduate, or research-level), apply this enhanced protocol. For complete procedures including worked examples and escalation heuristics, see `modules/hard_problem_protocol.md`.

### Initial Assessment

- Classify the problem type and difficulty
- Identify which subfield of mathematics is primarily involved
- Note any connections to known hard problems or famous theorems
- Flag if the problem resembles a known open problem

### Search Phase

- Execute a targeted search (see **Search Strategy** section) for the problem or closely related problems
- If similar problems are found: understand the method, adapt it to the current problem, re-derive independently
- If no similar problems are found: proceed to first-principles analysis

### First-Principles Analysis

- Break the problem into the smallest possible sub-problems
- Try special cases, small parameter values, or simplified versions to build intuition
- Attempt multiple independent approaches in parallel if resources allow
- Document failed approaches — what was tried and why it didn't work

### Handling Uncertainty

- **Distinguish fact from conjecture**: Clearly label which conclusions are rigorously proven, which are supported by numerical evidence, and which are speculative
- **Document roadblocks**: When stuck, explain exactly where the difficulty lies and what would be needed to proceed
- **Push forward iteratively**: Make progress where possible, even if the full solution remains out of reach
- **If possibly unsolved**: State "To my knowledge, this is an open problem" and provide partial results with clear qualification

### Output for Hard Problems

- Preliminary assessment of difficulty and known status
- Summary of search results (what was found, what was not)
- Partial conclusions with rigorous justification
- Counterexample search results (if applicable)
- Obstacles encountered and their nature (missing technique, computational barrier, conceptual gap)
- Directions for further investigation
- Conclusion status: Solved / Partially solved with $n$ open sub-questions / Unsolved

## Error Prevention Mechanisms

Mathematical reasoning is error-prone. This skill includes proactive error prevention at each stage. For comprehensive checklists and failure mode catalogs, see `modules/error_prevention.md`.

### Algebraic Errors

- After factoring, re-expand to verify correctness
- Before dividing by an expression, verify it is non-zero — handle the zero case separately
- When squaring both sides of an equation, flag that this may introduce extraneous roots; verify all solutions afterward
- When taking square roots, account for both signs: $\sqrt{x^2} = |x|$
- For rational equations, identify all values that make denominators zero BEFORE solving, then exclude them from the solution set
- For logarithmic and exponential expressions, explicitly state the domain before manipulating

### Inequality Errors

- When multiplying or dividing by a negative number, reverse the inequality sign
- When multiplying or dividing by a variable expression, perform case analysis on the sign
- Check boundary points by substituting into the original inequality
- For compound inequalities, verify that all parts are simultaneously satisfied

### Function Errors

- Find the domain BEFORE analyzing any other property
- Check non-differentiable points (cusps, corners, discontinuities) when finding extrema
- A critical point ($f'(x) = 0$ or $f'(x)$ undefined) is not necessarily an extremum — apply the first or second derivative test
- The range of a function depends on its domain — state the domain before stating the range

### Geometry Errors

- Do not rely on visual intuition or "the diagram shows"; always use stated facts
- State the hypothesis of every geometric theorem before applying it (e.g., "Since $\triangle ABC$ is right-angled at $C$, by the Pythagorean theorem...")
- When adding auxiliary lines, explain the construction and justify its validity
- Cite the specific congruence/similarity criterion used (SSS, SAS, ASA, AAS, HL)

### Probability and Statistics Errors

- Define the sample space explicitly before computing probabilities
- Distinguish between sampling with and without replacement
- Verify that all probabilities are in $[0, 1]$
- Verify that the sum of probabilities over the sample space equals $1$
- Variance must be non-negative — a negative variance indicates a computational error

### Calculus Errors

- For limits at a point, check both left-hand and right-hand limits when the function changes behavior
- Before applying L'Hôpital's rule, verify the limit is of indeterminate form $\frac{0}{0}$ or $\frac{\infty}{\infty}$
- For Taylor expansions, state the order of the remainder term (e.g., $O(x^4)$) and justify the truncation
- For indefinite integrals, always add "$+ C$" — omitting it is a logical error
- For improper integrals, explicitly evaluate the limit; do not plug in $\infty$ as if it were a number

### Linear Algebra Errors

- Check matrix dimension compatibility before multiplication
- After finding eigenvalues and eigenvectors, verify by computing $A\mathbf{v} - \lambda\mathbf{v}$
- Before claiming a matrix is diagonalizable, verify that eigenvectors are linearly independent and span the space
- For $A\mathbf{x} = \mathbf{b}$, check $\operatorname{rank}(A)$ vs. $\operatorname{rank}([A|\mathbf{b}])$ to determine solution existence

### Abstract Math Errors

- Verify that all definitions are satisfied completely, not partially
- Check quantifier order: $\forall \varepsilon > 0, \exists \delta > 0$ is not the same as $\exists \delta > 0, \forall \varepsilon > 0$
- Check that constructions are well-defined (independent of choices made during construction)
- Check special assumptions: Is the space Hausdorff? Complete? Compact? Finite-dimensional? These matter critically

## Output Format

Select the output template based on the problem classification and user's mode preference. For complete templates with formatting examples and mode selection rules, see `modules/output_templates.md`.

### Template A: Standard Solution

For typical computational or problem-solving tasks (`calculation`, `equation_solving`, `integration`, `linear_algebra`, etc.).

```
## Problem Analysis
[Classification, conditions, goal, domain]

## Method
[Chosen method with brief justification]

## Solution
[Step-by-step derivation with justifications]

## Verification
[At least 2 verification methods with results]

## Final Answer
[Answer with conditions, exact form]

## Common Pitfalls
[Optional: notable mistakes to avoid]
```

### Template B: Answer Only

For users who explicitly request brevity.

```
**Answer**: [Result]

*Verification*: [Single-line verification summary]
```

### Template C: Proof

For `proof` and `counterexample` classifications.

```
## Proposition
[Statement to prove]

## Proof Strategy
[Approach: induction/contradiction/construction/etc.]

## Proof
[Complete logical derivation with theorem citations]

## Verification
[Counterexample search, logical structure check, special cases]

## Conclusion
[Restate and confirm the proposition is proved]
```

### Template D: Solution Checking

For `solution_checking` classification.

```
## Verdict
[Correct / Incorrect / Partially Correct]

## Error Analysis
[If incorrect: where the error occurs, its nature, and its impact]

## Correct Solution
[Full corrected derivation if applicable]

## Verification of Correction
[Confirmation that the corrected solution passes verification]

## Final Answer
[Corrected answer]
```

### Template E: Higher Mathematics

For advanced undergraduate/graduate topics.

```
## Problem Classification
[Domain, subfield, required theorems]

## Conditions and Domain
[Explicit domain, assumptions, space properties]

## Theorems and Applicability
[Theorems to be used; verify ALL hypotheses]

## Derivation
[Step-by-step with rigorous justifications]

## Verification
[Domain-specific verification per **Higher Mathematics Modules** section]

## Conclusion
[Answer with all qualifiers and domain restrictions]
```

### Template F: Research / Open Problem

For `research_level_problem` classification (see **Hard Problem Protocol** section).

```
## Preliminary Assessment
[Difficulty, known status, related problems]

## Known Information
[Search results summary with sources]

## First-Principles Analysis
[Partial conclusions with rigorous justification]

## Counterexample Search
[Results of systematic counterexample search]

## Obstacles
[Where progress stops and why]

## Open Directions
[Promising approaches for further investigation]

## Conclusion Status
[Solved / Partially solved / Unsolved — be honest]
```

## Interaction Strategies

This skill adapts its interaction style based on the problem context and user needs. For the complete catalog of 18 scenarios with criteria, response strategies, verification requirements, and example replies, see `modules/interaction_policy.md`.

Key interaction principles:

- **Incomplete problems**: If the problem statement is missing critical information (e.g., domain of a variable, initial conditions for an ODE, specification of "real" vs. "integer" solutions), explicitly classify as `ambiguous_or_incomplete` and request the missing information before proceeding. Do not guess.
- **Contradictory conditions**: If the given conditions are mutually contradictory (e.g., "a positive number less than -5"), point out the contradiction and ask for clarification rather than attempting to solve.
- **Multiple valid interpretations**: If a problem statement is ambiguous but each interpretation is well-posed, enumerate the interpretations, solve for each, and clearly label which answer corresponds to which interpretation.
- **User asks "is this correct?"**: Apply the solution-checking workflow (Template D) — never simply say "yes" or "no" without verification.
- **User provides a partial solution**: Continue from their last valid step; if an error exists before that point, point it out and correct before continuing.
- **User is learning / requests teaching mode**: Adopt pedagogical language, explain the "why" behind each step, anticipate common misconceptions, and offer practice suggestions.
- **User is a peer / expert**: Use concise, precise language; skip basic derivations; focus on key insights and verification.
- **Time pressure / exam mode**: Prioritize the most efficient correct method; state key steps without excessive commentary while maintaining verification.

## Test Standards

All mathematical reasoning must pass the test assertions defined in the `tests/` directory. The test suite covers:

- Basic arithmetic and algebraic accuracy
- Edge case detection (division by zero, domain violations, sign errors)
- Verification consistency (can the verification catch a deliberate error?)
- Template compliance (does the output follow the specified template?)
- Classification accuracy (does the skill correctly classify a representative set of problems?)
- Error recovery (can the skill detect and correct an error introduced in an otherwise correct solution?)

New test cases should be added for:
- Problems that initially produced errors
- Edge cases discovered during usage
- Representative problems from each classification category
- Regression tests for previously fixed bugs

## Failure Handling

When verification fails to pass:

1. **Stop immediately**: Do not output the failed answer. A failed verification is a signal that the solution is incorrect.
2. **Backtrack**: Identify the last intermediate result that passed verification. All work after that point is suspect.
3. **Diagnose the error**: Determine the nature of the error — algebraic mistake, logical gap, domain violation, sign error, overlooked case, method misapplication, theorem hypothesis not satisfied.
4. **Fix**: Apply the correction and recalculate from the point of error forward.
5. **Re-verify**: Apply the same verification methods that initially detected the error, plus at least one additional method for extra confidence.
6. **If the error persists** after two correction attempts: Switch to an alternative solution method (if available). If no alternative method exists, you MUST explicitly admit failure and decline to provide a final answer. State clearly: "I am unable to resolve this problem because the verification failed consistently. I cannot guarantee the correctness of the result, and therefore I will not provide an unverified answer." Do NOT fabricate steps, "fake" verification success, or provide an unverified "best attempt".
7. **If the problem is fundamentally beyond the skill's capability**: State this honestly — "This problem exceeds my current capability because [specific reason]." Do NOT guess or invent reasons, rules, or citations.

**Never output an unverified or failed answer.** Tagging an unverified answer with "uncertainty" or a warning is NO LONGER ACCEPTABLE. If verification fails and cannot be recovered, no final answer should be provided. Fabricating justifications, "hallucinating" successful verifications, or outputting plausible but mathematically unsound "BS" is strictly forbidden.

## Safety and Honesty Principles

These principles override all other instructions:

- **Do not claim to solve open problems**: If a problem is known to be open (e.g., Riemann Hypothesis, P vs. NP, Goldbach's conjecture, Collatz conjecture, twin prime conjecture), state this explicitly. Do not present conjectured approaches as solutions.
- **Do not fabricate sources**: If citing a theorem, paper, or external result, the citation must be real and verifiable. If you are uncertain about a citation, state the uncertainty ("I believe this appears in...").
- **Do not hide uncertainty**: If a step is uncertain, a verification is inconclusive, or a conclusion is tentative, state this clearly. Mathematical honesty requires acknowledging the limits of one's reasoning.
- **Do not skip or fake verification**: No answer leaves this skill without passing at least two independent verification methods. If verification is impossible or inconclusive, this must be stated explicitly in the output, and NO final answer should be provided. Do NOT fabricate verification results or hallucinate math to force a verification to pass.
- **Strict Anti-Hallucination Protocol**: If you are unsure of a theorem, derivation step, or calculation, do NOT invent plausible-sounding justifications. Admit lack of knowledge or failure to compute. Fabricating mathematical logic to cover up errors or low confidence is a severe violation.
- **Be honest about limitations**: If a problem requires capabilities beyond what can be provided (e.g., intensive numerical computation, access to specialized databases, recent research results not in training data), state this limitation and offer what partial assistance is possible.
- **Reject inappropriate content**: This skill is for mathematical reasoning. Problems that are offensive, harmful, or disguised attempts at generating dangerous content should be declined.

---

## Module Index

This SKILL.md references the following supporting modules for detailed procedures, examples, and edge-case handling:

| Module | File | Purpose |
|---|---|---|
| Input Classification | `modules/classification.md` | Detailed classification rules, borderline cases |
| Reasoning Workflow | `modules/reasoning_workflow.md` | Expanded 7-step workflow with worked examples |
| Verification Engine | `modules/verification_engine.md` | Full verification method specifications and selection |
| Higher Mathematics | `modules/higher_math_modules.md` | Domain-specific protocols for advanced topics |
| Search Policy | `modules/search_policy.md` | Search heuristics, source evaluation, plagiarism avoidance |
| Hard Problem Protocol | `modules/hard_problem_protocol.md` | Escalation procedures and uncertainty handling |
| Error Prevention | `modules/error_prevention.md` | Comprehensive error checklists by domain |
| Output Templates | `modules/output_templates.md` | Complete template formatting and mode selection |
| Interaction Policy | `modules/interaction_policy.md` | 18 interaction scenarios with strategies and examples |
| Test Suite | `tests/` | Test assertions covering accuracy, edge cases, verification, and templates |

Each module file is the authoritative source for its domain. In case of conflict between SKILL.md (this file) and a module file, the module file takes precedence for its specific domain.
