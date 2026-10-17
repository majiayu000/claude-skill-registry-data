---
name: repo-demo-copywriter
description: Writes clear, natural, technically accurate copy for repository demo sites by inspecting the README, package metadata, source exports, examples, and actual plugin behavior. Use when the user asks to write or improve demo-page text, hero copy, feature explanations, code-example introductions, setup instructions, SEO metadata, calls to action, or complete landing-page content for a JavaScript or TypeScript package without generic marketing language, robotic phrasing, or invented claims.
license: MIT
compatibility: Portable Agent Skill. Can be copied into an Agent Skills-compatible environment with repository file access unless stated otherwise.
metadata:
  category: docs-seo
  task_type: writer
  audience: open-source-maintainers
  tags:
    - demo-site
    - documentation
    - copywriting
    - developer-experience
    - plugins
    - seo
    - code-examples
  status: draft
  side_effects: none
---

# Repository Demo Copywriter

## Purpose

Write useful, human-sounding content for the demo or documentation site of an open-source repository.

The skill reads the repository before writing. It uses the actual package behavior, API, examples, terminology, constraints, and intended audience as its source material.

The resulting copy should help a visitor quickly understand:

- what the project does
- what problem it solves
- when it is useful
- how the live demo should be used
- how the implementation works
- what code is required
- which features or extension points matter
- where to find installation, API, and repository information

The demo site should feel like a practical explanation from the project’s maintainer, not a generic product landing page generated from the package name.

## When to use this skill

Use this skill when:

- The user asks for better text for a repository demo site.
- A plugin demo contains only controls and code without enough explanation.
- A demo page repeats the README without adapting it for the web.
- The user wants hero copy, section introductions, feature explanations, or calls to action.
- A JavaScript or TypeScript package needs a clearer public-facing demo.
- The user wants code examples explained without turning the page into a long tutorial.
- Existing copy sounds generic, exaggerated, repetitive, or machine-generated.
- The demo needs SEO titles, descriptions, headings, or introductory text.
- The page needs to explain addons, options, events, lifecycle methods, or integration behavior.
- The user wants consistent copy across several plugin demo sites.

Do not use this skill when:

- The user only wants the README audited.
- The task is limited to visual design or page layout.
- The user wants API documentation generated from source types.
- The request is only for package metadata or an npm description.
- The repository has not been provided and there is no reliable description of its behavior.
- The user wants fictional marketing claims rather than repository-grounded documentation.
- Another skill already handles the requested structural or implementation work.

## Core writing principles

### The repository is the source of truth

Do not infer capabilities from the package name alone.

Every factual claim must be supported by at least one of:

- implementation code
- public types
- package exports
- tests
- examples
- demo behavior
- README documentation
- package metadata
- existing project documentation

If a capability cannot be confirmed, omit it or mark it for verification.

### Explain behavior, not adjectives

Prefer:

> The plugin reads native form constraints and adds accessible inline error messages.

Avoid:

> A powerful and intuitive validation solution that transforms your forms.

Prefer:

> Add the script to an existing form. You do not need to replace your labels, inputs, or validation attributes.

Avoid:

> Seamlessly integrate robust validation into any modern workflow.

Concrete behavior is more convincing than praise.

### The demo page is not a second README

The README is usually optimized for repository visitors.

The demo page should be optimized for someone who wants to:

1. understand the project
2. try the interaction
3. inspect a realistic example
4. see the required code
5. decide whether to open the full documentation

Do not copy large README sections without adapting their purpose and hierarchy.

### Code must have a narrative role

Do not place unexplained code blocks on the page.

Each important example should answer:

- What does this code demonstrate?
- Which lines are essential?
- What should the visitor try in the demo?
- What behavior should they expect?
- Where can they learn about advanced options?

Keep explanations close to the relevant example.

### Write for developers without sounding like a specification

Use technically precise language, but avoid making every paragraph read like API reference material.

A demo page may say:

> Submit the empty form to see how the validator connects each message to its field and moves focus to the error summary.

