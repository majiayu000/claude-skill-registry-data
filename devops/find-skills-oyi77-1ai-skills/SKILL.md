---
name: find-skills
description: Use when automatically discover, evaluate, and activate community skills
  when local skills don't cover user needs. Includes credibility scoring and safety
  checks for complete OpenClaw self-sufficiency.
domain: core
author: oyi77
license: Apache-2.0
subdomain: core-platform
tags:
- find
- infrastructure
- memory
- self-improvement
- skills
version: 1.0.0
category: core
---

persona:
  name: "Sergey Brin"
  title: "The Search Expert - Master of Information Retrieval"
  expertise: ['Search', 'Information Retrieval', 'Ranking', 'Recommendations']
  philosophy: "The perfect search engine would understand exactly what you mean and give you exactly what you want."
  credentials: ['Co-founder of Google', 'PhD in Computer Science from Stanford', 'Revolutionized search']
  principles: ['Relevance is king', 'Speed matters', 'Personalize results', 'Learn from queries']



# Find Skills - Intelligent Skill Discovery System

## Overview

Automatically discover and integrate community skills from skills.sh and awesome-openclaw-skills when your local skills don't cover a need. Includes credibility scoring, safety checks, and seamless activation.

**Makes your OpenClaw complete and self-sufficient** - never say "I can't do that" again!


## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "I'll figure it out as I go" | A structured approach saves time and reduces errors. Follow the workflow in this skill rather than improvising. |
| "I already know this topic" | Familiarity breeds shortcuts. Use the checklist to verify you haven't missed critical steps. |
| "This doesn't apply to my situation" | The patterns here generalize across contexts. Adapt, don't skip — the underlying principles hold. |
| "One more tool will fix it" | Adding complexity rarely solves process gaps. Master the core workflow first. |

## When to Use
**Trigger phrases:**
- "find skills"
- "Automatically discover, evaluate, and activate community skills when local skill"


**Automatic Activation** when:
- User asks "how do I do X" where X isn't covered by local skills
- User says "find a skill for X" or "is there a skill for X"
- User asks "can you do X" where X is specialized
- User wants to extend agent capabilities
- User mentions wishing for help with a specific domain

**Examples**:
- "How do I optimize my React app?" → Search for React performance skills
- "Can you help with Docker?" → Search for Docker skills
- "I need to create a changelog" → Search for changelog skills

## Skill Discovery Process
1. Validate input and check prerequisites
2. Initialize required connections and contexts
3. Execute core operation with monitoring
4. Validate output against expected format
5. Deliver results and log execution summary


### Step 1: Check Local Skills First

```javascript
function checkLocalSkills(userRequest) {
  // Check .skill-activation.json
  const localSkills = loadActivationRules();
  
  // Search by keywords
  const matches = findMatchingSkills(userRequest, localSkills);
  
  if (matches.length > 0) {
    return { found: true, skills: matches, source: 'local' };
  }
  
  return { found: false };
}
```

### Step 2: Search Community Skills

```bash
# Search skills.sh
npx skills find [query]

# Example searches
npx skills find react performance
npx skills find docker deployment
npx skills find api testing
```

**Search Strategy**:
1. Extract key terms from user request
2. Search skills.sh first (curated, high quality)
3. Fall back to awesome-openclaw-skills (comprehensive)
4. Return top 5 results ranked by credibility

### Step 3: Evaluate Credibility

**Credibility Score** (0-100):

```javascript
function calculateCredibilityScore(skill) {
  let score = 0;
  
  // 1. Usage Stats (40 points)
  const usageCount = skill.usageCount || 0;
  if (usageCount > 100000) score += 40;
  else if (usageCount > 50000) score += 35;
  else if (usageCount > 10000) score += 30;
  else if (usageCount > 5000) score += 25;
  else if (usageCount > 1000) score += 20;
  else score += Math.min(usageCount / 50, 15);
  
  // 2. Author Reputation (30 points)
  const trustedAuthors = [
    'vercel-labs',
    'anthropics',
    'obra',
    'supabase',
    'remotion-dev',
    'expo',
    'better-auth'
  ];
  
  if (trustedAuthors.includes(skill.author)) {
    score += 30;
  } else if (skill.authorStars > 1000) {
    score += 25;
  } else if (skill.authorStars > 500) {
    score += 20;
  } else {
    score += Math.min(skill.authorStars / 25, 15);
  }
  
  // 3. Update Frequency (15 points)
  const daysSinceUpdate = getDaysSince(skill.lastUpdated);
  if (daysSinceUpdate < 30) score += 15;
  else if (daysSinceUpdate < 90) score += 12;
  else if (daysSinceUpdate < 180) score += 8;
  else if (daysSinceUpdate < 365) score += 5;
  else score += 2;
  
  // 4. Documentation Quality (15 points)
  if (skill.hasExamples) score += 5;
  if (skill.hasCodeSamples) score += 5;
  if (skill.descriptionLength > 500) score += 5;
  
  return Math.min(score, 100);
}
```

