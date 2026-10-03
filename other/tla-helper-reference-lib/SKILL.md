---
name: tla-helper-reference-lib
description: Leslie Lamport’s personal workstation and external reference library for deep TLA+/PlusCal research, assumption challenging, pattern extraction, industrial stress-testing, anti-pattern detection, and expert citation. Invoke whenever the agent requires grounding in real observable examples, clarification of modeling choices, external validation of complex specification ideas, or recovery from uncertainty. This skill never rewrites or pastes examples into context; it points directly to primary sources and enforces strict selective consultation so that working memory remains clean. It is the designated deep-research fallback for the entire TLA+ skill tree.
---

# Leslie’s Workstation — tla-helper-reference-lib

## 1. Workstation Philosophy (Binding)

You possess a physical desk and library. This skill is that desk.

Five axioms govern every use of this workstation:

1. The highest accuracy in complex TLA+ specification arises only when the agent continuously contests its own modeling decisions against external, observable, high-fidelity examples and industrial stress tests.
2. Context is a scarce and precious resource. Any reference mechanism that floods working memory degrades rather than improves mathematical clarity.
3. You treat this library as a physical workstation: a place one deliberately returns to for grounding, not a stream of text that arrives unbidden.
4. Integration is hierarchical and early: you know of this workstation’s existence and authority from the first moment of reasoning on any non-trivial specification task.
5. The library never rewrites examples. It points directly to primary sources. Your job is to study, extract, challenge, and return.

These axioms are non-negotiable. Violation of the selective-consultation discipline is treated as a methodological error equivalent to skipping sample behaviors.

## 2. Selective Consultation Protocol (Mandatory)

When modeling uncertainty, abstraction doubt, invariant weakness, or the need for external grounding arises, execute the following sequence exactly:

1. Formulate a precise research question or modeling uncertainty in one or two sentences.
2. Identify the one or two most relevant clusters from the Cluster Index.
3. Select at most 1–4 references from the Annotated Link Library (or a deepened cluster file). Prefer primary sources and industrial examples over secondary commentary.
4. Load only those references. Read with the explicit goal of extracting:
   - Concrete abstraction decisions and their justifications
   - Invariant patterns or proof structure
   - Modeling choices that succeeded or failed under real complexity
   - Anti-patterns that must be avoided
5. Explicitly record (internally) which of your current assumptions are confirmed, weakened, or overturned.
6. Close the references. Do not leave large excerpts in active context.
7. Return to the current specification task and apply the strengthened insight. State, if useful, that the workstation was consulted and what class of insight was obtained.

Never load the entire library. Never paste long specifications into the working context unless the user has explicitly requested a particular example for joint examination.

## 3. Cluster Index

Use this index to locate material rapidly.

- **Foundations & Pedagogy** — Lamport’s own writings, video course, Hyperbook, Specifying Systems, elementary to intermediate teaching examples.
- **Canonical Examples** — The official tlaplus/Examples repository and its interactive mirrors.
- **Consensus & Agreement** — Paxos family, Raft family, Byzantine variants, Flexible Paxos, EPaxos, HotStuff, Tendermint, etc.
- **Termination Detection & Classical Distributed Algorithms** — EWD algorithms, Dijkstra, Misra, Chang-Roberts, etc.
- **Refinement & Successive Abstraction** — Lamport’s refinement examples, multi-grained industrial specifications, stepwise implementation proofs.
- **Industrial Distributed Systems & Databases** — AWS, Azure, Elasticsearch, etcd, TiDB, MongoDB, Kafka, Signal, Ceph, BookKeeper, etc.
- **PlusCal Advanced Patterns** — Complex concurrent algorithms expressed in PlusCal, translation discipline, and realistic multi-process models.
- **Proof Style (TLAPS)** — Examples of inductive invariants and machine-checked proofs.
- **Anti-Patterns & Lessons Learned** — Explicit failures, common modeling mistakes, industrial post-mortems, and methodological warnings.
- **Reusable Operators & Community Modules** — CommunityModules and other high-quality operator libraries.
- **Tools & Model-Checking Practice** — TLC, Apalache, Toolbox, configuration patterns, and performance considerations for large models.

**Deepened cluster files** (load only when the corresponding cluster is the focus of consultation):

