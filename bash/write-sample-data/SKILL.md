---
name: write-sample-data
description: Fill an Endless Studios view's system.user and system.sample (store state, store handlers and GraphQL responses) so the copied app components render the intended role, status and permission state. Use when a view or named state needs a particular kind of signed-in user (learner, mentor, program, cohort or institution admin, a youth without consent, a restricted partner, a disabled account), needs app data such as programs, cohorts, tasks, games, posts, notifications or events, when a copied component renders empty or wrong, or when the console reports an [Endless Studios] gap.
---

# Write sample data

A view's `export const system = { user, sample: { state, getters, mutations, actions, queries } }` is everything the app around a copied component knows. The [system README](../../README.md#choosing-a-screens-locale-user-and-samples) is the contract for the options; [data shapes](references/data-shapes.md) records how the stand-ins in `runtime/` answer and what the app receives. A *gap* is an `[Endless Studios]` warning in the console: the stand-in found no sample and rendered empty. A wrong sample is silent, so a clean console is necessary, not sufficient.

Give each named state the sample its experience needs, and every value the *response shape*: what the query returns to the component, keyed the way the component reads it, never the schema's type layout.

## Steps

1. **Collect the gaps.** Load the view and each named state at its own address, reloading between them: a gap is reported once per page, so one already shown for another state stays silent. Open every popover, tab and modal the state shows, because a component queries only when it mounts: the shell's notifications popover asks for `NOTIFICATIONS_LIST` only when opened. Record each warning:

   | Console says | Add |
   | --- | --- |
   | `query "X" has no sample response` | `sample.queries.X` |
   | `mutation "X" has no sample response` | `sample.queries.X` (mutations share the map) |
   | `store action "x" is not stood in` | `sample.actions.x` |
   | `store mutation "X" is not stood in` | `sample.mutations.X` |
   | `unknown sample user …` | a preset name, a user object or `null` (step 4) |
   | `missing translation "key"` | not a sample gap: the key is missing from the copied locale files |
   | `subscriptions are not stood in`, `GraphQLClient.request is not stood in` | nothing a sample answers; report it as a runtime follow-up |

   Lines logged with `console.info` (navigation, login requested, error toast) are not gaps. Also note each copied component that renders empty or wrong without a gap.

   Done when every state has its list of gaps and silent failures.

2. **Read each operation in the copied source.** Find the `gql` document by operation name in the view or the system's `studios/` and `runtime/` folders (`grep -rn "query X\b\|mutation X\b" src/systems/endless-studios`). Note its root fields and aliases, every nested field the template or script reads, and its options: `auth` (`required` by default, so a signed-out state gets the default; `anonymous` is the reverse), `flattenData`, `transform`, `default`, and whether `useStreamingGraphQLQuery` runs it. For data a component takes as props, read its `defineProps`. [Data shapes](references/data-shapes.md#copied-components) lists what each copied component reads at the copy's revision.

   Check field names, nullability and enum values against the live schema rather than any copy of it, with an account that can read the private app repository:

   ```sh
   gh api -H 'Accept: application/vnd.github.raw' 'repos/Endless-Game-Making-Studio/studio/contents/backend/gql-schema.graphql?ref=dev'
   ```

   Use `?ref=<revision>` from [studios/README.md](../../studios/README.md) for the schema the copied components were written against. Without access, use the references here and say so in the report.

   Done when every gap and silent failure has an operation name, its root response keys and the fields read.

3. **Shape each response.** Write `sample.queries[Operation]` in response shape, as the query's `data`: keyed by alias where the document has one, with only the selected fields, lists as arrays, and `__typename` on union results. Give a function of the variables when the answer depends on them. A mutation's sample is its return value: `Void` is `null`. Store state merges over the app's initial state; supply the actions the components dispatch. The rules and common shapes are in [data shapes](references/data-shapes.md).

   Keep a sample the view alone uses as constants in its regular `<script>`, and one several views share in a helper folder such as `_data/`. A state's `sample` replaces the view's whole, so build it from the view's (`{ ...sample, queries: { ...sample.queries, X: … } }`), as [build-prototype](../../../../modules/prototypes/skills/build-prototype/SKILL.md) step 10 describes.

   Done when each sample's top-level keys equal the operation's root response keys and every field the component reads is present, null only where the state means it.

4. **Choose the user.** Use a preset (`'learner'`, `'mentor'`, `'admin'`) only when the state depends on nothing they lack; otherwise paste the role's object from [users by role](references/users-by-role.md), which says what the presets lack. Use `null` for signed out: required queries then resolve to their defaults and streaming lists stay empty. What each role may do is in [Platform model](../../context/platform-model.md).

   Done when each state's user gives the `$auth` checks the screen branches on (`isAdmin`, `isCohortAdmin`, `isAdult`…) and its age category, consent, restricted-partner and disabled fields match the state.

5. **Check statuses and permissions.** Compare every status, kind, phase and permission value with [state enums](references/state-enums.md), or the live schema, on the field that takes it: `ProgramStatus` is `inprogress` while `CohortStatus` is `in_progress`, and `permissions.publish` is the one boolean. Make the user and each entity's `permissions` tell one story: a youth without consent sees `parental_consent_required` wherever the schema gives it, a restricted partner `restricted_partner`, a signed-out visitor `not_authenticated` or `not_member`.

   Done when no value falls outside its enum and no permission contradicts the user.

6. **Make it believable.** Take people, programs, cohorts and games from the [demo cast](references/demo-cast.md) and follow its content rules: real words instead of placeholders, uneven counts and reactions, timestamps a few days to weeks old, and youth usernames in the Adjective+Animal+Number pattern. Text arrives already translated, so a Spanish state's sample is in Spanish; product wording follows [Voice and tone](../../context/voice-and-tone.md).

   Done when no sample holds lorem ipsum, "Test", or numbered filler such as "Program 1".

7. **Verify.** Reload each named state at its own address, open its overlays, read the console and look at the screen. If the preview errors, follow build-prototype step 14.

## Done

Every named state renders the experience it names, its console shows no `[Endless Studios]` gaps, and every status, kind and permission value matches the schema. Report each state's user and sampled operations, any gap no sample can answer, and any value you could not check against the live schema.
