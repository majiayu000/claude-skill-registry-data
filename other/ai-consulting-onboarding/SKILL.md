---
name: ai-consultant-onboarding
description: >
  Generates a complete, professional client onboarding package for AI consultants,
  AI auditors, and solopreneurs working in the AI space (AI strategy, automation,
  AI readiness audits, implementation, training, etc.). Use this skill whenever
  a user asks to onboard a new client, set up a client folder, write a welcome
  email, generate a discovery questionnaire, draft a service agreement, or create
  a project brief — especially in an AI consulting context. Also trigger when the
  user says things like "I have a new client", "prepare onboarding docs", "create
  a client package", or "set up a new project". Produces four ready-to-use
  deliverables: intake questionnaire, welcome email, service agreement, and
  project brief.
---

# AI Consultant Client Onboarding Skill

You are helping an AI consultant, AI auditor, or AI solopreneur onboard a new
client professionally and efficiently. Your job is to gather key details and
then generate a complete onboarding package — four polished, ready-to-use
documents tailored to the AI services world.

---

## Step 1: Gather Client Information

Before generating anything, ask the user for the following. If some information
is already provided in the conversation, extract it — don't ask again.

**Ask in a single, friendly message:**

```
To create your onboarding package, I need a few quick details:

1. **Client name** (person and/or company name)
2. **Your name / business name**
3. **Service type** — which best fits? (or describe your own)
   - AI Readiness Audit
   - AI Strategy & Roadmap
   - AI Tool Implementation
   - AI Workflow Automation
   - AI Team Training / Workshops
   - Ongoing AI Retainer / Advisory
   - Custom (describe briefly)
4. **Project scope** — one sentence about what they want to achieve
5. **Timeline** — start date and rough duration (e.g., "starting March 2026, 6 weeks")
6. **Budget / investment** (optional — leave blank to omit from agreement)
7. **Primary contact & email** at the client side
8. **Anything special** — industry, pain points, tech stack, tools they use?
```

Wait for the user's answers before proceeding.

---

## Step 2: Generate the Onboarding Package

Once you have the details, generate all four documents in sequence. Label each
one clearly with a header. Use a warm, expert, and modern tone — the kind an
in-demand AI consultant would use. Avoid corporate jargon. Be specific and
professional.

---

### Document 1: Discovery & Intake Questionnaire

**Purpose:** Sent to the client before the first call to gather context.

**Format:** Numbered questions grouped by theme.

**Sections to include:**

#### About Your Business
- What does your company do, and who are your customers?
- How large is your team, and how is it structured?
- What tools and platforms do you currently use day-to-day?

#### AI Awareness & Current State
- Have you experimented with AI tools so far? Which ones?
- What's your team's general comfort level with AI (1–5)?
- Have you had any failed AI experiments? What happened?

#### Goals & Challenges
- What's the #1 problem you're hoping AI can help solve?
- What does success look like for you after working together?
- Are there any internal blockers (budget, buy-in, technical limits)?

#### Practical & Logistical
- Who will be our main point of contact during the project?
- Are there any deadlines, events, or launches we should plan around?
- Is there anything else you'd like me to know before we start?

Customize questions based on the service type provided. For audits, add
questions about data, security, and compliance. For training, add questions
about learning styles and team availability.

---

### Document 2: Welcome Email

**Purpose:** Sent immediately after the contract is signed. Sets the tone.

**Format:** A warm, personal email. Not a template that looks like a template.

**Structure:**
- Subject line (punchy, personal, professional)
- Opening: genuine excitement about working together
- What happens next: 3–4 clear bullet points (e.g., complete questionnaire,
  schedule kickoff call, receive access to shared workspace)
- Brief overview of your working style / what they can expect from you
- Practical details: response times, preferred communication channel,
  how to reach you urgently
- Warm closing with a specific forward-looking line

**Tone:** Confident, human, enthusiastic — like a trusted expert, not a
faceless agency.

---

### Document 3: Service Agreement (Plain Language)

**Purpose:** A clear, professional agreement the client can sign quickly.

**Format:** Structured document with numbered sections.

**Note to Claude:** This is a plain-language agreement, not a legal document.
Include a disclaimer at the top: *"This is a plain-language service agreement
intended for small business use. For legally binding contracts, consult a
qualified attorney in your jurisdiction."*

**Sections:**

1. **Parties** — Full names of consultant and client
2. **Services** — Clear description of what is included (and what is not)
3. **Timeline** — Start date, milestones, end date
4. **Investment** — Total fee, payment schedule, late payment terms
   (omit if budget not provided)
5. **What You Need from the Client** — Input, access, feedback, decisions
6. **Revisions & Scope Changes** — How changes are handled
7. **Confidentiality** — Both parties keep each other's info private
8. **Intellectual Property** — Who owns what (deliverables go to client,
   consultant retains methodology)
9. **Termination** — Notice period and what happens to work in progress
10. **Signatures** — Space for both parties to sign and date

Keep language plain, fair, and direct. No legalese.

---

### Document 4: Project Brief

**Purpose:** Internal reference document and/or shared with the client as a
project overview. Creates alignment from day one.

**Format:** Clean, structured brief — professional enough to share with
stakeholders.

**Sections:**

#### Project Overview
- Client, consultant, service type
- One-paragraph description of the engagement

#### Objectives
- 3–5 specific, measurable goals for this project

#### Scope of Work
- What is included (be explicit)
- What is out of scope (be equally explicit)

#### Timeline & Milestones
- Visual-friendly breakdown (use a simple table or numbered phases)
- Key dates and deliverables per phase

#### Roles & Responsibilities
- What the consultant does
- What the client needs to provide or decide

#### Success Metrics
- How will both parties know the project succeeded?
- What does the "finish line" look like?

#### Communication & Tools
- Meeting cadence (e.g., weekly check-in, async updates)
- Tools used (e.g., Notion, Slack, Google Drive, ClickUp)
- How decisions get documented

---

## Step 3: Deliver & Offer File Export

After generating all four documents in the conversation, ask the user:

```
Your onboarding package is ready! Would you like me to:
- [ ] Export everything as a Word document (.docx)
- [ ] Export as a PDF
- [ ] Export as separate Markdown files
- [ ] Keep it here to copy-paste (no export needed)
```

If they want an export, use the appropriate skill (docx or pdf) to create the
files and present them for download.

---

## Quality Standards

- **Specificity over generality**: Use the actual client name, service type,
  and details throughout — never leave placeholder brackets like [CLIENT NAME]
  visible in the final output.
- **AI-native language**: Reference real AI concepts appropriately (LLMs,
  automation, audits, prompts, workflows) — this client is in the AI space.
- **Tone consistency**: Warm but expert. Like talking to a smart friend who
  also happens to be very good at their job.
- **No filler**: Every sentence should earn its place.
- **Length**: Questionnaire ~15 questions, welcome email ~250 words, agreement
  ~600 words, project brief ~500 words. Adjust if scope is complex.

---

## Reference Files

- `references/service-types.md` — Detailed scope notes per service type
  (audit, strategy, automation, training, retainer)
- `references/ai-industry-glossary.md` — Common AI terms to use naturally
  in documents
- `assets/email-subject-lines.md` — 20 welcome email subject line options
  by service type

Load these only if needed for extra detail or when the user's service type
is niche or complex.
