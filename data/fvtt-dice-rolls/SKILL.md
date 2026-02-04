---
name: fvtt-dice-rolls
description: This skill should be used when implementing dice rolling, creating Roll formulas, sending rolls to chat with toMessage, preparing getRollData, creating custom dice types, or handling roll modifiers like advantage/disadvantage. Covers Roll class, evaluation, and common patterns.
---

# Foundry VTT Dice Rolls

**Domain:** Foundry VTT Module/System Development
**Status:** Production-Ready
**Last Updated:** 2026-01-04

## Overview

Foundry VTT provides a powerful dice rolling system built around the `Roll` class. Understanding this system is essential for implementing game mechanics.

### When to Use This Skill

- Creating roll formulas with variable substitution
- Implementing attack rolls, damage rolls, saving throws
- Sending rolls to chat with proper speaker/flavor
- Preparing actor/item roll data with getRollData()
- Creating custom dice types for specific game systems
- Using roll modifiers (keep, drop, explode, reroll)

## Roll Class Basics

### Constructor

```javascript
const roll = new Roll(formula, data, options);
```

- `formula`: Dice expression string (e.g., "2d20kh + @prof")
- `data`: Object for @ variable substitution
- `options`: Optional configuration

```javascript
const roll = new Roll("2d20kh + @prof + @strMod", {
  prof: 2,
  strMod: 4
});
```

### Formula Syntax

```javascript
// Basic dice
"1d20"          // Roll one d20
"4d6"           // Roll four d6

// Variables with @ syntax
"1d20 + @abilities.str.mod"
"1d20 + @prof"

// Nested paths
"@classes.barbarian.levels"
"@abilities.dex.mod"

// Parenthetical (dynamic dice count)
"(@level)d6"    // Roll [level] d6s

// Dice pools
"{4d6kh3, 4d6kh3, 4d6kh3}"  // Multiple separate rolls
```

## Roll Evaluation

### Async evaluate() - REQUIRED

```javascript
const roll = new Roll("1d20 + 5");
await roll.evaluate();

console.log(roll.result);  // "15 + 5"
console.log(roll.total);   // 20
```

**Critical:** `roll.total` is undefined until evaluated.

### Evaluation Options

```javascript
await roll.evaluate({
  maximize: true,    // All dice roll max value
  minimize: true,    // All dice roll min value
  allowStrings: true // Don't error on string terms
});
```

### Sync Evaluation (Deterministic Only)

```javascript
// Only for maximize/minimize (deterministic)
roll.evaluateSync({ strict: true });

// With strict: false, non-deterministic = 0
roll.evaluateSync({ strict: false });
```

## Roll.toMessage()

Sends a roll to chat as a ChatMessage.

### Basic Usage

```javascript
await roll.toMessage();
```

### With Options

```javascript
await roll.toMessage({
  speaker: ChatMessage.getSpeaker({ actor: this.actor }),
  flavor: "Attack Roll",
  user: game.user.id
}, {
  rollMode: game.settings.get("core", "rollMode")
});
```

### Roll Modes

| Mode | Command | Visibility |
|------|---------|------------|
| Public | `/roll` | Everyone |
| GM | `/gmroll` | Roller + GM |
| Blind | `/blindroll` | GM only |
| Self | `/selfroll` | Roller only |

**Always respect user's roll mode:**
```javascript
rollMode: game.settings.get("core", "rollMode")
```

## getRollData()

Prepares data context for roll formulas.

### Actor getRollData()

```javascript
getRollData() {
  // Always return a COPY
  const data = foundry.utils.deepClone(this.system);

  // Add shortcuts
  data.lvl = data.details.level;

  // Flatten ability mods for easy access
  for (const [key, ability] of Object.entries(data.abilities)) {
    data[key] = ability.mod;  // @str, @dex, etc.
  }

  return data;
}
```

### Item getRollData()

Merge item and actor data:

```javascript
getRollData() {
  const data = foundry.utils.deepClone(this.system);

  if (!this.actor) return data;

  // Merge actor's roll data
  return foundry.utils.mergeObject(
    this.actor.getRollData(),
    data
  );
}
```

### Debugging Roll Data

