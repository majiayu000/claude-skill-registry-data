---
name: construct-or-inject
description: Decide whether a class should construct its own dependencies, receive built instances, or receive factories (newable vs injectable, instance vs Provider<T>). Use when designing or reviewing constructors — especially nn.Module composition — when a wrapper forwards constructor params to its sub-objects, or when a class needs N copies of a configurable block.
argument-hint: [file-or-class to analyze]
---

# Construct, Inject, or Take a Factory

Every class with dependencies answers one question per dependency: **who knows how to construct it?** There are exactly four honest answers:

1. **Construct it yourself** — call the dependency's constructor in your own `__init__`.
2. **Inject the instance** — the caller builds it and passes in the finished object.
3. **Inject a factory** — the caller passes a recipe (any callable); you invoke it when needed.
4. **Method argument** — it isn't a dependency at all, it's runtime data; it arrives per-call.

Forwarding the dependency's constructor params through your own signature is **not** on this list — it is the failure mode (see Smells).

## Definitions

- **Newable** (Hevery) / **stable dependency** (Seemann): an object whose identity is its data. Cheap, concrete, no meaningful alternative implementation, never mocked. `Money`, `Email`, `nn.Linear(256, 1024)`, `nn.LayerNorm(d)`. Construct these freely, anywhere.
- **Injectable** (Hevery) / **volatile dependency** (Seemann): an object that *does* things — a service with behavior that callers might swap, configure, or mock. `Database`, `PaymentProcessor`, an attention layer, a descriptor extractor. Obtain these through the constructor.
- **Instance injection**: receive `T`, already built.
- **Factory injection**: receive `Callable[..., T]` (Guice's `Provider<T>`). Each call yields a fresh, independent instance.
- **Wiring time vs operation time**: injectables are assembled once into a graph at startup; newables are created constantly during operation from runtime data. In torch this split is physical: `__init__` is wiring time (modules), `forward()` is operation time (tensors).

The two caste rules (Hevery):

1. **Injectables may ask for other injectables in their constructor, but not for newables.** A `PaymentProcessor` must not take a `CreditCard` in its constructor — the card is runtime data and arrives as a method argument. Violation name: *constructor over-injection*.
2. **Newables may hold other newables, but not injectables.** A `User` value object holding a `Database` reference can no longer be constructed in a test without the whole service graph.

## The Decision Table

| Situation | Verdict |
|---|---|
| Dependency is standard, value-like, and its config is fully derived from your own params | Construct it yourself |
| One volatile collaborator, lifetime matches yours | Inject the instance |
| N independent copies needed | Inject a factory |
| Created lazily / conditionally / at times only you know about | Inject a factory |
| Long-lived consumer needs short-lived dependencies (per-request, per-rollout) | Inject a factory |
| Object derives from runtime data (a batch, a request, user input) | Method argument — never constructor state |

The one-line guideline (Guice's `T` vs `Provider<T>`): **one collaborator → inject the instance; many, or construction at times you control → inject a factory.**

## Parameter Ownership (assisted injection)

When you inject a factory, split the dependency's constructor params by who owns them:

- **Structural params the consumer owns** — passed by the consumer at factory-call time. These are the params *derived from the consumer's own config* (e.g. `dim` must equal the consumer's `hidden_dim`). Single source of truth, no duplicate-and-assert.
- **Flavor params the consumer has no business knowing** — bound by the caller into the factory (`functools.partial`, a lambda, a config-built closure).

```python
AttnFactory = Callable[[int], nn.Module]   # dim -> attention block

class PerceiverResampler(nn.Module):
    def __init__(self, num_layers: int, hidden_dim: int, num_latents: int,
                 attn_factory: AttnFactory):
        super().__init__()
        self.latents = nn.Parameter(torch.empty(num_latents, hidden_dim))
        self.layers = nn.ModuleList(attn_factory(hidden_dim) for _ in range(num_layers))

resampler = PerceiverResampler(6, 256, 8,
    attn_factory=partial(LightGlueAttn, num_heads=4, flash=False))
```

The resampler never learns `num_heads`, `flash`, or `dropout` exist. When the attention layer grows a tenth knob, the resampler's signature does not change.

This is exactly `java.util.concurrent.ThreadPoolExecutor`'s `ThreadFactory`: the pool's call is `newThread(Runnable r)` — the pool passes the one argument it owns (the work); naming, daemon flag, and priority are bound inside the factory by whoever configured it.

## When Injected Parts Must Agree (the Enforcement Ladder)

Injection creates cross-module contracts: an instance-injected encoder must emit tokens of the width the consumer's stack expects. The knowledge of that dim now exists in two places. There is a ladder of enforcement, and each rung moves **who holds authority** over the value:

**Rung 0 — comment.** `obs_encoder: nn.Module,  # -> B,N,hidden`. Contract in prose, authority nowhere. The failure is a shape error at first forward, three frames deep in a matmul (`mat1 and mat2 shapes cannot be multiplied`), not at the wiring line where the mistake lives. Indefensible — the next rung is nearly free.

**Rung 1 — assert against an exposed attribute.**

```python
def __init__(self, hidden_dim, obs_encoder, ref_encoder, attn_factory):
    assert obs_encoder.out_dim == hidden_dim, f"{obs_encoder.out_dim=} != {hidden_dim=}"
    assert ref_encoder.out_dim == hidden_dim
```

Requires a protocol: every injectable of this kind exposes `out_dim: int` (detectron2 precedent: backbones expose `output_shape() -> ShapeSpec` and consumers build against it). Fails at wiring time with a message that names the mistake.

**Rung 2 — derive instead of duplicate.**

```python
def __init__(self, obs_encoder, ref_encoder, attn_factory):
    hidden_dim = obs_encoder.out_dim              # single source of truth
    assert ref_encoder.out_dim == hidden_dim      # irreducible — see below
    self.layers = nn.ModuleList(attn_factory(hidden_dim) for _ in range(L))
```

One parameter gone, one duplicate eliminated. The remaining assert is irreducible *in this topology*: an agreement between two independently constructed objects can only be checked, never derived.

**Rung 3 — invert construction so disagreement is unrepresentable.**

```python
def __init__(self, hidden_dim, obs_encoder_factory, ref_encoder_factory, attn_factory):
    self.obs_encoder = obs_encoder_factory(hidden_dim)   # consumer owns the dim,
    self.ref_encoder = ref_encoder_factory(hidden_dim)   # passes it to everyone
```

Parameter Ownership applied consistently — mismatch is impossible to write.

Choosing the rung:

- **Rung 3 for lightweight blocks** (attention layers, FFNs, norms) — this is ordinary factory injection.
- **Rung 1–2 for heavyweight, pretrained, or shared modules** (backbones, extractors). Factory-injecting these forces presets into `lambda d: prebuilt` — which ignores `d`, silently defeating the enforcement while adding indirection. When the one-collaborator→instance rule collides with enforcement, instance + assert is the standard resolution; prefer rung 2 (derive) so only the irreducible assert remains.
- **There is no higher rung in Python.** Type-level impossibility needs the dim in the type (dependent types — `ObsEncoder[256]` vs `Verifier[384]`). `jaxtyping` + `beartype` give runtime-checked shape annotations on `forward` (`Float[Tensor, "b n {self.dim}"]`) — better ergonomics for rung 1, not static proof. "Structurally impossible" is only reachable by changing construction topology: single source (rung 2), single owner (rung 3), or a single lexical variable threaded through one preset (the composition root's free mitigation).
- The only indefensible configuration is **two independent authorities and no check** — rung 0.

This refines the duplicate-and-assert smell: it is a smell when the consumer could own the param (rung 3 is available — take it). When instances must be injected, the assert is not the smell; the *duplicate* is — derive it away (rung 2).

## Test Cases

Apply the table. Verdicts below each case.

### Test 1 — N copies of a configurable block

```python
class PerceiverResampler(nn.Module):
    def __init__(self, num_layers, hidden_dim, ...):
        # needs num_layers independently-weighted attention layers
```

**Verdict: factory injection.** Multiple independent instances, created in a loop only the consumer knows about. Passing one built instance would force cloning; passing `(num_heads, dropout, flash, ...)` makes the wrapper a middle man.

### Test 2 — exactly one collaborator

```python
class GligenBlock(nn.Module):
    def __init__(self, gated_mha: nn.Module):   # uses exactly one
        self.attn = gated_mha
```

**Verdict: instance injection.** One collaborator, lifetime matches. The block should not know how to build a gated MHA.

### Test 3 — sub-objects with fully derived config

```python
class TransformerEncoderLayer(nn.Module):
    def __init__(self, d_model, nhead, dim_feedforward):
        self.linear1 = nn.Linear(d_model, dim_feedforward)   # dims derived
        self.linear2 = nn.Linear(dim_feedforward, d_model)
```

**Verdict: construct it yourself.** `nn.Linear` is a newable (tiny frozen ctor: in, out, bias) and its config is a pure function of the wrapper's own params. Injecting the linears would let callers pass mismatched dims — injection here *adds* an error class. This is `nn.Transformer`'s legitimate side.

### Test 4 — forwarding a bag of constructor params

```python
class TransformerLayer(nn.Module):
    def __init__(self, *args, **kwargs):          # LightGlue, real code
        self.self_attn = SelfBlock(*args, **kwargs)
        self.cross_attn = CrossBlock(*args, **kwargs)
```

**Verdict: smell — middle man.** The wrapper's signature is invisibly coupled to its children's. Every new child knob is shotgun surgery (or worse, silently swallowed by `**kwargs`). Replace with explicit factory injection or explicit owned construction; never a catch-all kwargs relay.

### Test 5 — constructing a module inside forward()

```python
def forward(self, x):
    proj = nn.Linear(x.shape[-1], self.dim)   # operation-time construction
    return proj(x)
```

**Verdict: caste violation, mechanically punished.** An injectable constructed at operation time: its parameters were never registered at wiring time, the optimizer never sees them, and they silently don't train (fresh random weights every call). Torch enforces Hevery's rule for you.

### Test 6 — runtime data in the constructor

```python
class Verifier(nn.Module):
    def __init__(self, sample_batch):           # constructor over-injection
        self.scale = sample_batch.std()
```

**Verdict: method argument.** Tensors are newables of the purest kind — per-batch runtime data. Anything derived from a batch belongs in `forward()` (or an explicit `fit()`/calibration step), not in wiring.

### Test 7 — prototype + deepcopy

```python
decoder = nn.TransformerDecoder(decoder_layer, num_layers=6)
# internally: copy.deepcopy(decoder_layer) x 6
```

**Verdict: a third way with a gotcha.** PyTorch dodges the factory by cloning a prototype instance — but `deepcopy` copies *initialized weights*, so all six layers start identical. Factory injection gives independent inits for free. Prefer the factory; if you accept the prototype pattern, know what you signed up for.

### Test 8 — a "newable" that turned volatile

```python
class ResNet(nn.Module):
    def __init__(self, block, layers, norm_layer=nn.BatchNorm2d):  # torchvision, real code
        ...
        norm = norm_layer(planes)   # consumer passes the params it owns
```

**Verdict: defaulted factory hole.** BatchNorm was "the" norm until GroupNorm/SyncBN users needed to swap it. torchvision punched a factory-shaped hole, defaulted to the old behavior — callers who don't care see a simple constructor; callers who do get the hole. This is the standard retrofit when a construct-it-yourself call turns out to be a variation point.

## Case Studies — Torch

**torchvision `ResNet(block=Bottleneck, layers=[3,4,6,3], norm_layer=...)`.** The "torchvision-simple" API *is* factory injection: `block` and `norm_layer` are callables; ResNet invokes `block(inplanes, planes, stride, downsample, ...)` passing the structural params it owns. timm generalizes the convention (`block_fn=`, `act_layer=`, `norm_layer=`) — mature vision libraries punched factory holes exactly where users demanded variation, and kept owned construction everywhere else.

**`nn.Transformer` — both the example and the cautionary tale.** Constructing its own `nn.Linear`s is correct by the table (derived dims, stable newable). But it *also* hard-wired the FFN shape, activation, and attention internals — then the field wanted SwiGLU, RoPE, GQA, LoRA-wrapped and quantized linears, and the answer was "you can't." The ecosystem abandoned it and rewrote the block. The boundary it drew was right by 2017's knowledge and wrong by 2022's: variation points are discovered empirically.

**`nn.TransformerDecoder(layer, num_layers)`** — prototype + `deepcopy` instead of a factory; all clones start with identical weights (Test 7).

**LightGlue `TransformerLayer(*args, **kwargs)`** — the middle-man relay in the wild (Test 4).

**The torch/DI isomorphism.** `__init__` = wiring time, modules = injectables; `forward()` = operation time, tensors = newables. Torch mechanically enforces both directions: modules built in `forward` don't get registered (Test 5); tensors baked into `__init__` are stale runtime data (Test 6).

## Case Studies — Java (and one from C++)

**Guice `T` vs `Provider<T>`.** Declare a dependency as `T` → the container builds one and hands it over. Declare `Provider<T>` (interface with one method, `get()`) when you need many instances, lazy/conditional construction, or per-request lifetimes inside a long-lived object. The guideline in The Decision Table is this API's documentation distilled.

**Guice AssistedInject.** Formalizes Parameter Ownership: some constructor params are bound by the container at wiring time; the ones marked `@Assisted` are supplied by the consumer at `get()`-time. `attn_factory(dim)` with `partial`-bound flavor params is AssistedInject in Python clothes.

**`ThreadPoolExecutor(..., ThreadFactory)`.** The pool creates threads at times only it knows about (load spikes) — so it takes a factory, never `(name_prefix, daemon, priority)` params. `newThread(Runnable r)`: consumer passes what it owns, factory binds the rest.

**`DataSource` vs `DriverManager.getConnection(url, user, password)`.** A connection pool injects a connection *factory* (`DataSource`), not the connection params. Who knows the password is the factory's configuration problem, not the pool's.

**C++ STL allocators.** `std::vector<T, Allocator>` takes an allocation *strategy*, not allocation parameters — the same split, enforced at the type level.

## Smells

- **Middle-man relay**: your `__init__` accepts `(d_model, nhead, dropout, bias, flash, ...)` only to forward them to a sub-object's constructor. Your signature is now coupled to a dependency's; every new knob is shotgun surgery. Catch-all `**kwargs` doesn't fix this — it hides it, and typos stop being errors.
- **Duplicate-and-assert**: the same `dim` passed both to the wrapper and inside the factory binding, with an assert to keep them equal. Move the param to factory-call time — the wrapper passes the value it owns (Parameter Ownership). Exception: when the dependency must be instance-injected (heavyweight/pretrained), the assert is correct and the *duplicate* is the smell — see the Enforcement Ladder, rung 2.
- **Constructor over-injection**: runtime data (a batch, a request) in a constructor. Move to the method.
- **Newable holding an injectable**: a value object with a service reference — untestable without the service graph.
- **Pre-emptive injection**: injecting `nn.LayerNorm`, the FFN, every projection "for flexibility" nobody asked for. Indirection has a cost; you can no longer see what the object is made of. Construct the definitional parts; punch a defaulted factory hole *when* a variation point is discovered, not before.

## The Time Dimension

Caste membership is empirical, not metaphysical. `nn.Linear` sat firmly in the newable caste until LoRA and quantization made people want to substitute it. The rule with its time dimension:

> Construct what is definitional and derived; inject what is variational — knowing you will sometimes discover a "definitional" part was variational, and the fix is one more defaulted factory hole (`norm_layer=nn.BatchNorm2d`).

## The Limit: Constructor Over-Injection

Injection has a limit, and it is cohesion, not a hard count. Seemann's rule of thumb: past ~4 injected dependencies the smell flips — the class is injecting at too fine a grain and is missing intermediate abstractions. **The cure is not to start constructing things internally; it is to group collaborators that always travel together** (Seemann: *facade services*).

Warning signs:

- The constructor reads as a parts list of leaf modules rather than a statement of what the class is parameterized by.
- Several injected deps are only ever used together, in a fixed pattern — a pipeline fragment masquerading as independent parts.
- The wrapper checks dimension/compatibility contracts *between* injected deps (`assert ref_extractor.dim == proj.in_features`) — cross-module invariants it shouldn't own.
- Every call site repeats the same multi-object assembly.

```python
# BAD — seven leaf injections; dim contracts live in the wrapper; every caller assembles everything
class Verifier(nn.Module):
    def __init__(self, hidden_dim, ffn, fpn, ref_extractor,
                 attn_factory, resampler, pool):
        self.proj = nn.Linear(ref_dim_from_somewhere, hidden_dim)   # whose dim?
        ...
```

The recipe:

1. **Find the clusters.** Deps that only function as a unit are a missing class. `fpn + level_proj + pool` is an *observation tokenizer*; `ref_extractor + proj + resampler` is a *reference tokenizer*.
2. **Each facade owns its derived glue.** The cluster class constructs its own projections/norms because their dims derive from the collaborator it holds. This needs collaborators to expose their output dims — give extractors an `out_dim` attribute (detectron2 precedent: backbones expose `output_shape()`, consumers derive their own layers from it).
3. **Re-apply the decision table at the new grain.** The top class now injects 2–4 coarse modules. Precedent: detectron2's `GeneralizedRCNN(backbone, proposal_generator, roi_heads)` — top-level models aggregate a few coarse modules, never ten leaf modules.
4. **Add a composition root.** Pair the honest injected constructor with preset builders that own assembly — torchvision's split between `ResNet(block=...)` (fully injected, nobody suffers) and `resnet50()` (the preset). Experiments edit presets; the class never changes.

```python
# GOOD — stratified: three injection points; dim derived from the encoder (rung 2
# of the Enforcement Ladder), facades own their internal dim contracts
class Verifier(nn.Module):
    def __init__(self, obs_encoder: nn.Module,      # (image, proposals) -> B,N,out_dim
                 ref_encoder: nn.Module,            # (image) -> B,K,out_dim
                 attn_factory: AttnFactory):
        ...
        hidden_dim = obs_encoder.out_dim            # single source of truth
        assert ref_encoder.out_dim == hidden_dim
        self.layers = nn.ModuleList(attn_factory(hidden_dim) for _ in range(L))
        self.logit_proj = nn.Linear(hidden_dim, 1)  # derived newable — construct

def verifier_dift(hidden_dim=256) -> Verifier:      # composition root / preset:
    return Verifier(                                # one lexical hidden_dim, threaded
        obs_encoder=ObsEncoder(DiftFpn(...), hidden_dim, pool="attn"),
        ref_encoder=RefEncoder(M2FExtractor(...), hidden_dim, num_latents=8),
        attn_factory=partial(LightGlueAttn, num_heads=4, flash=False))
```

The axes of variation don't disappear — they stratify. Which extractor is an `ObsEncoder`-level question; how tokens mix is a `Verifier`-level question. Each layer carries 2–3 axes instead of one layer carrying seven.

**Early-stage corollary.** Feeling "everything is an axis of variation" at design time is normal and is not a reason to inject everything. The cost asymmetry decides: promoting a constructed part to injected later is one defaulted parameter (cheap, mechanical, no call sites break); carrying a speculative injection is a recurring cost at every config, every reader, every wiring. So: **inject only the axes actively being varied right now; construct the rest with explicit hyperparams; promote on demand.** "I might want to vary it someday" is the pre-emptive-injection smell wearing a research-code costume.

## When Applying This Skill

1. **List every dependency** the class touches; tag each newable or injectable (would any test or second caller substitute it? is its config fully derived from yours?).
2. **Newables with derived config** → construct in `__init__`; no parameters for them in your signature.
3. **Injectables, exactly one, matching lifetime** → instance parameter. If it must dimensionally agree with you or with other injected parts, require an exposed `out_dim`-style attribute, then derive or assert (Enforcement Ladder — never rung 0).
4. **Injectables, many copies or consumer-controlled timing** → factory parameter; split its params by ownership (structural → call-time, flavor → bound by caller).
5. **Anything derived from runtime data** → method argument.
6. **Hunt the smells**: forwarded ctor params, `**kwargs` relays, duplicate-and-assert dims, modules built in `forward`, tensors in `__init__`.
7. **Count the injection points** — past ~4, look for deps that only travel together and group each cluster into a facade module that owns its derived glue (see The Limit); then add a preset builder as the composition root.
8. **Don't pre-emptively inject** — inject only axes actively being varied; add defaulted factory holes when variation is demanded, defaulting to current behavior.

## Related Skills

- [separate-mechanism-policy](../separate-mechanism-policy/SKILL.md) — this skill is mechanism/policy applied to object construction: *which implementation a dependency gets* is a policy decision that belongs to the caller, and a factory parameter is how mechanism receives it. Its identity-vs-choice-point test is the same boundary as definitional-vs-variational here.
- [fold-knowledge-into-data](../fold-knowledge-into-data/SKILL.md) — where the bound half of a factory's params should live. A registry mapping names to classes/partials (its Case Study 4, and the `OPTIMIZERS` table of partials) is a *table of factories*: the config layer declares the flavor params as data, and the consuming class stays stupid.
