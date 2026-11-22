---
name: physics
description: "Maps Puck physics and contact: Puck.Physics kernels, IContactField and its providers, the body step, sweeps, step-up and snap, rigid solver, tether, gravity, navigation, field lattices, motion."
---

# Physics

A map of the deterministic fixed-point kernels in `Puck.Physics` and the World
code that applies them to bodies. Two layers, and the split is the first thing
to get right:

- **The kernels** (`src/Puck.Physics`) return a correction, an acceleration or
  a route and decide nothing. They parse no document and know no body
  identity: contact geometry, the contact seam's analytic and field solvers,
  step-up and snap, the rigid solver, the tether, gravity solvers,
  navigation, field lattices, bounded perception and the motion-program core.
- **The host** (`src/Puck.World.Server`) owns body state and decides what a
  result means: `WorldBody` (one body's step, contacts, rigid, carry, tether,
  hold, sleep, refusal capture), `WorldPopulation` (the roster, body pairs,
  the rigid solve, wakes), `WorldColliderSet` and `WorldSolidField` (the two
  contact providers), `WorldEventFeed`. Authored rows become kernel input in
  `Puck.World.Schema` (`BodyMotionProgramFactory`, `BodyActionSpecFactory`,
  `WorldMotionTuningFactory`, the collider compiler).