**Safety Thresholds**:
- **90-100**: Auto-install (trusted sources)
- **70-89**: Recommend with high confidence
- **50-69**: Recommend with caution
- **Below 50**: Show but warn user

### Step 4: Present to User

```markdown
## Found Skills for [Query]
This section covers found skills for [query] for the find-skills skill.
Key operations include input validation, core processing, and output verification.
Refer to the skill overview for detailed usage instructions.


### 🌟 Highly Recommended (Score: 95/100)
**vercel-react-best-practices** by vercel-labs
- React and Next.js performance optimization
- 137.4K uses | Updated 2 days ago
- [View Details](https://skills.sh/vercel-labs/agent-skills/vercel-react-best-practices)

**Install**: `npx skills add vercel-labs/agent-skills@vercel-react-best-practices`

### ✅ Recommended (Score: 78/100)
**react-performance-tips** by community-dev
- React optimization patterns
- 8.2K uses | Updated 1 month ago
- [View Details](https://skills.sh/community-dev#)

### ⚠️ Use with Caution (Score: 55/100)
**react-optimizer** by new-dev
- Basic React optimization
- 450 uses | Updated 6 months ago
- [View Details](https://skills.sh/new-dev#)

**Would you like me to install the top recommendation?**
```

### Step 5: Auto-Install (with Permission)

```bash
# For high-credibility skills (90+)
npx skills add vercel-labs/agent-skills@vercel-react-best-practices -g -y

# -g: Install globally (user-level)
# -y: Skip confirmation prompts
```

**After Installation**:
1. Update `.skill-activation.json` with new skill reference
2. Reload skill activation rules
3. Confirm to user that skill is now available

---

## Integration with Activation Rules
- Connects with existing toolchain via standard interfaces
- Supports webhook-based event notifications
- Compatible with CI/CD pipelines for automated workflows
- Provides structured output for downstream consumption


### Update `.skill-activation.json`

```json
{
  "skillActivation": {
    "strategy": "selective",
    "coreSkills": [
      "core/agent-docs",
      "core/joko-orchestrator",
      "core/find-skills"
    ],
    "externalSkills": {
      "vercel-labs/agent-skills": {
        "skills": [
          "vercel-react-best-practices",
          "next-best-practices"
        ],
        "credibilityScore": 95,
        "installedDate": "2026-02-17",
        "autoUpdate": true
      },
      "obra/superpowers": {
        "skills": [
          "systematic-debugging",
          "test-driven-development"
        ],
        "credibilityScore": 92,
        "installedDate": "2026-02-17",
        "autoUpdate": true
      }
    },
    "fallbackBehavior": {
      "searchCommunity": true,
      "minCredibilityScore": 70,
      "autoInstallThreshold": 90,
      "askUserBelow": 90
    }
  }
}
```

---

## Credibility Indicators
This section covers credibility indicators for the find-skills skill.
Key operations include input validation, core processing, and output verification.
Refer to the skill overview for detailed usage instructions.


### Trusted Sources (Auto-Install at 90+)

| Author | Reputation | Why Trusted |
|--------|-----------|-------------|
| **vercel-labs** | ⭐⭐⭐⭐⭐ | Official Vercel engineering team |
| **anthropics** | ⭐⭐⭐⭐⭐ | Official Anthropic (Claude) team |
| **obra** | ⭐⭐⭐⭐⭐ | Superpowers creator, trusted community leader |
| **supabase** | ⭐⭐⭐⭐⭐ | Official Supabase team |
| **remotion-dev** | ⭐⭐⭐⭐ | Official Remotion video team |
| **expo** | ⭐⭐⭐⭐ | Official Expo/React Native team |

### Red Flags (Warn User)

- ⚠️ No updates in 1+ year
- ⚠️ Less than 100 uses
- ⚠️ Unknown author with no GitHub stars
- ⚠️ No documentation or examples
- ⚠️ Suspicious package name
- ⚠️ Requests unusual permissions

---

## Automation Examples
```
# Basic usage
invoke <skill-name> with appropriate parameters

# Advanced usage with options
invoke <skill-name> --option value --verbose
```


### Example 1: User Asks for React Help

```
USER: "How do I make my React app faster?"

AGENT:
1. Check local skills → No React performance skill found
2. Search community → npx skills find react performance
3. Evaluate results:
   - vercel-react-best-practices (Score: 95)
   - react-performance-patterns (Score: 82)
4. Present top result to user
5. Offer to install

RESPONSE:
"I found a highly-rated skill for React performance optimization!

**vercel-react-best-practices** (Credibility: 95/100)
- Official Vercel engineering guidelines
- 137.4K uses, updated 2 days ago

Would you like me to install it? This will give me comprehensive React and Next.js optimization knowledge."
```

### Example 2: User Needs Docker Help

```
USER: "Can you help me with Docker?"

AGENT:
1. Check local skills → No Docker skill found
2. Search → npx skills find docker
3. Find: docker-expert (Score: 92)
4. Auto-install (score > 90)
5. Update activation rules
6. Confirm to user

RESPONSE:
"✅ I've installed the 'docker-expert' skill (Credibility: 92/100)!

I can now help you with:
- Docker containerization
- Dockerfile optimization
- Docker Compose
- Container debugging
- Best practices

What Docker task would you like help with?"
```

