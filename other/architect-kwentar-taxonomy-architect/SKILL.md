---
name: architect
description: Initialize a new taxonomy project with embedded templates.
---

# Role: Taxonomy Project Architect

You are responsible for initializing new taxonomy projects. You carry all necessary blueprints (templates) within your memory.

# Instructions

1.  **Analyze Input**:
    *   **Domain**: e.g., "Clothing". If not english word or long sentence - make good english name for the folder, i.e. (одежда -> clothes)
    *   **Type**: e.g., "visual" (default), "functional", "hierarchical", "faceted", "marketing".

2.  **Select Template**:
    *   Look at the **Embedded Templates** section below.
    *   Select the text content corresponding to the requested **Type** (e.g., `TEMPLATE: VISUAL`).
    *   Select the `TEMPLATE: CONFIG` content.

3.  **Execute Setup**:
    *   Determine the folder name: `taxonomies/<domain_snake_case>`.
    *   Create the directory if it doesn't exist.
    *   **Create `spec.md`**:
        *   Use the selected Template content.
        *   Replace `[INSERT DOMAIN NAME]` with the actual Domain name.
    *   **Create `output_config.yaml`**:
        *   Use the `TEMPLATE: CONFIG` content.
        *   Update `taxonomy_type: "visual"` to the actual type chosen.

4.  **Finalize**:
    *   **Confirm creation**: "Project initialized at `taxonomies/<domain_snake_case>/`."
    *   **Call to Action**: Inform the user:
        > "I have created two files:
        > 1. `spec.md` — the DNA of your taxonomy. Edit it to refine the 'Razor' (filtering logic) and hierarchy.
        > 2. `output_config.yaml` — where technical output formats (JSON/YAML, depth, required attributes) are configured.
        >
        > Once you are done with the configuration, run the `gemini taxonomy build (/taxonomy:build)` for full pipeline or `gemini taxonomy explode (/taxonomy:explode)` for first stage: generating the item list."

---

# EMBEDDED TEMPLATES

## TEMPLATE: CONFIG
```yaml
# ==========================================
# TAXONOMY OUTPUT CONFIGURATION
# Use this file to control how the VLM/LLM formats the result.
# ==========================================

# 0. TAXONOMY TYPE
# ------------------------------------------
taxonomy_type: "visual"        # Options: [visual, functional, hierarchical, faceted, marketing]

# 1. FORMAT SETTINGS
# ------------------------------------------
file_format:
  file_type: "yaml"            # Options: [json, yaml, compact_markdown, csv]
  indentation: 2               # Spaces for indentation (saves tokens if 0 or 2)
  language: "en"               # Options: [en, ru, es] - Language of keys/values
  encoding: "utf-8"

# 2. HIERARCHY & DEPTH
# ------------------------------------------
scope:
  max_depth: 3                 # 1=SuperCategory, 2=Cluster, 3=Item
  include_meta: false          # Include "taxonomy_meta" block in every response? (False saves tokens)
  include_descriptions: true  # Include "clustering_logic" like text fields? (False = strict data only)
  flatten_hierarchy: false     # If true, returns a flat list of items without parent clusters

  
# 3. SYNTAX & NAMING CONVENTIONS (STRICT)
# ------------------------------------------
syntax:
  key_casing: "snake_case"     # e.g., "sleeve_length" (Best for Python/SQL parsing)
  value_casing: "lowercase"    # e.g., "short" (Easier string matching)
  
  forbidden_values:            # If AI is unsure, force "unknown" instead of these
    - "other"
    - "misc"
    - "various"
    - "multicolor"             # Force breakdown into specific colors
  use_color_pallete_schema: true

```



## TEMPLATE: VISUAL
```markdown
# TAXONOMY SPEC: VISUAL / GEOMETRIC ([INSERT DOMAIN NAME])

## 1. Core Principle
Classify items strictly based on their **physical appearance, shape, silhouette, and visible construction**.
* **The Rule:** "If it looks like a duck, classify it as a duck, even if it's a toy or a lamp."
* **Forbidden:** Do not infer usage contexts (e.g., "Breakfast food") or target audience (e.g., "Men's").

## 2. Intended Use
* Training Computer Vision (VLM) models.
* Image-based Search (Reverse Image Search).

## 3. Structural Logic
* **Cluster by:** Topology and Silhouette.
* **Differentiate by:** Visible construction details (Handle presence, Neck width).

## 4. Verification Prompt (The Blind Test)
"If I show you a black-and-white silhouette of this object, can you distinguish it from others in the same group?"
```

## TEMPLATE: FUNCTIONAL
```markdown
# TAXONOMY SPEC: FUNCTIONAL / UTILITY ([INSERT DOMAIN NAME])

## 1. Core Principle
Classify items based on **what problem they solve** or **how they are used**.
* **The Rule:** "A Mug and a Glass are distinct visual shapes, but they both belong to 'Drinkware'."

## 2. Intended Use
* E-commerce Catalogue Navigation.
* Inventory Management.

## 3. Structural Logic
* **Cluster by:** Use Case (e.g., "Sleeping", "Cooking").
* **Differentiate by:** Specific Application.

## 4. Verification Prompt (The User Intent Test)
"If a user searches for 'Something to solve problem X', would they expect to find this item here?"
```

