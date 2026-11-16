---
name: agency-agents
description: "Library of 232 AI agent personalities across 16 business divisions — Engineering, Design, Sales, Marketing, Security, Finance, Game Dev, GIS, Academic and more. Platform-agnostic (Claude Code, Cursor, Copilot, Windsurf, Aider, Gemini CLI). Triggers on: 'agency agents', 'agent library', 'agent personalities', '232 agents', 'agent divisions', 'specialized AI agents', 'frontend developer agent', 'security architect agent', 'paid media agent', 'AI team structure', 'company as agents', 'multi-division agents', 'agent role catalog', 'msitarzewski agency', 'install agent roles', 'agent markdown files', 'cross-platform agent'."
origin: msitarzewski/agency-agents (MIT)
license: MIT
version: "1.0.0"
compatibility: "yana-ai >= 0.41.0"
allowed-tools: Bash, Read, WebFetch
---

# Agency Agents — 232 Agent Library
# Source: msitarzewski/agency-agents (MIT)
# Tier: TIER 3 — PRODUCTIVITY

Thư viện 232 agent personalities theo cơ cấu công ty — plain markdown, chạy trên 12+ AI tools.

**Do NOT use for:** Yana AI internal agents (khác biệt về architecture), `agents-v2.md` (Yana AI orchestration rules).

---

## Cơ cấu 16 division

```
Engineering       Frontend Dev · Backend Architect · AI Engineer · DevOps Automator
Design            UI Designer · UX Researcher · Brand Guardian · Whimsy Injector
Paid Media        PPC Strategist · Search Query Analyst · Creative Strategist
Sales             Outbound Strategist · Discovery Coach · Deal Strategist
Marketing         Growth Hacker · Content Creator · Social Media Strategist
Product           Sprint Prioritizer · Trend Researcher · Product Manager
Proj. Management  Studio Producer · Project Shepherd · Operations Manager
Security          Security Architect · Penetration Tester · Incident Responder
Testing           Evidence Collector · Reality Checker · Performance Benchmarker
Support           Support Responder · Analytics Reporter · Finance Tracker
Game Development  Game Designer · Level Designer · Technical Artist
GIS               Web GIS Developer · Spatial Data Engineer · Cartography Designer
Academic          Anthropologist · Historian · Psychologist
Finance           Bookkeeper · Financial Analyst · Tax Strategist
Spatial Computing XR Interface Architect · Vision Pro Engineer
Specialized       50+ unique specialists cho niche domains
```

---

## Cài đặt

```bash
# Clone repo
git clone https://github.com/msitarzewski/agency-agents
cd agency-agents

# Install cho một tool cụ thể
./scripts/install.sh --tool cursor        # → .cursor/rules/
./scripts/install.sh --tool claude-code   # → CLAUDE.md agents section
./scripts/install.sh --tool copilot       # → .github/copilot-instructions.md
./scripts/install.sh --tool windsurf      # → .windsurfrules

# Convert từ format này sang format khác
./scripts/convert.sh --from claude-code --to cursor
```

---

## Cách hoạt động

Agents được kích hoạt bằng cách mention trong conversation:

```
Người dùng: "@Frontend Developer, build me a responsive navbar in React"

→ Frontend Developer agent responds với:
  - Tech stack đề xuất (React + Tailwind)
  - Component structure
  - Code đầy đủ với accessibility
  - Testing approach
```

### Multi-agent collaboration

```
# Ví dụ: Paid Media takeover workflow
Người dùng: "Run a paid media audit on our Google Ads account"

→ Auditor          — comprehensive audit + findings report
→ Tracking Specialist — verify all conversion tracking
→ PPC Strategist   — redesign campaign structure
→ Creative Strategist — refresh ad copy + creatives
→ Analytics Reporter — setup dashboard + KPIs
```

---

## Cấu trúc agent (markdown format)

```markdown
# [Agent Name] [Emoji]
[One-line description]

## Identity & Memory
[Personality + background + communication style]

## Core Mission
[Primary objective — what this agent optimizes for]

## Critical Rules
[Domain-specific non-negotiables]

## Technical Deliverables
[Real output examples với code/templates]

## Workflow Process
1. [Step 1]
2. [Step 2]
...

## Success Metrics
[Measurable outcomes — không phải vibes]
```

---

## Platform compatibility

| Tool | Install method | Format |
|------|---------------|--------|
| Claude Code | `./scripts/install.sh --tool claude-code` | CLAUDE.md section |
| Cursor | `./scripts/install.sh --tool cursor` | `.cursor/rules/` |
| GitHub Copilot | `./scripts/install.sh --tool copilot` | `.github/copilot-instructions.md` |
| Windsurf | `./scripts/install.sh --tool windsurf` | `.windsurfrules` |
| Aider | `./scripts/install.sh --tool aider` | `.aider.conf.yml` |
| Gemini CLI | `./scripts/install.sh --tool gemini` | gemini config |
| Qwen Code | `./scripts/install.sh --tool qwen` | format tương đương |

---

## Tạo agent mới

```markdown
# My Custom Agent 🎯
Expert in [domain].

## Identity & Memory
Bạn là [persona]. Background: [experience]. Communication: [style].

## Core Mission
[Single sentence — primary goal]

## Critical Rules
- [Rule 1 — non-negotiable]
- [Rule 2]

## Technical Deliverables
[Example output với code]

## Workflow Process
1. Gather requirements
2. Plan approach
3. Execute with evidence
4. Validate output

## Success Metrics
- [Measurable outcome 1]
- [Measurable outcome 2]
```

---

## Dùng với Yana AI

Agency Agents là external agent *personalities* — dùng để enrich prompts, không replace Yana AI's rule system:

```typescript
// Load agent personality vào system prompt
import { readFileSync } from 'fs'

function loadAgentPersonality(division: string, role: string): string {
  return readFileSync(
    `agency-agents/${division}/${role}.md`,
    'utf-8'
  )
}

const systemPrompt = [
  loadAgentPersonality('engineering', 'backend-architect'),
  '---',
  'Additional constraints: follow Yana AI core/rules/*',
].join('\n')
```

---

## Anti-Fake-Pass Checks

```
❌ FAIL nếu agent chỉ có generic advice mà không có concrete deliverables
❌ FAIL nếu install script không tạo file đúng path cho tool được chọn
❌ FAIL nếu "Success Metrics" chỉ có vibes ("great results") thay vì measurable outcomes
✅ PASS khi: agent output có ít nhất 1 code example hoặc template cụ thể
✅ PASS khi: convert.sh tạo đúng format cho target tool (verify bằng diff)
```

## See also

- `ai-system-prompts-intel` — phân tích system prompts của 30+ AI tools
- `agents-v2.md` — Yana AI internal agent orchestration rules
- `subagent-policy.md` — cách spawn subagents trong Yana AI