- `clusters/consensus.md` — Highest-leverage material on Paxos family, Raft family, Byzantine variants, refinement chains for agreement, and Dr. TLA+ series.
- `clusters/refinement.md` — Successive abstraction discipline, Lamport’s canonical refinement examples, multi-grained industrial thinking.
- `clusters/industrial.md` — Production-scale systems, operational constraints, and concrete bug stories from AWS, Azure, Elasticsearch, TiDB, MongoDB, Kafka, Signal, etc.
- `clusters/anti-patterns.md` — Negative knowledge, classic methodological failures, and industrial post-mortems that interrupt bad modeling decisions early.

These files contain richer annotations, challenge questions, and ranked guidance. Prefer them over the high-level entries below when the modeling uncertainty is concentrated in one of these domains.

## 4. Annotated Link Library

Each entry is written for the agent. The note tells you what the resource is, why it matters for deep complexity work, how to read it, and what class of assumption it is most likely to challenge.

### Foundations & Pedagogy

- **Specifying Systems** (Lamport)  
  https://lamport.azurewebsites.net/tla/book.html (and direct PDFs linked from the page)  
  The definitive methodological and mathematical foundation. Chapters 7 and 8 are binding. Read the advanced examples only after the sample-behavior discipline is internalized. Challenges any tendency to treat TLA+ as a programming language.

- **Lamport’s TLA+ Home Page**  
  https://lamport.azurewebsites.net/tla/tla.html  
  The map of all official material. Always orient from here when the intellectual landscape feels fragmented.

- **TLA+ Video Course**  
  https://lamport.azurewebsites.net/video/videos.html  
  Lamport’s own voice and pacing. Use when you need to re-ground in fundamental state-machine thinking or when abstraction choices feel forced.

- **TLA+ Hyperbook**  
  https://lamport.azurewebsites.net/tla/hyperbook.html  
  Deeper pedagogical development; unfinished but still valuable for realistic examples and the transition from simple to complex models.

- **PlusCal Tutorial (official)**  
  https://lamport.azurewebsites.net/tla/tutorial/intro.html  
  The authoritative bridge from algorithmic thinking to TLA+. Use when deciding whether PlusCal is the clearer medium for a given algorithm.

### Canonical Examples

- **tlaplus/Examples (primary repository)**  
  https://github.com/tlaplus/Examples  
  The single most important external corpus. Contains pedagogical puzzles, classical algorithms, Paxos variants, termination detection, industrial-style models, and proof examples. Always begin exploration from the README table (beginner / PlusCal / TLAPS / Apalache flags). Treat each subdirectory as a self-contained case study. Challenges both under-abstraction and over-abstraction.

- **Interactive / web mirrors**  
  https://examples.tlapl.us and related learning sites (tlabyexample.com lineage)  
  Useful for rapid visual inspection and model-checking experiments without local setup. Prefer the GitHub source for serious study.

### Consensus & Agreement (High-Value Industrial and Research Specs)

- Classical and refined Paxos examples inside tlaplus/Examples (Paxos, PaxosHowToWinATuringAward, byzpaxos, MultiPaxos variants, diskpaxos, etc.)
- Raft family: https://github.com/ongardie/raft.tla , etcd-related work, Atomix Raft + client sequencer
- Flexible Paxos: https://github.com/fpaxos/fpaxos-tlaplus
- Egalitarian Paxos: https://github.com/efficient/epaxos
- Tendermint / CometBFT light client and accountability specs: https://github.com/tendermint/spec
- Signal SVR2 (Raft + SGX enclaves): https://github.com/signalapp/SecureValueRecovery2/blob/main/docs/svr2.tla
- Additional modern variants: HotStuff, CBC Casper, Spire, Just-in-Time Paxos (search the awesome-tlaplus real-world list for current links)

These challenge assumptions about synchrony, reconfiguration, linearizability under failure, and the cost of Byzantine tolerance.

### Termination Detection & Classical Distributed Algorithms

- EWD687a, EWD840, EWD998, Huang, Misra Reachability, Chang-Roberts, Dijkstra mutual exclusion, Echo algorithm — all present in tlaplus/Examples with high-quality models and (often) PlusCal variants.
- Use these when modeling detection, token circulation, or leader election under asynchrony. They expose subtle fairness and stuttering issues.

### Refinement & Successive Abstraction

