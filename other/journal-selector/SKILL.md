---
name: journal-selector
description: "Resolve a target food/nutrition journal to its author-guideline skill and formatting constraints. Use at the start of writing, formatting, or submission-prep for a food-science paper, and whenever the user names a journal they want to publish in or format their manuscript for, to load that journal's rules (word/abstract limits, structure, reference/citation style, figure spec). Triggers: which journal, target journal, publish on a journal, publish in a journal, I want to publish on Food Chemistry, submit to LWT, format for a journal, format my manuscript for a named journal, edit the manuscript based on a journal's style, journal style, journal reference style, journal citation style, submission guidelines, prepare for submission, pick a journal."
metadata:
  version: "0.1.0"
  verified: "2026-07"
  related_skills: [academic-paper, academic-pipeline, food-figure]
---

# Journal Selector — Route a Manuscript to Its Journal Skill

> **Shared procedure, not an installed skill.** `journal-selector` is **not**
> registered in the plugin's skill list — it is machinery the other skills use, so it
> doesn't clutter the user's `/` menu. The `food-*` and `agri-*` skills **load this
> file** (`journal-selector/SKILL.md`) and follow the steps below; users reach it
> automatically by naming a target journal to any of them. It still ships with the
> plugin, exactly like the `journals/*` author-guideline files it resolves to.

Maps a target journal to the correct `journals/<folder>` author-guideline skill
and returns its `## Formatting constraints`. Authoritative mappings:
[food (60)](../journals/_coverage.md) ·
[nutrition (59)](../journals/_coverage_nutrition.md) ·
[multidisciplinary (35)](../journals/_coverage_multidisciplinary.md) ·
[**agriculture Q1+Q2 (230)**](../journals/_coverage_agriculture.md).

## Behavior

1. **Determine the target journal — ask once.** If the author has already named a
   journal (full name or JCR abbreviation), resolve it. If a target journal is
   **already on record for this project/session** (resolved earlier, or set by
   `food-pipeline`), reuse it and skip the question. Otherwise **ask exactly once**:
   > "Which journal are you targeting? (name or JCR abbreviation — e.g. Food
   > Chemistry, LWT, Nature Food). If undecided, say 'generic' and I'll use
   > standard food-science conventions."
2. **Resolve** the journal to its skill folder using the alias table below (or
   `journals/_coverage.md`). Match case-insensitively on full name or abbreviation.
3. **Load** `journals/<folder>/SKILL.md` and return its `## Formatting constraints`
   block plus the checklist. Note any per-journal override row in that skill's
   "Applies to" table (limits can differ within a publisher group).
4. **Hand off:** the calling pipeline applies these constraints to structure,
   word/abstract limits, and reference style, and passes `figure_dpi` /
   `column_widths_*` to the `food-figure` skill.
5. **If 'generic' or unresolved:** use standard food-science conventions
   (IMRaD; abstract ≤250 words; numbered or author–date references; figures
   ≥300 dpi; ~90/190 mm columns) and state the assumption so the author can
   correct it.

## Ask once, then persist
The journal question is asked **at most once per project**. Once resolved (to a
journal *or* to 'generic'/APA 7.0), **record the choice and its constraints** and
reuse them for every downstream stage and subagent — never re-prompt. Re-run this
resolution **only** when the user explicitly asks to target a **different**
journal; then replace the recorded choice and re-flow the affected formatting
(structure, limits, reference style, figure spec).

## Resolution table (journal / abbreviation → skill folder)

- **nature-food** — Nature Food (NAT FOOD); npj Science of Food (NPJ SCI FOOD)
- **food-chemistry** — Food Chemistry (FOOD CHEM)
- **j-dairy-science** — Journal of Dairy Science (J DAIRY SCI)
- **elsevier-food** — Trends in Food Science & Technology; Food Hydrocolloids;
  Food Hydrocolloids for Health; Food Packaging and Shelf Life; Global Food
  Security; Current Opinion in Food Science; Food Chemistry-X; Future Foods;
  Food Research International; Current Research in Food Science; Postharvest
  Biology and Technology; Innovative Food Science & Emerging Technologies; LWT;
  Food Control; Journal of Agriculture and Food Research; Applied Food Research;
  Meat Science; Food Policy; Food Bioscience; Food Structure; Journal of Food
  Engineering; International Journal of Food Microbiology; Food Quality and
  Preference; Food Chemistry: Molecular Sciences; Food Microbiology; Journal of
  Food Composition and Analysis; Microbial Risk Analysis; Journal of Functional
  Foods; Journal of Cereal Science
