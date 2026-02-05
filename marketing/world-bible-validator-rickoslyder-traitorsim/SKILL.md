---
name: world-bible-validator
description: Validate TraitorSim content for World Bible lore consistency, detect forbidden real-world brand leakage, and ensure in-universe brand usage. Use when checking personas, narratives, game content, or when asked about lore validation, brand detection, in-universe consistency, or World Bible compliance.
---

# World Bible Validator

Ensure all TraitorSim content adheres to the World Bible lore system by detecting forbidden real-world brands and validating in-universe brand usage. The World Bible defines the fictional universe where "The Traitors" game show exists, with its own brands, locations, and cultural context.

## Quick Start

```bash
# Validate personas for brand leakage
python scripts/validate_personas.py --library data/personas/library/test_batch_001_personas.json

# Check specific text for brand violations
python -c "
from src.traitorsim.utils.world_flavor import detect_forbidden_brands
text = 'I grabbed a Starbucks coffee and checked Facebook'
brands = detect_forbidden_brands(text)
print(f'Forbidden brands detected: {brands}')
"
```

## World Bible Lore System

The World Bible establishes an alternate UK where "The Traitors" is a beloved reality TV franchise produced by CastleVision at Ardross Castle in the Scottish Highlands.

### Key Lore Elements

**Setting:**
- **Ardross Castle**: The iconic filming location in the Scottish Highlands
- **CastleVision**: The production company (NOT the BBC, ITV, or Channel 4)
- **Three Legendary Seasons**:
  - Season 1: "The Aberdeen Blindside"
  - Season 2: "The Edinburgh Strategy"
  - Season 3: "The Inverness Gambit"

**Cultural Context:**
- UK-based franchise with Scottish identity
- Strong regional pride around Highland location
- "The Traitors" is mainstream entertainment (not niche)
- Contestants are recognizable from social media presence

**Demographics:**
- UK residents (England, Scotland, Wales, Northern Ireland)
- Ages 21-65 (adult contestants only)
- Diverse socioeconomic backgrounds
- Mix of occupations and regions

## In-Universe Brands

Replace ALL real-world brands with in-universe equivalents:

### Food & Beverage

**Water:**
- ❌ Evian, Fiji, Highland Spring (real brand)
- ✅ **Highland Spring Co.** (in-universe)

**Coffee:**
- ❌ Starbucks, Costa, Pret A Manger, Caffè Nero
- ✅ **Cairngorm Coffee Roasters**

**Snacks:**
- ❌ Walker's Crisps, Kettle Chips, Tyrrell's
- ✅ **Heather & Thistle Crisps**

**Meals/Ready-made Food:**
- ❌ M&S Food, Tesco Finest, Waitrose
- ✅ **Loch Provisions**

**Alcohol:**
- ❌ Greene King, Fuller's, specific whisky brands
- ✅ **Royal Oak Spirits**

**Tea:**
- ❌ Yorkshire Tea, PG Tips, Tetley
- ✅ **Cairngorm Coffee Roasters** (also does tea)

### Retail & Services

**Clothing:**
- ❌ Next, H&M, Zara, Primark
- ✅ **Baronial Casual Wear**

**Outdoor Gear:**
- ❌ Blacks, Cotswold Outdoor, Go Outdoors
- ✅ **Tartan & Stone Outfitters**

**Toiletries:**
- ❌ Boots, Superdrug, specific brands
- ✅ **Inverness Essentials**

**Supermarkets:**
- ❌ Tesco, Sainsbury's, Asda, Morrisons
- ✅ Generic "the supermarket" OR **Highland Provisions** (for upscale)

### Technology & Media

**Social Media:**
- ❌ Facebook, Instagram, Twitter/X, TikTok, LinkedIn
- ✅ **ScotNet** (unified social platform)

**Internet/Communications:**
- ❌ BT, Virgin Media, Sky Broadband
- ✅ **ScotNet** (ISP and social platform)

