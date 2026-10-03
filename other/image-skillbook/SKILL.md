---
name: image-skillbook
description: >-
  Compare Image Skillbook treatments and route an image request to the most suitable
  installed style Skill. Use when the user wants help choosing an AI photo treatment,
  wants several styles compared, or names Image Skillbook without choosing a style.
  Do not use for ordinary image conversion or when a specific style Skill is already named.
license: MIT
metadata:
  version: "0.1.0"
  author: AlbertAZ1992
---

# Image Skillbook

Help the user choose one focused visual treatment, then route execution to that style's own
instructions. This Skill is a selector and does not replace the independently installable
style Skills.

## Compare the treatments

| Style Skill | Choose when |
| --- | --- |
| `editorial-painted-memory` | the image needs sparse acrylic shapes on warm paper |
| `enamel-travel-keepsake` | a person or place should become a physical souvenir object |
| `crayon-memory-postcard` | wax grain and personal travel-journal warmth fit the subject |
| `rubber-stamp-travel-journal` | place-specific contours should become carved ink layers |
| `painted-editorial-reconstruction` | a scene needs a broad painterly retelling |
| `photo-doodle-story` | a person or pet can interact with tiny line figures |
| `impasto-miniature-world` | the scene can become sculptural thick-paint relief |

Inspect the supplied image and the user's intended mood, subject fidelity, layout, and output
use. Recommend at most three treatments. Give one image-specific reason and one material
trade-off for each recommendation.

Do not generate during comparison unless the user asked the router to choose and proceed.

## Route the request

When the user chooses a treatment:

1. Check whether that style Skill's instructions are available in the current session.
2. If available, follow that Skill exactly. Keep one input per output unless the user asks for
   a combined composition.
3. If unavailable, do not approximate the treatment from this comparison table. Return its
   exact install command:

   ```bash
   npx skills add AlbertAZ1992/image-skillbook \
     --skill <style-skill-name> --global --agent codex --yes
   ```

4. Ask the user to start a new agent session after installation, attach the image again, and
   invoke `$<style-skill-name>`.

Do not blend treatments unless the user explicitly requests a hybrid. In that case, explain
which visual decisions come from each Skill before generation.