- **wiley-food** — Comprehensive Reviews in Food Science and Food Safety; Food
  Frontiers; eFood; Legume Science; Food and Energy Security; Molecular
  Nutrition & Food Research; Journal of Food Biochemistry; Food Science &
  Nutrition
- **springer-food** — Food Engineering Reviews; Food and Bioprocess Technology;
  Food Security; Food Production Processing and Nutrition
- **crit-rev-food** — Critical Reviews in Food Science and Nutrition; Food
  Reviews International; International Journal of Food Properties
- **foods-mdpi** — Foods; Antioxidants; Toxins
- **food-function** — Food & Function; Sustainable Food Technology
- **jafc** — Journal of Agricultural and Food Chemistry
- **annu-rev-food** — Annual Review of Food Science and Technology (invited only)
- **food-quality-safety** — Food Quality and Safety (Oxford)
- **british-food-journal** — British Food Journal (structured abstract required)
- **j-future-foods** — Journal of Future Foods; Food Science and Human Wellness
- **qas-crops-foods** — Quality Assurance and Safety of Crops & Foods
- **agri-food-security** — Agriculture & Food Security (BMC declarations block)

### Nutrition journals (Nutrition & Dietetics category)
Grouped by publisher format, same as food. Clinical-nutrition titles add
structured abstracts, trial registration, and reporting guidelines.
- **elsevier-food** — Progress in Lipid Research; Advances in Nutrition; American
  Journal of Clinical Nutrition; Clinical Nutrition; Clinical Nutrition ESPEN;
  Journal of Nutrition; Journal of Nutritional Biochemistry; Journal of the
  Academy of Nutrition and Dietetics; Journal of Nutrition Health & Aging;
  Current Developments in Nutrition; Journal of Renal Nutrition; Nutrition
  Metabolism and Cardiovascular Diseases; Nutrition; Nutrition Research; Appetite;
  NFS Journal
- **wiley-food** — Obesity; International Journal of Eating Disorders; Nutrition
  Bulletin; Nutrition & Dietetics; Journal of Parenteral and Enteral Nutrition;
  Journal of Pediatric Gastroenterology and Nutrition; Journal of Nutrition and
  Metabolism; International Journal of Food Science
- **springer-food** — Current Obesity Reports; Current Nutrition Reports;
  European Journal of Nutrition; International Journal of Obesity; Nutrition &
  Diabetes; European Journal of Clinical Nutrition; Plant Foods for Human Nutrition
- **crit-rev-food** (Taylor & Francis) — Journal of the International Society of
  Sports Nutrition; International Journal of Food Sciences and Nutrition; Journal
  of the American Nutrition Association; Nutritional Neuroscience; Journal of
  Dietary Supplements
- **foods-mdpi** — Nutrients; Dietetics; Obesities
- **annu-rev-food** — Annual Review of Nutrition (invited only)
- **agri-food-security** (BMC) — International Journal of Behavioral Nutrition and
  Physical Activity; Lipids in Health and Disease; Journal of Eating Disorders;
  Nutrition Journal; Nutrition & Metabolism; BMC Nutrition; Genes and Nutrition
- **food-quality-safety** (Oxford) — Nutrition Reviews
- **cambridge-nutrition** — British Journal of Nutrition; Nutrition Research
  Reviews; Proceedings of the Nutrition Society; Public Health Nutrition; Journal
  of Nutritional Science
- **frontiers-nutrition** — Frontiers in Nutrition; Frontiers in Sustainable Food Systems
- **nutrition-other** — Obesity Facts (Karger); Current Opinion in Clinical
  Nutrition and Metabolic Care (Lippincott); Hepatobiliary Surgery and Nutrition
  (AME); Beneficial Microbes (Brill); Food & Nutrition Research (Swedish Nutrition
  Foundation)

