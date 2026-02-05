---
name: candidate-kb
description: Manage candidate knowledge base. Use when ingesting CVs, adding profile information, or querying candidate details for resume/cover letter generation.
---

# Candidate Knowledge Base Skill

You help users manage their candidate knowledge base, which stores profile information and contextual data used for resume and cover letter generation. The KB ensures factual consistency across all applications.

## Storage Location

The knowledge base is stored in `candidate-kb.jsonl` in the project root. Each line is a JSON object representing one entry.

## Two-Tier Structure

### 1. Profile Entries (Structured)
Core candidate information with strict schemas:

| Category | Required Fields | Optional Fields |
|----------|----------------|-----------------|
| `contact` | name, email | phone, location, linkedin, github, website |
| `experience` | company, role, start_date | end_date, location, description, highlights |
| `education` | institution, degree | field, start_date, end_date, gpa |
| `skills` | (none) | languages, frameworks, tools, databases, cloud, other |
| `certifications` | name | issuer, date, expiry_date, credential_id |
| `languages` | language | proficiency |

### 2. Context Entries (Flexible)
Accumulated details from applications and conversations:
- Achievements with metrics
- Project details
- Industry-specific experience
- Soft skills
- Preferences (remote, relocation, salary)

## CLI Interface

```bash
# Show all KB entries
bragger kb show

# Show only profile or context
bragger kb show profile
bragger kb show context

# Add profile entry
bragger kb add --type profile --category contact --source "cv-import" \
  --data '{"name":"John Doe","email":"john@example.com"}'

# Add experience
bragger kb add --type profile --category experience --source "cv-import" \
  --data '{"company":"Acme","role":"Senior Engineer","start_date":"2020-01","end_date":"present"}'

# Add context entry
bragger kb add --type context --category achievement --source "user" \
  --content "Led migration to microservices, reducing latency by 40%"

# Update entry
bragger kb update kb-xxx --content "Updated description"

# Remove entry
bragger kb remove kb-xxx
```

## Capabilities

### 1. CV Ingestion

When user provides a CV/resume file or text, parse it and populate the KB:

**Process:**
1. Read the CV content (use Read tool for files)
2. Extract structured information for each category
3. Use CLI to add entries: `bragger kb add --type profile --category <cat> --data '<json>'`
4. Set source to "cv-import" for traceability

**Example workflow:**
```
User: "Here's my CV: [paste or file path]"

1. Parse contact info → add contact entry
2. Parse each job → add experience entries
3. Parse education → add education entries
4. Parse skills → add skills entry
5. Parse certifications → add certification entries
6. Confirm what was imported
```

### 2. Query KB for Resume Generation

When generating a resume or cover letter, query the KB first:

```bash
bragger kb show profile   # Get all profile data
bragger kb show context   # Get contextual details
```

Parse the output and use relevant information to tailor the resume.

### 3. Gap Detection

Compare JD requirements against KB to identify missing information:

1. Analyze job description for required skills/experience
2. Query KB for matching entries
3. Identify gaps
4. Prompt user to provide missing information
5. Store new information in KB for future use

**Example:**
```
JD requires: "Experience with Kubernetes"
KB has: {"tools": ["Docker", "Git"]}
Gap: No Kubernetes mentioned

Prompt: "The job requires Kubernetes experience. Do you have any experience with Kubernetes or container orchestration? If so, please describe it."

User response → Add to context or update skills
```

### 4. Add Contextual Information

During conversations, capture and store valuable details:

**User requests:**
- "I led a team of 5 engineers at my last job"
- "My project handled 10k transactions per second"
- "I prefer remote work"

**Process:**
1. Identify the category (achievement, project_detail, preference, etc.)
2. Add as context entry with source "user"

```bash
bragger kb add --type context --category achievement --source "user" \
  --content "Led team of 5 engineers"
```

### 5. Factuality Enforcement

All resume/cover letter content MUST be sourced from:
1. Profile entries in KB
2. Context entries in KB
3. Explicitly provided by user in current conversation

Never fabricate or assume information not in KB.

## Data Model

```json
// Profile entry example
{
  "id": "kb-abc123",
  "type": "profile",
  "category": "experience",
  "data": {
    "company": "Acme Corp",
    "role": "Senior Engineer",
    "start_date": "2020-01",
    "end_date": "present",
    "highlights": ["Led team of 5", "Reduced latency by 40%"]
  },
  "source": "cv-import",
  "created_at": "2025-01-01T00:00:00Z",
  "updated_at": "2025-01-01T00:00:00Z"
}

// Context entry example
{
  "id": "kb-def456",
  "type": "context",
  "category": "achievement",
  "content": "Built real-time trading system handling 10k TPS with 99.99% uptime",
  "source": "user",
  "created_at": "2025-01-01T00:00:00Z",
  "updated_at": "2025-01-01T00:00:00Z"
}
```

## Example Interactions

**User:** "Import my CV" [provides CV text or file]

**Response:**
1. Parse CV content
2. For each section, create KB entries using CLI
3. Report: "I've imported your CV and created the following entries:
   - Contact: John Doe (john@example.com)
   - Experience: 3 positions
   - Education: 2 entries
   - Skills: 15 skills across 4 categories
   - Certifications: 2 entries"

---

**User:** "What do you know about my experience?"

**Response:**
1. Run `bragger kb show experience`
2. Parse and present in readable format

---

**User:** "I also want to mention that I mentored 3 junior developers at Acme"

**Response:**
1. Add context entry:
   ```bash
   bragger kb add --type context --category achievement --source "user" \
     --content "Mentored 3 junior developers at Acme Corp"
   ```
2. Confirm: "Added to your knowledge base. I'll include this when relevant for future applications."

---

**User:** "Generate a resume for this job posting" [provides JD]

**Response:**
1. Query KB for all profile and context data
2. Analyze JD requirements
3. Identify any gaps and ask user if needed
4. Generate resume using ONLY information from KB
5. If claims can't be verified from KB, ask user to confirm
