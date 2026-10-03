---
name: theme-factory
description: Toolkit for styling artifacts with a theme. These artifacts can be slides, docs, reportings, HTML landing pages, etc. There are 10 pre-set themes with colors/fonts that you can apply to any artifact that has been creating, or can generate a new theme on-the-fly.
license: Complete terms in LICENSE.txt
---


# Theme Factory Skill

This skill provides a curated collection of professional font and color themes themes, each with carefully selected color palettes and font pairings. Once a theme is chosen, it can be applied to any artifact.

## Purpose

To apply consistent, professional styling to presentation slide decks, use this skill. Each theme includes:
- A cohesive color palette with hex codes
- Complementary font pairings for headers and body text
- A distinct visual identity suitable for different contexts and audiences

## Usage Instructions

To apply styling to a slide deck or other artifact:

1. **Show the theme showcase**: Display the `theme-showcase.pdf` file to allow users to see all available themes visually. Do not make any modifications to it; simply show the file for viewing. The PDF covers themes 1-10 only; list the Hangul themes (11-14) as text alongside it, since they were added after the showcase was rendered.
2. **Ask for their choice**: Ask which theme to apply to the deck
3. **Wait for selection**: Get explicit confirmation about the chosen theme
4. **Apply the theme**: Once a theme has been chosen, apply the selected theme's colors and fonts to the deck/artifact

**For Korean-language artifacts, default to a Hangul theme (11-14).** Themes 1-10 specify Latin-only faces (DejaVu Sans, FreeSans) that carry no Hangul glyphs, so Korean text silently falls back to a system font and breaks the intended typography.

## Themes Available

Themes 1-10 are showcased in `theme-showcase.pdf`:

1. **Ocean Depths** - Professional and calming maritime theme
2. **Sunset Boulevard** - Warm and vibrant sunset colors
3. **Forest Canopy** - Natural and grounded earth tones
4. **Modern Minimalist** - Clean and contemporary grayscale
5. **Golden Hour** - Rich and warm autumnal palette
6. **Arctic Frost** - Cool and crisp winter-inspired theme
7. **Desert Rose** - Soft and sophisticated dusty tones
8. **Tech Innovation** - Bold and modern tech aesthetic
9. **Botanical Garden** - Fresh and organic garden colors
10. **Midnight Galaxy** - Dramatic and cosmic deep tones

Themes 11-14 are Hangul-first (not in the PDF). Each ships a full Hangul font stack with system fallbacks and WCAG AA verified contrast:

11. **Hangeul Editorial** (한글 에디토리얼) - Ink black and vermilion for Korean publishing; Hahmlet + Noto Sans KR
12. **Hangeul Corporate** (한글 기업) - Navy and steel blue for enterprise and finance; Gothic A1 + IBM Plex Sans KR
13. **Hangeul Minimal** (한글 미니멀) - Warm neutral with a muted plum accent; Pretendard single family
14. **Hangeul Impact** (한글 임팩트) - Dark-first with magenta accent for headlines; Black Han Sans + Nanum Gothic

### Hangul font notes

- Each Hangul theme lists a **fallback chain** (Malgun Gothic on Windows, Apple SD Gothic Neo on macOS, Noto Sans CJK KR on Linux). When rendering to PPTX/PDF where the primary face is not installed, the fallback is what actually renders — verify which one applies before promising the primary.
- For HTML output, the web font must actually be loaded via the `<link>` or `@import` in each theme file. Naming the family in CSS without loading it falls back silently.
- Pretendard (theme 13) is not on Google Fonts; it loads from the jsDelivr CDN specified in the theme file.

## Theme Details

Each theme is defined in the `themes/` directory with complete specifications including:
- Cohesive color palette with hex codes
- Complementary font pairings for headers and body text
- Distinct visual identity suitable for different contexts and audiences

## Application Process

After a preferred theme is selected:
1. Read the corresponding theme file from the `themes/` directory
2. Apply the specified colors and fonts consistently throughout the deck
3. Ensure proper contrast and readability
4. Maintain the theme's visual identity across all slides

## Create your Own Theme
To handle cases where none of the existing themes work for an artifact, create a custom theme. Based on provided inputs, generate a new theme similar to the ones above. Give the theme a similar name describing what the font/color combinations represent. Use any basic description provided to choose appropriate colors/fonts. After generating the theme, show it for review and verification. Following that, apply the theme as described above.
