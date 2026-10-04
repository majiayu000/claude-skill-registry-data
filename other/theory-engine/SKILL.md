---
name: theory-engine
description: >
  Activate when the user needs to select a theoretical lens, formulate a research gap,
  derive hypotheses or design principles, or write a contribution statement.
  Provides concrete theory-to-paper templates, not abstract advice.
---

> **Orchestration Log**: When this skill is activated, append a log entry to `outputs/orchestration_log.md`:
> ```
> ### Skill Activation: Theory Engine
> **Timestamp:** [current date/time]
> **Actor:** AI Agent (theory-engine)
> **Input:** [brief description of the theory selection/gap formulation request]
> **Output:** [brief description of what was produced — e.g., "Selected sociotechnical systems theory, drafted theoretical framing (800 words)"]
> ```

# Theory Engine

## Purpose
Turn "I don't know which theory to use" into a concrete theoretical framing 
with drafted paragraphs ready for the paper.

## Step 1: Match Topic to Theory

### Theory Selection by Research Topic

**AI Adoption & Implementation:**
| Theory | Use When | Key Constructs | Seminal Reference |
|--------|----------|---------------|-------------------|
| TOE Framework | Studying organizational adoption factors | Technology, Organization, Environment | Tornatzky & Fleischer (1990) |
| UTAUT/UTAUT2 | Studying individual user acceptance | Performance/Effort Expectancy, Social Influence | Venkatesh et al. (2003/2012) |
| Absorptive Capacity | Studying how orgs learn/integrate new AI knowledge | Acquisition, Assimilation, Transformation, Exploitation | Cohen & Levinthal (1990) |
| Dynamic Capabilities | Studying how orgs adapt to AI disruption | Sensing, Seizing, Reconfiguring | Teece (2007) |
| Socio-Technical Systems | Studying joint optimization of social + technical | Social subsystem, Technical subsystem, Joint optimization | Bostrom & Heinen (1977) |
| Institutional Theory | Studying mimetic/coercive/normative adoption pressures | Isomorphic pressures, Legitimacy | DiMaggio & Powell (1983) |

**AI Agents & Automation:**
| Theory | Use When | Key Constructs | Seminal Reference |
|--------|----------|---------------|-------------------|
| Agency Theory | Studying delegation to autonomous agents | Principal, Agent, Information asymmetry | Eisenhardt (1989) |
| Affordance Theory | Studying what AI enables in practice | Affordances, Constraints, Actualization | Markus & Silver (2008) |
| Human-AI Collaboration | Studying augmentation vs. replacement | Complementarity, Task allocation | Raisch & Krakowski (2021) |
| Paradox Theory | Studying tensions from AI adoption | Control-autonomy, Transparency-efficiency | Smith & Lewis (2011) |

**Digital Transformation (broadly):**
| Theory | Use When | Key Constructs | Seminal Reference |
|--------|----------|---------------|-------------------|
| Ambidexterity | Studying exploration/exploitation balance | Exploitation, Exploration, Structural/Contextual | O'Reilly & Tushman (2013) |
| Resource-Based View | Studying AI as strategic resource | VRIN resources, Competitive advantage | Barney (1991) |
| Organizational Learning | Studying how orgs learn from AI experiments | Single/double-loop learning | Argyris & Schön (1978) |
| Structuration Theory | Studying technology-in-use patterns | Structure, Agency, Duality | Giddens (1984) / Orlikowski (2000) |

### For the GenAI/Agents Paper Specifically

Most promising theoretical lenses:
1. **Socio-Technical Systems Theory** — GenAI/Agents change both the technical AND social system; implementation success depends on joint optimization
2. **Dynamic Capabilities** — Organizations need to sense AI opportunities, seize them through implementation strategies, and reconfigure processes
3. **Affordance Theory** — GenAI/Agents offer specific affordances (text generation, autonomous decision-making) that are actualized differently depending on organizational context
4. **Paradox Theory** — AI agents create inherent tensions (autonomy vs. control, efficiency vs. transparency, innovation vs. risk)

## Step 2: Formulate the Gap

### Gap Formula Templates

**Template A — Fragmented Knowledge:**
```
While prior research has examined [aspect 1] (Author, Year; Author, Year) and 
[aspect 2] (Author, Year; Author, Year) in isolation, an integrative understanding 
of [how these aspects interact / the full picture] is lacking. This is problematic 
because [specific consequence of the fragmentation for theory or practice].
```

