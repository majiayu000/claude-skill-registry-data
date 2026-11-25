---
name: ai-cover
description: Generates illustrations and YouTube covers/thumbnails (1280x720) with SDXL running locally on ComfyUI, in Kurzgesagt or Samurai Jack style (or a free style), and puts a big title on top. Use when the user asks "make a cover" / "faz uma capa", "thumbnail" / "miniatura", "generate an image/illustration" / "gera uma imagem/ilustração", "in kurzgesagt style" / "no estilo kurzgesagt", "samurai jack style" / "estilo samurai jack", "more variations" / "gera mais variações", or wants to redo a video's cover.
---

# Cover with local SDXL

Two scripts in `~/.claude/skills/ai-cover/scripts/`:

- `sdxl.py`: generates the illustrations (1344x768, ~15 s each on the GPU once the model is loaded).
- `title.py`: puts the title on top and outputs 1280x720 ready for YouTube.

## Flow

1. First, `free -h`. The 6.9 GB model goes through RAM before VRAM, and the peak gets close to 7 GB.
   `sdxl.py` refuses with less than 6 GB free. If memory is short, show what is eating RAM
   (`ps -eo rss,comm --no-headers | awk '{m[$2]+=$1} END{for(k in m) print int(m[k]/1024), k}' | sort -rn | head`;
   "Isolated"/"Web" are Firefox tabs) and suggest closing tabs or idle sessions. Or run with `--wait`, in the background.
2. Write each scene in English, short and concrete: one subject, one action, one setting. Base SDXL ignores
   fine detail (a key in a hand, puppet strings tend to vanish); it follows silhouette and composition well.
   Never ask for text in the image, the title comes later.
3. Generate a few at a time (`--n 1` or `2`), build a mosaic and send it to the user to choose:

       python3 ~/.claude/skills/ai-cover/scripts/sdxl.py --out renders/art --style jack --n 2 \
         eye="a lone man in a long coat standing small at the bottom, looking up at a giant glowing eye in the sky" \
         strings="a lone man walking forward with glowing puppet strings on his arms rising into the dark sky"
       ffmpeg -v error -y -i a.png -i b.png -i c.png -i d.png -filter_complex "[0][1]hstack[x];[2][3]hstack[y];[x][y]vstack,scale=1344:-1" mosaic.jpg

4. On the chosen one, add the title (short, 2 to 4 words, uppercase, in the video's language):

       python3 ~/.claude/skills/ai-cover/scripts/title.py renders/art/eye_1000.png "WHO HOLDS THE KEY?" renders/cover.png

   Check the image before sending: text on a single line, not covering the face/main object. If it does not fit, `--fs 88`.

## Styles

- `kurz`: flat vector with gradients, purple/navy with magenta, cyan and orange neon. Comes out closer to a synthwave poster
  than faithful Kurzgesagt, but the user liked it.
- `jack`: flat black silhouette with no outline, giant moon, magenta sky. What worked best as a cover:
  small figure at the bottom + huge element in the sky, which leaves room for the title on top.
- Any other text in `--style` becomes a free style.

## What the user rejected

Covers made from the video's own frames and SVG montages with the video's character (basilisk + contract). He wants
a new, good-looking illustration, one strong image, thick white title on top, like Kurzgesagt covers.

## Environment

ComfyUI at `~/ComfyUI` (`.venv`), checkpoint `models/checkpoints/sd_xl_base_1.0.safetensors`. The script starts the server
on port 8199 with `systemd-run MemoryMax=8G` and stops it at the end. Log at `/tmp/comfy-sdxl.log`. Progress in taskline (`sdxl`).
Cover published with the Portuguese cut of the example video (title in Portuguese): cover-pt-BR.png on the `media` branch of the `claude-code-video-studio` repo.