```javascript
// In console with token selected:
console.log(canvas.tokens.controlled[0].actor.getRollData());
```

## Roll Modifiers

### Keep/Drop

```javascript
"4d6kh3"   // Keep 3 highest (ability scores)
"4d6kl3"   // Keep 3 lowest
"4d6dh1"   // Drop 1 highest
"4d6dl1"   // Drop 1 lowest
"2d20kh"   // Advantage (keep highest)
"2d20kl"   // Disadvantage (keep lowest)
```

### Exploding Dice

```javascript
"5d10x"    // Explode on max (10)
"5d10x8"   // Explode on 8+
"2d10xo"   // Explode once per die
```

### Reroll

```javascript
"1d20r1"    // Reroll 1s (once)
"1d20r<3"   // Reroll below 3 (once)
"1d20rr<3"  // Recursive reroll while < 3
```

### Count Successes

```javascript
"10d6cs>4"  // Count successes > 4
"10d6cf<2"  // Count failures < 2
```

### Min/Max

```javascript
"1d20min10"  // Minimum result 10
"1d20max15"  // Maximum result 15
```

## Common Patterns

### Attack Roll

```javascript
async rollAttack() {
  const rollData = this.actor.getRollData();

  const parts = ["1d20"];
  if (this.system.proficient) parts.push("@prof");
  if (this.system.ability) parts.push(`@${this.system.ability}.mod`);
  if (this.system.attackBonus) parts.push(this.system.attackBonus);

  const formula = parts.join(" + ");
  const roll = new Roll(formula, rollData);
  await roll.evaluate();

  return roll.toMessage({
    speaker: ChatMessage.getSpeaker({ actor: this.actor }),
    flavor: `${this.name} - Attack Roll`,
    rollMode: game.settings.get("core", "rollMode")
  });
}
```

### Damage Roll (with Critical)

```javascript
async rollDamage(critical = false) {
  const rollData = this.actor.getRollData();

  let formula = this.system.damage.formula;

  // Add ability mod
  if (this.system.damage.ability) {
    formula += ` + @${this.system.damage.ability}.mod`;
  }

  // Double dice on critical
  if (critical) {
    formula = formula.replace(/(\d+)d(\d+)/g, (m, num, faces) => {
      return `${num * 2}d${faces}`;
    });
  }

  const roll = new Roll(formula, rollData);
  await roll.evaluate();

  return roll.toMessage({
    speaker: ChatMessage.getSpeaker({ actor: this.actor }),
    flavor: `${this.name} - ${critical ? "Critical " : ""}Damage`,
    rollMode: game.settings.get("core", "rollMode")
  });
}
```

### Ability Check with Advantage/Disadvantage

```javascript
async rollAbility(abilityId, { advantage = false, disadvantage = false } = {}) {
  const rollData = this.actor.getRollData();

  let dieFormula = "1d20";
  if (advantage && !disadvantage) dieFormula = "2d20kh";
  if (disadvantage && !advantage) dieFormula = "2d20kl";

  const formula = `${dieFormula} + @abilities.${abilityId}.mod`;
  const roll = new Roll(formula, rollData);
  await roll.evaluate();

  return roll.toMessage({
    speaker: ChatMessage.getSpeaker({ actor: this.actor }),
    flavor: `${CONFIG.abilities[abilityId]} Check`,
    rollMode: game.settings.get("core", "rollMode")
  });
}
```

### Sheet Rollable Button

```javascript
// In activateListeners
html.on("click", ".rollable", this._onRoll.bind(this));

async _onRoll(event) {
  event.preventDefault();
  const element = event.currentTarget;
  const { roll: formula, label } = element.dataset;

  if (!formula) return;

  const roll = new Roll(formula, this.actor.getRollData());
  await roll.evaluate();

  return roll.toMessage({
    speaker: ChatMessage.getSpeaker({ actor: this.actor }),
    flavor: label || "Roll",
    rollMode: game.settings.get("core", "rollMode")
  });
}
```

**Template:**
```html
<a class="rollable" data-roll="1d20 + @str" data-label="Strength Check">
  <i class="fas fa-dice-d20"></i> Roll
</a>
```

## Custom Dice

### Custom Die Class

