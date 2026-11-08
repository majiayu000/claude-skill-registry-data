---
name: spec-driven-sweep
kind: pattern
rule: spec-driven
description: Pattern of rule spec-driven. Load for a full sweep of a domain's binding — five passes, three of them done by the machine, reading through the hits and the share of false ones per layer. Not for creating a domain spec — that is pattern spec-driven-domain.
---
<!-- rt-kit v0.34.0 · patterns/spec-driven-sweep.md · dae9cd38917b · правится надстройкой, не здесь -->

# A full review of a domain's binding

Pattern of the rule `spec-driven`. What must be true — the project-documentation law.

## When to use

- A domain's binding is reviewed whole: every statement against the code it points to.
- The tree's texts are checked against the tree as a task, not along the way of other work.

## There are five passes, and their order is one

The first three the machine does over the whole domain at once, the last two are reading. The
order is not rearranged: reading goes over the lines the machine has already selected, otherwise
the whole domain gets read.

1. **A dead address.** The named file is not in the tree, or the symbol is nowhere. Gives zero on
   a domain already reviewed, and a whole batch on one that code recently moved out of.
2. **An anchor living only in an explanation.** The symbol occurs in the tree only in comments.
   The binding check counts a comment the same as code, so it is green for such an anchor, and
   there is no place carrying it out behind it.
3. **The symbol is not declared in the named file.** The file imports and calls it, and the
   declaration lies elsewhere. The most fruitful pass and the noisiest.
4. **The promise against the code.** The code at the address is read: does it do what the rule
   states. The machine cannot do this pass at all — the divergence here is usually in a condition
   and in the order of steps.
5. **A number, a refusal code and a glossary key — by name.** Every number from the text is looked
   for in the tree, every named refusal code in the place where it is thrown, every glossary key
   in all locales. A divergence here looks like a typo and lives for years.

## A hit is a queue for reading, not a list of defects

A pass yields lines; a finding is one confirmed by reading. The difference is not verbal: a third
of the third pass's lines are legitimate in any domain, and written down as findings they turn
the review into editing correct code. Both numbers go into the progress — how many lines the pass
gave and how many of them turned out to be divergences.

## The share of false hits depends on the layer

Where the rule lives in a procedure, the place carrying it out is one and public: a hit of the
third pass is more often a divergence — six lines out of fourteen. Where the rule lives in a
component or a service, the place carrying it out is legitimately a private field or a private
method: out of thirty-six lines, not one turned out to be a divergence. So the number of findings
of the previous domain does not carry over to the next — only the order of passes carries over.

## Common misses

- **A pass's yield promised as fact.** "The pass will give so many" is an estimate, and on a
  different layer it misses entirely. The grill names the passes, not the number of findings.
- **A pass that gave zero was not written down.** The next session runs it again over the same
  domain. Zero is a result like any other, and it is written along with the rest.
- **Counting sides was taken for a review.** A green binding check says every statement has a
  line, and says nothing about where the line leads.
