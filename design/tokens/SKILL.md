---
name: tokens
description: Audits whether the colors on a Figma frame or page are bound to design system tokens, and maps and binds hardcoded colors to the right token. Derives token-to-hex from bindings already in the file so every mapping has evidence, grades the results, and auto-proposes only the safe ones. Lint mode (check only) and bind mode are separate. Which library and which token groups come from the design_system section of figma-conventions.yaml; on auto it detects the library the file is connected to. Triggers - "/fig:tokens", "check the token bindings", "find unbound colors", "토큰 바인딩 검수", "하드코딩 색상 검사", "디자인시스템 연동 점검".
allowed-tools: AskUserQuestion, mcp__plugin_figma_figma__use_figma, mcp__plugin_figma_figma__search_design_system, mcp__plugin_figma_figma__get_screenshot, mcp__plugin_figma_figma__get_metadata, mcp__plugin_figma_figma__whoami
---

# fig:tokens — audit and repair design system token bindings

Checks whether the colors inside a frame are actually bound to design system variables, and connects unbound hardcoded colors to a token through **a mapping that has evidence behind it**. Theming, rebranding, and consistency only hold if every color goes through a token, so this runs as the last check before handoff.

**Prerequisites**: always load the `figma:figma-use` skill before calling `use_figma`.

**Seat check before the first write** — call `whoami` once. Where every plan it lists carries `seat: View`, stop before any `use_figma` write and say so: the reading half of this skill runs on a View seat, the writing half needs an Edit seat on the file's plan, and no retry changes that. Where the seats are mixed, go ahead — and if the first write comes back as a permission error, report the seat table and stop rather than retrying.

## When to invoke

- "check whether this frame's colors are all bound", "find colors that aren't on a variable"
- "convert the hardcoded hex values to tokens"
- The token check right before handoff, once the design is done

## When NOT to invoke

- Frame naming and section tidying → `/fig:prep`
- Structure and flow rule violations → `/fig:lint`
- Flow arrows → `/fig:arrows`
- Creating the tokens (variables) themselves → `figma:figma-generate-library`
- Designing screens → `/fig:draw`

## Inputs

- `figma_url` (required): the page or frame to audit
- `mode` (optional): lint mode (check only) / bind. Omitted, it checks and proposes a mapping table

The rules come from `figma-conventions.yaml` — read the `design_system` section (library, token groups, thresholds) with `resolve-config.py --js <fileKey>`.

## Why this needs its own skill — tool constraints

- **`get_metadata` cannot see colors.** Metadata carries node id, type, coordinates, and size, with no fill, stroke, or effect color. On a large frame it also blows the token limit and fails wholesale. So **all color inspection and binding walks nodes directly through a `use_figma` script.**
- **`search_design_system` does not return a token's hex.** It returns the name, key, scope, and owning library. The actual color has to be worked out separately (see below).

## Where token values come from — auto-detection plus reverse-derivation (the core)

A mapping is only as trustworthy as your knowledge of "what color is this token, really". Two routes run together.

1. **Detect the connected library**: query the token groups in `design_system.token_prefixes` with `search_design_system` to get names and keys. `design_system.library` decides the target, and on `auto` it detects the library the file is connected to. **Never hardcode a library name in this document** — it differs per file. When `token_prefixes` is empty, use whatever prefixes appear in the reverse-derived map (route 2) as candidates.
2. **Reverse-derive token-to-hex from existing bindings (the most reliable)**: walk the colors in the same file that are *already bound to a variable* and build a `{token name → actual hex}` map. A bound paint carries both the token id in `boundVariables.color` and the last resolved color in `paint.color`. That shows exactly what color this file actually renders that token as, which makes it the primary evidence for any mapping.

> **Caution — a token's real value may differ from the hex you were given.** "Change this grey to `fill/primary`" can still mean `fill/primary` is slightly different from that grey (which is fine if tokenizing is the goal). Whenever the color changes, **the preview must say "this token is #AAA, so the screen becomes #BBB".**

## Properties checked

fill · stroke · text color (a TEXT node's fills) · effect color (an effect's color) are all checked. Different properties match different token scopes — a background fill against `FRAME_FILL`/`SHAPE_FILL`, a border against `STROKE`, text against `TEXT_FILL`. **Only map a property to a token whose scope fits it** — never bind a text color to a border token.

