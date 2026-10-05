---
name: ui-stress-test
description: Stress-test a running web interface with extreme content, narrow containers, zoom, and relevant locale variations, then reproduce and fix authorized layout defects. Use for deliberate robustness testing, not every styling change.
---

# UI stress test

Expose failures that ordinary sample content hides. Preserve the project's design system and intentional density. A changed wrap or horizontal scroll region is not automatically a defect.

## Establish a baseline

Identify the requested components, supported environments, relevant states, and existing browser/test tools. Capture the ordinary state before altering fixtures. Inspect tokens and component constraints so tests exercise the actual design rather than enforce arbitrary spacing rules.

Use isolated local fixtures or the project's test environment. Do not change real user records or persistent production content to create extremes. If only a screenshot or code is available, provide a static assessment and name the unavailable runtime checks.

## Select stress inputs

Read `assets/content-cases.json` for reusable text, quantity, and asset cases. Map them to actual component fields; the file is test input, not a universal product requirement. Choose cases supported by the product and likely to expose distinct risks. Preserve semantic validity when testing numeric ranges or required fields. Pseudo-localization is a layout probe, not verified translation.

Test the smallest supported viewport, a normal desktop, and widths immediately around observed layout transitions. Vary the component's container independently when it can appear in a pane or grid. Use actual browser zoom when available; reducing viewport width is not equivalent. Record unavailable zoom, font, locale, or device behavior explicitly.

Exercise one stress dimension at a time to diagnose causes, then combine relevant extremes such as a long error message in a narrow dialog. Include missing or delayed assets when they affect geometry. Restore fixtures after each case.

## Judge failures by use

Check whether essential content remains readable, actions remain reachable, focus stays visible, and the task can finish. Distinguish intended truncation with access to full content from lost information. Check nested scrolling and sticky regions before declaring overflow erroneous. A large document scroll width is a lead, not proof; inspect the rendered region.

Trace failures to intrinsic sizing, wrapping, fixed dimensions, source order, or container behavior. Prefer existing tokens and intrinsic fixes over extra breakpoints. Do not erase useful content or hide overflow merely to remove a scrollbar.

## Fix and verify

For review-only requests, report findings. For authorized fixes, reproduce each defect first, apply a coherent correction, and rerun the same case plus adjacent widths and affected shared components. Keep fixture values, viewport/container dimensions, state, steps, and before/after evidence with each finding.

Add regression coverage for meaningful repeatable failures using the project's existing tooling. Report observed failures and tested coverage, including unavailable checks. Do not claim robustness across locales or devices that were not exercised.
