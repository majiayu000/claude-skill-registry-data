---
id: angular.i18n.angular-localize-v9-migration
name: Angular Localize v9 Migration
description: >
  Migrate Angular i18n apps to @angular/localize and $localize usage. Use when legacy i18n extraction or runtime localization needs to be aligned with Angular 9+ tooling.
stack:
  - Angular
  - TypeScript
category: i18n
status: stable
version: 0.10.0
owner: NgAutoPilot
triggers:
  - "@angular/localize"
  - $localize
  - Angular i18n
compatibility:
  angular:
    min: "9"
---

# Angular Localize v9 Migration

## Purpose

Migrate Angular i18n apps to `@angular/localize`.

## When to Use

- The app uses Angular i18n.

## When Not to Use

- The app does not use Angular i18n.

## Required Inputs

- translation files
- localize config

## Procedure

1. Review i18n usage.
2. Add localize support.
3. Validate extraction/builds.

## Do

- Keep translation behavior stable.

## Do Not

- Do not add localize when not needed.

## Review Checklist

- [ ] i18n is configured.
- [ ] Builds pass.

## Expected Output

1. Localize migration summary.

## Exit Criteria

- Localize support is explicit.
