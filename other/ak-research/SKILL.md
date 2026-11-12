---
name: ak-research
description: "Research technical solutions, analyze architectures and gather requirements."
when_to_use: "Invoke before implementation to evaluate technology or best practices."
category: workflow
keywords: [research, evaluation, analysis, solutions]
license: Proprietary
argument-hint: "[topic] [--ultra] [--yagni]"
metadata:
  author: agentkit
  version: "1.1.3"
---

# Research

## Research Methodology

Always honoring **KISS** and **DRY** principles. Deliver the full requested scope — never trim or defer what the user explicitly asked for. Add nothing unrequested. With `--yagni`, additionally challenge and cut any scope not needed for the stated outcome.
**Be honest, be brutal, straight to the point, and be concise.**

### Phase 1: Scope Definition

First, you will clearly define the research scope by:
- Identifying key terms and concepts to investigate
- Determining the recency requirements (how current must information be)
- Establishing evaluation criteria for sources
- Setting boundaries for the research depth

### Phase 2: Systematic Information Gathering

You will employ a multi-source research strategy:

1. **Search Strategy**:
   - Use the runtime's native `web_search capability` for current external research.
   - Treat legacy `.claude/.ck.json` keys `skills.research.useGemini` and `gemini.model` as compatibility input only; they do not enable retired CLI dispatch.
   - Run multiple independent `web_search capability` queries in parallel when the runtime supports parallel tool calls.
   - Craft precise search queries with relevant keywords
   - Match queries to the decision question, relevant version and required recency
   - Search for official documentation, GitHub repositories, and authoritative blogs
   - Prioritize results from recognized authorities (official docs, major tech companies, respected developers)
   - Respect explicit user budgets. Otherwise stop when requested questions have credible coverage, disagreements are explained and gaps recorded; do not impose an arbitrary tool-call cap or search without a decision-relevant gap.

2. **Deep Content Analysis**:
   - When you found a potential Github repository URL, use `ak-docs-seeker` skill to find read it.
   - Focus on official documentation, API references, and technical specifications
   - Analyze README files from popular GitHub repositories
   - Review changelog and release notes for version-specific information

3. **Video Content Research**:
   - Prioritize content from official channels, recognized experts, and major conferences
   - Focus on practical demonstrations and real-world implementations

4. **Cross-Reference Validation**:
   - Verify information across multiple independent sources
   - Check publication dates to ensure currency
   - Identify consensus vs. controversial approaches
   - Note any conflicting information or debates in the community

### Phase 3: Analysis and Synthesis

You will analyze gathered information by:
- Identifying common patterns and best practices
- Evaluating pros and cons of different approaches
- Assessing maturity and stability of technologies
- Recognizing security implications and performance considerations
- Determining compatibility and integration requirements

### Phase 4: Report Generation

**Notes:**
- Research reports are saved using `Report:` path from `## Naming` section.
- If `## Naming` section is not available, ask main agent to provide the output path.

For broad deliverables, use `references/report-template.md` selectively. A narrow question needs the answer, supporting sources, scope/version and uncertainty:

## Quality Standards

You will ensure all research meets these criteria:
- **Accuracy**: Information is verified across multiple sources
- **Currency**: Prioritize information from the last 12 months unless historical context is needed
- **Completeness**: Cover all aspects requested by the user
- **Actionability**: Provide practical, implementable recommendations
- **Clarity**: Use clear language, define technical terms, provide examples
- **Attribution**: Always cite sources and provide links for verification

## Special Considerations

- When researching security topics, always check for recent CVEs and security advisories
- For performance-related research, look for benchmarks and real-world case studies
- When investigating new technologies, assess community adoption and support levels
- For API documentation, verify endpoint availability and authentication requirements
- Always note deprecation warnings and migration paths for older technologies

## Output Requirements
Use the provided report path or repository convention; load organization guidance only for a real unresolved layout decision.

Your final report must:
1. Be saved using the `Report:` path from `## Naming` section with a descriptive filename
2. Include a timestamp of when the research was conducted
3. Provide clear section navigation with a table of contents for longer reports
4. Use code blocks with appropriate syntax highlighting
5. Include diagrams or architecture descriptions where helpful (in mermaid or ASCII art)
6. Conclude with specific, actionable next steps

Lead with the outcome. Keep reports short by being selective, not by compressing the writing into fragments or arrow chains; write complete sentences.
In reports, list any unresolved questions at the end, if any.


## Ultra Verifier Mode (`--ultra`)

When `--ultra` is present, produce the research as a best-of-5 verifier pass
instead of a single report. The controller builds one immutable evidence packet
(the topic, scope definition from Phase 1, recency requirements, and evaluation
criteria) plus a rubric, dispatches exactly five independent read-only candidate
researchers in one parallel wave, then a single strongest-model verifier scores
and ranks the five reports.

- **Candidate task:** each candidate runs Phases 2-4 independently and produces
  a complete research report (each candidate honors the per-run search budget).
- **Rubric:** source quality and currency, cross-source verification, coverage
  of the requested scope, actionability of recommendations, and honesty about
  conflicting evidence.
- **Finalizer:** the verifier selects the single winning report unchanged (or
  rejects all); the controller saves that winner and records a short ranking
  appendix. On reject-all, hard-stop and report why.

Full mechanics — evidence packet, anonymization, the five-usable-candidate gate,
reject-all, and the fail-closed runtime rule — are in
`../ak-brainstorm/references/ultra-verifier-mode.md`. `--ultra` composes with
`--yagni`. It is a best-of-5 verifier mode inspired by LLM-as-a-Verifier, not
the full framework; never claim its logprob/tournament algorithm.
