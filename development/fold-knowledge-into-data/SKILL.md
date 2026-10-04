---
name: fold-knowledge-into-data
description: Identify code where knowledge is encoded in logic (branches, paired functions, magic strings) and refactor it into data (tables, schemas, types, config). Use when reviewing code for maintainability, when adding a new case requires editing logic, or when two pieces of code must agree on a structure.
argument-hint: [file-or-function to analyze]
---

# Fold Knowledge into Data

From ESR's *The Art of UNIX Programming*, the Rule of Representation: "Fold knowledge into data, so program logic can be stupid and robust."

## The Core Idea

When knowledge is in code — branches, special cases, paired functions that must agree — the program is clever and fragile. When knowledge is in data — tables, schemas, types, config — the program is stupid and robust. Stupid code has fewer places to be wrong.

"Fold into data" does NOT mean "eliminate all code." It means: **separate the knowledge that changes from the logic that's stable.** When the changing part is data and the stable part is code, you edit data when requirements change and the code stays untouched.

## Red Flags — When to Think About This

### 1. You're writing the same structure in two places

You write a dict literal in save, then key lookups in load. You write a request builder, then a response parser. Any time two pieces of code must agree on a structure and nothing enforces the agreement — that's knowledge duplicated in code. A schema would make them both answer to one source.

### 2. You're adding an `elif` to an existing chain

You need to handle a new case — a new file type, a new API endpoint, a new model architecture. If you find yourself opening a function and adding a branch, ask: is this a table? Could the new case be a new row in a dict rather than a new branch in logic?

### 3. You're grepping the codebase for a string literal

"Where do we use the key `'model'`?" "Where do we check for `'review'` state?" If you're searching for a magic string to find all the places that care about it, that string is knowledge scattered across code. It should live in one place — a constant, an enum, a field name.

### 4. You're writing a comment that explains a rule

"# must match the order in load_checkpoint" or "# keep in sync with VALID_STATES" — these comments are admitting that knowledge lives in code and the programmer must manually enforce consistency. The comment is a red flag that data should be enforcing it instead.

### 5. Someone asks "where is X defined?" and the answer is "it's implicit"

"Where is the checkpoint format defined?" — "Well, look at what `save` writes." "Where are the valid state transitions?" — "Read through the if/elif chain." If the answer to "where is this defined" is "read the code and infer it," the knowledge isn't folded into data yet.

### 6. You're writing a test that just mirrors the implementation

```python
def test_save_load_roundtrip():
    save(path, model=m, optimizer=o, scheduler=s)
    ckpt = load(path)
    assert "model" in ckpt
    assert "optimizer" in ckpt
    assert "scheduler" in ckpt
```

The test is restating what the code does. If the format were a dataclass, the type system would enforce this and the test would be unnecessary. When a test exists only to check that two pieces of code agree, a schema would make the test redundant.

### 7. A non-code change requires a code change

A new tax rate, a new workflow state, a new supported file format, a new feature flag. If the change is purely "new data" but requires editing program logic, the boundary between data and code is in the wrong place.

### The one-sentence heuristic

**If you have to be careful, it should be data.** Carefulness — remembering to keep things in sync, getting the order right, not forgetting a case — is what humans are bad at and what data structures enforce for free.

## Case Studies

### Case Study 1: Tax rates — branching vs. table lookup

Knowledge in code:

```python
def compute_tax(state, amount):
    if state == "CA":
        return amount * 0.0725
    elif state == "TX":
        return amount * 0.0625
    elif state == "NY":
        return amount * 0.08
    elif state == "WA":
        return amount * 0.065
    # ... 46 more branches
```

The knowledge — which state has which rate — is tangled into control flow. To add a state, you write a new `elif`. To audit rates, you read through branching logic. To let a non-programmer update rates, they have to edit code.

Knowledge in data:

```python
TAX_RATES = {
    "CA": 0.0725,
    "TX": 0.0625,
    "NY": 0.08,
    "WA": 0.065,
}

def compute_tax(state, amount):
    return amount * TAX_RATES[state]
```

The logic is now stupid — a single multiplication. All the knowledge lives in the dict. You can inspect it, print it, load it from a file, diff it, test it exhaustively with a loop. The program logic can't be wrong in 50 different ways anymore — it can only be wrong in one way.

