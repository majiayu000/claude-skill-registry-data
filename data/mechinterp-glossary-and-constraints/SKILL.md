---
name: mechinterp-glossary-and-constraints
description: Reference skill for Splatoon ability families, AP rungs, token constraints, and domain rules for mechinterp experiments
---

# MechInterp Glossary and Constraints

A read-only reference skill providing domain knowledge for mechanistic interpretability research on SplatNLP's SAE features.

## Purpose

This skill provides the domain-specific knowledge needed to design valid experiments:
- Ability token families and their AP rungs
- Main-only vs stackable abilities
- Constraints that experiments must respect
- Common pitfalls to avoid

## When to Use

Invoke this skill when you need to:
- Look up ability family codes (SCU, ISS, SSU, etc.)
- Understand AP rung meanings
- Check constraint definitions
- Verify valid token combinations

## Quick Reference

### Ability Family Short Codes

| Code | Full Name | Stackable |
|------|-----------|-----------|
| SCU | special_charge_up | Yes |
| SPU | special_power_up | Yes |
| SS | special_saver | Yes |
| ISS | ink_saver_sub | Yes |
| ISM | ink_saver_main | Yes |
| SSU | swim_speed_up | Yes |
| RSU | run_speed_up | Yes |
| IRU | ink_recovery_up | Yes |
| QR | quick_respawn | Yes |
| QSJ | quick_super_jump | Yes |
| IA | intensify_action | Yes |
| SubPU | sub_power_up | Yes |
| SRU | sub_resistance_up | Yes |
| INKR | ink_resistance_up | Yes |

### Main-Only Abilities (Fixed 10 AP) — BINARY

| Ability | Gear Slot |
|---------|-----------|
| comeback | head |
| last_ditch_effort | head |
| opening_gambit | head |
| tenacity | head |
| ability_doubler | clothes |
| haunt | clothes |
| ninja_squid | clothes |
| respawn_punisher | clothes |
| thermal_ink | clothes |
| drop_roller | shoes |
| object_shredder | shoes |
| stealth_jump | shoes |

**⚠️ IMPORTANT FOR EXPERIMENTS:** These abilities are **binary** (present or absent, no scaling). In 1D sweeps, they will always show **delta = 0** because there's no AP variation to test. This does NOT mean they don't affect the feature.

**⚠️ TOKEN FORMAT:** Binary abilities appear as just the ability name (e.g., `comeback`, `stealth_jump`) WITHOUT an AP suffix. They do NOT appear as `comeback_10` or `stealth_jump_10`. The `parse_token()` function returns `(name, None)` for these tokens, not `(name, 10)`.

**To evaluate binary abilities:**
1. Check their PageRank score (correlation with high activation)
2. Check presence rate enrichment in high-activation examples (>1.5x = characteristic)
3. Check mean activation WITH vs WITHOUT the token (delta > 0.03 = meaningful)
4. Run **manual 2D analysis** at each scaling ability level to see conditional effects
5. Test combinations of binary abilities together (they may have stronger effects as a group)

### Standard AP Rungs

| AP | Typical Source |
|----|----------------|
| 3 | 1 sub slot |
| 6 | 2 sub slots |
| 12 | 4 subs OR 1 main |
| 21 | 1 main + 3-4 subs |
| 29 | 1 main + 6 subs |
| 35 | 2 mains + 5 subs |
| 41 | 2 mains + 7 subs |
| 45 | 3 mains + 5 subs |
| 48 | 3 mains + 6 subs |
| 51 | 3 mains + 7 subs |
| 54 | 3 mains + 8 subs |
| 57 | 3 mains + 9 subs (MAX) |

## Constraints

### one_rung_per_family (HARD)

**Only one AP rung per ability family can appear in a build.**

Invalid: `[swim_speed_up_21, swim_speed_up_12]` - same family, different rungs
Valid: `[swim_speed_up_21, special_charge_up_12]` - different families

Rationale: AP rungs represent cumulative investment. You can't have both 21 AP and 12 AP in the same ability simultaneously.

### no_weapon_gating_if_relu_floor (SOFT)

**Skip weapon-specific experiments when base activation is near zero.**

When base activation is at the ReLU floor (~0), activation changes become quantized and unreliable. Check `diagnostics.relu_floor_detected` before trusting weapon gating results.

### valid_gear_combinations (HARD)

**Main-only abilities can only appear on their designated gear slot.**

Invalid: ninja_squid on headgear (it's clothes-only)
Valid: ninja_squid on clothes

### max_ap_budget (SOFT)

**Total AP should not exceed 57 (3 mains + 9 subs).**

Builds exceeding this are physically impossible in-game.

## Common Pitfalls

1. **Multi-rung conflicts**: When sweeping family levels, ensure base contexts don't already contain the family being swept.

2. **ReLU floor quantization**: Low base activations cause delta measurements to be unreliable. Check for `relu_floor_detected: true` in diagnostics.

3. **OOD token combinations**: Very rare ability combinations may produce unreliable activations. Prefer combinations that appear in training data.

4. **Weapon bias**: Some features respond to weapon kit properties (sub/special type) rather than abilities. Control for this in experiments.

## Programmatic Access

```python
from splatnlp.mechinterp.schemas.glossary import (
    TOKEN_FAMILIES,
    DOMAIN_CONSTRAINTS,
    STANDARD_RUNGS,
    get_family_for_token,
    parse_token,
    validate_build_tokens,
    get_glossary_text,
)

# Get family for a token
family = get_family_for_token("swim_speed_up_21")
print(family.short_code)  # "SSU"

# Parse token into family and AP
name, ap = parse_token("special_charge_up_57")
# ("special_charge_up", 57)

# Validate a build
violations = validate_build_tokens(["ssu_21", "ssu_12"])
# ["Constraint 'one_rung_per_family' violated: ..."]

# Get full glossary text
text = get_glossary_text()
```

## See Also

- **mechinterp-state**: Manage research hypotheses and evidence
- **mechinterp-next-step-planner**: Propose experiments respecting constraints
- **mechinterp-runner**: Execute experiments with constraint enforcement