## Excluded (untouched in both audit and binding)

| Target | Why |
|---|---|
| Colors **inside a component instance** | They are instance overrides, fragile, and really a separate issue to be tokenized on the source component in the library. The instance node's *own* color (an override) is in scope; its *children* are not |
| Working scaffolding | Nodes matching the scaffolding name conventions in `naming` (`arrow_delimiter`, `label_prefix`, `state_chain_prefix`) and anything painted with `section_style` or `placeholder_style` — those are `/fig:arrows` and `/fig:prep` output, not design to tokenize |
| User-designated protected areas | Archives, templates, and the like |

Excluded items that turn up are **reported, never fixed** — colors inside instances in particular get grouped separately as "a component repair issue".

## Grading — only auto-propose what is safe

Each unbound color is compared against the nearest token of the same property and graded.

| Grade | Basis | Handling |
|---|---|---|
| 1 — exact or near match | Identical to the token's hex, or within `design_system.match_threshold_channel` per channel | Binding effectively does not change the color → **auto-propose the mapping** |
| 2 — color shifts | Visibly different from the nearest token (off-palette) | Snapping changes the color → **report only; the user decides** |
| 3 — no matching token | Far from every token, or a brand or special color | Binding not advised, report only |

The threshold is a baseline, not a verdict — for borderline colors, show the delta so the user can judge.

## Lint mode — check only (no writes)

For "just check" requests, or the survey step before repair. Read-only, report only:

- Unbound colors in scope **aggregated by hex** (property, count, representative locations), classified as inside-instance / scaffolding / directly editable
- Directly editable colors get the grade table plus a recommended token and delta
- Nothing is changed; proceeding requires a separate go into the procedure below

## Procedure

### 1. Build the token dictionary

- Get names and keys for the configured token groups via `search_design_system`
- Walk the target frames and build the **existing binding → {token name, actual hex}** reverse map
- Merge both into a `{token name, key, scope, hex}` dictionary — the evidence table behind every mapping

### 2. Scan for unbound colors (read-only)

- Walk the target frames and aggregate **SOLID and unbound** colors from fills, strokes, text, and effects, by hex
- Classify each node as inside-instance / scaffolding / directly editable (see the snippet below)
- For the directly editable ones, compare against the dictionary to derive grade, recommended token, and delta → the mapping table

### 3. Settle the mapping (user's choice)

- Present grade 1 as a table. **When one hex matches two tokens with different meanings equally** (white matching both a static white and a background token, say), do not pick — present the difference in meaning and let the user choose
- Grades 2 and 3 are reported only; the user decides whether to proceed
- Any mapping that changes the color says so explicitly

### 4. Bind (preview → go, split into steps)

- Show the settled mapping as a **preview** (targets, hex → token, counts, exclusions) and get a **go**
- With a lot to do, **split by frame or by color** — never write it all at once
- Import tokens with `importVariableByKeyAsync`, and bind only unbound paints whose hex matches exactly

### 5. Verify (required)

- **Re-scan after binding** and confirm "unbound remainder among the targeted, directly editable colors = 0"
- The count from the aggregation step and the number actually bound may differ — the traversal boundary for nodes inside instances can shift between calls, changing the classification (inferred). **Prove nothing was missed by the re-scan reaching zero**, and report the discrepancy honestly
- Report remaining inside-instance colors and grades 2–3 separately, as out of scope for this pass

## Implementation snippets

Color to hex, and the inside-instance test:

```js
function hex(c){const f=x=>Math.round(x*255).toString(16).padStart(2,"0").toUpperCase();return "#"+f(c.r)+f(c.g)+f(c.b);}
function insideInstance(n){let p=n.parent;while(p){if(p.type==="INSTANCE")return true;p=p.parent;}return false;}
```

Reverse-deriving token to hex from existing bindings:

```js
const map={}; // varId -> {name, hexes:{}, count}
for(const id of ROOT_IDS){
  const root=await figma.getNodeByIdAsync(id);
  for(const n of [root,...root.findAll(()=>true)]){
    for(const key of ["fills","strokes"]){
      const arr=n[key]; if(!Array.isArray(arr)) continue;
      for(const p of arr){
        if(p.type==="SOLID"&&p.visible!==false&&p.boundVariables&&p.boundVariables.color){
          const vid=p.boundVariables.color.id;
          if(!map[vid]){const v=await figma.variables.getVariableByIdAsync(vid);map[vid]={name:v?v.name:"?",hexes:{},count:0};}
          map[vid].count++; const h=hex(p.color); map[vid].hexes[h]=(map[vid].hexes[h]||0)+1;
        }
      }
    }
  }
}
return Object.values(map).map(e=>({name:e.name,count:e.count,hex:Object.keys(e.hexes).join(",")}));
```

