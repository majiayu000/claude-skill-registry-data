---
name: new-arch-check
description: Audit dependencies for New Architecture compatibility and maintenance status. Use when the user asks whether their libraries support the New Architecture or which dependencies are risky.
---

Audit the project's dependencies for New Architecture readiness and abandonment risk.

1. Read `package.json` and collect dependencies that ship native code or are React Native specific. Skip pure-JS utility packages; they are not the risk.

2. Run `npx expo-doctor@latest` and capture what it flags. It checks packages against React Native Directory metadata and catches known-incompatible and unmaintained ones. It needs the expo package; in a bare React Native project without it, skip to step 3 and query the directory for every native dependency.

3. For each remaining native dependency not covered by doctor output, query React Native Directory:
   `https://reactnative.directory/api/libraries?search=<package-name>`
   Note the New Architecture flag and the last-release recency. A package missing from the directory is not automatically bad, but combined with an old last-publish date it goes in the risk column.

4. Produce a single table: package, version, New Architecture status (supported / interop-expected / unsupported / unknown), last release age, and verdict. Three verdicts only:
   - keep: maintained and compatible
   - watch: works today via interop or unclear, has a pulse; recheck at the next SDK upgrade
   - replace: abandoned or incompatible; name the standard replacement (the new-architecture skill lists the usual swaps)

5. End with the two or three highest-risk items and one concrete next step for each. No generic advice; name packages and replacements.
