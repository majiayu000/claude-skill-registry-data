---
name: github-social-preview-generator
description: Creates a polished, repository-specific GitHub social preview image from the repository README, package metadata, branding, screenshots, demos, and public-facing purpose. Use when the user asks for a GitHub social card, repository Open Graph image, repo preview image, social media preview, link preview, or a 1280×640 repository share image.
license: MIT
compatibility: Portable Agent Skill. Requires repository file access and an available image-generation, SVG-rendering, HTML-screenshot, or image-processing capability to produce the final raster asset.
metadata:
  category: repo-readiness
  task_type: generator
  audience: open-source-maintainers
  tags:
    - github
    - social-preview
    - open-graph
    - repository-branding
    - image-generation
  status: draft
  side_effects: file-write
---

# GitHub Social Preview Generator

## Purpose

Create a polished social preview image that communicates what a GitHub repository is, why it is useful, and what makes it recognizable when the repository link is shared.

Derive the design from the actual repository instead of placing its name on a generic gradient. Inspect the README, package metadata, screenshots, documentation, demos, logos, and visual language before deciding what belongs in the image.

Use this normal deliverable:

```txt
.github/social-preview.png
```

Prepare the final image for manual upload through the repository's GitHub settings.

## When to use this skill

Use this skill when:

- The user asks for a GitHub repository social preview.
- The user asks for a repository Open Graph or link-preview image.
- A public repository has no recognizable preview when shared.
- A repository is being prepared for launch or public promotion.
- The repository's current preview is outdated, generic, unreadable, or inconsistent with its documentation.
- Several repositories need a consistent family of social cards.
- Another repository-polish skill identifies the social preview as missing.

Do not use this skill when:

- The user only needs a website `og:image` implementation.
- The request is for a README banner without a social-preview deliverable.
- The repository identity and purpose cannot be determined from available material.
- The user is asking to upload or modify GitHub settings but has not explicitly authorized that remote action.
- A more specific brand-design workflow owns the complete project identity.

## Inputs to inspect

Inspect the smallest relevant set of available files.

### Repository identity

- `README.md`
- Repository description
- Repository topics
- `package.json`
- `pyproject.toml`
- `Cargo.toml`
- `composer.json`
- Other ecosystem metadata files
- Monorepo package manifests

### Public-facing content

- Documentation homepage
- Demo pages
- `examples/`
- `demo/`
- `docs/`
- Feature lists
- Installation examples
- Usage examples
- Release notes when the repository recently changed direction

### Visual assets

- Logos
- Icons
- Screenshots
- Product or component previews
- Existing banners
- Brand colors
- CSS custom properties
- Design tokens
- Documentation styles
- Existing Open Graph images

Check common locations such as:

```txt
.github/
assets/
public/
docs/
images/
screenshots/
demo/
examples/
src/assets/
```

### Existing repository conventions

Check whether the repository already specifies:

- An asset output location
- Image naming conventions
- Brand typography
- Light or dark presentation
- A generated-assets workflow
- Image optimization scripts
- A repository-wide visual system

Do not assume that `package.json` is present. Adapt to the repository's ecosystem.

## Required output specification

Create the final image using these defaults:

```txt
Dimensions: 1280 × 640 pixels
Aspect ratio: 2:1
Preferred format: PNG
Maximum file size: 1 MB
Default path: .github/social-preview.png
```

Treat these as GitHub's current published requirements and recommendations, not permanent constants. When network access is available, verify them against the current official GitHub documentation before making final compliance claims.

Use PNG for typography-led cards, interfaces, icons, and flat graphics in most cases.

Prefer JPG when the design is primarily photographic and PNG compression cannot remain below the size limit.

Use GIF only when animation is explicitly requested and the resulting file still satisfies platform limits.

Create SVG only as an editable source, not as the final upload asset.

When an editable source improves maintainability, use:

```txt
.github/social-preview-source.svg
.github/social-preview.png
```

Do not add the source file when it provides no practical benefit.

## Content hierarchy

Use a restrained hierarchy.

### Required

1. Repository or product name
2. Concise explanation of what it does
3. One recognizable visual element or intentional visual treatment

