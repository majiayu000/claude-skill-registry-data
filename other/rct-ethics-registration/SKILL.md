---
name: rct-ethics-registration
description: "Handle ethical requirements, IRB approval, trial registration, and pre-analysis plans for RCTs. Use when user mentions: research ethics, IRB, informed consent, trial registration, pre-analysis plan, PAP, data security, vulnerable populations, research transparency."
---

<skill_content>

<overview>
Ethical research with human subjects requires IRB approval, informed consent, data security, and transparency through trial registration and pre-analysis plans. The Belmont Report establishes three core principles: respect for persons (autonomy, consent), beneficence (maximize benefits, minimize harms), and justice (fair distribution of burdens and benefits). Violations risk participant harm, legal liability, and inability to publish.

Ethics and transparency are prerequisites, not afterthoughts.
</overview>

<mandatory_requirements>

<requirement priority="critical">
  <name>IRB Approval Before Any Contact With Participants</name>
  <description>Obtain Institutional Review Board approval BEFORE recruiting, consenting, or enrolling any participants</description>
  <rationale>IRB review ensures participant protections, informed consent procedures, and risk minimization. Federal regulations (45 CFR 46) require approval before human subjects research</rationale>
  <consequence>Research misconduct, legal liability, inability to publish, harm to participants, institutional sanctions</consequence>
</requirement>

<requirement priority="critical">
  <name>Register Trial Before Data Collection</name>
  <description>Register trial on AEA RCT Registry, ClinicalTrials.gov, or equivalent BEFORE beginning intervention or data collection</description>
  <rationale>Pre-registration prevents publication bias, specification searching, and selective reporting. Required by many journals and funders (CONSORT guidelines)</rationale>
  <consequence>Journals may reject, results perceived as cherry-picked, inability to make credible causal claims</consequence>
</requirement>

<requirement priority="critical">
  <name>File Pre-Analysis Plan Before Seeing Outcome Data</name>
  <description>Document hypotheses, specifications, and analysis plan BEFORE accessing outcome data</description>
  <rationale>PAPs prevent p-hacking, HARKing (hypothesizing after results known), and data mining. Critical for credibility revolution</rationale>
  <consequence>Results dismissed as data-mined, loss of scientific credibility, failed publication</consequence>
</requirement>

<requirement priority="high">
  <name>Informed Consent With All Required Elements</name>
  <description>Obtain voluntary, written informed consent covering: purpose, procedures, risks, benefits, compensation, confidentiality, right to withdraw</description>
  <rationale>Respect for persons requires informed, voluntary participation. Incomplete consent violates ethical principles and federal regulations</rationale>
  <consequence>IRB violations, research misconduct findings, legal liability, inability to use data</consequence>
</requirement>

<requirement priority="high">
  <name>Data Security and Confidentiality Protections</name>
  <description>Implement encryption, de-identification, secure storage, and limited access for all participant data</description>
  <rationale>Participants trust researchers with sensitive information. Breaches violate confidentiality, harm participants, and create legal liability</rationale>
  <consequence>Data breaches, participant harm, IRB sanctions, legal penalties, loss of trust</consequence>
</requirement>

</mandatory_requirements>

<assumptions>

<assumption name="Minimal Risk Determination">
  <description>IRB classifies study as minimal risk or greater than minimal risk</description>
  <how_to_check>Submit IRB protocol, document all procedures and potential harms, compare to everyday life risks</how_to_check>
  <if_violated>More stringent review required, additional safeguards needed, possible rejection</if_violated>
</assumption>

<assumption name="Voluntary Participation">
  <description>Participants can freely choose whether to enroll without coercion or undue influence</description>
  <how_to_check>Ensure compensation not coercive, no power relationships (employer/employee), clear opt-out</how_to_check>
  <if_violated>Consent invalid, research cannot proceed ethically</if_violated>
</assumption>

<assumption name="Equipoise">
  <description>Genuine uncertainty about whether treatment is beneficial (ethical randomization requirement)</description>
  <how_to_check>Can you justify withholding treatment from control group? Is there scientific uncertainty?</how_to_check>
  <if_violated>Unethical to randomize if treatment clearly beneficial; use phase-in or observational design</if_violated>
</assumption>

</assumptions>