- Lamport’s own refinement chains (especially PaxosHowToWinATuringAward and Byzantizing Paxos by Refinement) inside the Examples repository.
- Multi-grained industrial specifications (search Murat Demirbas writings and Azure/Cosmos-related material).
- Challenges the temptation to jump directly to an implementation-level model.

### Industrial Distributed Systems & Databases

- Elasticsearch formal models: https://github.com/elastic/elasticsearch-formal-models
- TiDB / PingCAP: https://github.com/pingcap/tla-plus
- MongoDB replication: https://github.com/visualzhou/mongo-repl-tla
- Kafka replication / KRaft related specifications
- Azure Cosmos DB related material and industrial-use reports
- Ceph consensus, BookKeeper, Xen vchan, Linux kernel concurrency primitives, Ubisoft lock-free queues, etc.
- Primary industrial narrative: https://lamport.azurewebsites.net/tla/industrial-use.html (AWS, Microsoft, Intel, Dropbox, etc.)

These provide the only reliable stress tests for state-space size, partial failure, and real operational constraints.

### PlusCal Advanced Patterns

- muratdem/PlusCal-examples: https://github.com/muratdem/PlusCal-examples
- BlockingQueue lineage (Markus Kuppe): https://github.com/lemmy/BlockingQueue
- PlusCal Cheat Sheet (Stephan Merz): https://github.com/tlaplus/PlusCalCheatSheet
- spacejam/tla-rust (lock-free and distributed systems guided by TLA+): https://github.com/spacejam/tla-rust

Use when the algorithmic structure is clearer in PlusCal and the translation discipline must remain rigorous.

### Proof Style (TLAPS)

- LearnProofs and other TLAPS-flagged examples inside tlaplus/Examples
- Spire consensus proofs and other machine-checked industrial/academic proofs
- Challenges weak or non-inductive invariants and incomplete proof structure.

### Anti-Patterns & Lessons Learned

- AWS formal methods experience (2015 CACM paper and follow-ups) — the strongest industrial statement of what formal methods actually catch.
- Microsoft Azure / Cosmos DB case studies (bugs found before coding, safety violations under power failure, etc.)
- Hillel Wayne’s Practical TLA+ discussions of common modeling mistakes
- Murat Demirbas writings on multi-grained specifications and TLA+ as design accelerator
- Explicit anti-patterns already encoded in the master agent (treating TLA+ as code, skipping sample behaviors, trivial invariants, missing UNCHANGED, etc.) are reinforced here by concrete external evidence.

### Reusable Operators & Community Modules

- https://github.com/tlaplus/CommunityModules  
  Preferred source of high-quality, community-vetted operators. Prefer these over ad-hoc definitions when the concept is standard.

### Tools & Model-Checking Practice

- Official tool documentation via Lamport’s site and the TLA+ Foundation (https://foundation.tlapl.us)
- Apalache symbolic model checker examples and documentation
- Configuration patterns visible inside the Examples repository (.cfg files)

## 5. Scouting Interface

When you need material, formulate requests of the following form (internally or in reasoning):

- “Show the strongest industrial Raft / Paxos / Byzantine consensus examples for refinement study.”
- “Locate termination-detection models that expose fairness subtleties.”
- “Find anti-pattern evidence related to premature concretization or weak invariants.”
- “Retrieve PlusCal models of concurrent data structures with known subtle bugs.”
- “What does the workstation say about multi-grained specification of a distributed key-value store?”

The workstation answers by pointing to the relevant cluster entries and their interpretive notes. It does not dump source text.

## 6. Relationship to the Master Agent and the TLA+ Skill Tree

This skill is the designated deep-research and assumption-challenging workstation for the entire TLA+ skill tree, and in particular for `specification-master-agent`.

- The master agent knows of this workstation from the beginning of every non-trivial task.
- Supporting skills (foundations, syntax, state-machines, invariants, refinement, composition, from-code-to-spec, tooling, review) may recommend consultation of the workstation when external grounding would strengthen their contribution.
- The workstation defers to the master persona and to the chapter guardrails of *Specifying Systems*. It never overrides mathematical discipline; it supplies the external data against which that discipline is tested.

When in doubt about an abstraction, an invariant, a fairness condition, or a modeling decision, consult the workstation before proceeding.

---

**End of core workstation definition.**

Future expansion of individual clusters occurs only by adding high-signal entries that meet the same quality bar and by deepening the interpretive notes. The selective-consultation protocol remains inviolable.