It does not need to say:

> Upon invocation of the submission lifecycle, validation state is programmatically evaluated and subsequently surfaced through generated interface nodes.

### Respect the reader’s time

The opening section should explain the project before discussing architecture, implementation history, or every available option.

Lead with the practical value. Move detail progressively deeper into the page.

## Inputs to inspect

Inspect the minimum relevant files available in the repository.

### Project identity

- `package.json`
- `README.md`
- repository description
- package description
- package keywords
- `LICENSE`
- `CHANGELOG.md`

### Public implementation

- package entry points
- `src/index.*`
- exported classes and functions
- public TypeScript types
- option interfaces
- event types
- addon interfaces
- lifecycle methods
- generated declaration files
- package export maps

### Demo and example behavior

- `demo/`
- `demos/`
- `examples/`
- `playground/`
- `site/`
- `docs/`
- `index.html`
- example scripts
- example styles
- demo navigation
- existing page copy
- screenshots when supplied

### Behavioral evidence

- tests
- fixtures
- accessibility tests
- browser tests
- integration tests
- example markup
- error messages
- status messages
- CSS class names
- data attributes
- custom events

### Build and usage context

- import examples
- browser bundle entry points
- CDN examples
- CSS imports
- initialization functions
- destroy methods
- framework adapters
- supported environments
- browser support documentation

Do not read unrelated implementation files after the public behavior is sufficiently understood.

## Workflow

### 1. Determine the page’s job

Identify what kind of page is being written.

Common page types include:

- project demo homepage
- single-plugin demo page
- example index
- feature-specific example
- interactive playground
- documentation landing page
- package comparison page
- integration guide
- accessibility behavior demo

Determine the primary visitor intent.

Examples:

- evaluate whether the package fits a project
- understand a particular feature
- try the interaction
- copy a minimal example
- compare configuration options
- inspect accessibility behavior
- learn how addons change the base plugin

Do not give every demo page the same content structure.

### 2. Build a repository fact sheet

Before writing copy, record the confirmed facts.

Use this structure internally:

