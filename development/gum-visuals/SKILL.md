---
name: gum-visuals
description: Create plots, diagrams, and other visualizations with the "gum" language.
---

# Introduction

The `gum` language allows for the elegant and concise creation of SVG visualizations. It has a React-like JSX syntax, but it does not actually use React internally. When interpreted, it produces pure SVG of a specified size. Your task is to generate the appropriate `gum` JSX code to satisfy the user's request. Be sure to place the actual code inside ```jsx``` tags. Rendering of the SVG will be done on the client side.

You will typically construct your figure with a combination of `Element` derived components such as `Circle`, `Stack`, `Plot`, `Network`, and many more. Some of these map closely to standard SVG objects, while others are higher level abstractions and layout containers. You can add standard SVG attributes (like `fill`, `stroke`, `stroke-width`, `opacity`, etc.) to any `Element` component and they will be applied to the resulting SVG.

*Proportional values*: In most cases, values are passed in proportional floating point terms. So to place an object in the center of its parent, you would specify a position of `[0.5, 0.5]`. When dealing with inherently absolute concepts like `stroke-width`, standard SVG units are used, and numerical values assumed to be specified in pixels. Most `Element` objects fill the standard coordinate space `[0, 0, 1, 1]` by default. To reposition them, either pass the appropriate internal arguments (such as `pos` or `rad`) or use a layout component such as `Box` or `Stack` to arrange them.

*Aspect ratio*: Any `Element` object can have an aspect ratio `aspect`. If `aspect` is not defined, it will stretch to fit any box, while if `aspect` is defined it will be sized so as to fit within the specified rectangle while maintaining its aspect ratio. However, when `expand` is set to `true`, the element will be resized so as to instead cover the specified rectangle, while maintaining its aspect ratio.

*Subunit arguments*: For compound elements that inherit `Group`, some keyword arguments are passed down to the constituent parts. For instance, in [Plot](/docs/Plot), one can specify arguments intended for the `XAxis` unit by prefixing them with `xaxis-`. For example, setting the `stroke-width` for this subunit can be achieved with `xaxis-stroke-width`.

# Examples

Below are some examples of user prompts and code output.

**Example 1: Basic Circle**

Prompt: Create a blue circle that is enclosed in box. It should mostly fill the box, but not completely.

Generated code:
```jsx
<Frame padding margin rounded>
  <Circle fill={blue} />
</Frame>
```

*Notes*: We used boolean defaults for `padding`, `margin`, and `rounded`. These will get mapped to `padding={0.1}`, `margin={0.1}`, and `rounded={0.1}` respectively. This adds a little bit of a Tailwind-like flavor and is used throughout the library. Adding a `margin` on the outside is usually good so things like borders don't get clipped.

**Example 2: Symbolic Plot**

Prompt: Create a simple plot of a sine wave titled "Sine Wave" with dashed grid lines.

Generated code:
```jsx
<Frame margin={0.2}>
  <Plot aspect={2} ylim={[-1.5, 1.5]} title="Sine Wave" grid grid-stroke-dasharray={4}>
    <DataPath fy={sin} xlim={[0, 2*pi]} />
  </Plot>
</Frame>
```

**Example 3: Custom Component**

Prompt: Create two rounded boxes side by side in a frame. Left one should be blue, right one should be red.

Generated code:
```jsx
const Squire = attr => <Square rounded {...attr} />
return <Frame padding margin rounded>
  <HStack spacing>
    <Squire fill={blue} />
    <Squire fill={red} />
  </HStack>
</Frame>
```

*Notes*: The user didn't specify the aspect ratio, so we use `2` as a default. The `grid` attribute is a boolean, so we can omit the `true` part. To specify only one grid direction, we could instead use `xgrid` and `ygrid`. For sub-components like `grid` we can pass attributes using the `grid-` prefix. In general, `Plot` will auto-detect the y-axis limits, but I wanted to add a bit of padding to the top and bottom. We also need to be careful to add enough `margin` on the outside to avoid clipping the axis labels.

# Element Class

The base class for all `gum.js` objects. You will usually not be working with this object directly unless you are implementing your own custom elements. An **Element** has a few methods that can be overriden, each of which takes a **Context** object as an argument. The vast majority of implementations will override only `props` and `inner` (for non-unary elements).

Parameters:
- `tag` = `g` — the SVG tag associated with this element
- `unary` = `false` — whether there is inner text for this element
- `aspect` = `null` — the width to height ratio for this element
- `pos` — the desired position of the center of the child's rectangle
- `rad` ­— the desired radius of the child's rectangle (can be single number or pair)
- `xrad`/`yrad` ­— specify the radius for a specific dimension (and expand the other)
- `rect` — a fully specified rectangle to place the child in (this will override `pos`/`rad`)
- `xrect`/`yrect` ­— specify the rectangle for a specific dimension
- `aspect` — the aspect ratio of the child's rectangle
- `expand` — when `true`, instead of embedding the child within `rect`, it will make the child just large enough to fully contain `rect`
- `align` — how to align the child when it doesn't fit exactly within `rect`, options are `left`, `right`, `center`, or a fractional position (can set vertical and horizontal separately with a pair)
- `rotate` — how much to rotate the child by (degrees counterclockwise)
- `spin` — like rotate but will maintain the same size
- `vflip/hflip` — flip the child horizontally or vertically
- `flex` ­— override to set `aspect = null`
- `...` = `{}` — additional attributes that are included in `props`