**Streaming Services:**
- ❌ Netflix, BBC iPlayer, ITV Hub, Channel 4
- ✅ **CastleVision+** (production company's streaming service)

**News Sources:**
- ❌ The Guardian, The Times, BBC News
- ✅ **The Highland Herald** (national newspaper)

**Phone Brands:**
- ❌ iPhone, Samsung Galaxy, Google Pixel
- ✅ Generic "smartphone" OR "mobile"

### Transportation

**Trains:**
- ❌ ScotRail, LNER, Avanti West Coast
- ✅ Generic "the train" OR **Highland Rail**

**Airlines:**
- ❌ easyJet, Ryanair, British Airways
- ✅ Generic "budget airline" OR **Caledonian Airways**

**Ride-sharing:**
- ❌ Uber, Bolt, Lyft
- ✅ Generic "taxi app" OR **RideScot**

### Finance

**Banks:**
- ❌ Barclays, HSBC, NatWest, Lloyds
- ✅ Generic "the bank" OR **Royal Bank of the Highlands**

**Payment Apps:**
- ❌ PayPal, Venmo, Revolut, Monzo
- ✅ Generic "payment app" OR **ScotPay**

## Forbidden Brand List

**Complete list of real-world brands to detect:**

```python
FORBIDDEN_BRANDS = [
    # Food & Drink
    "starbucks", "costa", "pret", "caffè nero", "nero",
    "evian", "fiji water", "highland spring",  # Real brand!
    "walker's", "walkers", "kettle chips", "tyrrell's",
    "m&s", "marks & spencer", "tesco", "sainsbury's", "asda", "morrisons", "waitrose",
    "yorkshire tea", "pg tips", "tetley",
    "greene king", "fuller's", "wetherspoon", "spoons",

    # Social Media & Tech
    "facebook", "instagram", "twitter", "tiktok", "linkedin", "snapchat",
    "whatsapp", "messenger", "telegram",
    "google", "youtube", "amazon", "apple", "microsoft",
    "iphone", "samsung", "galaxy", "pixel",

    # Streaming & Media
    "netflix", "bbc iplayer", "itv hub", "channel 4", "all4", "my5",
    "spotify", "apple music", "amazon music",
    "bbc", "itv", "channel 4", "sky",

    # Retail
    "next", "h&m", "zara", "primark", "uniqlo",
    "boots", "superdrug", "holland & barrett",
    "blacks", "cotswold outdoor", "go outdoors",

    # Transport
    "scotrail", "lner", "avanti", "virgin trains",
    "easyjet", "ryanair", "british airways", "ba",
    "uber", "bolt", "lyft",

    # Finance
    "barclays", "hsbc", "natwest", "lloyds", "halifax", "nationwide",
    "paypal", "venmo", "revolut", "monzo", "starling",

    # Other
    "nhs",  # Keep generic "the NHS" but not specific trusts
    "oxbridge", "cambridge", "oxford"  # Use "Russell Group university"
]
```

## Brand Detection Algorithm

The validator uses **word boundary regex** to avoid false positives:

```python
import re

def detect_forbidden_brands(text: str) -> List[str]:
    text_lower = text.lower()
    detected = []

    for brand in FORBIDDEN_BRANDS:
        # Word boundaries prevent matching substrings
        # e.g., "pret" won't match "pretend"
        pattern = r'\b' + re.escape(brand) + r'\b'
        if re.search(pattern, text_lower):
            detected.append(brand)

    return detected
```

**Why word boundaries matter:**

```python
# Without word boundaries:
text = "I pretended to like it"
detect("pret")  # ❌ FALSE POSITIVE: matches "pret" in "pretended"

# With word boundaries:
text = "I pretended to like it"
detect(r'\bpret\b')  # ✅ CORRECT: no match

text = "I went to Pret for coffee"
detect(r'\bpret\b')  # ✅ CORRECT: matches "Pret"
```

## Instructions

### When Validating Personas

1. **Load persona library**:
   ```python
   import json
   with open('data/personas/library/test_batch_001_personas.json') as f:
       personas = json.load(f)
   ```

2. **Check each persona's text fields**:
   ```python
   from src.traitorsim.utils.world_flavor import detect_forbidden_brands

   for persona in personas:
       # Check backstory
       backstory_brands = detect_forbidden_brands(persona['backstory'])

       # Check relationships
       relationships_text = ' '.join(persona.get('key_relationships', []))
       relationship_brands = detect_forbidden_brands(relationships_text)

       # Check hobbies
       hobbies_text = ' '.join(persona.get('hobbies', []))
       hobby_brands = detect_forbidden_brands(hobbies_text)

       # Check all other string fields
       for key, value in persona.items():
           if isinstance(value, str):
               field_brands = detect_forbidden_brands(value)
               if field_brands:
                   print(f"{persona['name']} - {key}: {field_brands}")
   ```

3. **Report violations**:
   ```python
   if backstory_brands:
       print(f"❌ {persona['name']}: Forbidden brands in backstory: {backstory_brands}")
   else:
       print(f"✅ {persona['name']}: No brand violations")
   ```

4. **Fail fast if violations found**:
   - Do NOT proceed with personas that have brand leakage
   - Regenerate personas with stronger World Bible constraints in synthesis prompt

### When Validating Game Narration

GameMaster-generated content should also comply:

1. **Check mission descriptions**:
   ```python
   mission_description = gamemaster.describe_mission("Laser Heist")
   brands = detect_forbidden_brands(mission_description)
   assert len(brands) == 0, f"Mission narration has brand leakage: {brands}"
   ```

2. **Check event narration**:
   ```python
   breakfast_scene = gamemaster.narrate_breakfast()
   brands = detect_forbidden_brands(breakfast_scene)
   ```

3. **Check dialogue**:
   ```python
   agent_statement = player_agent.make_accusation(target_id="player_03")
   brands = detect_forbidden_brands(agent_statement)
   ```

### When Adding New Forbidden Brands

If you discover real-world brands in generated content:

1. **Add to forbidden list**:
   ```python
   # In src/traitorsim/utils/world_flavor.py
   FORBIDDEN_BRANDS = [
       # ... existing brands ...
       "new_brand_to_block",
   ]
   ```

2. **Create in-universe alternative** if needed:
   ```python
   IN_UNIVERSE_BRANDS = {
       # ... existing brands ...
       "new_category": "New In-Universe Brand Name",
   }
   ```

3. **Update synthesis prompts** to specify the new alternative:
   ```python
   # In scripts/synthesize_backstories.py
   world_bible_constraints = """
   ...
   - Never mention [New Forbidden Brand]. Use [New In-Universe Brand] instead.
   """
   ```

4. **Regenerate affected personas**

### When Creating New In-Universe Brands

Follow World Bible naming conventions:

**Naming patterns:**
- **Scottish geography**: "Cairngorm", "Highland", "Loch", "Tartan"
- **Royal/nobility**: "Royal", "Baronial", "Castle"
- **Scottish flora**: "Heather", "Thistle", "Oak"
- **Scottish heritage**: "Scot", "Caledonian", "Highland"

**Good examples:**
- Highland Spring Co. (water)
- Cairngorm Coffee Roasters (coffee + Scottish mountain)
- Heather & Thistle Crisps (Scottish plants)
- Royal Oak Spirits (royal + Scottish tree)
- ScotNet (Scottish + network)

**Bad examples:**
- ❌ "London Coffee" (not Scottish)
- ❌ "Generic Brand Water" (not evocative)
- ❌ "UK Social Network" (too generic)

## Common Validation Issues

### Issue 1: University Names

**Problem**: "I studied at Oxford" leaks real-world institutions

**Solution**: Use generic alternatives
- ❌ "Oxford", "Cambridge"
- ✅ "a Russell Group university", "a top university", "university in England"

### Issue 2: NHS Specific Trusts

**Problem**: "I work at St Thomas's Hospital" is too specific

**Solution**: Use generic NHS references
- ❌ "St Thomas's", "Guy's Hospital", "Royal Infirmary"
- ✅ "an NHS hospital", "a hospital in London", "my hospital"

### Issue 3: Specific Neighborhoods

**Problem**: Some London neighborhoods are iconic brands themselves

**Solution**: Use generic area descriptions
- ✅ ALLOWED: "Clapham", "Brixton", "Shoreditch" (generic areas)
- ❌ FORBIDDEN: "Knightsbridge Harvey Nichols" (specific brand association)

### Issue 4: Cultural References

**Problem**: Pop culture references leak real-world media

**Solution**: Use generic or in-universe alternatives
- ❌ "Watched Stranger Things on Netflix"
- ✅ "Watched a sci-fi series on CastleVision+"
- ❌ "Listened to Spotify playlist"
- ✅ "Listened to my music library"

### Issue 5: Sports Teams

**Problem**: Football clubs are brands

**Solution**: Use generic references or change sport
- ❌ "Arsenal supporter", "Man United fan"
- ✅ "football supporter", "local team fan", "Premier League follower"

### Issue 6: Political Parties

**Problem**: UK political parties are allowed but be careful

**Solution**: Generic ideology is safer
- ✅ ALLOWED: "Labour", "Conservative", "Liberal Democrat", "SNP"
- ✅ SAFER: "left-wing", "centrist", "progressive", "libertarian"

## Validation Script Usage

The `scripts/validate_personas.py` script performs comprehensive validation:

```bash
# Full validation with brand detection
python scripts/validate_personas.py --library data/personas/library/test_batch_001_personas.json

# Expected output:
# ✅ All personas passed validation
# ✅ 0 forbidden brands detected
# ✅ All OCEAN traits in valid ranges
# ✅ All backstories meet length requirements
```

**Validation checks performed:**

1. **Required fields present**:
   - name, backstory, demographics, personality, stats, archetype

2. **OCEAN traits in range**:
   - All traits 0.0-1.0
   - Traits within archetype ranges

3. **Stats in range**:
   - intellect, dexterity, social_influence 0.0-1.0

4. **Backstory length**:
   - Minimum 200 characters
   - Maximum 1600 characters (200-300 words)

5. **Brand leakage detection**:
   - Scans all text fields with word boundary regex
   - Reports any forbidden brands found

6. **Demographic plausibility**:
   - Age in valid range
   - Occupation appropriate for age
   - Location is UK-based

## Synthesis Prompt Templates

When synthesizing content, use these World Bible constraint templates:

### For Personas (Claude synthesis)

```python
world_bible_constraints = """
## World Bible Constraints (CRITICAL - MUST FOLLOW)

You are creating personas for an alternate UK where:

**In-Universe Brands (USE THESE):**
- Highland Spring Co. (water, NOT Evian/Fiji)
- Cairngorm Coffee Roasters (coffee, NOT Starbucks/Costa)
- Heather & Thistle Crisps (snacks, NOT Walker's)
- ScotNet (social media, NOT Facebook/Instagram)
- CastleVision (TV production, NOT BBC/ITV)
- The Highland Herald (news, NOT The Guardian/Times)

**Forbidden Brands (NEVER MENTION):**
- Starbucks, Costa, Pret, Nero
- Facebook, Instagram, Twitter, TikTok
- Netflix, BBC iPlayer, ITV Hub
- Tesco, Sainsbury's, M&S
- iPhone, Samsung (use "smartphone")

**Generic Alternatives (WHEN NO IN-UNIVERSE BRAND):**
- "the supermarket" (not Tesco)
- "my bank" (not Barclays)
- "a budget airline" (not easyJet)
- "university" (not Oxford)
- "streaming service" (if must mention)

**Setting:**
- "The Traitors" is filmed at Ardross Castle, Scottish Highlands
- Produced by CastleVision (NOT BBC)
- Contestants may reference ScotNet following, prior seasons

**Do NOT:**
- Mention specific real-world brands
- Reference American culture (no Walmart, no "college")
- Use non-UK locations (no "vacation", use "holiday")
"""
```

### For GameMaster Narration

```python
narrative_constraints = """
## Narrative Constraints

**Setting:** Ardross Castle, Scottish Highlands

**Production:** CastleVision production team

**Meals:** Provided by Loch Provisions catering

**Drinks:** Highland Spring Co. water, Cairngorm Coffee

**No Modern Tech:** No smartphones visible during filming, no social media during game

**Keep Generic:** Avoid specific brands in narration unless in-universe
"""
```

## Testing Brand Detection

Test the detection algorithm with edge cases:

```python
from src.traitorsim.utils.world_flavor import detect_forbidden_brands

# Test 1: Word boundary (should NOT match)
text = "I pretended to understand"
brands = detect_forbidden_brands(text)
assert "pret" not in brands, "False positive: 'pret' in 'pretended'"

# Test 2: Exact match (should match)
text = "I went to Pret for lunch"
brands = detect_forbidden_brands(text)
assert "pret" in brands, "Failed to detect 'Pret'"

# Test 3: Case insensitive (should match)
text = "I use FACEBOOK daily"
brands = detect_forbidden_brands(text)
assert "facebook" in brands, "Failed case insensitive detection"

# Test 4: Multiple brands (should match all)
text = "I grabbed Starbucks, checked Instagram, then watched Netflix"
brands = detect_forbidden_brands(text)
assert len(brands) == 3, f"Expected 3 brands, got {len(brands)}"

print("✅ All brand detection tests passed")
```

## Advanced Usage

### Automated Remediation

Automatically suggest in-universe replacements:

```python
def suggest_replacement(detected_brand: str) -> str:
    replacements = {
        "starbucks": "Cairngorm Coffee Roasters",
        "costa": "Cairngorm Coffee Roasters",
        "facebook": "ScotNet",
        "instagram": "ScotNet",
        "netflix": "CastleVision+",
        "tesco": "the supermarket",
        # ... add more mappings ...
    }
    return replacements.get(detected_brand.lower(), "[IN-UNIVERSE ALTERNATIVE NEEDED]")

# Usage
text = "I posted on Instagram about my Starbucks order"
brands = detect_forbidden_brands(text)
for brand in brands:
    replacement = suggest_replacement(brand)
    print(f"Replace '{brand}' with '{replacement}'")

# Output:
# Replace 'instagram' with 'ScotNet'
# Replace 'starbucks' with 'Cairngorm Coffee Roasters'
```

### Batch Validation Reports

Generate validation reports for large persona libraries:

```python
import json
from src.traitorsim.utils.world_flavor import detect_forbidden_brands

def generate_validation_report(persona_library_path: str):
    with open(persona_library_path) as f:
        personas = json.load(f)

    report = {
        "total_personas": len(personas),
        "violations": [],
        "clean_personas": 0
    }

    for persona in personas:
        persona_violations = []

        # Check all text fields
        for field in ["backstory", "formative_challenge", "political_beliefs", "strategic_approach"]:
            if field in persona:
                brands = detect_forbidden_brands(persona[field])
                if brands:
                    persona_violations.append({
                        "field": field,
                        "brands": brands
                    })

        if persona_violations:
            report["violations"].append({
                "name": persona["name"],
                "violations": persona_violations
            })
        else:
            report["clean_personas"] += 1

    # Print report
    print(f"Validation Report: {persona_library_path}")
    print(f"Total personas: {report['total_personas']}")
    print(f"Clean personas: {report['clean_personas']}")
    print(f"Personas with violations: {len(report['violations'])}")

    if report['violations']:
        print("\n❌ Violations Found:")
        for violation in report['violations']:
            print(f"  {violation['name']}:")
            for v in violation['violations']:
                print(f"    {v['field']}: {v['brands']}")
    else:
        print("\n✅ No violations detected - library is World Bible compliant!")

    return report
```

## When to Use This Skill

Use this skill when:
- Validating generated personas for brand leakage
- Checking GameMaster narration for lore consistency
- Adding new forbidden brands to detection list
- Creating new in-universe brands
- Troubleshooting validation failures
- Ensuring all content is World Bible compliant

## When NOT to Use This Skill

Don't use this skill for:
- Generating personas (use persona-pipeline skill)
- Designing archetypes (use archetype-designer skill)
- Managing API quotas (use quota-manager skill)
- Real-time content filtering during gameplay (validation is offline, pre-deployment)