```md
## Repository fact sheet

- Project name:
- Package name:
- Project category:
- Primary problem:
- Intended users:
- Main behavior:
- Initialization method:
- Required markup:
- Required CSS:
- Public API:
- Important options:
- Events:
- Addons or extensions:
- Accessibility behavior:
- Cleanup behavior:
- Browser or runtime constraints:
- Dependencies:
- Demo scenarios:
- Documentation links:
- Claims requiring verification:
````

This fact sheet is not necessarily part of the final user-facing output.

### 3. Identify the strongest message

Find the most useful and defensible project distinction.

Strong distinctions describe implementation or user benefit, such as:

* enhances existing semantic markup
* has no runtime dependencies
* keeps optional features outside the base bundle
* uses native browser behavior where practical
* supports direct browser and module imports
* exposes lifecycle events for integration
* restores generated DOM when destroyed
* works with existing form controls
* provides a focused alternative to a framework component

Do not invent a unique selling proposition when the repository does not support one.

A project does not need to be revolutionary to be worth using.

### 4. Establish the message hierarchy

Write the page in descending order of importance.

A typical hierarchy is:

1. What the project is
2. What problem it solves
3. What the visitor can try
4. How the implementation works
5. The smallest useful code example
6. Important capabilities
7. Configuration or extension points
8. Accessibility and lifecycle behavior
9. Installation and documentation links

Adjust this structure to the repository.

### 5. Write the opening section

The opening should usually contain:

* an optional eyebrow
* one H1
* a short supporting paragraph
* one primary action
* one secondary action
* optional project facts

The H1 should identify the project and its practical purpose.

Good:

> Accessible form validation that works with your existing markup

Weak:

> The future of effortless form experiences

The supporting paragraph should add implementation context rather than repeat the heading.

Good:

> A11y Form Validator reads native constraints, supports custom and asynchronous rules, and adds connected error messages without replacing your form controls.

Avoid opening paragraphs that list every feature.

### 6. Introduce the live demo

Tell the visitor what to do and what to observe.

A useful demo introduction may explain:

* which control to activate
* which values to enter
* how to trigger an error or state change
* what keyboard behavior to try
* what content is generated
* what remains native
* how to reset the example

Example:

> Submit the form without completing the required fields. The demo adds an inline message to each invalid control and moves focus to the error summary. Correct a field and submit again to see the validation state update.

Avoid empty instructions such as:

> Interact with the demo below to explore the possibilities.

### 7. Select code examples

Use code that already exists in the repository where possible.

Choose examples that demonstrate the primary path with minimal noise.

A useful example commonly includes:

* required HTML
* package import
* initialization
* one meaningful option
* cleanup only when relevant

Do not:

* invent method names
* simplify code until it becomes invalid
* hide required markup
* show internal APIs as public APIs
* use deprecated options
* combine several unrelated features in the first example
* present pseudocode as runnable code without labeling it

If multiple build formats exist, show the project’s preferred format first.

### 8. Explain the code

Introduce each code block with one or two sentences.

After the code, explain only the decisions that are not obvious from reading it.

Useful explanations include:

* why an element needs an attribute
* why initialization happens after the DOM is available
* which markup remains under the developer’s control
* what the plugin generates
* how an option changes behavior
* when destruction or cleanup is needed
* how an addon is registered

Do not translate every line of code into prose.

### 9. Explain features as outcomes

Group related features instead of creating one card per method or option.

Possible groups include:

* markup and initialization
* validation or state management
* feedback and announcements
* keyboard interaction
* customization
* addons and integrations
* events and lifecycle
* cleanup and restoration
* package and build formats

Each feature description should answer:

* What does it do?
* Why does it matter?
* Is there an important limitation or condition?

Bad:

> Highly customizable

Better:

> Override message text, validation timing, CSS hooks, and locale strings without changing the plugin source.

### 10. Explain addons and optional features accurately

When a package supports addons:

* distinguish core behavior from optional behavior
* explain whether addons are separately imported
* state whether they affect bundle size
* show how they are registered
* identify dependencies between addons
* avoid describing a default feature as optional
* avoid describing an internal module as a public addon

Use the repository’s own terminology consistently.

### 11. Describe accessibility behavior with evidence

Do not call a project “fully accessible” or “WCAG compliant” based only on intent.

Describe confirmed behavior instead.

Examples:

* connects error messages with `aria-describedby`
* moves focus to an error summary
* supports keyboard activation
* uses a native `<dialog>`
* restores focus to the opener
* announces asynchronous status updates
* respects `prefers-reduced-motion`
* preserves semantic form controls
* avoids adding keyboard interaction where native behavior already exists

Mention known responsibilities that remain with the implementer.

For example:

> The plugin manages message associations and focus movement. The surrounding form still needs visible labels, meaningful instructions, and an appropriate submit flow.

### 12. Write SEO metadata

When requested, provide:

* page title
* meta description
* H1
* optional social title
* optional social description

Use the actual project name, package type, and primary behavior.

Do not stuff repeated keywords into headings or descriptions.

A title should normally include:

* project or plugin name
* primary task or category
* optional repository or documentation context

A description should explain the project in one natural sentence. It should not be a comma-separated feature inventory.

### 13. Run the anti-robotic writing pass

Review the complete draft and remove wording that sounds generic, inflated, or mechanically generated.

Avoid these words unless they are technically necessary and supported:

* seamless
* seamlessly
* powerful
* robust
* cutting-edge
* revolutionary
* game-changing
* innovative
* next-generation
* intuitive
* effortless
* effortlessly
* supercharge
* elevate
* unlock
* unleash
* transform
* comprehensive
* feature-rich
* modern solution
* ultimate
* dynamic
* versatile

Rewrite common AI patterns.

Avoid:

> Whether you are a beginner or an experienced developer, this powerful plugin provides everything you need.

Prefer:

> Start with the default initialization, then add custom rules or asynchronous checks when the form requires them.

Avoid:

> Say goodbye to complicated implementations.

Prefer:

> The plugin initializes from the existing form and does not require a separate component tree.

Avoid:

> More than just a plugin—it is a complete solution.

Prefer:

> The base package handles validation state and inline messages. Optional modules add features such as summaries and character counts.

Avoid:

> Built with developers in mind.

Prefer:

> The public API includes initialization, validation, server-error handling, and cleanup methods.

Avoid:

> Explore the endless possibilities.

Prefer:

> Try the examples for custom rules, asynchronous validation, and server-returned errors.

Also remove:

* unnecessary rhetorical questions
* repeated three-adjective phrases
* repeated “designed to” constructions
* repetitive sentence openings
* fake enthusiasm
* exaggerated claims
* excessive em dashes
* generic conclusions
* filler before code examples
* claims that merely repeat section headings

### 14. Run the human rhythm pass

Improve the natural rhythm of the copy.

Check for:

* varied sentence length
* direct verbs
* concrete nouns
* short paragraphs
* contractions where appropriate to the project voice
* transitions that explain why the next section matters
* headings that describe content rather than advertise it
* occasional plain language instead of constant technical terminology

Do not deliberately add slang, jokes, or personality that conflicts with the repository.

Natural does not mean casual everywhere.

### 15. Run the technical truth pass

Verify that:

* every public method exists
* every option name is correct
* imports use exported paths
* code samples are internally consistent
* described default behavior matches the source
* optional features are labeled correctly
* accessibility claims match implementation
* dependencies are represented accurately
* browser and runtime claims are supported
* cleanup behavior is not invented
* code examples do not omit mandatory steps

When evidence conflicts, prefer implementation and tests over promotional README wording, and report the discrepancy.

### 16. Run the page usefulness pass

Confirm that the page helps a visitor complete a real decision or task.

A useful page should answer:

* What is this?
* Why would I use it?
* What should I try?
* What code do I need?
* What happens after initialization?
* Which parts can I customize?
* What responsibilities remain mine?
* Where is the full documentation?

Remove sections that only make the page longer.

### 17. Apply changes only when requested

By default, return finished copy without editing files.

When the user explicitly requests implementation:

* identify the relevant page or content file
* preserve existing components and layout where practical
* replace placeholder or weak copy
* keep code snippets synchronized with repository examples
* update metadata when included in scope
* avoid changing functional code unless required to correct a displayed example
* report every file changed

Do not redesign the page, install packages, publish, or deploy unless separately requested.

## Default page content structure

Use this structure when the repository does not provide a stronger existing hierarchy.

### 1. Hero

Include:

* optional category or package label
* H1
* supporting paragraph
* primary documentation or demo action
* secondary GitHub or package action

### 2. Project facts

Include only useful confirmed facts, such as:

* package format
* dependency status
* TypeScript support
* browser build availability
* accessibility approach
* framework independence

Do not turn ordinary implementation facts into marketing badges.

### 3. Demo introduction

Explain what to try and what behavior to observe.

### 4. Why this exists

Explain the practical problem or implementation gap.

Keep this section specific to the repository.

### 5. How it works

Explain the main lifecycle in a few steps.

For example:

1. Use existing semantic markup.
2. Initialize the plugin.
3. The plugin observes or enhances the relevant interaction.
4. Listen for events or call public methods when deeper integration is needed.
5. Destroy the instance when the interface is removed.

Adapt the steps to the actual package.

### 6. Minimal code example

Show the shortest representative implementation.

### 7. Key capabilities

Group capabilities by outcome rather than listing every export.

### 8. Configuration or addons

Explain meaningful extension points.

### 9. Accessibility and implementation notes

Describe confirmed behavior and developer responsibilities.

### 10. Next steps

Link visitors to:

* installation
* full API
* examples
* GitHub repository
* package registry
* changelog
* contribution guide

Include only destinations that exist.

## Output format

When the user asks for complete copy, return:

````md
## Repository understanding

- Project:
- Primary audience:
- Main use case:
- Strongest confirmed distinction:
- Important limitations:
- Source files inspected:

## Content direction

- Page goal:
- Primary message:
- Recommended tone:
- Main visitor action:

## Page copy

### SEO

**Title:**  
...

**Meta description:**  
...

### Hero

**Eyebrow:**  
...

# H1

Supporting paragraph.

**Primary action:** ...  
**Secondary action:** ...

### Demo introduction

...

### Why this exists

...

### How it works

...

### Code example introduction

...

```html
...
````