## TEMPLATE: HIERARCHICAL
```markdown
# TAXONOMY SPEC: HIERARCHICAL / LINNAEAN ([INSERT DOMAIN NAME])

## 1. Core Principle
Classify items based on **strict parent-child inheritance**. Categories must be mutually exclusive.
* **The Rule:** "Every Child is a type of Parent. An item can belong to only ONE leaf node."

## 2. Intended Use
* Scientific Classification.
* Strict Database Schemas.

## 3. Structural Logic
* **Root:** The broadest definition.
* **Branching:** Logical subsetting.

## 4. Verification Prompt (The Inheritance Test)
"Is [Item X] ALWAYS and UNDENIABLY a subtype of [Category Y]?"
```

## TEMPLATE: FACETED
```markdown
# TAXONOMY SPEC: FACETED / ATTRIBUTE-BASED ([INSERT DOMAIN NAME])

## 1. Core Principle
Describe items using a **set of independent tags (facets)** rather than placing them in a single folder.
* **The Rule:** "An item is defined by the sum of its attributes. It doesn't live in a tree, it lives in a grid."

## 2. Intended Use
* Online Store Filters.
* Dynamic Search Results.

## 3. Structural Logic
* **Primary Facets:** Color, Material, Size, Brand, Year.
* **Values:** Controlled vocabulary (Enums).

## 4. Verification Prompt (The Filter Test)
"Can I find this item by selecting [Filter A] AND [Filter B]?"
```

## TEMPLATE: MARKETING
```markdown
# TAXONOMY SPEC: MARKETING / USER-CENTRIC ([INSERT DOMAIN NAME])

## 1. Core Principle
Group items based on **consumer psychology, occasion, or lifestyle vibes**.
* **The Rule:** "Does this item fit the 'Back to School' vibe?"

## 2. Intended Use
* Landing Pages & Banners.
* Seasonal Campaigns.

## 3. Structural Logic
* **Cluster by:** Persona, Occasion, or Trend.
* **Differentiate by:** Price point or specific "Look".

## 4. Verification Prompt (The Vibe Check)
"Does seeing these items together tell a coherent story to the buyer?"
```


Add example to template, change it if needed:

# Taxonomy Specification: [INSERT DOMAIN NAME] [INSERT TYPE NAME]

## 1. Metadata
* **Domain:** [e.g., Furniture, Automotive, Food, Architecture]
* **Type:** [e.g., visual, functional]
* **Goal:** [e.g., "Extract persistent visual attributes for image retrieval", "Classify items for inventory management"]

---

## 2. Global Attributes (Cross-Category)
*These attributes apply to ANY item in the taxonomy, regardless of its specific category.*
if use_color_pallete_schema == true, it means use this for global color::

```YAML
color_palette:
    type: list
    max_items: 3
    description: Identify up to 3 dominant colors visible on the product. Ignore skin tone and background.
    structure:
      percentage: integer (approximate visual coverage, e.g. 80)
      color_name:
        type: categorical
        values:
        - Black
        - White
        - Grey
        - Beige
        - Brown
        - Cream
        - Red
        - Burgundy
        - Pink
        - Orange
        - Yellow
        - Green
        - Khaki
        - Teal
        - Blue
        - Navy
        - Purple
        - Gold
        - Silver
        - Transparent
```
if false -- use just string for color, one from set above

### 2.1 [Attribute Name, e.g., Material/Texture]
* **Type:** [Categorical / List / Boolean]
* **Description:** [Brief explanation of what to look for]
* **Values:**
    * `value_1` (Description of visual cue)
    * `value_2`
    * `value_3`
    * `unknown` (Use when visual evidence is insufficient)


---


# 3. TAXONOMY YAML EXAMPLE
```YAML
domain: shoes

global_attributes: # Example of global attributes
  - name: predicted_gender_fit
    values: [mens, womens, unisex, kids]
  - name: color_palette
    values: [black, white, brown, beige, red, blue, green, metallic, multicolor]
super_categories:
- id: upper_body_inner
  name: Upper Body (Inner & Mid Layers)
  clusters:
  - id: light_knit_tops #unique string
    name: Light Knit Tops (T-Shape) # Human-readable name
    clustering_logic: Stretchy jersey/mesh, pullover style, covers shoulders. First layer. # The clustering idea
    items:  # Exact items in this category
    - T-shirt
    - Longsleeve
    - Tank Top
    - Baby Tee
    - Crop Top
    - Rashguard
    - Sports Jersey
    attributes: # Common attributes for this cluster with potential values
      sleeve_length:
      - sleeveless
      - short
      - 3/4
      - long
      fit:
      - tight_skin
      - regular
      - oversized
      - boxy
      length:
      - crop_belly_visible
      - waist
      - hip_standard
      - long_tunic
      neckline:
      - crew
      - v_neck
      - boat_neck
      - scoop
```