Aggregating unbound colors (editable versus inside-instance):

```js
const agg={};
for(const id of ROOT_IDS){
  const root=await figma.getNodeByIdAsync(id);
  for(const n of [root,...root.findAll(()=>true)]){
    const ii=insideInstance(n);
    for(const key of ["fills","strokes"]){
      const arr=n[key]; if(!Array.isArray(arr)) continue;
      for(const p of arr){
        if(p.type!=="SOLID"||p.visible===false) continue;
        if(p.boundVariables&&p.boundVariables.color) continue;
        const k=key+"|"+hex(p.color);
        if(!agg[k]) agg[k]={prop:key,hex:hex(p.color),editable:0,inInstance:0,examples:[]};
        agg[k][ii?"inInstance":"editable"]++;
        if(agg[k].examples.length<4) agg[k].examples.push((ii?"⟨inst⟩":"")+n.name+" ["+n.type+"]");
      }
    }
  }
}
return Object.values(agg).sort((a,b)=>b.editable-a.editable);
```

> Text colors arrive in `fills` above, on TEXT nodes. Effect colors are checked the same way through `n.effects[].color`, and bound through the effect-specific API (check the `setBoundVariableForEffect` family in the d.ts).

Binding (exact hex match only, reassigning a new paint array):

```js
const V={ tokenA: await figma.variables.importVariableByKeyAsync("KEY_A"), /* ... */ };
const fillMap={"#FFFFFF":V.tokenA, /* hex: variable */ };
const strokeMap={/* ... */};
const counts={};
const root=await figma.getNodeByIdAsync(FRAME_ID);
for(const n of [root,...root.findAll(()=>true)]){
  if(insideInstance(n)) continue;                 // skip inside instances
  for(const [key,mapObj] of [["fills",fillMap],["strokes",strokeMap]]){
    const arr=n[key]; if(!Array.isArray(arr)||!arr.length) continue;
    let changed=false;
    const next=arr.map(p=>{
      if(p.type==="SOLID"&&p.visible!==false&&!(p.boundVariables&&p.boundVariables.color)){
        const v=mapObj[hex(p.color)];
        if(v){changed=true;counts[v.name]=(counts[v.name]||0)+1;return figma.variables.setBoundVariableForPaint(p,"color",v);}
      }
      return p;                                    // fills is read-only — build a new array with map
    });
    if(changed) n[key]=next;
  }
}
return {frame:FRAME_ID, counts};
```

Verification (confirm zero remaining):

```js
let editableLeft=0;
for(const id of ROOT_IDS){
  const root=await figma.getNodeByIdAsync(id);
  for(const n of [root,...root.findAll(()=>true)]){
    if(insideInstance(n)) continue;
    for(const key of ["fills","strokes"]){
      const arr=n[key]; if(!Array.isArray(arr)) continue;
      for(const p of arr){
        if(p.type==="SOLID"&&p.visible!==false&&!(p.boundVariables&&p.boundVariables.color)&&TARGET_HEXES.includes(hex(p.color))) editableLeft++;
      }
    }
  }
}
return {editableLeft};   // must be 0 to be done
```

## Constraints

- **Preview → go before writing.** Settling the mapping and running the binding are separate; binding is split by frame or by color
- **Never touch colors inside instances or scaffolding** — report only
- Only map where the property and the token scope agree (text color to a text token, and so on)
- Any mapping that changes the color says so in the preview — never assume the color is unchanged from the token's name
- Keep each call small, verifying between steps with a re-scan or a screenshot
- Never write "done" without verification — prove zero remaining with a re-scan

## Notes

- The primary evidence for a mapping is always **what value this file actually renders that token as** (the reverse-derived map). Never infer from how a token's name sounds
- "Lots of unbound colors" does not automatically mean somebody forgot — off-palette colors may simply have found their way in, so grades 2 and 3 go back to design judgement
- A mass of hardcoded colors inside instances is not this skill's scope; raise it separately as **a component library repair task**
