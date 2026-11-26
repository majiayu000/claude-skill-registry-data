---
name: rtl-ltr-layout-control
description: Flip sidebar left/right based on RTL locale.
---
# RTL/LTR Layout Control for OpenAmer Desktop

## Description
Provides a central mechanism to dynamically flip the main sidebar placement based on the current locale (RTL vs LTR). The sidebar automatically moves to the right when an RTL language (e.g., Hebráisch) is active, while remaining on the left for LTR languages (Deutsch, English, etc.). This ensures consistent user experience across all 187 supported languages without manual configuration.

## Trigger
Use when you need to change the sidebar placement based on the current language direction, or when adding new RTL language support.

## Steps
1. **Detect RTL status**  
   ```ts
   const isRtl = getRuntimeI18nLocale() !== undefined && 
                 isRtlLocale(getRuntimeI18nLocale());
   ```
   - `isRtlLocale` checks the locale against `RTL_LOCALES` (e.g., `['ar','he','fa','ur','dv','ps','yi','ug','ks','sd']`).

2. **Compute target placement**  
   ```ts
   const targetFlipped = isRtl ? true : $panesFlipped.get();
   ```
   - If RTL, set `targetFlipped = true`; otherwise keep the current `targetFlipped` value.

3. **Update `$panesFlipped` store**  
   ```ts
   $panesFlipped.set(targetFlipped);
   ```
   - This ensures the layout tree subscription reacts and the sidebar flips correctly.

4. **Ensure sidebar toggle respects flipped state**  
   Modify `toggleSidebar` (or the relevant UI hook) to read `$isSidebarFlipped` (derived from `$panesFlipped`) before applying the state change.

5. **Validate**  
   - Switch language to Hebráisch → sidebar should move to the right.  
   - Switch back to Deutsch → sidebar returns to the left.  
   - Verify that existing layout presets (e.g., `quad`, `focus`) still respect the flipped state.

## Pitfalls
- **RTL locale detection**: Ensure `RTL_LOCALES` includes all languages that require right‑hand sidebar placement. Adding a new language requires updating this set.
- **Store synchronization**: The `$panesFlipped` store must be updated *after* the locale change takes effect; otherwise the sidebar may flip based on stale data.
- **Sidebar toggle logic**: If the toggle logic directly manipulates `$sidebarOpen` without considering `$isSidebarFlipped`, the sidebar may appear to stay on the wrong side. Adjust the toggle to read `$isSidebarFlipped` before applying the state change.
- **Layout presets**: Some layout presets (e.g., `quad`, `focus`) may override pane placement. Verify that `mirrorLayoutTree` and `setSplitWeights` respect `$panesFlipped`.

## References
- `src/store/layout.ts` – `$panesFlipped` store and subscription logic.
- `src/i18n/context.tsx` – `getRuntimeI18nLocale` and `RTL_LOCALES` definition.
- `src/components/pane-shell/tree/store.ts` – `mirrorLayoutTree` and `setSplitWeights` utilities.
- `src/components/pane-shell/tree/model.ts` – `split` and `mirrorTreeHorizontal` operations.
- `references/rtl-ltr-layout-control.md` – detailed implementation notes, pitfalls, and testing checklist.