[Physics kernels](../../../docs/reference/physics.md) is the kernel reference;
[the server README](../../../src/Puck.World.Server/README.md#the-entity-table-worldpopulationcs-worldbodycs)
documents the host side; the document fields (kits, `motion`, `collision`,
`navigation`, `fields`) are in the `puck-world` references
([motion](../puck-world/references/documents-motion.md),
[render facets](../puck-world/references/documents-render.md),
[state and navigation](../puck-world/references/documents-state.md)). When this
file and the code disagree, the code wins and this file is corrected in the
same change.

## Find the owner by what you need

| You need | Owner | Read |
|---|---|---|
| A body resolves its swept position against the world | the seam `IContactField` (`Resolve`, `ResolveSweep`, `TrySupportDistance`, `TryUp`), providers `WorldColliderSet` (analytic) and `WorldSolidField` (signed distance) | [contact seam](../../../docs/reference/physics.md#contact-and-rigid-body-kernels) |
| Every sweep that moves a body, entity-aware | `WorldBody.SweepContact`, the one dispatch; an `IEntityContactField` learns which body moves | [below](#the-body-step-and-the-seam-door) |
| Analytic colliders: spheres, boxes (rounded, chamfered, oriented), superellipsoids, cylinders, half-spaces | `FixedStaticCollider` (`TryGetPush`, `RoundedBox`, `ChamferedBox`, `Cylinder`), `FixedOrientedBox`, `FixedConvexContact` (GJK and EPA), `FixedStaticContactSolver` | [physics reference](../../../docs/reference/physics.md#contact-and-rigid-body-kernels) |
| A solid creation grows or shrinks with contact | `WorldColliderSet.RefreshAttached` reads compiled `sizeBy` bindings by arena ordinal; `WorldCreationSize.Of` clamps the sample; `TryRideDisplacement` carries the support's material point through `WorldBody.SweepContact`; `WorldSnapshot.SolidScales` publishes the sample | [rig size](../sdf-authoring/references/rig.md#drivers) |
| A carved, relieved or smoothly blended creation collides as drawn | field colliders (`WorldColliderSet.CollidesAsField`) with a `FixedFieldPartition` narrowing hard unions to their exact pieces | [sdf-authoring contact admission](../sdf-authoring/references/shapes.md#contact-admission) |
| Never tunnel, however fast or thin | `FixedFieldContactSolver.ResolveSweep` (certified sweep through `ICertifiedSweepQuery`); `FixedStaticContactSolver.ResolveSweep` (sliced analytic sweep); both refuse with `ContactRefusal` rather than wrap | [physics reference](../../../docs/reference/physics.md#contact-and-rigid-body-kernels) |
| Walk up a kerb; stick to a downhill slope | `FixedStepUp.TryStep` and `FixedStepUp.TrySnap` over one `IContactField.TrySupportDistance` query, driven by kit `motion.stepHeight` and `motion.groundSnap` | [motion](../puck-world/references/documents-motion.md) |
| Body-against-body depenetration and collision events | `FixedDynamicBodyContacts.TryCorrection`; events ask `FixedDynamicBodyContacts.Overlaps` (a positive push at zero margin, so a touching pair is neither), so an event and a contact never disagree; host pairs in `WorldPopulation.ResolveDynamicContacts` | [physics reference](../../../docs/reference/physics.md#contact-and-rigid-body-kernels) |
| Which bodies might touch: pairs in sweep order under a candidate budget, or the bodies near a box | `FixedSweepGrid` (X sweep crossed with a Y/Z grid, culling before it charges the budget), the one broadphase behind body contacts, `WorldEventFeed` discovery and the sleeping index (`WorldPopulation.NearbySleepingBodies`, `WakeSleepersNear`) | [physics reference](../../../docs/reference/physics.md#contact-and-rigid-body-kernels) |
| Remove a velocity's approach into a contact | `FixedVector3.LimitAlong` with the inward axis and a zero bound, shared by ordinary, field, tether and seam responses | `maths-usage` |
| Rigid bodies: impulses, friction, restitution, warm-started manifolds | `FixedRigidWorld` (the one solver), `FixedRigidContacts`, `FixedRigidManifold`, `FixedPairManifoldSlotTable`, `FixedTwoBodyKernel`; host side `WorldBody.Rigid.cs`, `WorldPopulation.Rigid.cs` | [the rigid solver](../../../docs/reference/physics.md#the-rigid-solver) |
| A rope that caps distance and keeps swing momentum | `FixedTetherConstraint` (`ResolveAnchor`, `Reel`); host `WorldBody.Tether.cs` | [tether](../../../docs/reference/physics.md#the-tether-constraint) |
| Climb a wall, grapple, pick an anchor | `FixedSurfaceQuery.TryNearest`, `TryNearestDirected`; `IContactField.TryHoldableSurfaceAlongDirection` | [physics reference](../../../docs/reference/physics.md#contact-and-rigid-body-kernels) |
| Gravity between many bodies | `GravitySolvers.Create` over `PairwiseGravitySolver` (the oracle), `FastMonopoleGravitySolver`, `AdaptiveFmmGravitySolver` | [choose a solver](../../../docs/reference/physics.md#choose-a-gravity-solver) |
| Routes, shared goal searches, off-grid checks | `NavigationRuntime` over `NavigationDomainInput`, proved with the body's own resolve and sweep against the static contact geometry (`WorldColliderSet.StaticField`, a `FixedStaticContactField`, or `WorldSolidField.StaticField`), each domain baked once on the thread pool (`NavigationDomainBake`, kept across rebuilds while its `IRegionalContactField.Within` part is equal); medium fields through `INavigationMediumField`; host `WorldPopulation.Navigation.cs` | [navigation](../../../docs/reference/physics.md#navigation-kernel-navigation) |
| One route across several domains (a building's levels and stairwells, the valley), to a cell or a place | `NavigationRuntime.FindRoute` with an `INavigationRouteGoal` (`NavigationCellGoal`, the host's `WorldNavigationPlaceGoal`), joined at aligned grids' shared cells; `world.navigation route` checks it against the contact field, `world.navigation map` draws a domain | [navigation](../../../docs/reference/physics.md#navigation-kernel-navigation) |
| A path a walker steers along: off walls, through a doorway's middle, cut to the corners it turns at | the route search's clearance cost (`RouteClearanceCells`, in `Domain.RouteSteps`), `NavigationRuntime.Straighten` over `Domain.IsStraightClear`, `NavigationRuntime.TryLocateNear` for a body against a wall; host `WorldDocumentNavigation.Plan`, the navigation one world document describes, compiled from that document alone, which the seat driver (`WorldSeatDriver`) plans over for the document its seat's client was delivered | [the benchmark plan](../../../docs/plans/benchmark.md#the-route-is-places-played-by-an-authored-seat-program-stage-4) |
| A door or swap that changes part of a domain's geometry without re-baking the domain | `Domain.TryBeginRebakeFrom` over `IRegionalContactField.TryDifference`: a worker copies the predecessor's bake and proves again only the cells and edges the changed colliders reach; `world.navigation` counts `rebaked=` | [physics reference](../../../docs/reference/physics.md#navigation-kernel-navigation) |
| Evolving scalar fields (water, heat, snow) and their solids | `FieldLattice` (reactions, `IFieldLatticeHost`), `FieldLatticeSolid`, `UnionField`, ordering by `ReadWriteHazard.Conflicts` | [field lattice](../../../docs/reference/physics.md#field-lattice-fields) |
| Steering samples and flocks | `FixedSpatialNeighborhood` (bounded, never a broadphase), `FixedFlockSteering` | [perception](../../../docs/reference/physics.md#bounded-local-perception) |
| How a body moves under its kit: drive, shaping, holds, actions | `CompiledBodyMotionProgram`, `BodyMotionOp`, `FixedMotionTuning` (Schema; gate-bearing host records), executed by `WorldBody` phases | [motion core](../../../docs/reference/physics.md#the-motion-program-core-motion) |
| Sleep, wake on a moved carrier or lattice, rest | `WorldBody.Sleep.cs` (the authored idle floor; the standard's is `idleSleepAfter` in `worlds/standard/kits.puck`), `WorldPopulation.ObserveContactFieldChange`, which settles parked rigid islands and idle kit sleepers (`SettleIdleSleepers`) by the change's box, `WorldPopulation.ContactFieldVersion` | [server README](../../../src/Puck.World.Server/README.md#the-entity-table-worldpopulationcs-worldbodycs) |

## The body step and the seam door

- `WorldPopulation` steps bodies one at a time; `WorldBody.Advance` runs the
  motion program's phases, then `ResolveProgramContacts` sweeps the step
  through the field. A rigid kit only prepares its step and joins the
  population's one `FixedRigidWorld` solve; carried and tethered bodies have
  their own files beside it.
- **One door for every moving sweep.** `WorldBody.SweepContact` is the
  dispatch every sweep that moves a body goes through; an
  `IEntityContactField` (today `WorldAdjacencyContactField`) learns which
  local body moves, so a neighbour's answer is admitted against that body. A
  probe that moves no body calls the field directly and names none. A new
  path that moves a body calls `SweepContact` or the `BodyContactStep` bound to
  it, never `IContactField.ResolveSweep` directly.
- **A refused sweep is a full block.** `ContactRefusal` means the body keeps
  the pose it started the tick with. `WorldBody.SweepRefusal.cs` captures
  everything the step writes (`WorldBodyTransferState`,
  `WorldBodyIntegrationResidue`, pose and contact facts) before the step and
  restores it, and a walking body's emitted effects are withdrawn. A body
  refused this tick (`WorldBody.SweepRefusedThisTick`) is static to its pair
  partners, unpulled by a tether and never corrects a carrier until
  `WorldPopulation.CompleteStep`. A field added to either captured record is
  covered with no change.
- **Only a proven contact corrects a carrier.** A sweep that held its body for
  want of proof reports `ContactResolution.Unproved` and hands the carrier
  nothing.
- A `timedMove` action uses `FixedTimedMove.Sample` for both its yaw and its
  travel. `WorldBody.ProposeTimedMove` updates the proposal before the contact
  phase, and the refused-step snapshot includes the move's progress.
  [Authoring](../puck-world/references/documents-motion.md#timed-moves)
- **Two snaps share one answer** where the body has not moved between them
  (`BodySupportMemo`, keyed by field, volume derivation, start, orientation, up
  and reach).
- A kit change whose collider would embed the body steps it out along up or
  world X/Z, never down (`WorldBody.EscapeEmbedding`).

## Contracts that bite

- **Determinism.** Every kernel is fixed point over `Puck.Maths`; mixed-scale
  products and wide roundings go through `FusedArithmetic` and its siblings,
  so a kernel rounds the way every other consumer does (`maths-usage`). A
  deliberate correction moves body poses and state hashes; judge it by the
  new answer's exactness, not by matching old bytes (AGENTS.md rule 4).
- **Kernels decide nothing.** Walkability, authority, waking and admission
  are the caller's. A kernel returning a correction must not mutate a body.
- **One mechanism per question.** One rigid solver, one body broadphase
  (`FixedSweepGrid`), one static-collider grid (`FixedColliderGrid`, behind
  `FixedStaticContactField` and so `WorldColliderSet`), one round-core rule
  (`TryRoundPush`, behind both static spheres and dynamic round pairs), one
  box geometry owner (`FixedOrientedBox`), one approach-removal
  (`FixedVector3.LimitAlong`), one overlap sense for events and contacts.
  Writing a second is a defect; extend the one that exists.
- **Perception is not a broadphase.** `FixedSpatialNeighborhood` drops
  candidates when its attention budget binds; a contact solver may not.
- **Work is counted, not timed.** `physics.contact`
  (`FixedStaticContactWork`), `physics.sweep` (`FixedContactSweepWork`) and
  `physics.bodies` are deterministic work sources; read them with
  `world.counters` before and after a change. `physics.contact.field-unproved`
  counts every field solve that proved nothing, the ground snap's bracket
  probes included, so a body standing at an unprovable feature adds several a
  tick and the total follows that body's path: a change that moves one pose by
  a raw can move a sweep's total by thousands. Before calling such a delta a
  bounds regression, run the same poses through both builds and compare each
  outcome and box interval ([the crease item](../../../docs/plans/open-items.md#certified-field-contact)).
- **Scale reaches every contact query.** A body's `Scale` multiplies its
  collider volumes for world contact, body pairs, events, the adjacency
  sweep's local side and rigid probing alike.
- **Carried rigid contacts use the solve.** `TwoBodyHandle` makes a carried body
  static with its carrier's velocity. Its owned pair manifolds still join the
  solve; it never joins the integration roster. Carry's positional pair split
  handles only locomotion neighbours.
- **Contact softness is authored.** `collision.bodyContacts` supplies
  `contactHertz`, `contactDampingRatio` and `contactSpeed`; the standard package
  chooses their values. `RigidContactPolicy` compiles them once, and a retune
  rebuilds the solver. The authored rolling lever also bounds torsion as the
  contact patch radius; neither row resists without normal load.
- **Solid size reads the current authority.** `WorldTick` passes its live definition to
  `WorldPopulation.AdvanceSimulated` for `WorldColliderSet.RefreshAttached` to sample.
  The geometry compiler's retained definition can still name a retired arena after a
  checkpoint restore. Restore keeps the captured sample; the next tick reads the restored arena.
- **Workspaces are reused and not thread-safe.** The hierarchical gravity
  solvers and navigation domains allocate once and keep their arrays.
- **Moving solids reach gameplay queries too.** `WorldSolidField` queries the
  static program and the contact owner's live roots through `FieldWorldQuery`,
  which uses the existing SDF march. Grip reads the sampled row's own policy.
  Moving fields compile without world-space partitions at every scale, including
  one. A solid-consumer rebuild retains unchanged roots' last samples.
- **A sampled size is a state disclosure.** Session and federation deliveries
  filter it with `WorldSolidScaleDisclosure` through the source cell's live
  `WorldRecipientView`; a cached binding never caches read permission.

## Where each contract is enforced

| Contract | Enforced by |
|---|---|
| A body never moves through space no sweep proved clear | `FixedFieldContactSolver.ResolveSweep` and `FixedStaticContactSolver.ResolveSweep`: budget exhaustion keeps the proved prefix, an unrepresentable step refuses whole |
| A kit capsule fits its sweep ceiling; no volume quantizes to a point | collider validation (`CapsuleCoreFitsSweep`, `VolumeCoreSweeps`) at load |
| A refused step changes nothing | `WorldBody.SweepRefusal.cs`'s capture of whole records, restored on refusal |
| A neighbour's contact answer is admitted against the moving body | `WorldBody.SweepContact` dispatching to `IEntityContactField` |
| A lattice's solid stays inside the carrier | `FieldLatticeSolid.CellFits` at world validation; the constructor throws otherwise |
| Field-program dependency edges mean the same on both sides | `ReadWriteHazard.Conflicts`, called by the lattice and the Schema compiler |
| Same input, same poses | the population's checkpoint codecs and `puck test --reproduce` |

A field row’s `simulationOnly` flag keeps the height scale in `FieldLattice.StepFlow` and excludes the row from body contact and medium queries. Presentation checks `WorldFieldRow.DrawsSurface` before it subscribes to the row or allocates a height field.

## Open gaps

- **The adjacency sweep's remote side reads a neighbour's unscaled collider**:
  the delivered snapshot carries no per-entity `Scale` yet.
- **No query crosses a portal door.** Line of sight (`WorldPopulation.HasLineOfSight`),
  a tether's aim, a hold's reach, body pairs and routes all stop at the glass,
  and a door that moves is not swept. `WorldPortalHoleContactField` only takes
  back the push of the wall behind an opening.
  [Portals in play](../../../docs/plans/portals-in-play.md#2-queries-through-doors)
  designs the one layer that carries every ray through, composed where the
  opening and seam layers are.
- **Approximations the reference names.** Rounded or chamfered circular rims
  use a contained cylinder core with a reported inward bound (the fix is an
  exact rim contact); a superellipsoid above exponent two and the carved
  primitives stay bounded approximations in the analytic provider (an
  exponent-2 collider measures its exact distance through
  `FixedEllipsoidProjection`, and a spheroid is the field's own surface); a
  triaxial ellipsoid's gauge field dilates past its collider's true margined
  surface along its long axes (the field side's fix is the true distance
  under a non-uniform scale); tilted box-in-cylinder edges are conservative.
- Packets: [certified field contact](../../../docs/plans/open-items.md#certified-field-contact),
  [collision versus drawn mesh](../../../docs/plans/open-items.md#collision-versus-drawn-mesh),
  [water](../../../docs/plans/open-items.md#water) and
  [the Moth's motion](../../../docs/plans/open-items.md#dual-stick-play-and-the-moths-motion).

## Verify

- Kernel laws: `tests/Puck.Physics.Tests` (gravity against the pairwise oracle,
  contact kernels, sweeps, the rigid solver's mechanism and sabotage cases,
  navigation, lattices, neighborhoods), filtered to the class you touched.
  Body integration laws are in `tests/Puck.World.Server.Tests`.
- Scenarios in the debug world: `puck test worlds/debug/hall-tests.puck --jobs 1`
  (stairs, slabs, the lift), `noclip-tests`, `suit-tests`, the `water-*-tests`,
  `meadow-tests`; add `--reproduce` for anything that moves a pose.
- Live read-backs over stdin: `body.where` (pose, support,
  `sweep=refused(...)`, `asleep=`), `body.motion` (effective `stepHeight=`),
  `world.kits`, `world.collision.status`, `world.fields`, `world.counters
  physics.contact`, `physics.sweep` and `physics.bodies`. `puck creation stats`
  builds a creation's contact field offline (`sdf-authoring`).
- The reference pages' canary names (`thin-wall-sweep` and others) are
  quarantined under `experimental/` with the other canaries.

## Look-alikes

- The chase camera's clearance sweeps and an effector's surface probe query
  the rendered field for presentation (`WorldFieldAnswer`, `puck-world`), not
  the contact seam.
- `FixedSpatialNeighborhood` is perception; the body-pair broadphase is
  `FixedSweepGrid`, budgeted by `collision.bodyContacts` for contacts and by
  `collision.events` for events.
- Binary heaps (navigation's `NodeHeap`, the board path cost, the
  neighbourhood's top-k) all run on `Puck.Abstractions.Collections.BinaryHeap`;
  a new priority queue uses it with a struct `IComparer<T>`.
- `collision.events` budgets proximity events; `collision.bodyContacts`
  budgets physical depenetration. They are separate limits.

## Route adjacent work

| Skill | Route there for |
|---|---|
| `puck-world` | Kit, `motion`, `collision`, `navigation` and `fields` document fields, the tick order, running a World. |
| `sdf-authoring` | Which shapes a creation's contact admits, contact tuning, `puck creation stats` and `creation.shape`. |
| `maths-usage` | Fixed-point vectors, rate accumulators, rounding and the certified sweep's field queries. |
| `maths-laws` | Law coverage for a changed `Puck.Maths` member a kernel uses. |
| `state` | Rules that read body facts or write body targets, and the rule-gate interpreter. |
| `rendering` | The SDF evaluator and mesh the drawn surface comes from. |
| `verification` | Leases, the private CLI copy, flaky versus failing scenarios. |