### Agriculture journals (Q1 + Q2, seven JCR categories)
The **230 Q1/Q2 journals** of Agronomy, Agriculture Multidisciplinary, Agriculture
Dairy & Animal Science, Soil Science, Agricultural Economics & Policy, Horticulture,
and Agricultural Engineering — deduplicated across categories at their best quartile.
They **reuse the publisher-tier folders above** (an Elsevier agronomy journal follows
the same Guide for Authors as an Elsevier food journal), so resolve them from the
full table: [`journals/_coverage_agriculture.md`](../journals/_coverage_agriculture.md).
Common routings:
- **elsevier-food** — Soil Biology & Biochemistry; Computers and Electronics in Agriculture; Industrial Crops and Products; Agricultural Systems; Agricultural Water Management; Field Crops Research; Soil & Tillage Research; European Journal of Agronomy; Scientia Horticulturae; Animal Feed Science and Technology; Livestock Science; Geoderma; Agriculture Ecosystems & Environment; Bioresource Technology; Biosystems Engineering; Biomass & Bioenergy; Smart Agricultural Technology.
- **wiley-food** — Agronomy Journal; Crop Science; Soil Science Society of America Journal; Journal of Animal Breeding and Genetics; Journal of Agronomy and Crop Science; Journal of the Science of Food and Agriculture; Plant Breeding; Grass and Forage Science; European Journal of Soil Science; Land Degradation & Development; Vadose Zone Journal; Agricultural Economics.
- **springer-food** — Biochar; Molecular Horticulture; Precision Agriculture; Agronomy for Sustainable Development; Biology and Fertility of Soils; Plant and Soil; Irrigation Science; Journal of Soils and Sediments; Tropical Animal Health and Production; Food Security.
- **crit-rev-food** (Taylor & Francis) — Critical Reviews in Plant Sciences; Journal of Sustainable Agriculture; Archives of Animal Nutrition; Soil Science and Plant Nutrition.
- **foods-mdpi** — Agronomy; Agriculture; Horticulturae; Land; Animals; Plants; AgriEngineering.
- **food-quality-safety** (Oxford) — Horticulture Research; Journal of Animal Science; Translational Animal Science; Journal of Economic Entomology.
- **cambridge-nutrition** — Journal of Agricultural Science; Animal; Experimental Agriculture; Renewable Agriculture and Food Systems.
- **j-future-foods** (KeAi) — Artificial Intelligence in Agriculture; The Crop Journal; Rice Science; Journal of Integrative Agriculture.
- **annu-rev-food** — Annual Review of Animal Biosciences; Annual Review of Resource Economics.
- **british-food-journal** (Emerald) — China Agricultural Economic Review; Agricultural Finance Review.
- **agri-food-security** (BMC) — Agriculture & Food Security; CABI Agriculture and Bioscience.
- **frontiers-nutrition** — Frontiers in Plant Science; Frontiers in Veterinary Science; Frontiers in Sustainable Food Systems.
- **jafc** — Journal of Agricultural and Food Chemistry. · **j-dairy-science** — Journal of Dairy Science.
- **agri-other** — society/regional titles with no shared format: SOIL (Copernicus); Crop and Pasture Science (CSIRO); Animal Bioscience; Journal of Animal Science and Technology; Plant Soil and Environment; Czech Journal of Animal Science; Scientia Agricola; American Journal of Enology and Viticulture; Australian Journal of Grape and Wine Research; Seed Science and Technology; and similar.

### Multidisciplinary & cross-discipline journals
High-priority venues food/nutrition researchers publish in, grouped by publisher
format (the Nature/Science/Cell families and PNAS are top-priority per the
ranking rule).
- **nature-portfolio** — Nature; Nature Communications; Nature Microbiology;
  Nature Metabolism; Nature Sustainability; Nature Biotechnology; Nature Medicine;
  Nature Reviews titles. (**Nature Food** and **npj Science of Food** → `nature-food`.)
- **science-aaas** — Science; Science Advances; Science Translational Medicine;
  Science Immunology; Science Signaling; Science Robotics.
- **cell-press** — Cell; Cell Metabolism; Cell Host & Microbe; Molecular Cell;
  Immunity; Current Biology; Cell Reports Medicine; One Earth; Joule; Matter; Chem.
- **pnas** — Proceedings of the National Academy of Sciences (PNAS).
- **multidisciplinary** — eLife; PLOS Biology; PLOS Medicine; National Science
  Review; The Innovation; Environmental Science & Technology; Gut; Gastroenterology;
  Diabetes Care; The ISME Journal.

## Output contract
Return: `{journal, publisher, skill_folder, reference_style, abstract_words,
figure_spec, notes}` drawn from the resolved skill's constraints block, so the
paper pipeline and `food-figure` can consume it directly.
