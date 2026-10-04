---
name: "Delphi Clean Code"
description: "Pragmatic clean code standards for Delphi — concise, direct, no over-engineering"
---

# Delphi Clean Code — Skill

> **CRITICAL SKILL** — Be **concise, direct and solution-focused**.

## Fundamental Principles

| Principle | Rule |
|-----------|-------|
| **SRP** | A function/class does ONE thing |
| **DRY** | Don't repeat code — extract and reuse |
| **KISS** | Simplest solution that works |
| **YAGNI** | Don't build what wasn't asked for |
| **Boy Scout** | Leave the code better than you found it |

## Naming Rules (Pascal Guide)

| Element | Convention |
|----------|-----------|
| **Variables** | Reveal intent: `LCustomerCount` not `N` |
| **Methods** | Verb + noun: `GetCustomerById` not `Customer` |
| **Booleans** | Question form: `IsActive`, `HasPermission`, `CanEdit` |
| **Constants** | SCREAMING_SNAKE: `MAX_RETRY_COUNT` |
| **Fields** | Prefix `F`: `FCustomerName` |
| **Parameters** | Prefix `A`: `ACustomerName` |
| **Var. locations** | Prefix `L`: `LCustomer` |

> **Rule:** If you need a comment to explain a name, rename it.

## Method Rules

| Rule | Description |
|-------|-----------|
| **Short** | Maximum 20 lines, ideal 5-10 |
| **One Thing** | Do one thing and do it well |
| **One Level** | One level of abstraction per method |
| **Few Args** | Maximum 3 arguments, prefer 0-2 |
| **No Side Effects** | Don't mute inputs unexpectedly |

## Code Structure

| Standard | Application |
|--------|-----------|
| **Guard Clauses** | Early returns for edge cases |
| **Flat > Nested** | Avoid deep nesting (max 2 levels) |
| **Composition** | Small compound methods |
| **Colocation** | Related code together |

### Guard Clauses in Delphi

```pascal
// ❌ RUIM — nesting excessivo
procedure ProcessOrder(AOrder: TOrder);
begin
  if Assigned(AOrder) then
  begin
    if AOrder.Items.Count > 0 then
    begin
      if AOrder.IsValid then
      begin
        // logic real aqui
      end;
    end;
  end;
end;

// ✅ BOM — guard clauses
procedure ProcessOrder(AOrder: TOrder);
begin
  if not Assigned(AOrder) then
    raise EArgumentNilException.Create('AOrder cannot be nil');
  if AOrder.Items.Count = 0 then
    raise EBusinessRuleException.Create('Order must have items');
  if not AOrder.IsValid then
    raise EValidationException.Create('Order validation failed');

  // logic real aqui — sem nesting
end;
```

## Anti-Patterns (DO NOT DO)

| ❌ Pattern | ✅ Fix |
|-----------|------------|
| Comment each line | Delete obvious comments |
| Method > 20 lines | Share by responsibility |
| Magic numbers | Named constants |
| `with` statement | Explicit local variables |
| Global variables | Constructor injection |
| Generic Catch | Specific exceptions |
| Logic in `OnClick` | Delegate to Service |
| God class / God unity | One class = one responsibility |
| Ignore `Free` | `try/finally` always |

## Memory Management

```pascal
// ✅ Objetos temporários — sempre try/finally
LList := TStringList.Create;
try
  LList.Add('item');
  // usar LList
finally
  LList.Free;
end;

// ✅ Interfaces — reference counting automático
var LService: IMyService;
LService := TMyService.Create; // liberado automaticamente

// ✅ Owner pattern para componentes visuais
LButton := TButton.Create(Self); // Self libera automaticamente
```

## AI Code Style

| Situation | Action |
|----------|------|
| User requests feature | Write directly |
| User reports bug | Correct, don't explain |
| Requirement unclear | Ask, don't assume |

## 🔴 Before Editing (THINK FIRST!)

| Question | Why |
|----------|---------|
| **Which units use this?** | They can break |
| **What does this unit matter?** | Interfaces can change |
| **What tests cover this?** | Tests may fail |
| **Is it a shared component?** | Multiple points affected |

> 🔴 **Rule:** Edit the file + all dependents in the SAME task.

## 🔴 Self-Check (MANDATORY)

| Check | Pergunta |
|-------|----------|
| ✅ **Goal achieved?** | Did I do exactly what was asked? |
| ✅ **Edited files?** | Have I modified everything necessary? |
| ✅ **Does the code work?** | Have I tested/verified? |
| ✅ **No errors?** | Compiles without warnings? |
| ✅ **Nothing forgotten?** | Edge cases treated? |
| ✅ **Memory safe?** | Objects released correctly? |

> 🔴 **Rule:** If ANY check fails, correct it before finishing.
