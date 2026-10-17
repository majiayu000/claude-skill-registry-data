---
genre_slug: materials
status: draft
kind: technique
markers: SetMaterial, material_instance, MaterialInstance, UI_Shape, M_UI
file_markers: M_, MI_, MF_, MPC_, Materials
last_updated: 2026-10-01
pattern_counts: proven=0 confirmed=0 hypothesis=0 reference=0 contested=0
---

# Technique Skill: Materials

Same engine and growth rules as the genre skills: official facts enter as REFERENCE, the owner's maps
upgrade them (1 map confirmed, 2 proven, against contested), nothing is learned without approval.
It applies when a project contains material assets (M_, MI_, MF_, MPC_ files or a Materials folder) or Verse
that sets materials. The owner's maps are full of reusable materials: harvest them as lessons.

## How to use

- Before creating a material, look for an existing reusable one (project, then the owner's other maps via the
  inventory, then the second brain). Reuse a parent and make an instance instead of a new material.
- REFERENCE items are official platform facts in our own words. Items from the owner's maps outrank them.

## Create a new material from known ones (recipes)

A recipe says: start from this known asset, change these parameters. Faster than building from scratch.
1. `python Claude/hooks/skills_lib.py recipes materials <keyword>` lists official and learned recipes
   (official ones come from Epic's docs; learned ones from the owner's maps).
2. Pick the closest recipe, make an instance of its parent, set the parameters from its steps. Only when no
   recipe is close, build a new parent material and say why.
3. The coder (who has the UEFN MCP) tries the MCP tools that create material assets or instances; if none
   exists, give the owner the recipe steps to do in the editor. Note the MCP tool names that worked in
   `~/.claude/skills/genre/materials/local/mcp-notes.md` so next time starts from them.
4. After the owner confirms the result works, save it as a recipe: write a JSON file (name, parent, use, steps,
   params) and run `python Claude/hooks/skills_lib.py recipe-add materials <file> "<map name>"`. A learned
   recipe is a hypothesis; used in a second map it becomes confirmed (each map counts once).
5. Recipes marked verify_names list parameters by category: confirm the exact parameter names in the editor.

## Harvest from a map (read-only)

Run `python Claude/hooks/skills_lib.py materials .` : it lists the material assets by folder and prefix
(parents M_, instances MI_, functions MF_, parameter collections MPC_, textures T_) and counts. Binary assets are
not parsed: names and folders only. Turn what repeats across maps (naming, parent/instance structure, a
reusable parent for UI shapes, folder layout) into lessons through skill-reflector, for approval.

## Audit checklist

1. Instances share a few parents; no copy-pasted parent materials.
2. UI uses material instances (shapes, stroke, gradient) rather than imported textures where a shape is enough.
3. Parameters named consistently, exposed on the instance, not hard-coded per use.
4. Textures only where materials cannot do it (memory cost); prefer one SDF texture over several.
5. Physical material assigned on UI shape instances so there are no transparent boundary issues.
6. Folder and prefix naming consistent (M_, MI_, MF_, MPC_).

<!-- PATTERNS:BEGIN -->
<!-- PATTERNS:END -->