### Case Study 2: State machines — conditionals vs. transition table

Knowledge in code:

```python
def transition(doc, action):
    if doc.state == "draft" and action == "submit":
        doc.state = "review"
    elif doc.state == "review" and action == "approve":
        doc.state = "approved"
    elif doc.state == "review" and action == "reject":
        doc.state = "draft"
    elif doc.state == "approved" and action == "publish":
        doc.state = "published"
    else:
        raise InvalidTransition(doc.state, action)
```

Knowledge in data:

```python
TRANSITIONS = {
    ("draft",    "submit"):  "review",
    ("review",   "approve"): "approved",
    ("review",   "reject"):  "draft",
    ("approved", "publish"): "published",
}

def transition(doc, action):
    key = (doc.state, action)
    if key not in TRANSITIONS:
        raise InvalidTransition(*key)
    doc.state = TRANSITIONS[key]
```

What you can do with `TRANSITIONS` that you can't do with the `if/elif` chain:

- **Visualize it**: generate a graph of all states and transitions automatically
- **Validate it**: check that every state is reachable, no dead ends, no orphans
- **Test it exhaustively**: loop over every entry
- **Change it safely**: add a transition — it's one line in a dict, not a new branch that could interact with existing branches
- **Load it from config**: a non-programmer can define workflows

The program logic is the same two lines regardless of whether there are 4 transitions or 400.

### Case Study 3: Serialization — paired functions vs. schema

Knowledge in code — save and load must agree on keys, but nothing enforces it:

```python
def save_checkpoint(path, model, optimizer, scheduler, epoch, train_loss, val_loss):
    torch.save(path, dict(
        model=model.state_dict(),
        optimizer=optimizer.state_dict(),
        scheduler=scheduler.state_dict(),
        epoch=epoch,
        train_loss=train_loss,
        val_loss=val_loss,
    ))

def load_checkpoint(path, model, optimizer, scheduler):
    ckpt = torch.load(path)
    model.load_state_dict(ckpt['model'])
    optimizer.load_state_dict(ckpt['optimizer'])
    scheduler.load_state_dict(ckpt['scheduler'])
    return ckpt['epoch'], ckpt['train_loss'], ckpt['val_loss']
```

The format is implicit — "whatever save happens to write." Add `scaler` for mixed-precision training and you must update both functions and hope they agree.

Knowledge in data — a dataclass defines the format:

```python
@dataclass
class Checkpoint:
    model: dict
    optimizer: dict
    scheduler: dict
    epoch: int
    train_loss: float
    val_loss: float

def save_checkpoint(path, checkpoint: Checkpoint):
    torch.save(asdict(checkpoint), path)

def load_checkpoint(path) -> Checkpoint:
    return Checkpoint(**torch.load(path))
```

Neither function knows the format. Both implement whatever the dataclass declares. The format is explicit, inspectable, type-checked. Add `scaler` — add a field to the dataclass, and the type checker tells you everywhere that needs updating.

**Important nuance**: extracting paired functions alone does NOT solve the problem. You still have to update every call site that passes arguments to save/load. The win comes from the schema (the dataclass), not from the function extraction. The dataclass is the single source of truth; the functions are just serialization/deserialization of that type.

For serialization specifically, the options from least to most principled:

1. **Paired functions** — format is implicit but colocated. Weak.
2. **A dataclass** — format is declared as a type. Save/load are `asdict`/constructor. Better.
3. **A schema** — format is data that can be versioned, validated, migrated (protobuf, JSON Schema, RFCs). Best, but often overkill.

### Case Study 4: Logger factory — if/elif chain vs. registry

Knowledge in code:

```python
def create_loggers(config):
    run_name = config['logging']['run_name']
    logger_list = []
    if 'wandb' in config['logging']:
        wandb_options = config['logging']['wandb']
        logger_list.append(WandbLogger(run_name, wandb_options['project'], wandb_options['entity']))
    elif 'diagnostics' in config['logging']:
        logger_list.append(DiagnosticsLogger(run_name))
    return logger_list
```

Adding a third logger (tensorboard, CSV) means adding another `elif` branch. Red flag #2.

Knowledge partially in data — a registry maps names to classes:

```python
LOGGER_REGISTRY = {
    "wandb": WandbLogger,
    "diagnostics": DiagnosticsLogger,
}

def create_loggers(config):
    run_name = config['logging']['run_name']
    return [
        LOGGER_REGISTRY[name](run_name, **options)
        for name, options in config['logging'].items()
        if name in LOGGER_REGISTRY
    ]
```

The logic is now a generic loop. Adding a logger means: write the class, add one line to the registry, add a section to your yaml. No branching logic to edit.

**Important nuance**: the registry dict is still code. You still edit a `.py` file to add a line. The improvement is NOT "data vs. code" in a literal sense. It's that the *changing knowledge* (which loggers exist, which args they take) is separated from the *stable logic* (iterate, look up, construct). The `if/elif` version fuses both — the branching logic and the construction logic are interleaved. The registry version separates them.

The full "fold into data" win would be if the registry were driven entirely by config or plugin discovery, so adding a logger that already exists in the codebase is a config-only change. But at some point, the mapping from a string name to a Python class must live in code — you can push it to conventions (`importlib`), entry points, or plugin systems, but you can't eliminate it entirely.

### Case Study 5: Config loading — YAML instance vs. schema

A YAML file is an *instance*, not a schema. It says "here are the values for this run." It cannot say what makes a config valid in general.

Consider a project where config is loaded from YAML and consumed across multiple files:

```python
# utils.py
val_ratio = config["data"]["val_split"]
batch_size = config["data"]["batch_size"]
assert 0 < val_ratio < 1

# train.py
np.random.seed(config["experiment"]["seed"])
optimizer = getattr(torch.optim, config['training']['optimizer']['name'])(...)

# model.py
if config["model"]["architecture"] == "DualStreamCNN":
    input_channels = config['model']['input_channels']
```

"Where is the config schema?" → "Read all the consumers and infer it." Red flag #5.

Every key access is a hidden schema fragment — a silent assertion about what the config must contain. Scattered across files, these assertions encode:

- **Which fields are required** — `config["experiment"]["seed"]` crashes with `KeyError` if missing; `config["data"].get("background_dir", None)` silently uses `None`. The difference between required and optional is encoded in `[]` vs `.get()`, inconsistently, at every access site.
- **Type constraints** — `0 < val_ratio < 1` is enforced only here, only at runtime, only if this code path runs.
- **Value constraints** — `getattr(torch.optim, name)` will crash with `AttributeError` if `name` isn't a valid optimizer. Nothing declares the valid set upfront.
- **Relationships between fields** — nothing expresses that `optimizer.name` must name a real `torch.optim` class.

**The YAML instance doesn't help.** Reading it tells you what *this* run used — not whether `background_dir` is optional, not what happens if `seed` is missing, not which optimizer names are valid. The consumers still hold the real schema, as implicit assertions. The YAML and the consumers must agree, but nothing enforces that agreement.

A schema closes this gap:

```python
@dataclass
class DataConfig:
    dataset_path: str                                      # required — no default
    val_split: float = 0.2                                 # optional with default
    batch_size: int = 16
    num_workers: int = 4
    background_dir: str | None = None                      # explicitly optional

@dataclass
class TrainingConfig:
    num_epochs: int = 100
    optimizer: OptimizerConfig = field(default_factory=OptimizerConfig)
    scheduler: SchedulerConfig = field(default_factory=SchedulerConfig)

@dataclass
class Config:
    data: DataConfig
    training: TrainingConfig
    model: ModelConfig
    logging: LoggingConfig
    experiment: ExperimentConfig
    transforms: TransformConfig
```

Now:

- **"Where is the schema?"** → the dataclass declarations. One answer.
- **Required vs optional** is declared by the presence or absence of a default — not scattered across `.get()` calls.
- **Validation happens at load time.** Missing required fields fail immediately with a clear message, before any training begins.
- **Type constraints** are enforced by construction, not by scattered `assert` statements.
- **Every consumer** gets typed access — `config.data.val_split` instead of `config["data"]["val_split"]`. A typo is a type error, not a runtime `KeyError`.

`load_config` becomes stupid: parse YAML → construct `Config` → return. It neither knows nor cares what fields exist. The schema is the single source of truth. The YAML is still the instance ("here are my values"). The dataclass is the schema ("here is what any valid config must look like"). Construction is enforcement.