```javascript
export class StressDie extends foundry.dice.terms.Die {
  static DENOMINATION = "s";  // Use as "1ds"

  async evaluate(options = {}) {
    await super.evaluate(options);

    // Custom logic: explode on 6, panic on 1
    for (const result of this.results) {
      if (result.result === 6) result.exploded = true;
      if (result.result === 1) result.panic = true;
    }

    return this;
  }
}
```

### Custom Roll Class

```javascript
export class CustomRoll extends Roll {
  static CHAT_TEMPLATE = "systems/mysystem/templates/roll.hbs";

  get successes() {
    return this.dice.reduce((sum, die) => {
      return sum + die.results.filter(r => r.success).length;
    }, 0);
  }
}
```

### Registration

```javascript
Hooks.once("init", () => {
  CONFIG.Dice.terms.s = StressDie;
  CONFIG.Dice.rolls.push(CustomRoll);
});
```

**Critical:** Register custom rolls or they won't reconstruct from chat messages.

## Common Pitfalls

### 1. Using total Before evaluate()

```javascript
// WRONG - total is undefined
const roll = new Roll("1d20");
console.log(roll.total);  // undefined!

// CORRECT
const roll = new Roll("1d20");
await roll.evaluate();
console.log(roll.total);  // 15
```

### 2. Ignoring Roll Mode

```javascript
// WRONG - always public
roll.toMessage();

// CORRECT - respects user setting
roll.toMessage({}, {
  rollMode: game.settings.get("core", "rollMode")
});
```

### 3. Modifying getRollData() Return

```javascript
// WRONG - modifies document data
getRollData() {
  return this.system;  // Direct reference!
}

// CORRECT - return a copy
getRollData() {
  return foundry.utils.deepClone(this.system);
}
```

### 4. Stale Roll Data

```javascript
// WRONG - data captured once
const rollData = this.actor.getRollData();
// ...actor updates...
new Roll("1d20 + @prof", rollData);  // Stale!

// CORRECT - get fresh data
new Roll("1d20 + @prof", this.actor.getRollData());
```

### 5. Unvalidated User Input

```javascript
// UNSAFE
const roll = new Roll(userInput);

// SAFER - validate first
if (!Roll.validate(userInput)) {
  ui.notifications.error("Invalid roll formula");
  return;
}
const roll = new Roll(userInput, rollData);
```

### 6. Forgetting to Register Custom Rolls

```javascript
// WRONG - rolls break on reload
class MyRoll extends Roll {}

// CORRECT - register with CONFIG
class MyRoll extends Roll {}
CONFIG.Dice.rolls.push(MyRoll);
```

### 7. Async in preCreate Hooks

```javascript
// PROBLEMATIC - hooks can't reliably await
Hooks.on("preCreateItem", async (doc, data) => {
  const roll = new Roll("1d20");
  await roll.evaluate();  // May fail!
});

// BETTER - use onCreate
Hooks.on("createItem", async (doc, options, userId) => {
  if (userId !== game.user.id) return;
  const roll = new Roll("1d20");
  await roll.evaluate();  // Safe
});
```

## Implementation Checklist

- [ ] Always `await roll.evaluate()` before accessing `roll.total`
- [ ] Use `getRollData()` returning a deep clone
- [ ] Pass `rollMode: game.settings.get("core", "rollMode")` to toMessage
- [ ] Use `ChatMessage.getSpeaker({ actor })` for proper speaker
- [ ] Validate user-provided formulas with `Roll.validate()`
- [ ] Register custom Roll/Die classes in CONFIG.Dice
- [ ] Add flavor text describing the roll
- [ ] Use @ syntax for variable substitution in formulas

## References

- [Roll API](https://foundryvtt.com/api/classes/foundry.dice.Roll.html)
- [Roll Wiki](https://foundryvtt.wiki/en/development/api/roll)
- [Dice Modifiers](https://foundryvtt.com/article/dice-modifiers/)
- [Advanced Dice](https://foundryvtt.com/article/dice-advanced/)
- [Dice in V12+](https://foundryvtt.wiki/en/development/guides/dice-in-v12)

---

**Last Updated:** 2026-01-04
**Status:** Production-Ready
**Maintainer:** ImproperSubset
