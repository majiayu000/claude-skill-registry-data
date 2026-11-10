---
name: viz3d
description: Start the visualize-in-3d skill from a command, with an optional mode and look first and then the subject, for example "/viz3d film white model the 1906 San Francisco earthquake". With no request it shows the menu of modes and looks.
argument-hint: "[app|lesson|prototype|embed|film|doc|action|showcase|book|game] [look] <subject>"
disable-model-invocation: true
---

# viz3d

The user started viz3d with this request:

$ARGUMENTS

In tools that do not fill in the line above, the request is the rest of the user's message.

1. If the request is empty or is `help`, show the menu below as it is, then ask one question: what do you want to
   make 3D? Stop there.
2. Otherwise load the `visualize-in-3d` skill and follow it from the start. It is installed next to this one
   (`../visualize-in-3d/SKILL.md`).
3. Read the request from the left: an optional mode word, then an optional look word (one or two words, from the
   table below), then the subject. A look word may also come first when there is no mode. Drop the mode and look
   words from the subject. Match whole words, in any case, and take the longest match (`dark documentary` is one
   look). Text in quotes is always subject, so `/viz3d "film noir city"` is a subject, not a mode.
4. With no mode word, pick the shape from the subject with the skill's table. A named look that fits only one shape
   settles it (`plate` is a book). When the subject still fits more than one shape, ask one question that names
   them, for example: watch it, play it, learn how it works, or open it up?
5. A look the user names always wins over the default. With no look word, use the default look for the shape
   (`references/looks.md`, Choosing).

| Look word | Section of `references/looks.md` |
|---|---|
| `ops` | Clean ops world |
| `toy` | Toy isometric |
| `lived-in` | Lived-in isometric |
| `terrain` | Photoreal terrain analysis |
| `documentary`, `dark` | Dark documentary |
| `white model` | White model documentary |
| `layer build` | Layer build film |
| `point cloud` | Point-cloud survey |
| `plate`, `cutaway` | Illustrated cutaway plate |
| `space-time` | Space-time cube |
| `pixel` | Pixel diorama |
| `ASCII` | Dither + ASCII showcase |
| `glow` | Gradient glow ASCII |

## Menu

**Modes**, by what you want people to do with it:

| Watch it | Explore it | Put it in your product |
|---|---|---|
| `film` or `doc`: documentary film of a story or event | `app`: live 3D app with a dashboard and a 30 s film | `prototype`: quick prototype from primitives, no Blender |
| `action`: action short, things fighting, chasing, launching | `lesson`: a real object built and explained step by step | `embed`: live 3D view inside your dashboard, on your data |
| `showcase`: a film or stills that show off one object or model | `book`: illustrated cutaway plate, or a book with quizzes | |
| | `game`: playable browser game | |

**Looks**, in four families:

| Clean product | Real and cinematic | Technical | Stylized art |
|---|---|---|---|
| ops, toy, lived-in | terrain, documentary, white model, layer build | point cloud, plate, space-time | pixel, ASCII, glow |

Examples: `/viz3d app a container port`, `/viz3d film white model the Chernobyl accident`,
`/viz3d showcase glow a cockroach`, `/viz3d game pixel a worm that eats a city`.