### Optional

- Logo
- Product screenshot
- Component screenshot
- Short package category
- Up to three stable technology or capability labels
- Maintainer or organization name when it adds useful context

### Usually exclude

- Installation commands
- Long feature lists
- Full paragraphs
- Tiny code examples
- Version numbers that will quickly become stale
- Star or fork counts
- Multiple competing screenshots
- Decorative GitHub branding
- Unsupported claims such as “best,” “fastest,” or “most accessible”
- Generic filler such as “modern,” “powerful,” and “next generation” without evidence

Communicate one idea instead of reproducing the README.

## Copy rules

Derive the copy from repository evidence.

Prefer this structure:

```txt
Repository name

A specific 6–14 word explanation of what the project helps users do.
```

Examples of useful descriptions:

```txt
Accessible client-side validation for progressively enhanced forms.
```

```txt
A lightweight JavaScript utility for restoring long form drafts safely.
```

```txt
Portable Agent Skills for repository, documentation, accessibility, and release workflows.
```

Avoid descriptions such as:

```txt
A modern and powerful solution.
```

```txt
The ultimate developer experience.
```

```txt
Next-generation tools for everyone.
```

Do not invent a tagline when the repository purpose remains ambiguous. Report the ambiguity and propose copy options instead.

## Safe-area rules

Keep all essential content inside the safety boundary defined by the current GitHub social-preview template or another supplied preview template.

Apply the safe area to:

- Repository name
- Description
- Logo
- Important parts of screenshots
- Small labels
- Decorative elements whose cropping would make the composition look broken

Allow background color, texture, gradients, and nonessential decoration to extend to the canvas edges.

Do not place important content against the outer edge merely because the full image looks balanced at 1280 × 640. Shared-link previews may display the image at smaller sizes or with platform-specific cropping.

If no safe-area template is available, use a conservative inset and document it in the design direction rather than implying that GitHub publishes a fixed safe-area specification.

## Layout selection

Choose one layout based on the repository instead of using the same template blindly.

### 1. Typography-led card

Use when:

- No suitable screenshots exist.
- The repository is a utility, library, configuration, or research project.
- The project name and purpose are the main identity.

Use a composition such as:

```txt
Large repository name
Short value proposition
Small logo, icon, monogram, or abstract system motif
```

### 2. Product or demo preview

Use when:

- A strong interface screenshot exists.
- The repository produces a visible component, site, application, or interaction.
- The screenshot remains understandable when reduced.

Use a composition such as:

```txt
Copy block on one side
Cropped interface or component preview on the other
```

Do not shrink an entire website into an unreadable miniature.

### 3. Component-focused card

Use when:

- The repository contains a UI widget or plugin.
- One component state can explain the project better than a full demo page.

Use a composition such as:

```txt
Repository name
One-line explanation
Enlarged component example
One or two supporting state details
```

### 4. Developer-tool card

Use when:

- The repository is a CLI, API, build tool, package, or developer workflow.
- No graphical product surface is available.

Consider visual elements such as:

- Simplified terminal output
- Package structure
- Abstract code blocks
- Data-flow diagram
- Generated artifact preview

Do not use real code at a size that becomes unreadable.

### 5. Collection or library card

Use when:

- The repository contains several related tools, packages, examples, or skills.
- Showing one item would misrepresent the repository.

Use a composition such as:

```txt
Repository or collection name
One-line collection purpose
A restrained set of three to six visual tokens or item cards
```

Avoid dense dashboards and walls of miniature cards.

## Art-direction rules

Make the design feel connected to the repository.

Derive visual decisions from available evidence:

- Use existing brand colors when they have sufficient contrast.
- Reuse the typography character of the documentation where practical.
- Reuse existing icons or logos instead of inventing replacements.
- Match the tone of the project: technical, editorial, playful, minimal, enterprise, experimental, or accessibility-focused.
- Use screenshots only when they are current and representative.
- Simplify screenshots instead of adding excessive decorative framing.
- Prefer one strong focal point.
- Use whitespace intentionally.
- Keep background treatment subordinate to the content.

Do not automatically create:

- Purple-to-blue gradients
- Floating glass cards
- Fake browser chrome
- Random blobs
- Neon code fragments
- Oversized GitHub logos
- Decorative accessibility symbols unrelated to the repository
- Fake application screenshots

Treat a generic card with the project name pasted over a gradient as a fallback, not a finished design.

## Workflow

### 1. Establish the task boundary

Confirm:

- The target repository
- Whether the task is analysis-only or includes file creation
- The desired output path
- Whether an existing image should be replaced
- Whether a family style from related repositories should be reused
- Whether the user wants an editable source

Do not upload the image or modify remote repository settings unless that action is explicitly requested and authorized.

### 2. Extract the repository story

Read the relevant repository files and identify:

- What the repository is
- Who it is for
- The main problem it solves
- Its most distinctive capability
- The preferred public-facing name
- Existing visual assets
- The strongest visual proof of the project

Summarize the repository in one sentence before designing.

If the repository purpose cannot be summarized accurately, stop and report what information is missing.

### 3. Audit existing assets

For every candidate asset, check:

- Is it current?
- Is it sharp enough?
- Does it represent the main project?
- Does it contain private or test data?
- Does it remain understandable at thumbnail size?
- Does it conflict with the intended background?
- Does its license or ownership permit use?

Reject stale, blurry, misleading, or unrelated assets.

### 4. Define the card brief

Create a compact internal brief:

```md
Repository:
Audience:
Primary message:
Secondary message:
Visual anchor:
Layout:
Tone:
Background treatment:
Output path:
```

Do not begin image generation until the primary message and visual anchor are clear.

### 5. Write the preview copy

Create two or three concise description options.

Select the option that:

- Is supported by repository evidence
- Explains the actual use case
- Avoids duplicated wording
- Remains readable at preview size
- Does not depend on temporary metrics or release numbers

Preserve official capitalization from the repository.

### 6. Choose the composition

Select the best layout pattern.

Determine:

- Primary focal point
- Copy alignment
- Screenshot or illustration placement
- Relative visual weight
- Safe-area boundaries
- Contrast strategy
- How the image behaves when reduced to 640 × 320 and smaller

Avoid centering every element by default. Choose alignment based on the content.

### 7. Create the source composition

Use the best available production method.

Possible methods include:

- SVG composition
- HTML and CSS rendered to an image
- Canvas rendering
- Image-generation tooling
- Existing design-tool automation
- ImageMagick or similar processing
- A repository-specific generation script

Prefer deterministic SVG or HTML composition when:

- The image is primarily typography and interface assets.
- The repository may need future updates.
- Several repositories need a consistent system.
- Exact alignment and text accuracy matter.

Use generative imagery only when it supports the project identity. Do not use generated text inside an image when exact typography can be rendered directly.

### 8. Export the final asset

Export the final raster image.

Validate:

- Exact dimensions
- Correct format
- File size
- Color profile
- Text rendering
- Image sharpness
- Transparency behavior
- No clipped content
- No placeholder text
- No accidental private information

Optimize the file without visibly degrading important text or screenshots.

### 9. Test reduced-size readability

Inspect the image at:

```txt
1280 × 640
640 × 320
320 × 160
```

At the smallest preview:

- The repository name should still be identifiable.
- The central visual idea should remain visible.
- Supporting text should not become distracting noise.
- The composition should not rely on thin borders or tiny labels.
- The safe-area placement should still feel intentional.

Remove details that fail instead of making everything larger and more crowded.

### 10. Compare against repository truth

Before finishing, verify:

- The name matches the repository.
- The description matches the README and package metadata.
- The screenshot represents the current project.
- The visual style does not promise a product experience the repository does not provide.
- The image does not imply official affiliation with another organization.
- No current statistics or version claims have become embedded accidentally.

### 11. Provide upload guidance

Return concise manual instructions for adding the final image through the repository's social-preview settings.

When network access is available, verify the current GitHub interface before describing exact menu labels.

Do not claim that the image has been uploaded unless the remote action was actually completed.

## Repeatable generation

Create a regeneration script only when:

- The repository frequently changes its title or branding.
- Several repositories share one visual system.
- The social card includes generated screenshots.
- The user explicitly requests automation.
- Reproducible output is important.

Consider paths such as:

```txt
scripts/generate-social-preview.mjs
scripts/social-preview/
```

Require a generation script to:

- Produce the final image at the documented path.
- Fail when required assets are missing.
- Verify dimensions.
- Verify the maximum file size.
- Avoid network calls unless documented.
- Use deterministic local assets where possible.
- Be documented in the README or contributor documentation.

Do not add a build dependency for a single static image unless the maintenance benefit justifies it.

## Output format

Return:

```md
## Summary

State what was created or recommended.

## Repository story

- Repository:
- Audience:
- Main purpose:
- Primary message:
- Visual anchor:

## Design direction

- Layout:
- Copy:
- Typography:
- Background:
- Supporting elements:
- Safe-area strategy:

## Files created or updated

- `.github/social-preview.png`
- Other files, when applicable

## Asset sources

| Asset | Source | Reason used |
|---|---|---|

## Validation

- [ ] Final image is 1280 × 640 pixels.
- [ ] Final image uses PNG, JPG, or GIF.
- [ ] Final image is no larger than 1 MB.
- [ ] Important content remains inside the safe area.
- [ ] Repository name is readable at thumbnail size.
- [ ] Description accurately represents the repository.
- [ ] Screenshots and logos are current.
- [ ] No private or placeholder content is visible.
- [ ] No remote GitHub settings were changed without approval.

## Upload instructions

Provide the current manual GitHub steps.

## Remaining TODOs

- ...
```

If no image was generated, replace `Files created or updated` with:

```md
## Proposed deliverables
```

## Quality bar

The task is complete only when:

- The image is based on the actual repository.
- The repository can be understood from the image within a few seconds.
- The design has one clear visual hierarchy.
- Important content respects the safe area.
- The project name remains recognizable at small sizes.
- The description is concise and evidence-based.
- The image contains no stale metrics or unnecessary version numbers.
- Screenshots and logos are current and appropriately licensed.
- The final raster file meets GitHub's format, dimension, and file-size requirements.
- The output file is stored at the agreed repository path.
- No remote upload is performed without explicit authorization.
- Validation results are reported instead of assumed.

## Edge cases

### No logo exists

Use a typography-led composition. Do not invent a logo unless the user explicitly requests identity design.

### No screenshots exist

Use repository structure, component shapes, diagrams, code motifs, documentation styling, or a type-led composition.

Do not fabricate a product interface.

### The repository name is very long

Reduce supporting copy before reducing the project name to an unreadable size.

Consider:

- A controlled line break
- An official short name
- A package scope separated from the main name
- A smaller supporting namespace

Do not silently rename the project.

### The repository is a monorepo

Determine whether the card represents:

- The complete monorepo
- One package
- One product
- A documentation portal

Do not mix unrelated package identities into one card.

### Multiple screenshots are available

Choose the image that best demonstrates the primary use case.

Use multiple screenshots only when the repository is explicitly a collection and the composition remains legible.

### Existing branding has poor contrast

Preserve the brand character but adjust background, scale, spacing, or supporting colors to maintain readability.

Document any deliberate deviation from existing colors.

### The project has no visual identity

Build the card from:

- Strong typography
- Repository purpose
- A restrained color system
- Simple shapes derived from the project's function

Do not default automatically to a generic AI-style visual.

### Dynamic statistics are requested

Explain that star, fork, download, contributor, or version counts will make the image stale.

Include them only when:

- The user explicitly requires them.
- Current values can be verified.
- The user accepts future maintenance.
- The metric is not misleading.

### Existing preview image is already strong

Do not redesign it merely to produce output.

Report that the existing image is suitable and list only meaningful improvements.

### Image-generation capability is unavailable

Return:

- The complete design brief
- Exact copy
- Composition instructions
- Asset list
- Output specification
- Validation checklist

Do not claim that the final image was generated.

## Related skills

- `repo-public-profile-polish`
- `layout-art-direction`
- `repo-demo-copywriter`
- `docs-discoverability-audit`
