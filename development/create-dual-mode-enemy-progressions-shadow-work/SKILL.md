---
name: Create Dual-Mode Enemy
description: Creates a new GameMaker enemy that can switch between melee and ranged attacks based on distance, formation role, cooldowns, and line of sight. Use when the user asks to create an enemy with both melee and ranged capabilities, context-based attack switching, or tactical combat behavior.
---

# Create Dual-Mode Enemy Skill

This skill creates GameMaker enemies that intelligently switch between melee and ranged attacks based on tactical context.

## Core Requirements

### 1. Object Setup
- Create object inheriting from `obj_enemy_parent`
- Call `event_inherited()` in Create event before setting properties

### 2. Enable Dual-Mode System
```gml
// In enemy Create event (after event_inherited())
enable_dual_mode = true;
```

### 3. Configure Attack Preference
```gml
preferred_attack_mode = "ranged";  // Options: "none", "melee", or "ranged"
```

**Attack Preferences:**
- `"melee"`: Prefers close combat, uses ranged as backup
- `"ranged"`: Maintains distance, retreats when player gets close
- `"none"`: No preference, purely distance-based decisions

### 4. Set Both Attack Stat Sets

**Melee Stats:**
```gml
attack_damage = 5;           // Base melee damage
attack_speed = 1.0;          // Animation speed multiplier
attack_range = 32;           // Pixels for melee range
damage_type = DamageType.physical;
```

**Ranged Stats:**
```gml
ranged_damage = 3;           // Base ranged damage (often lower than melee)
ranged_attack_speed = 0.8;   // Animation speed multiplier
ranged_attack_range = 150;   // Pixels for ranged range
ranged_damage_type = DamageType.physical;
```

### 5. Configure Tactical Behavior

**Range Thresholds:**
```gml
melee_range_threshold = attack_range * 0.5;  // Distance below which melee is preferred
ideal_range = attack_range * 0.75;           // Preferred standoff distance for ranged
```

**Retreat Behavior (for ranged-preferred enemies):**
```gml
retreat_when_close = true;   // Retreat if player breaches ideal_range
```

### 6. Sprite Requirements

**47-Frame Layout** (dual-mode enemies need ranged animations):
- Frames 0-10: Idle (down, left, right, up)
- Frames 11-22: Walking (down, left, right, up)
- Frames 23-31: Melee attacking (down, left, right, up)
- **Frames 35-46: Ranged attacking (down, left, right, up)** ← Required for dual-mode
- Frames 32-34: Death animation

**Note:** Melee-only enemies use 35-frame layout (no ranged frames).

### 7. Sound Configuration

Set separate sounds for melee vs ranged attacks:
```gml
custom_attack_sfx = "snd_sword_hit";    // Melee attack sound
custom_ranged_sfx = "snd_arrow_fire";   // Ranged attack sound
```

**Variant Support:** Use numbered variants (e.g., `snd_sword_hit_1`, `snd_sword_hit_2`) for automatic randomization.

### 8. Apply Traits via Tags

```gml
array_push(tags, "fireborne");  // Example: fire immunity, fire damage
apply_tag_traits();             // Call after adding all tags
```

**Common Tags:** fireborne, arboreal, aquatic, glacial, swampridden, sandcrawler

See `/docs/TRAIT_SYSTEM.md` for tag definitions and trait bundles.

## Attack Mode Decision Logic

The enemy uses this priority order to decide melee vs ranged:

1. **Formation Role Override** (if in enemy party)
   - "rear" or "support" → Force ranged
   - "front" or "vanguard" → Force melee

2. **Distance Thresholds**
   - `dist < melee_range_threshold` → Prefer melee
   - `dist > ideal_range` → Prefer ranged

3. **Cooldown Availability**
   - If chosen mode is on cooldown, try other mode

4. **Line of Sight** (for ranged)
   - No LOS → Fall back to melee

## Complete Example: Orc Raider

```gml
// obj_orc_raider Create event
event_inherited();

// Dual-mode configuration
enable_dual_mode = true;
preferred_attack_mode = "melee";
melee_range_threshold = 48;
ideal_range = 60;
retreat_when_close = false;  // Aggressive positioning

// Base stats
hp_total = 20;
move_speed = 1.0;
detection_range = 200;

// Melee stats (primary)
attack_damage = 5;
attack_speed = 1.0;
attack_range = 32;
damage_type = DamageType.physical;

// Ranged stats (backup)
ranged_damage = 3;
ranged_attack_speed = 0.8;
ranged_attack_range = 150;
ranged_damage_type = DamageType.physical;

// Sounds
custom_attack_sfx = "snd_sword_hit";
custom_ranged_sfx = "snd_arrow_fire";

// Traits
array_push(tags, "fireborne");
apply_tag_traits();

// Flanking behavior
flank_chance = 0.3;
flank_trigger_distance = 120;

// Sprite (must have 47-frame layout with ranged animations)
sprite_index = spr_orc_raider;
```

## Key Files Reference

- `/docs/ENEMY_AI_ARCHITECTURE.md` - Complete dual-mode documentation
- `/objects/obj_enemy_parent/Create_0.gml` - Parent initialization
- `/scripts/scr_enemy_state_targeting/scr_enemy_state_targeting.gml` - Attack mode logic
- `/scripts/scr_enemy_state_ranged_attacking/scr_enemy_state_ranged_attacking.gml` - Ranged state
- `/docs/TRAIT_SYSTEM.md` - Trait and tag system

## Important Notes

- Dual-mode enemies have **independent cooldowns** for melee (Alarm[0]) and ranged (Alarm[1])
- Ranged attacks allow **movement while shooting** (unlike melee which commits to position)
- Retreat behavior only triggers for `preferred_attack_mode = "ranged"` enemies
- Formation role (from enemy party system) **overrides** distance-based decisions
- Always test line of sight blocking with walls/obstacles in your test rooms

## Testing Checklist

After creating a dual-mode enemy:
- [ ] Test melee attack at close range
- [ ] Test ranged attack at medium range
- [ ] Verify switching between modes based on distance
- [ ] Test retreat behavior (if ranged-preferred)
- [ ] Verify both cooldowns work independently
- [ ] Test line of sight blocking (ranged should fail, fallback to melee)
- [ ] Verify sprite has all 47 frames with ranged animations
- [ ] Test sounds play correctly for both attack types
- [ ] Verify traits apply correctly from tags