**Template B — New Phenomenon, Existing Theory Untested:**
```
[Theory] has proven valuable for understanding [prior phenomenon] (Author, Year). 
However, the emergence of [new phenomenon, e.g., autonomous AI agents] introduces 
dynamics that [Theory] has not yet been applied to — specifically, [what's new: 
e.g., agent autonomy, non-deterministic outputs, emergent behavior]. Whether and 
how [Theory]'s core mechanisms operate in this new context remains an open question.
```

**Template C — Practice Outpacing Theory:**
```
Organizations are rapidly adopting [technology/practice], as evidenced by 
[practitioner evidence: industry reports, adoption statistics]. Yet academic 
research lags behind: existing studies [are mostly conceptual / focus on 
narrow aspects / rely on early-stage data]. There is an urgent need for 
[systematic empirical investigation / theoretically grounded guidance / 
comprehensive frameworks] to inform both scholarship and practice.
```

**Template D — Methodological Gap:**
```
The existing body of research on [topic] is dominated by [dominant method: 
surveys / case studies / conceptual papers]. This methodological concentration 
limits our understanding because [what it can't capture: longitudinal dynamics / 
cross-contextual comparison / causal mechanisms / implementation details]. 
A [different method] approach can complement existing knowledge by [what it adds].
```

### For the GenAI/Agents Paper:
Likely combination of B + C:
```
While research on AI adoption in organizations has a rich tradition grounded in 
theories such as [TOE/UTAUT/Dynamic Capabilities], the emergence of generative AI 
and autonomous AI agents introduces qualitatively new dynamics — including 
non-deterministic outputs, emergent agent behavior, and the delegation of cognitive 
tasks previously considered uniquely human. These characteristics challenge 
fundamental assumptions in existing adoption and implementation frameworks. 
Meanwhile, organizational practice is advancing rapidly, with [X]% of enterprises 
piloting GenAI solutions (Source, Year), yet academic research providing systematic, 
theoretically grounded implementation guidance remains scarce.
```

## Step 3: Derive Hypotheses or Propositions

### For Quantitative Studies (Hypothesis Derivation):

Template:
```
[Theory] suggests that [theoretical mechanism] (Author, Year). In the context 
of [your study], this implies that [contextual application], because [reasoning 
linking theory to context]. Therefore:

H[N]: [Independent variable] [positively/negatively] influences [dependent variable] 
      [in the context of / when...].
```

### For Qualitative / SLR Studies (Proposition or Research Framework):

Template:
```
Based on [Theory] and the reviewed literature, we propose that [relationship or 
dynamic]. This proposition integrates insights from [Author1] (Year), who showed 
[finding], with [Author2] (Year), who demonstrated [finding]. We expect that 
[expected pattern], which we investigate through [method].
```

### For DSR (Design Principles):

Template (Chandra Kruse et al., 2016):
```
DP[N]: For [artifact type] to [aim/purpose] in [context], 
       [actors/the system] should [action/feature] 
       because [justification from kernel theory] (Theory, Author, Year).
```

## Step 4: Write the Contribution Statement

### The 3-Contribution Formula (most robust):

```
This study makes three contributions. First, we contribute to the literature on 
[stream 1] by providing [specific deliverable: a systematic overview / an empirical 
test / a design artifact / an integrative framework]. While prior work has [what they 
did], we [what's new and different]. 

Second, we [theoretical contribution]. By applying [Theory] to [new context/phenomenon], 
we [extend/challenge/refine] its explanatory scope. Specifically, we show that 
[concrete theoretical insight].

Third, we offer [practical contribution] in the form of [actionable deliverable: 
guidelines / a taxonomy / implementation recommendations / a decision framework]. 
This enables [practitioners/managers/organizations] to [specific benefit].
```

### Contribution Type Self-Check

Before finalizing, verify your contribution is one of these (not "Routine Application"):

| Type | Test | Example |
|------|------|---------|
| **New knowledge** | Does this tell us something we didn't know? | First systematic review of GenAI agent implementation |
| **New lens** | Does this apply theory in a genuinely new way? | Agency theory for human-AI delegation |
| **New method** | Does this introduce a methodological innovation? | Framework for evaluating agent autonomy levels |
| **New artifact** | Does this create something usable? (DSR) | Implementation maturity model for GenAI |
| **Integration** | Does this connect previously separate ideas? | Linking adoption factors + org change + governance |
