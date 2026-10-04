---
name: web-mermaid-diagrams
description: Catppuccin Mocha themed Mermaid diagrams in a browser page. Use when a frontend renders flowcharts, sequence diagrams, gantt charts, pie charts, git graphs, state diagrams, timelines, or mindmaps, or when Mermaid output does not match the page theme. Triggers on mermaid.initialize, mermaid.run, themeVariables, startOnLoad, a mermaid code fence, and diagrams rendering with default colors or on the wrong surface.
user-invocable: false
---

# Web Mermaid Diagrams

**One config object themes every Mermaid diagram type in Catppuccin Mocha.**

Mermaid is vendored and pinned at `mermaid@11.17.2`, served from the page's own origin.

```html
<script src="/static/js/mermaid.min.js"></script>
```

## Rules

`theme: 'base'` is what makes `themeVariables` authoritative. Any built-in theme name ignores most of the overrides and leaves diagrams half-themed, which reads as a rendering bug rather than a config choice.

`startOnLoad: false` with a manual `mermaid.run()` puts rendering under your control. Automatic rendering fires once at load and misses every diagram inserted afterwards, which is all of them on a page that renders Markdown.

```javascript
mermaid.initialize(mermaidConfig);
mermaid.run({ nodes: container.querySelectorAll('.mermaid') });
```

Passing an explicit node list re-renders only the diagrams in the container that changed, rather than rescanning the document.

A `mermaid` code fence becomes a `<div class="mermaid">` during Markdown parsing, and `mermaid.run()` takes over those elements afterwards.

`fontFamily: 'Inter'` matches the body text, so diagram labels do not arrive in a different typeface from the paragraph above them.

## Config

Every color is read off the page palette at run time rather than written as a literal, so a diagram follows the theme the page is actually wearing. Mermaid derives shades from several of these with its own color math, which needs a resolved value, so `getComputedStyle` is what supplies them rather than a `var()` reference passed through.

```javascript
const css = getComputedStyle(document.documentElement);
const c = (name) => css.getPropertyValue(`--ctp-${name}`).trim();
```

The diagram canvas takes `base`, the same rung as the container it sits in, so the two do not read as a box inside a box. Nodes sit one rung up on `surface0` and a cluster groups them one rung down on `mantle`.

```javascript
const mermaidConfig = {
    startOnLoad: false,
    theme: 'base',
    fontFamily: 'Inter',
    themeVariables: {
        darkMode: true,
        background: c('base'),
        mainBkg: c('base'),

        primaryColor: c('surface0'),
        primaryTextColor: c('text'),
        primaryBorderColor: c('blue'),
        secondaryColor: c('surface1'),
        secondaryTextColor: c('text'),
        secondaryBorderColor: c('overlay1'),
        tertiaryColor: c('surface0'),
        tertiaryTextColor: c('text'),
        tertiaryBorderColor: c('surface2'),

        lineColor: c('blue'),
        arrowheadColor: c('blue'),
        textColor: c('text'),
        titleColor: c('mauve'),
        noteBkgColor: c('surface1'),
        noteTextColor: c('yellow'),
        noteBorderColor: c('surface2'),

        // Flowchart
        nodeBkg: c('surface0'),
        nodeBorder: c('blue'),
        clusterBkg: c('mantle'),
        clusterBorder: c('surface2'),
        defaultLinkColor: c('blue'),
        edgeLabelBackground: c('surface0'),
        nodeTextColor: c('text'),

        // Sequence
        actorBkg: c('surface0'),
        actorBorder: c('blue'),
        actorTextColor: c('text'),
        actorLineColor: c('surface2'),
        signalColor: c('pink'),
        signalTextColor: c('text'),
        labelBoxBkgColor: c('surface1'),
        labelBoxBorderColor: c('surface2'),
        labelTextColor: c('text'),
        loopTextColor: c('yellow'),
        activationBorderColor: c('mauve'),
        activationBkgColor: c('surface1'),
        sequenceNumberColor: c('base'),

        // Gantt
        sectionBkgColor: c('mantle'),
        altSectionBkgColor: c('base'),
        sectionBkgColor2: c('crust'),
        taskBkgColor: c('blue'),
        taskBorderColor: c('lavender'),
        taskTextColor: c('base'),
        taskTextLightColor: c('base'),
        taskTextDarkColor: c('text'),
        taskTextOutsideColor: c('text'),
        taskTextClickableColor: c('sky'),
        activeTaskBkgColor: c('mauve'),
        activeTaskBorderColor: c('pink'),
        doneTaskBkgColor: c('surface1'),
        doneTaskBorderColor: c('surface2'),
        critBkgColor: c('red'),
        critBorderColor: c('maroon'),
        gridColor: c('surface0'),
        todayLineColor: c('red'),

        // Pie, twelve distinct hues
        pie1: c('mauve'), pie2: c('blue'), pie3: c('green'), pie4: c('yellow'),
        pie5: c('red'), pie6: c('teal'), pie7: c('peach'), pie8: c('sky'),
        pie9: c('pink'), pie10: c('sapphire'), pie11: c('maroon'), pie12: c('lavender'),
        pieTitleTextColor: c('text'),
        pieSectionTextColor: c('base'),
        pieLegendTextColor: c('text'),
        pieStrokeColor: c('base'),
        pieOuterStrokeColor: c('surface0'),

        // Git graph, eight branch colors
        git0: c('blue'), git1: c('mauve'), git2: c('green'), git3: c('yellow'),
        git4: c('red'), git5: c('teal'), git6: c('peach'), git7: c('sapphire'),
        gitInv0: c('base'), gitInv1: c('base'), gitInv2: c('base'), gitInv3: c('base'),
        gitInv4: c('base'), gitInv5: c('base'), gitInv6: c('base'), gitInv7: c('base'),
        commitLabelColor: c('subtext1'),
        commitLabelBackground: c('base'),
        tagLabelColor: c('base'),
        tagLabelBackground: c('yellow'),
        tagLabelBorder: c('peach'),

        // State diagram
        labelBackgroundColor: c('surface0'),

        // Color scale, used by mindmaps and timelines
        cScale0: c('surface0'), cScale1: c('blue'), cScale2: c('mauve'),  cScale3: c('green'),
        cScale4: c('yellow'), cScale5: c('red'), cScale6: c('teal'),  cScale7: c('peach'),
        cScale8: c('sky'), cScale9: c('pink'), cScale10: c('sapphire'), cScale11: c('lavender'),
    },
};
```

The pie, git, and colour-scale series each cycle through the full Catppuccin accent range rather than shades of one hue, so adjacent slices and branches stay distinguishable.

The config captures the palette once, so a page with a theme toggle rebuilds it and calls `mermaid.initialize` again before re-running. Already-rendered SVG keeps the colors it was drawn with.

## Container

```css
.mermaid {
    background-color: var(--ctp-base);
    padding: 1rem;
    border-radius: 0.5rem;
    margin: 1.5rem 0;
    text-align: center;
    overflow-x: auto;
}
```

`overflow-x: auto` keeps a wide diagram inside its own scroll region instead of stretching the page.

## Gantt Overrides

Gantt charts read several colors from stylesheet rules rather than from `themeVariables`, so they need CSS to finish the job. These are the only diagram type that does.

```css
.mermaid .grid .tick line {
    stroke: var(--ctp-surface0) !important;
    stroke-width: 0.5px !important;
    opacity: 0.5 !important;
}
.mermaid .grid .tick text { fill: var(--ctp-subtext0) !important; }
.mermaid .grid path { stroke: var(--ctp-surface0) !important; stroke-width: 0.5px !important; }

.mermaid .section { stroke: none !important; }
.mermaid .section0, .mermaid .section2 { fill: var(--ctp-mantle) !important; }
.mermaid .section1, .mermaid .section3 { fill: var(--ctp-base) !important; }

.mermaid .today { stroke: var(--ctp-red) !important; stroke-width: 2px !important; }

.mermaid .taskText { fill: var(--ctp-base) !important; font-size: 0.75em !important; }
.mermaid .taskTextOutsideRight,
.mermaid .taskTextOutsideLeft { fill: var(--ctp-text) !important; }

.mermaid .sectionTitle { fill: var(--ctp-mauve) !important; }
.mermaid .titleText { fill: var(--ctp-mauve) !important; }
```

`!important` is load-bearing here, because Mermaid writes its own inline and generated styles onto these elements after the page stylesheet has been applied.