Methods:
- `props(ctx)` — returns a dictionary of attributes for the SVG element. The default implementation returns the non-null `attr` passed to the constructor
- `inner(ctx)` — returns the inner text of the SVG element (for non-unary). Defaults to returing empty string
- `svg(ctx)` — returns the rendered SVG of the element as a `String`. Default implementation constructs SVG from `tag`, `unary`, `props`, and `inner`

## Example

Prompt: create a custom triangle element called `Tri` and use it to create a triangle with a gray fill

Generated code:
```jsx
const Tri = ({ pos0, pos1, pos2, ...attr }) => <Polygon {...attr}>{[pos0, pos1, pos2]}</Polygon>
return <Tri pos0={[0.5, 0.1]} pos1={[0.9, 0.9]} pos2={[0.1, 0.9]} fill={gray} />
```

# Group Class

*Inherits*: **Element**

This is the main container class that all compound elements are derived from. It accepts a list of child elements and attempts to place them according to their declared properties.

Placement positions are specified in the group's internal coordinate space, which defaults to the unit square. The child's `aspect` is an important determinant of its placement. When it has a `null` aspect, it will fit exactly in the given `rect`. However, when it does have an aspect, it needs to be adjusted in the case that the given `rect` does not have the same aspect. The `expand` and `align` specification arguments govern how this adjustment is made.

Parameters:
- `children` = `[]` — a list of child elements
- `aspect` = `null` — the aspect ratio of the group's rectangle (can pass `'auto'` to infer from the children)
- `coord` = `[0, 0, 1, 1]` — the internal coordinate space to use for child elements (can pass `'auto'` to contain children's rects)
- `xlim`/`ylim` = `null` — specify the `coord` limits for a specific dimension
- `clip` = `false` — clip children to the group's rectangle if `true` (or a custom shape if specified)

## Example

Prompt: a square in the top left and a circle in the bottom right

Generated code:
```jsx
<Group>
  <Rect pos={[0.3, 0.3]} rad={0.1} spin={15} />
  <Ellipse pos={[0.7, 0.7]} rad={0.1} />
</Group>
```

# Box Class

*Inherits*: **Group** > **Element**

This is a simple container class allowing you to add padding, margins, and a border to a single **Element**. It's pretty versatile and is often used to set up the outermost positioning of a figure. Mirroring the standard CSS definitions, padding is space inside the border and margin is space outside the border. There is a specialized subclass of this called **Frame** that defaults to `border = 1`.

**Box** can be pretty handly in various situations. It is differentiated from **Group** in that it will adopt the `aspect` of the child element. This is useful if you want to do something like shift an element up or down by a certain amount while maintaining its aspect ratio. Simply wrap it in a **Box** and set child's `pos` to the desired offset.

There are multiple ways to specify padding and margins. If given as a scalar, it is constant across all sides. If two values are given, they correspond to the horizontal and vertical sides. If four values are given, they correspond to `[left, top, right, bottom]`.

The `adjust` flag controls whether padding/margins are adjusted for the aspect ratio. If `true`, horizontal and vertical components are scaled so that their ratio is equal to the `child` element's aspect ratio. This yields padding/margins of constant apparent size regardless of aspect ratio. If `false`, the inputs are used as-is.

Parameters:
- `padding` = `0` / `0.1` — the padding to be added (inside border)
- `margin` = `0` / `0.1` — the margin to be added (outside border)
- `border` = `0` / `1` — the border width to use (stroke in pixels)
- `rounded` = `0` / `0.1` — the border rounding to use (proportional to the box size)
- `adjust` = `true` — whether to adjust values for aspect ratio
- `shape` = `Rect` — the shape class to use for the border
- `clip` = `false` — whether to clip the contents to the border shape

Subunit names:
- `border` — keywords to pass to border, such as `stroke` or `stroke-dasharray`

## Example

Prompt: the text "hello!" in a frame with a dashed border and rounded corners

Generated code:
```jsx
<Frame padding rounded border-stroke-dasharray={5}>
  <Text>hello!</Text>
</Frame>
```

# Documentation

Below is a list of files to reference for documentation examples on the various components.

**Layout**:
- [Stack](references/Stack.md): arrange elements vertically or horizontally
- [Grid](references/Grid.md): arrange elements in a grid of specified size
- [Points](references/Points.md): arrange one element at each of a list of points

**Shapes**:
- [Rect](references/Rect.md): a rectangle
- [Ellipse](references/Ellipse.md): an ellipse
- [Line](references/Line.md): a single straight line
- [Polyline](references/Polyline.md): a multi-segment line

**Text**:
- [Text](references/Text.md): a single text element
- [Latex](references/Latex.md): a single LaTeX equation
- [TitleFrame](references/TitleFrame.md): a frame with a title
- [Slide](references/Slide.md): a slide with a title and content

**Symbolic**:
- [SymPoints](references/SymPoints.md): plot points symbolically (i.e., using a function)
- [SymLine](references/SymLine.md): plot a line symbolically
- [SymFill](references/SymFill.md): plot a filled area symbolically

**Plotting**:
- [Graph](references/Graph.md): a graph containing multiple elements with a specified coordinate system
- [Plot](references/Plot.md): a plot containing a graph, axes, and labels
- [Axis](references/Axis.md): a single axis for a plot
- [BarPlot](references/BarPlot.md): a bar plot

**Networks**:
- [Node](references/Node.md): a node in a network
- [Edge](references/Edge.md): an edge in a network
- [Network](references/Network.md): a network containing nodes and edges

**Functions**:
- [Math](references/Math.md): mathematical functions
- [Arrays](references/Arrays.md): array operations
- [Colors](references/Colors.md): color operations
