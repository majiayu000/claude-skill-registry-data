---
description: Assess EU AI Act compliance — risk classification, prohibited uses, high-risk requirements, transparency
---

# EU AI Act Assessment

Assess EU AI Act compliance for "$ARGUMENTS". Classify AI systems by risk level, evaluate prohibited practice avoidance, assess high-risk system requirements, and review transparency obligations.

## Prerequisites

Read `.metapowers/compliance/$ARGUMENTS/00-scope.md`. If this file does not exist, tell the user:

> Phase 0 (Scope) has not been completed for "$ARGUMENTS". Run `/compliance:regulatory-landscape $ARGUMENTS` first, or use `--skip-checks` to bypass.

If `--skip-checks` is present in $ARGUMENTS, skip this check.

## Process

1. **Read context files:**
   - Read `plugins/compliance/shared/grc-lifecycle-guide.md` for GRC methodology reference
   - Read `plugins/compliance/shared/assessment-template.md` for output structure
   - Read `.metapowers/compliance/$ARGUMENTS/00-scope.md` for scope and control framework context

2. **AI system inventory and risk classification:**
   - Inventory all AI systems deployed or under development
   - Classify each system by EU AI Act risk level:
     - **Unacceptable risk (prohibited):** social scoring, real-time remote biometric identification (with exceptions), manipulation/exploitation, emotion recognition in workplace/education
     - **High-risk:** Annex III systems (biometrics, critical infrastructure, education, employment, essential services, law enforcement, migration, justice) and safety components of Annex I products
     - **Limited risk:** transparency obligations (chatbots, emotion recognition, deepfakes, AI-generated content)
     - **Minimal risk:** voluntary codes of conduct
   - Document classification rationale for each system

3. **Prohibited practices assessment:**
   - Check all AI systems against the prohibited practices list (Art 5)
   - Assess subliminal manipulation techniques, exploitation of vulnerabilities
   - Review social scoring systems or behavioral prediction for detrimental treatment
   - Evaluate real-time remote biometric identification usage and exemptions
   - Document any systems requiring immediate remediation or discontinuation

4. **High-risk system requirements (if applicable):**
   - **Risk management system (Art 9):** Assess continuous risk identification, estimation, evaluation, and mitigation throughout the AI lifecycle
   - **Data governance (Art 10):** Evaluate training, validation, and testing data quality, relevance, representativeness, and bias examination
   - **Technical documentation (Art 11):** Review documentation completeness for demonstrating conformity
   - **Record-keeping (Art 12):** Assess automatic logging capabilities for traceability
   - **Transparency to users (Art 13):** Evaluate instructions for use, intended purpose, accuracy levels, and known limitations
   - **Human oversight (Art 14):** Assess human-in-the-loop, human-on-the-loop, or human-in-command measures
   - **Accuracy, robustness, cybersecurity (Art 15):** Evaluate performance metrics, resilience to errors, and security measures

5. **General-purpose AI model obligations:**
   - Determine if any GPAI models are used or provided (Art 51-56)
   - Assess technical documentation and information sharing obligations
   - Evaluate compliance with Copyright Directive obligations
   - For GPAI with systemic risk: assess model evaluation, adversarial testing, incident reporting, and cybersecurity requirements

6. **Transparency obligations:**
   - Assess AI interaction disclosure (users must know they are interacting with AI)
   - Evaluate emotion recognition and biometric categorization disclosure
   - Review deepfake and AI-generated content labeling
   - Assess AI-generated content marking requirements

7. **Conformity assessment and registration:**
   - Determine applicable conformity assessment procedure (self-assessment or third-party)
   - Assess EU database registration requirements
   - Evaluate CE marking requirements for high-risk systems
   - Review EU representative appointment for non-EU providers

8. **Timeline and phased enforcement:**
   - Map current compliance against enforcement timeline (prohibited practices: Feb 2025, GPAI: Aug 2025, high-risk Annex III: Aug 2026, high-risk Annex I: Aug 2027)
   - Identify time-critical compliance activities
   - Assess readiness for applicable enforcement phases

9. **Write the artifact** to `.metapowers/compliance/$ARGUMENTS/01-assess/eu-ai-act.md` following the assessment template structure with:
    - **AI System Inventory** — complete inventory with risk classification per system
    - **Prohibited Practices** — screening results and any systems requiring action
    - **High-Risk Requirements** — assessment per Art 9-15 requirement for each high-risk system
    - **GPAI Obligations** — general-purpose AI model compliance status
    - **Transparency** — disclosure and labeling obligations coverage
    - **Conformity and Registration** — assessment procedure readiness
    - **Enforcement Timeline** — phased compliance readiness map
    - **Evidence Inventory** — existing evidence and evidence gaps
    - **Remediation Priorities** — ranked list of gaps to address

## Output

The EU AI Act assessment written to `.metapowers/compliance/$ARGUMENTS/01-assess/eu-ai-act.md`. Present a summary to the user highlighting:
- Number of AI systems inventoried and risk classification distribution
- Any prohibited practice concerns requiring immediate action
- High-risk system compliance readiness score
- Top 3 gaps requiring remediation