### Example 3: Low Credibility Skill

```
USER: "Find a skill for blockchain development"

AGENT:
1. Search → npx skills find blockchain
2. Find: crypto-dev-helper (Score: 48)
3. Below threshold (< 70)
4. Warn user

RESPONSE:
"⚠️ I found a skill for blockchain development, but it has low credibility:

**crypto-dev-helper** (Credibility: 48/100)
- Only 320 uses
- Last updated 8 months ago
- Unknown author

I recommend:
1. Searching for more established blockchain skills
2. Using general development skills instead
3. Proceeding with caution if you choose to install

Would you like me to search for alternatives?"
```

---

## Safety Features
- Core operation execution with comprehensive error handling
- Input validation and output quality assurance
- Integration with existing workflows and toolchains
- Detailed logging for debugging and audit trails


### 1. Sandboxed Evaluation
```javascript
// Before installing, check skill metadata
function evaluateSkillSafety(skill) {
  const risks = [];
  
  // Check for suspicious patterns
  if (skill.requiresSystemAccess) {
    risks.push('Requires system-level access');
  }
  
  if (skill.hasExternalDependencies) {
    risks.push('Has external dependencies');
  }
  
  if (skill.modifiesGlobalState) {
    risks.push('Modifies global configuration');
  }
  
  return {
    safe: risks.length === 0,
    risks: risks
  };
}
```

### 2. User Confirmation
```
For scores 70-89:
"This skill looks good but I recommend reviewing it first.
[View on skills.sh] [Install Anyway] [Skip]"

For scores < 70:
"⚠️ This skill has low credibility. I don't recommend installing it.
[View Details] [Install at Your Own Risk] [Cancel]"
```

### 3. Rollback Capability
```bash
# If skill causes issues
npx skills remove vercel-labs/agent-skills@vercel-react-best-practices

# Restore previous activation rules
git checkout .skill-activation.json
```

---

## Workflow Integration
1. Receive input and validate format
2. Route to appropriate handler based on input type
3. Execute core operation with monitoring
4. Transform output to expected format
5. Return results or trigger follow-up actions


### Daily Routine Assistant

```javascript
// Morning routine
async function morningRoutine() {
  // Check for skill updates
  await run('npx skills check');
  
  // Update high-credibility skills
  const updates = await getAvailableUpdates();
  for (const skill of updates) {
    if (skill.credibilityScore >= 90) {
      await run(`npx skills update ${skill.name}`);
    }
  }
  
  // Report to user
  console.log('✅ Skills updated and ready for the day!');
}
```

### Continuous Learning

```javascript
// Track what skills are used most
function trackSkillUsage() {
  // Log skill activations
  // Identify gaps
  // Suggest new skills proactively
  
  if (userFrequentlyAsksAbout('testing')) {
    suggestSkill('javascript-testing-patterns');
  }
}
```

---

## Best Practices
This section covers best practices for the find-skills skill.
Key operations include input validation, core processing, and output verification.
Refer to the skill overview for detailed usage instructions.


### 1. Always Check Local First
Don't search community if you already have the capability.

### 2. Prefer High-Credibility Sources
Trust vercel-labs, anthropics, obra over unknown authors.

### 3. Keep Skills Updated
```bash
# Weekly update check
npx skills check
npx skills update
```

### 4. Monitor Skill Performance
- Track which skills are actually helpful
- Remove unused skills
- Report issues to skill authors

### 5. Contribute Back
- If you create useful skills, publish them
- Share improvements with community
- Help others discover your Indonesian-specific skills

---

## Commands Reference

```bash
# Search for skills
npx skills find [query]

# Install skill
npx skills add <owner/repo@skill> -g -y

# Check for updates
npx skills check

# Update all skills
npx skills update

# Remove skill
npx skills remove <owner/repo@skill>

# List installed skills
npx skills list
```

---


## When NOT to Use

- When the task requires domain expertise the agent has not been configured with
- When human review is mandated by compliance or regulatory requirements
- When the task is too trivial to warrant this skill
- When a more appropriate skill exists

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll do this later" | Explain why this excuse is wrong for this skill |
| "This is simple, skip steps" | Even simple tasks benefit from process |

## Red Flags

- Agent output is not validated against expected quality standards
- Prerequisites are not verified before task execution
- Watch for shortcuts and skipped steps

## Verification

After completing this skill, confirm:

- [ ] Output meets the defined quality and completeness requirements
- [ ] All prerequisites are verified and documented
- [ ] All required outputs generated
- [ ] Success criteria met

## Related Skills

- `core/agent-docs` - Documentation for agent capabilities
- `core/joko-orchestrator` - Orchestrate multiple skills
- All your custom skills (payment, social media, etc.)

---

**Last Updated**: 2026-02-17  
**Purpose**: Make OpenClaw complete and self-sufficient  
**Key Feature**: Intelligent skill discovery with credibility scoring

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality
