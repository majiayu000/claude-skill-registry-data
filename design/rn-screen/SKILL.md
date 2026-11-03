---
name: rn-screen
description: Checklist for adding or changing a mobile screen or feature in the Expo app (route, feature hooks, API types, states, design tokens, accessibility, tests). Use for any UI work in mobile/.
argument-hint: "<screen or feature>"
---

# /rn-screen: add a mobile screen/feature

Follow `mobile/CLAUDE.md`.

1. **Data:** which endpoints? Make sure `src/api/schema.d.ts` is current (`npm run gen:api`). Add query keys and a hook in
   `src/features/<feature>/` (`useQuery` / `useInfiniteQuery` / `useMutation` with cache invalidation).
2. **Route:** add a thin file under `app/` that composes feature components. Choose the presentation (tab, stack push, or modal).
3. **States:** design loading (skeleton), empty (especially a new user with no runs), error (retry), and success.
4. **UI:** use `components/ui` primitives and theme tokens only. Dark-first. Use the Wrapped token set only inside the Wrapped experience.
5. **Formatting:** distances, paces, and durations go through `src/lib/format.ts` in the user's preferred units.
6. **Motion:** Reanimated on the UI thread. Respect `useReducedMotion`.
7. **Accessibility:** labels on icon buttons, a text summary for charts, and tap targets of at least 44pt.
8. **Tests:** unit tests for any new util. Use RNTL for state rendering, mocking at the fetch layer.
9. Run `npm run typecheck && npm run lint && npm test`, then tell the user exactly what to check in the simulator.
