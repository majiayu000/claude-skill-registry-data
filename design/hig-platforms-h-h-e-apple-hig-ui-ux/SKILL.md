---
name: hig-platforms
description: "Adapt an existing interface to Apple platforms or the web using platform-qualified guidance rather than copying appearances across input environments."
---

# Carry the product across contexts, not pixels

Follow the [root contract](../../SKILL.md). Read [numeric-and-web-rules.md](../../references/numeric-and-web-rules.md), [specialized-surfaces.md](../../references/specialized-surfaces.md), and [coverage-map.md](../../references/coverage-map.md). Sources HIG-002/003/006/008/013 and APPLE-003/007 contain relevant context; specialized details require a fresh primary-source read.

## Define the target environment

Record platform, supported OS/deployment versions, windowing model, display conditions, input devices, assistive technology, and distribution surface. Do not equate screen width with platform or assume every Apple user is using the latest release.

Record product invariants separately from presentation choices. Invariants may include object names, business rules, content, saved work, and permissions. Presentation can adapt navigation, control density, layout, shortcuts, feedback, and disclosure to the environment.

Determine whether the request is a native application, a website used on an Apple device, or a hybrid surface. A website on iPhone still needs browser semantics and browser navigation. A native Mac application is not merely a wide iPhone view.

## Context-specific audit questions

### iPhone and touch-first use

Can primary tasks be completed without hover or hidden gestures? Do safe areas, browser/system chrome, the software keyboard, and large text obscure content or actions? Does navigation remain stable when content is empty or restricted? Verify native component placement for the supported release before customizing it.

### iPad and resizable touch/pointer use

Does the interface adapt as the window changes, including intermediate widths? Can multi-column work become a coherent compact flow without discarding selection or draft state? Are touch, pointer, and hardware-keyboard paths complete? Do not treat a tablet as a scaled-up phone screenshot.

### Mac and desktop work

Can people navigate and operate with keyboard and pointer, use expected menus and shortcuts, resize windows, and keep working with dense information? Are document/window identity and unsaved changes clear? Avoid forcing every task into a phone-style stacked flow when comparison or simultaneous context is useful.

### Watch, TV, and spatial contexts

Do not invent control dimensions or interaction rules from phone guidance. Load the current platform and component sources before committing a design. For watch-sized tasks, investigate duration, glanceability, and continuation. For TV, investigate focus, distance, remote/controller input, and media. For spatial work, investigate comfort, input targeting, layout, windows/volumes, and accessible alternatives.

These are research prompts, not a substitute for those platform HIG chapters. If the actual device or simulator is unavailable, document the unverified input and display behavior.

### Web and cross-platform applications

Use semantic HTML and browser behavior first. Distinguish navigation links from action buttons, preserve browser Back and deep links, allow zoom, and test supported browsers. Adopt Apple’s emphasis on hierarchy and predictable behavior without pretending that CSS blur is native Liquid Glass.

Evaluate actual support before depending on new browser features or framework APIs. Provide a usable fallback or narrow the supported environment explicitly. Keep browser accessibility standards distinct from native point-based recommendations.

## Brand adaptation

Identify what makes the product recognizable: language, content, illustrative approach, distinctive tools, or other documented qualities. Preserve those strengths while adapting routine controls to the platform. Do not override familiar interaction merely to make every platform pixel-identical.

Check fonts, symbols, logos, illustrations, and media against their licenses before redistribution. This pack includes no permission to reuse Apple assets. Use existing licensed assets or appropriate alternatives when rights or platform restrictions are unclear.

## Output and gate

Deliver an adaptation matrix: invariant, current treatment, proposed platform treatment, source, fallback, test method, and unverified conditions. A pass requires appropriate input semantics, preserved tasks/data, supported APIs, and explicit limits for platforms that were not actually exercised.
