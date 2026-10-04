---
name: write-rules
description: "Write Mendix rules — a special kind of microflow returning a Boolean or enumeration, callable only from a decision. Use when writing CREATE RULE, or deciding whether logic belongs in a rule or a microflow."
---

# Mendix Rule Skill

Guidance for writing Mendix **rules** in MDL. Mendix's own reference calls a rule
["a special kind of microflow"](https://docs.mendix.com/refguide/rules/): it
returns a Boolean or an enumeration, and it can only be used from a decision.

## When to Use This Skill

- Writing `CREATE RULE` statements
- Deciding whether logic belongs in a rule or a microflow
- Understanding what `mxcli check` refuses in a rule body and why

The mirrors are [write-microflows](../write-microflows/SKILL.md) and
[write-nanoflows](../write-nanoflows/SKILL.md) — a rule is the third flavour and
shares their body syntax exactly.

## When to Use a Rule vs a Microflow

| Scenario | Use |
|----------|-----|
| One condition, evaluated from several decisions | Rule |
| A named business condition the model should show by name | Rule |
| Choosing one of several enumerated outcomes from input | Rule |
| Anything that changes data | Microflow |
| Anything the user sees (page, message, download) | Microflow |
| Anything that talks to another system | Microflow |

**Rule of thumb:** a rule *answers a question*. The moment it needs to *do*
something, it is a microflow.

## Key Differences from Microflows

| Aspect | Microflow | Rule |
|--------|-----------|------|
| **Return type** | Anything, including void | Boolean or enumeration — mandatory |
| **Called from** | Anywhere | A decision, and nowhere else |
| **Changes data** | Yes | No |
| **Talks to the client** | Yes | No |
| **Integration** | Yes | No |
| **Module-role security** | `grant execute on microflow …` | None — a rule has no security to grant |

That last row is not an mxcli omission. A rule document stores no
`AllowedModuleRoles`, because a rule is never called on its own; it is reached
through the microflow that evaluates it, and that microflow's security applies.

## Syntax

```
mdl 1;
create or modify rule Sales.Rule_IsSolvent ($pCustomer: Sales.Customer)
returns Boolean
folder 'Rules'
begin
  return $pCustomer/Balance >= 0;
end;
```

An enumeration rule lets one decision fan out to several branches:

```
mdl 1;
create or modify rule Sales.Rule_Outcome ($pCustomer: Sales.Customer)
returns enum Sales.Outcome
begin
  if $pCustomer/Balance >= 0 then
    return Sales.Outcome.Approved;
  else
    return Sales.Outcome.Rejected;
  end if;
end;
```

Calling one — the only place a rule may be called:

```
mdl 1;
create or modify microflow Sales.MF_Screen ($pCustomer: Sales.Customer)
begin
  if Sales.Rule_IsSolvent(pCustomer = $pCustomer) then
    return;
  else
    return;
  end if;
end;
```

The argument names are the rule's parameter names, so
`Rule_IsSolvent(pCustomer = $pCustomer)` reads the same way a microflow call does.

## Reading and managing rules

```
mdl 1;
list rules;                  -- `list rules` is the same statement
list rules in Sales;
describe rule Sales.Rule_IsSolvent;   -- round-trippable MDL
drop rule Sales.Rule_IsSolvent;
move rule Sales.Rule_IsSolvent to folder 'Rules/Customer';
```

`list microflows` lists microflows only — not nanoflows, not workflows, and not
rules. Each doctype has its own listing.

`list callers of Sales.Rule_IsSolvent` lists the microflows whose decisions
evaluate it, and a microflow called from inside a rule's body is a normal
reference: it will not be reported as dead code.

## What a rule may not contain

`mxcli check` refuses these before the build, with the same function `exec` uses,
so the two cannot disagree. Each was measured against mxbuild 11.13.0:

| Written in a rule | mxbuild says |
|---|---|
| `create` / `change` / `delete` / `commit` / `rollback` | CE0009 "This action is not supported in rules." |
| `show page`, `close page`, `show message`, validation feedback, download | CE0009 |
| `call web service` | CE0009 |
| A void, String, Integer … return type | CE0103 and CE0139 — the return type must be Boolean or an enumeration |

A missing `returns` clause is refused too. For a microflow, void is a legitimate
choice; for a rule it means the decision calling it has nothing to branch on.

## Validation checklist

Before presenting a rule:

- [ ] `returns Boolean` or `returns enum Module.Enum` is present
- [ ] The body only reads — no create/change/delete/commit/rollback
- [ ] Nothing in the body touches the client or another system
- [ ] Every path returns a value of the declared type
- [ ] The caller is a decision: `if Module.Rule_Name(Param = $Value) then`
- [ ] `mxcli check script.mdl -p app.mpr --references` passes

## Rules (LIST/DESCRIBE/CREATE [OR MODIFY]/DROP/MOVE RULE)

Mendix's "special kind of microflow" — returns Boolean or an enumeration, callable only from a decision. Handled as a third flow flavour beside microflows and nanoflows: its own semantic type, its own listing (`list microflows` stays microflow-only), the shared `microflowBody`, flow builder and describer. The document is the ten properties a Studio Pro rule stores, pinned against two reference rules (ako/TestApp, 11.13.0) — **no `AllowedModuleRoles`** (a rule is not independently callable, so there is no `grant execute on rule`) and **no `ReturnType`** despite gen declaring one beside `MicroflowReturnType`. Two keys only a reference document catches, both invisible to `mx check`: `ExportLevel` (Studio Pro writes "Hidden" on every rule) and `Flows` (written as the bare marker even when empty — a `MandatoryLists` entry). Rules are catalog objects and their bodies are walked for references, which together stop a microflow called only from a rule reading as dead. The body restrictions are refused at check time by the same function `exec` calls, each measured: create/change/delete/commit/rollback and client or web-service activities are **CE0009**, a non-Boolean/enum return is **CE0103 + CE0139**. Authoring is modelsdk-only; legacy refuses.
