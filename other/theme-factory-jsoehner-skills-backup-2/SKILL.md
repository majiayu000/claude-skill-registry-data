---

name: theme-factory

description: |

  Toolkit for styling presentation decks, documents, and web interfaces with professional color palettes and typography pairings. Trigger when asked to style, design, or apply theme presets to presentation slides, HTML templates, or generated reports, or when custom theme palettes are requested. Keywords: theme-factory, theme-showcase.pdf, themes/, Ocean Depths, Sunset Boulevard, Tech Innovation, font pairing, color palette, custom theme.



  Toolkit for styling presentation decks, documents, and web interfaces with professional color palettes and typography pairings. Trigger when asked to style, design, or apply theme presets to presentation slides, HTML templates, or generated reports, or when custom theme palettes are requested. Keywords: theme-factory, theme-showcase.pdf, themes/, Ocean Depths, Sunset Boulevard, Tech Innovation, font pairing, color palette, custom theme.



license: Complete terms in LICENSE.txt

---



# Theme Factory - Stylist Workflow & Standards



A high-performance styling toolkit providing curated, accessible theme configurations and layout constraints for presentation decks, documents, and web interfaces.



## Progressive Disclosure & Reference Triggers



This skill utilizes external theme specification files and a PDF preview:



- **Visual Showcases**: View the static compiled portfolio `theme-showcase.pdf` to see visual treatments. Do NOT modify this file.

- **Theme Assets**: Specific themes reside in `themes/<theme-name>.md`. Only load the chosen theme configuration into the context window once the user select it, keeping the context lightweight.

- **Trigger**: Run a grep or check folder files to ensure target themes exist before applying.



## Freedom Calibration & Constraints

- **Constraint Level: Medium**

  - **High Rigidity**: WCAG accessibility contrast ratios (minimum 4.5:1 for body text, 3:1 for headers) must be enforced. No more than two font families per theme.

  - **Medium Rigidity**: Standard theme directory schema must be followed.

  - **High Freedom**: Custom theme generation parameters, layout distribution, and structural styling details.



## Theme Selection & Design Decision Tree



Use this tree to match the audience and platform context to the perfect theme preset:



```

Who is the primary audience and what is the distribution channel?

 ├─ Corporate / Enterprise / Trust-Critical (Finance, Consulting, B2B)

 │   ├─ Print/Light Background → Use: ocean-depths (Navy/Teal) or modern-minimalist (Grayscale)

 │   └─ On-Screen/Dark Background → Use: midnight-galaxy (Deep Indigo) or tech-innovation (Charcoal/Blue)

 ├─ Creative / Editorial / Lifestyle (Brand Pitches, Consumer Products)

 │   ├─ Warm/Vibrant → Use: sunset-boulevard (Warm Orange/Red) or golden-hour (Autumnal Rust)

 │   └─ Soft/Organic → Use: desert-rose (Dusty Coral/Rose) or botanical-garden (Moss/Olive)

 └─ Nature / Ecology / Natural Sciences

     └─ Use: forest-canopy (Earth/Emerald) or arctic-frost (Ice Blue/Slate)

```



## Professional Mindset & Design Principles

1. **The 60-30-10 Rule**: Apply colors systematically:

   - **60% Dominant (Canvas)**: Backgrounds and structural spaces.

   - **30% Supporting (Structure)**: Main text, headers, and grid lines.

   - **10% Accent (Callout)**: Action buttons, highlighted metrics, and key data nodes.

2. **Readability & Contrast First**: Never sacrifice accessibility for aesthetic preferences. Ensure all text meets the WCAG AA minimum threshold.

3. **Typography Hierarchy**: Use a strict scale: Headers (2.0x base size, bold/heavy weight), subheadings (1.4x base size, medium weight), body text (1.0x base size, regular weight).



---



## Step-by-Step Theme Application Procedure



### Step 1: Theme Discovery

- Present the names of the 10 available themes to the user.

- Reference the existence of `theme-showcase.pdf` for visual inspection.



### Step 2: Theme Selection & Loading

- Wait for the user's confirmation or selection.

- Once selected, load the corresponding config file (e.g. `themes/ocean-depths.md`) to read hex codes and font pairings.

- If a custom theme is requested:

  - Generate a new markdown definition detailing: Name, Color Palette (hex codes), Typography (headers/body), and Best Used For description.

  - Show it to the user for validation before application.



### Step 3: Application & Verification

- Map the theme values to the target artifact format (e.g., CSS variables, HTML styling, markdown metadata, or template values).

- Verify contrast ratios programmatically or heuristically.

- Output the styled artifact.



---



## Critical Anti-Patterns (NEVER List)



| Anti-Pattern | Description | Alternative / Solution |

| :--- | :--- | :--- |

| **NEVER** load all themes at once | Loading all theme configuration files into the context window causes token bloat. | Disclose selectively; load only the chosen theme file once selected. |

| **NEVER** violate contrast ratios | Using light accent colors on light backgrounds (or dark on dark) renders text unreadable. | Always use high-contrast primary colors for text (e.g. Cream on Navy, Charcoal on White). |

| **NEVER** use more than 2 fonts | Combining three or more font families makes layouts appear disorganized. | Stick to one font family for headers and one for body. |

| **NEVER** modify `theme-showcase.pdf` | Attempting to write or rewrite the binary PDF showcase corrupts the file. | Keep the showcase file strictly read-only. |

| **NEVER** hardcode system fonts without fallback | Hardcoding platform-specific fonts (e.g., San Francisco, Segoe UI) breaks cross-platform rendering. | Specify standard web-safe fallbacks (e.g., "Helvetica Neue, Arial, sans-serif"). |



---



## Common Error Scenarios & Fallbacks



### Scenario 1: Selection of non-existent theme

- **Root Cause**: User requests a theme that is not one of the 10 presets and doesn't specify custom settings.

- **Fallback**: 

  1. Default to `modern-minimalist` or `ocean-depths` as safe corporate standards.

  2. Ask the user for clarification or if they would like to generate a custom theme.



### Scenario 2: Requested typography font is missing in the render system

- **Root Cause**: Standard system fonts (like DejaVu Sans or Arial) are missing on the target host.

- **Fallback**: Map to standard generic CSS families:

  - Sans-Serif: `sans-serif`

  - Serif: `serif`

  - Monospace: `monospace`

  ```css

  font-family: 'DejaVu Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;

  ```


## Memory Sync

After completing key technical findings, architectural decisions, code refactorings, or risk assessments, you **MUST** trigger the local memory capture.

1. Save the final summary or artifact as a Markdown file in the project directory.
2. Invoke the capture script:
   ```bash
   python3 ~/memory_system/capture_knowledge.py <file_path>
   ```
3. This ensures that new learnings, policies, and technical snippets are automatically routed to the correct local storage (OKF or ChromaDB).