<thinking_process>
When preparing ethics and registration:
1. Draft research protocol with theory of change and procedures
2. Conduct power analysis to justify sample size
3. Prepare IRB protocol (purpose, procedures, risks, benefits, consent)
4. Submit to IRB 2-3 months before planned start
5. Register trial immediately after IRB approval
6. File pre-analysis plan before data collection begins
7. Implement data security protocols
8. Monitor for adverse events throughout study
9. Submit amendments if protocol changes
10. Report final results to registry and participants
</thinking_process>

<implementation_pattern>

<code_template>
```python
@app.cell
def ethics_compliance_checklist():
    # Comprehensive ethics and registration checklist
    # Use before launching any RCT to ensure compliance

    checklist = {
        "Pre-Study (Before Participant Contact)": [
            "[ ] IRB protocol drafted",
            "[ ] Informed consent forms prepared",
            "[ ] Data security plan documented",
            "[ ] IRB approval obtained",
            "[ ] Trial registered (AEA/ClinicalTrials.gov)",
            "[ ] Pre-analysis plan filed",
            "[ ] Research team trained on ethics",
        ],
        "During Study": [
            "[ ] Informed consent obtained for all participants",
            "[ ] Adverse events monitored and reported",
            "[ ] Data encrypted and securely stored",
            "[ ] IRB amendments submitted for protocol changes",
            "[ ] Annual IRB renewal obtained",
            "[ ] Trial registry updated with progress",
        ],
        "Post-Study": [
            "[ ] Final IRB report submitted",
            "[ ] Trial registry updated with results",
            "[ ] Data de-identified before sharing",
            "[ ] Results shared with community",
            "[ ] Consent forms archived per retention policy",
            "[ ] PII destroyed per protocol timeline",
        ],
    }

    print("ETHICS & REGISTRATION COMPLIANCE CHECKLIST")
    print("=" * 60)

    for phase, items in checklist.items():
        print(f"\n{phase}")
        print("-" * 40)
        for item in items:
            print(f"  {item}")

    print("\nCritical deadlines:")
    print("- IRB submission: 2-3 months before start")
    print("- Trial registration: Before data collection")
    print("- PAP filing: Before accessing outcome data")
    print("- Annual renewal: Before approval expiration")

    return checklist,
```
</code_template>

</implementation_pattern>

<examples>

<example context="informed_consent" difficulty="basic">
<description>Create informed consent form with all required elements</description>
<code>
```python
@app.cell
def informed_consent_template():
    # Informed consent template meeting federal requirements
    # Must include all 8 basic elements per 45 CFR 46.116

    consent_text = """
    INFORMED CONSENT FOR RESEARCH PARTICIPATION

    Study Title: [Title]
    Principal Investigator: [Name, contact]

    1. PURPOSE
    You are invited to participate in research studying [purpose in plain language].
    We are enrolling approximately [N] participants.

    2. PROCEDURES
    If you agree, you will:
    - [Specific procedures]
    - [Time commitment]
    - [Number of visits/contacts]

    3. RISKS
    Possible risks include:
    - [List all risks, even if minimal]
    - [Be specific and complete]
    These risks are [minimal / greater than minimal].

    4. BENEFITS
    Possible benefits to you:
    - [Direct benefits, if any]
    - [Or state clearly if no direct benefit]

    Possible benefits to others:
    - [Broader societal benefit]

    5. COMPENSATION
    You will receive [specific compensation amount and timing].
    [If no compensation, state clearly]

    6. CONFIDENTIALITY
    Your information will be kept confidential:
    - Data will be de-identified (names removed)
    - Stored on encrypted, password-protected computers
    - Only research team will access identifiable data
    - Identifiers destroyed after [time period]

    7. VOLUNTARY PARTICIPATION
    Participation is completely voluntary. You may:
    - Refuse to participate
    - Skip any questions
    - Withdraw at any time without penalty

    Your decision will not affect [services, relationships, etc.].

    8. CONTACT INFORMATION
    Questions about study: [PI contact]
    Questions about rights: [IRB contact]

    CONSENT
    [ ] I have read this form
    [ ] My questions have been answered
    [ ] I voluntarily agree to participate

    _________________________  _________
    Participant Signature      Date

    _________________________  _________
    Researcher Signature       Date
    """

    print(consent_text)

    print("\nKey requirements:")
    print("- 8th grade reading level")
    print("- All 8 basic elements included")
    print("- Voluntary nature emphasized")
    print("- Specific risks and benefits")
    print("- Contact information provided")

    return consent_text,
```
</code>
<lesson>
Informed consent requires: (1) purpose, (2) procedures, (3) risks, (4) benefits, (5) alternatives, (6) confidentiality, (7) voluntary nature, (8) contacts. Written at 8th grade level. Emphasize voluntary participation and right to withdraw.
</lesson>
</example>

</examples>

<common_mistakes>

<mistake severity="critical">
  <what>Starting participant contact before IRB approval</what>
  <consequence>Research misconduct, legal liability, inability to use data, institutional sanctions</consequence>
  <prevention>IRB approval is prerequisite. Never recruit, consent, or collect data before approval</prevention>
</mistake>

<mistake severity="critical">
  <what>Not registering trial or filing pre-analysis plan</what>
  <consequence>Journal rejection, results perceived as data-mined, loss of scientific credibility</consequence>
  <prevention>Register trial immediately after IRB approval, file PAP before accessing outcome data</prevention>
</mistake>

<mistake severity="high">
  <what>Inadequate informed consent (missing elements, coercive, not voluntary)</what>
  <consequence>IRB violations, invalid consent, ethical breach, unusable data</consequence>
  <prevention>Include all 8 required elements, ensure voluntary participation, use plain language</prevention>
</mistake>

<mistake severity="high">
  <what>Weak data security (unencrypted data, no de-identification, broad access)</what>
  <consequence>Data breaches, participant harm, IRB sanctions, legal penalties</consequence>
  <prevention>Encrypt all data, separate PII from analysis files, limit access, destroy PII per protocol</prevention>
</mistake>

<mistake severity="medium">
  <what>Not reporting adverse events or protocol deviations</what>
  <consequence>IRB sanctions, continued participant harm, research misconduct findings</consequence>
  <prevention>Monitor for adverse events, report serious events within 24 hours, document all deviations</prevention>
</mistake>

</common_mistakes>

<interpretation_guide>

<irb_review_types>
- **Exempt**: Minimal risk, no intervention, secondary data (still requires IRB determination)
- **Expedited**: Minimal risk, specific categories (surveys, interviews, some RCTs)
- **Full board**: Greater than minimal risk, vulnerable populations, deception

Timeline:
- Exempt/Expedited: 2-4 weeks
- Full board: 4-8 weeks (meets monthly typically)
- Always add 2-3 months buffer to timeline
</irb_review_types>

<vulnerable_populations>
Extra protections required for:
- Children (parental consent + child assent)
- Prisoners (special IRB composition, no coercion)
- Pregnant women (consider fetal risk)
- Cognitively impaired (capacity assessment, LAR if needed)
- Economically disadvantaged (ensure compensation not coercive)

For vulnerable populations, demonstrate why inclusion is necessary and how risks are minimized.
</vulnerable_populations>

<registration_platforms>
- Economics/social science: AEA RCT Registry (socialscienceregistry.org)
- Health/medical: ClinicalTrials.gov
- General: OSF Registries (osf.io)
- Politics: EGAP Registry (egap.org)

Minimum info: title, PIs, outcomes, sample size, timeline, hypotheses
</registration_platforms>

</interpretation_guide>

<references>
<paper>Belmont Report (1979). Ethical Principles and Guidelines for the Protection of Human Subjects of Research. National Commission.</paper>
<paper>45 CFR 46 - Protection of Human Subjects (Common Rule). U.S. Department of Health and Human Services.</paper>
<paper>CONSORT Statement. Consolidated Standards of Reporting Trials. http://www.consort-statement.org/</paper>
<paper>Casey, K., Glennerster, R., & Miguel, E. (2012). Reshaping institutions: Evidence on aid impacts using a preanalysis plan. Quarterly Journal of Economics, 127(4), 1755-1812.</paper>
<paper>Christensen, G., & Miguel, E. (2018). Transparency, reproducibility, and the credibility of economics research. Journal of Economic Literature, 56(3), 920-980.</paper>
</references>

</skill_content>
