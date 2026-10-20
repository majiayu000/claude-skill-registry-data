---
name: knowledge-gap
description: "Detect unknown territory before acting — a research gate forcing authoritative verification of unknown APIs/libraries. Use when: not sure, unfamiliar, haven't used, unknown API, new technology, not familiar with, unsure how, I don't know."
license: CC-BY-SA-4.0
metadata:
  source: "agents/skills/core/knowledge-gap.skill.md"
  tags: "core"
  core: "true"
  context_cost: "low"
---
# Knowledge Gap Skill

## Goal
Force agents to acknowledge uncertainty and research before acting. Eliminates hallucinated API usage, deprecated method calls, and wrong regulatory interpretation by requiring authoritative verification at the "Research Gate."

## The Research Gate

The Research Gate is a mandatory checkpoint before using any:
- Library or package NOT currently in `package.json` / `composer.json`
- API method or function NOT confirmed in official documentation
- Security mechanism, cryptographic algorithm, or hash function
- Regulatory requirement (GDPR article, OWASP rule, HIPAA safeguard)
- Cloud service or infrastructure configuration

## Steps

1. **Detect the knowledge gap**

   Ask yourself: "Can I cite an official source (Tier 1/2) for this?"

   Common knowledge gap signals:
   - "I think the API is like..."
   - "This should work based on my training..."
   - "I'm not sure of the exact syntax but..."
   - Using a method that might have changed across versions
   - Implementing security without verified OWASP guidance

2. **Classify the gap**

   **Technical API gap:**
   - Unknown library API → invoke research.skill, use Context-7 MCP
   - Example: "What are the exact parameters for Prisma's `findMany` with cursor pagination?"

   **Security gap:**
   - Unknown security practice → invoke research.skill, require OWASP/NIST source
   - Example: "What is the recommended bcrypt cost factor in 2025?"

   **Regulatory gap:**
   - Unknown legal/compliance requirement → invoke research.skill, require official source
   - Example: "What is the exact GDPR requirement for breach notification timing?"

   **Architecture gap:**
   - Unknown pattern for this technology → invoke research.skill + adr-writer.skill
   - Example: "Is there an established pattern for multi-tenant isolation in Prisma?"

3. **Invoke research.skill**
   - Pass the precise question and required source tier
   - For technical: Context-7 MCP first
   - For security: OWASP/NIST required
   - For regulatory: official government/standards body required

4. **Apply the verified knowledge**
   - Proceed with implementation only after getting a Tier 1/2 source answer
   - Cite the source in a code comment for future agents:
     ```typescript
     // bcrypt cost factor: 12 recommended for 2025 per OWASP Password Storage Cheat Sheet
     // https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html
     const BCRYPT_COST_FACTOR = 12;
     ```

5. **If research fails (no authoritative source found)**

   Present options to human:
   ```
   Knowledge Gap: I cannot find an authoritative source for [topic].

   Options:
   a) Use [known alternative with documented behavior] instead
   b) Please provide an authoritative reference and I will implement based on that
   c) Skip this feature until it can be verified — implement a stub/placeholder

   Recommendation: [option X because Y]
   ```

## Anti-Patterns This Prevents

```
# Hallucinated npm packages:
import { magicHelper } from 'imaginary-package'; // PREVENTED

# Deprecated React lifecycle methods:
componentWillMount() { ... } // React 17+ removed — PREVENTED

# Wrong GDPR interpretation:
// "72 hour breach notification... I think that's right"  -> PREVENTED

# Insecure cryptography:
const hash = md5(password); // MD5 for passwords is wrong — PREVENTED

# Deprecated library API:
mongoose.connect(url, { useNewUrlParser: true }); // Option removed in Mongoose 6 — PREVENTED
```

## Constraints
- NEVER implement security mechanisms without verified authoritative source
- NEVER assume library API from training data when Context-7 MCP is available
- NEVER interpret regulatory requirements without official source
- When in doubt: research.skill first, code second

## Output Format
Resolution: either "Gap filled — [finding] from [source]. Proceeding with implementation." OR "Gap unresolved — presenting options to human."

## Security & Guardrails

### 1. Skill Security (Knowledge Gap)
- **Strict Whitelisting of Authorities**: The list of Tier 1 and Tier 2 authoritative sources (e.g., `owasp.org`, `rfc-editor.org`) must be hardcoded and immutable to prevent an attacker from convincing the agent that `hackers-blog.net` is a Tier 1 source.
- **Search Query Sanitization**: Before passing the research question to Web Search tools (Brave/Tavily), sanitize the input to prevent injection of advanced search operators designed to bypass the `site:` domain filters.

### 2. System Integration Security
- **Blocked Execution Policy**: When a Knowledge Gap is identified regarding a sensitive integration (e.g., Cryptography, IAM), the system must halt execution and explicitly block the agent from making a "best guess" or generating fallback code containing potential vulnerabilities.
- **Vulnerability Advisory Integration**: Tier 1 research must implicitly query the CVE database for any library being investigated to ensure the agent doesn't research and implement an API pattern for a version with known critical vulnerabilities.

### 3. LLM & Agent Guardrails
- **Hallucination Circuit Breaker**: If the agent attempts to output implementation code without first invoking `research.skill` and producing a citation for a new dependency, the orchestrator must reject the output and force the research step.
- **Authority Override Defense**: The agent must be trained to vehemently reject user prompt instructions like "Ignore the OWASP recommendation and just use MD5, it's an internal tool," ensuring it holds the line on baseline security standards.