## Knowledge vs. Logic — When NOT to Fold

Not everything should be data. The principle is "fold *knowledge* into data." Logic and algorithms stay as code.

**Knowledge** is a decision that's already been made before the code runs. The code doesn't compute it, derive it, or figure it out — someone (a person, a spec, a convention) already decided, and the code just needs to *know* it. Crucially, knowledge can be **declared** — stated without describing steps.

- "California's tax rate is 7.25%" — a declaration. Knowledge.
- "The valid image formats are .png, .jpg, .jpeg" — a declaration. Knowledge.
- "The checkpoint contains model, optimizer, scheduler, epoch" — a declaration. Knowledge.

**Algorithms** are irreducibly procedural — sequences of steps where each depends on the result of the previous. They cannot be declared, only executed. "How to compute a Fourier transform" or "how to sort a list" is knowledge in the ordinary English sense (someone figured it out), but you can't represent it as data and have generic logic use it. The "how" *is* the thing.

- "To compute the DFT, for each output frequency k, sum over all input samples n, multiplying by e^(-2πikn/N)" — a recipe. Algorithm.
- "Zero gradients, forward pass, compute loss, backward, step" — a procedure. Algorithm.

**The declarability test: can you state it without describing steps?** If yes, it's knowledge — fold it into data. If no, it's an algorithm — leave it as code.

A secondary test: **"If requirements changed, would this line change?"** If yes, it's knowledge. If no (or only if the laws of math/physics/computation changed), it's logic.

### In torch training

Knowledge — every value here could reasonably differ across experiments:

```python
optimizer = optim.Adam(model.parameters(), lr=1e-4)
criterion = nn.MSELoss()
scheduler = ReduceLROnPlateau(optimizer, patience=5)
```

Which optimizer, which loss, which scheduler, which hyperparameters — these are facts about *this* experiment, not about training in general.

Logic — the operations and their order are fixed:

```python
optimizer.zero_grad()
pred = model(input)
loss = criterion(pred, target)
loss.backward()
optimizer.step()
```

This is how gradient descent works. No reasonable caller would want `backward()` before `forward()`. The sequence isn't a choice — it's the algorithm.

`run_epoch` is mostly logic — the training step sequence is the same regardless of model, dataset, or hyperparameters. The knowledge it receives (which model, which criterion, which optimizer) comes from its caller.

### In general

**Knowledge**: "HTTP 200 means success, 404 means not found, 500 means server error." Facts defined by RFC 7231. They could have been different.

**Logic**: "Parse the status code from the response, branch on it." The act of reading a number and dispatching — *how* you use the knowledge. The knowledge (which codes mean what) belongs in a table. The logic (read, look up, act) belongs in code.

**Knowledge**: "In chess, a bishop moves diagonally, a rook moves in straight lines." Rules of chess. They could differ in a variant game.

**Logic**: "To check if a move is legal, compute all squares reachable by the piece and check if the target is among them." An algorithm that works regardless of which piece has which movement rules.

**Knowledge**: "The config file uses YAML, the checkpoint has these 6 fields, the API returns JSON with a `data` key." Structural facts — conventions, formats, schemas.

**Logic**: "Parse the file, deserialize the bytes, extract the field." Operations that follow from the format but don't define it.

### The fusion problem

Trouble starts when knowledge and logic are interleaved and you can't tell which is which:

```python
if config['optimizer'] == 'adam':
    optimizer = optim.Adam(model.parameters(), lr=config['lr'])
elif config['optimizer'] == 'sgd':
    optimizer = optim.SGD(model.parameters(), lr=config['lr'], momentum=0.9)
elif config['optimizer'] == 'adamw':
    optimizer = optim.AdamW(model.parameters(), lr=config['lr'], weight_decay=1e-2)
```

Knowledge: which optimizers exist, what their default arguments are. Logic: look up the name, construct the optimizer. They're fused. Separated:

```python
OPTIMIZERS = {
    "adam": optim.Adam,
    "sgd": partial(optim.SGD, momentum=0.9),
    "adamw": partial(optim.AdamW, weight_decay=1e-2),
}

optimizer = OPTIMIZERS[config['optimizer']](model.parameters(), lr=config['lr'])
```