```js
...
```

### Code explanation

...

### Key capabilities

#### Capability heading

...

### Accessibility and implementation notes

...

### Next steps

...

## Verification notes

* Confirmed from:
* Omitted because unverified:
* Existing documentation conflicts:

````

When the user asks for only one section, return only the requested finished copy plus brief verification notes.

When the user asks for an audit before rewriting, return:

```md
## Summary

## Copy problems

| Priority | Location | Problem | Evidence | Recommended direction |
|---|---|---|---|---|

## Replacement copy

...

## Validation

- [ ] Claims match the repository.
- [ ] Code uses the public API.
- [ ] Core and optional features are distinguished.
- [ ] The opening explains the project without hype.
- [ ] Demo instructions describe a real interaction.
- [ ] Accessibility claims are specific and evidenced.
- [ ] Generic AI phrasing has been removed.
````

## Quality bar

The task is complete only when:

* The repository was inspected before copy was written.
* The copy explains the project’s actual behavior.
* The page has a clear visitor journey.
* The opening identifies the project and its practical use.
* Demo instructions tell the visitor what to try.
* Code examples use real public APIs.
* Important code blocks have useful context.
* Features are described as concrete outcomes.
* Core and optional behavior are distinguished.
* Accessibility claims are specific and supported.
* Limitations and implementer responsibilities are not hidden.
* SEO metadata reads naturally.
* Generic AI language and unsupported superlatives have been removed.
* The copy does not merely repeat the README.
* The final text can be placed into the demo page with minimal rewriting.
* No files are modified unless implementation was explicitly requested.

## Edge cases

### The repository has little documentation

Inspect source exports, types, tests, and examples.

Write only what can be confirmed. Include a short list of facts that require maintainer verification.

Do not compensate for missing information with generic marketing copy.

### The README and implementation disagree

Use the current implementation and tests as the technical source of truth.

Report the conflicting README statement separately.

Do not silently publish contradictory copy.

### The demo contains several examples

Write:

* one shared project introduction
* a short description for each example
* unique instructions describing what to try
* links between related examples where useful

Do not repeat the same project description on every page.

### The plugin is intentionally small

Do not inflate the page to make the package appear larger.

Explain the narrow problem well.

A concise demo page is better than ten weak feature sections.

### The project has several build formats

Present the maintainer’s preferred installation method first.

Place browser bundles, CDN usage, or alternative module formats in a secondary section unless they are the main audience path.

### The project is accessibility-focused

Avoid broad compliance claims.

Explain:

* the accessibility behavior implemented by the package
* the semantic assumptions it makes
* keyboard behavior
* focus behavior
* announcements
* remaining developer responsibilities

### The package exposes addons

Verify whether each addon:

* is part of the base bundle
* requires a separate import
* is enabled by default
* depends on another addon
* has its own styles
* changes markup or lifecycle behavior

Do not call a built-in default feature an addon.

### Existing copy has a strong maintainer voice

Preserve its vocabulary and level of formality.

Improve clarity without replacing every sentence with a uniform house style.

### The user requests implementation

Edit only the content files necessary for the requested page.

Do not modify plugin behavior merely to make the copy easier to write.

## Related skills

* `demo-index-docs-enhancer`
* `docs-discoverability-audit`
* `repo-public-profile-polish`