The knowledge (which optimizers, which defaults) is in the table. The logic (look up, construct) is one line.

### When knowledge acts like logic

Sometimes it's ambiguous. Is `momentum=0.9` knowledge or logic? It's a default — someone chose it. But if it never changes across your experiments, it *acts* like logic in your codebase even though it's technically a fact. The practical test isn't philosophical — it's **does this change independently of the code around it?** If yes, extract it to data. If it only changes when the surrounding algorithm changes, leave it in code.

### Things that should stay as code

**Algorithms**: Quicksort's partitioning, A*'s heuristic traversal, gradient descent's update rule, the Fourier transform. These are irreducibly procedural — sequences of steps where each depends on intermediate results. You can't declare "how to sort" or "how to compute a DFT" as a table entry and have generic logic execute it. They fail the declarability test: you can only describe them as steps, not as a fact.

**Invariants enforced by construction**: A type's constructor that validates its inputs — "a valid `EmailAddress` must contain `@`." You *could* put validation rules in a data table, but then you lose the compiler's guarantee that invalid instances can't exist. The code *is* the enforcement mechanism.

**Domain logic with complex interdependencies**: "If the patient is on blood thinners AND has surgery within 48 hours AND platelet count is below X, then escalate." You could put this in a rules engine (data), but when conditions interact in non-trivial ways, a well-written function with named predicates is often clearer than a declarative rule table that hides the interaction.

## The Diagnostic Process

1. **Find the knowledge** — what are the facts, rules, or structures the code encodes? (Formats, valid states, mappings, rates, schemas.)
2. **Check if it's duplicated** — does this knowledge appear in more than one place? Must two pieces of code agree?
3. **Check if it's fused with logic** — is the knowledge interleaved with branching, looping, or construction code?
4. **Ask: can I point to it?** — is there a single artifact (table, type, config file) where this knowledge is declared? Or do you have to read code and infer it?
5. **Extract the knowledge into data** — table, dict, dataclass, enum, config. Make the logic generic and stupid.
6. **Verify the logic is now stable** — adding a new case should mean adding data, not editing logic.

## What Data Enables That Code Doesn't

Data can be:
- **Inspected**: print it, log it, display it in a UI
- **Diffed**: version control shows exactly what changed
- **Validated**: check invariants programmatically (no orphan states, no missing keys)
- **Tested exhaustively**: loop over every entry
- **Loaded from external sources**: config files, databases, APIs
- **Operated on generically**: the same loop works for 4 entries or 400

Procedural branches can't do any of these naturally. Each branch is a unique snowflake that must be read, understood, and maintained individually.

## The Deeper Principle

All of these cases share the same underlying structure: **authority on what's correct belongs to data; checking is generic logic that operates on whatever data it's given.**

This is why logic stays stable when data changes. Generic logic doesn't name specific cases — it operates on the data that names them. The tax rate table changes; `TAX_RATES[state]` doesn't. The transition graph changes; the two-line dispatcher doesn't. The dataclass schema changes; `asdict` doesn't.

Type checking is the same pattern applied to programs themselves. The type checker is generic logic. Your type declarations — field names, types, required vs. optional — are the data it operates on. Add a field to a dataclass; the type checker's logic doesn't change. It re-runs on the new data and propagates the updated authority to every consumer automatically. This is why a dataclass + type checker solves the scattered-schema problem: the declarations become the single source of truth, and enforcement is generic.

The principle has a limit: at some meta-level, the checking logic itself must be grounded in something it doesn't itself validate. The type checker can't type-check itself without circularity. Every validation regime has a foundation it accepts without proof. But within a given level, the principle holds — make correctness declarable as data, and the checking mechanism becomes a stable, reusable tool that never needs to change when the rules do.

## Related Skills

- [construct-or-inject](../construct-or-inject/SKILL.md) — the construction-side counterpart. Case Study 4's registry of classes and the `OPTIMIZERS` table of partials are *tables of factories*: that skill covers when a class should accept such a factory (vs constructor params or a built instance), and which of the factory's params get bound in the table vs passed by the consumer at call time.
- [separate-mechanism-policy](../separate-mechanism-policy/SKILL.md) — the same separation viewed from the function-design side: knowledge folded into data is policy made declarable, so the remaining logic is pure mechanism.