---
name: apeiron-game-code
description: Write Apeiron Engine gameplay in Rust — scaffold a game crate, register components/resources/systems through runtime::Plugin, expose Rust functions to Blueprint with #[ngine::node], and keep the simulation deterministic. Use when gameplay needs real code rather than editor authoring, when creating a new Apeiron game or plugin crate, when adding a component or system, or when asked how to extend Apeiron without editing the engine.
license: MIT OR Apache-2.0
compatibility: Requires a Rust toolchain and, today, an Apeiron Engine SOURCE checkout — the `ngine` facade is not published (its crate is publish = false), so a game crate depends on it by path. Also needs the `ngine` CLI plus an editor or server to run it. A checkout-free path is planned; until then the apeiron-editor skill is the route that needs no source.
---

# Write a game in Rust

A game is **its own crate** with exactly one dependency on `ngine`, the engine's semver'd facade.
You never edit engine code. The engine discovers your game from a manifest and composes it.

This is the code tier. The other tier — authoring scenes, materials and terrain in the running
editor — is the `apeiron-editor` skill. Most games need both; reach for code when you need a
component, a system, or behaviour the editor's nodes cannot express.

## Scaffold

**A project's game code lives IN the project** — `<Project>/Source/<name>/`, like an Unreal
project's `Source/`. This is the path to use for a game:

```bash
ngine new-game --project "<Project dir>" my-game   # -> <Project>/Source/my-game/
```

It is a BINARY crate whose whole `main` is `ngine_host::main!(game)`: building it produces the
project's own editor. In the running editor, **Build Output → Build Project Code** (`build.run`)
builds and installs it, and **Relaunch with new code** (`build.relaunch`) switches to it.
**Start Live Coding** (`build.live_start`) goes further: every save is patched into the running
editor — function bodies change on the next tick, no restart (a new component, a new system or a
changed struct needs the live session ended — close the dx console — then Build + Relaunch from
the normal editor). Poll `build.status` to see a patch land.

The crate's `[features]` are Unreal's targets: `editor` (the default, with `server`) is the
project's editor; `player` is the shipped game — no editor, no agent door. `ngine export
<Project>` builds THIS crate `--release --no-default-features --features player,server`, so the
exported `<Name>.exe` is your game, and `<Name>.exe --server --bundle <Name>.ngpkg` is its
dedicated server. Its `build.rs` calls `build_info::build_script::link_host_binary()` — the
engine's link rules; keep that line if you add your own build steps.

The other shape, for a self-contained game repo or tool (games never live inside the engine repo):

```bash
ngine new-game my-game                # a self-contained repo in ./my-game/
```

It produces this shape:

```
my-game/
  Cargo.toml     # ONE dependency: ngine
  game.toml      # the game's CODE IDENTITY — how the engine finds it
  src/lib.rs     # a component + a resource + a system, wired through Plugin
```

Then register it with the editor and the dedicated server (point it at the directory that holds your
games — `--dir=`, or `NGINE_GAMES_DIR`):

```bash
ngine games --dir=<parent of my-game> --codegen
```

Bare `--codegen` writes the game registry inside an engine source checkout, so run it from that
checkout's root; anywhere else (for example with an installed `ngine`), name the outputs with
`--codegen=FILE --cargo=FILE`. If the target directory does not exist, or there is no games
directory, it exits non-zero and generates nothing — it never reports success over an empty registry.

That scans every `game.toml` and writes the single registry both hosts read. **No engine file is
edited by hand** — that is the whole contract, and there is a test asserting the editor and the
registry cannot drift.

## `game.toml` — the two keys that matter

```toml
name = "my-game"        # the game's id: the crate name, and what a project selects
version = "0.1.0"
engine = "0.1"
setup = "setup"         # pub fn setup(&mut World) — places your game's DATA
plugin = "MyGame"       # pub struct MyGame; impl Plugin — your COMPONENTS, RESOURCES and SYSTEMS
banner = "My Game"
```

The division of labour between those two is the whole architecture in two lines:

- **`setup`** runs once when the world boots — in editor-Play, in the shipped player and on the
  dedicated server, the same function in all three, so they cannot disagree about what your game
  is. It spawns entities.
- **`plugin`** supplies the machinery that acts on them: components, resources, systems, Blueprint
  nodes.

Omit `plugin` for a data-only game that owns no systems. Omit `setup` and you have no world.

Two optional keys matter only on the dedicated server, per connecting client:

```toml
team = "pick_team"      # pub fn pick_team(&World, u64) -> u8 — asked BEFORE the pawn spawns
join = "equip_player"   # pub fn equip_player(&mut World, Entity) — runs right after it spawns
```

`team` is Unreal's team-on-PlayerState-before-ChoosePlayerStart: a non-zero answer picks a
`PlayerStart` of that team and is written onto the pawn as `gameplay::Team`. Without it every client
is team 0 and may take any start. `join` equips your per-player archetype on the fresh pawn.

A project selects its game in **Project Settings › Project › Game** (the `Project/Game` class, saved
with the project's settings; an agent sets it with
`settings.set {class:"Project/Game", field:"game", value:"my-game"}`). The project's own name is only
a label, so renaming it never unbinds the game. `NGINE_GAME=my-game` overrides the setting on every
host, and is how the dedicated server picks a game when it boots none from a bundle.

## The Plugin

```rust
use ngine::prelude::*;

/// A component. `Reflect` is what makes it visible to the editor.
#[derive(Clone, Copy, Debug, Default, reflect::Reflect)]
pub struct Orbit {
    pub radius: f32,
    pub speed: f32,
}

/// A system: a plain `fn(&mut World)`.
pub fn orbit_system(world: &mut World) {
    let Some(t) = world.resource::<gameplay::Time>().map(|time| time.elapsed) else {
        return;
    };
    let ents: Vec<(Entity, Orbit)> =
        world.query::<(Entity, &Orbit)>().map(|(e, o)| (e, *o)).collect();
    for (e, o) in ents {
        if let Some(tr) = world.get_mut::<Transform>(e) {
            tr.translation.x = o.radius as f64 * (t * o.speed as f64).cos();
            tr.translation.z = o.radius as f64 * (t * o.speed as f64).sin();
        }
    }
}

pub struct MyGame;

impl Plugin for MyGame {
    /// Name it. This is the Schedule panel's attribution column — how anyone playing a modded
    /// build finds out whose system is costing the tick. Defaults to "plugin" if you skip it.
    fn name(&self) -> &'static str {
        "my-game"
    }

    fn build(&self, app: &mut AppBuilder) {
        app.register_component::<Orbit>("Orbit")
            .insert_resource(MyGameConfig::default())
            .add_named(Phase::Gameplay, "orbit_system", orbit_system);
    }
}
```

### What one `register_component` call buys you

Registering a component makes it, with no further work:

- **spawnable** — it appears in the editor's Add Component list and in `scene.add_component`
- **inspectable** — editable in the Details panel, field by field
- **serialized** — saved into and restored from the scene file
- **readable from Blueprint** — get/set its fields in a graph

One call, one file — your own. There is no engine-side registry to edit.

### Systems and phases

`add_named(phase, "name", f)` — always the named door. `add_system` registers the system as
`<unnamed>`, which makes it anonymous in the Schedule panel and stops the editor badging a compile
error onto it. Naming costs one string.

Phases run in this fixed order, and your systems append to the end of their phase:

`Input` → `Brains` → `Movement` → `Gameplay` → `Rules` → `State` → `Transform`

Most gameplay belongs in `Gameplay`. Put anything that reads input in `Input`, AI decisions in
`Brains`, and win/lose evaluation in `Rules`.

**Where a system runs in multiplayer.** `add_named` systems run only where the simulation is
authoritative (the server, single-player, editor Play). A system that should ALSO run on a
player's machine connected to a server — an anim driver, a cosmetic effect, HUD logic — registers
with `add_named_everywhere(phase, "name", f)`: it then ticks in the client's presentation tick
too. On a client it must read replicated or local state only and gate any world change on
`gameplay::is_authority(world, entity)` (Unreal's `HasAuthority()`); `gameplay::NetMode::of(world)`
says what the world is (`Standalone`, `DedicatedServer`, `ListenServer`, `Client`). Blueprint has
`Net/HasAuthority` / `Net/IsServer`; a Rhai script has `has_authority()` / `is_server()`.

Replication bandwidth is authored per entity, as on Unreal's `AActor`: `gameplay::NetRelevancy`
(who receives it) and `gameplay::NetUpdatePolicy { update_hz, min_update_hz, adaptive, priority,
dormancy, dormant_beyond }` (how often, how urgently, whether). A dormant entity costs nothing per
tick until you flush it after changing it: `gameplay::flush_net_dormancy(world, e)` /
`gameplay::set_net_dormancy(world, e, NetDormancy::DormantAll)` / `gameplay::force_net_update(world,
e)` in Rust, `Net/FlushNetDormancy` / `Net/SetNetDormancy` / `Net/ForceNetUpdate` in Blueprint,
`flush_net_dormancy()` / `set_net_dormancy("dormant_all")` / `force_net_update()` in Rhai.
To see what each entity, component and field costs on the wire, open Window > Network Profiler in
Play, or ask the editor agent for `net.profile {top:10}`.

A declared replicated component's floats travel at 1/1024 unless you choose otherwise, like
Unreal's `FVector_NetQuantize*`: `schema.component::<Stats>("Stats").quantize("Stats",
net::Quantum::NET_QUANTIZE)` (1 cm), or `quantize_leaf("Stats", "hp", net::Quantum::Exact)` for a
value a client must reproduce bit for bit.

An entity reference inside a replicated component (a `scene::EntityRef` field, list or option)
arrives as the CLIENT's entity — the engine maps it through each side's NetIds, like Unreal's
PackageMap, and a reference to something the client has not received yet resolves the moment it
arrives. A child's `scene::Parent` replicates the same way.

A replicated component travels PER MEMBER: change one field of a 20-field component and one field
goes out. For a list whose items come and go (an inventory, a buff list), use
`gameplay::NetArray<Item>` (Unreal's FastArray): `push` returns a stable `NetArrayId`; one item's
change costs the same whether the list holds 10 items or 200; a client hears each add / change /
remove — `RepNotify::item` in Rust, `Event/OnNetArrayItem` in Blueprint, `fn
on_net_array_item(ev)` in Rhai.

Much multiplayer logic needs no Rust at all, the way it needs none in Unreal. A Blueprint variable
replicates when its `Variable/Set` says `Replicated` or `RepNotify` (optionally owner-only), and
only then. RPCs carry named arguments from either tier: the `Net/*` nodes' argument pins, or
`send_to_server(name, #{..})` in Rhai. Either tier receives them (`Event/OnNetEvent` +
`Value/EventArg`, or `fn on_net_event(name, args)`). The server VALIDATES a client's RPC before
it runs (Unreal's `WithValidation`): `gameplay::RpcValidators::install(world).register("chat/say",
|world, call| ...)` in Rust, an `Event/OnValidateNetEvent("chat/say")` handler that `return`s a
bool in Blueprint, or `fn validate_chat_say(args) { ... }` returning a bool in Rhai. A refusal
drops the RPC and strikes the sender; enough strikes kick it. A native `gameplay::GameMode`'s `post_login`
/ `logout` / `on_match_state_set` also raise `Event/OnPostLogin` / `OnLogout` / `OnSetMatchState`
(Rhai `on_post_login` / `on_logout` / `on_set_match_state`). So the Rust mode keeps the decisions,
and authored logic reacts to them. Reach the mode through `gameplay::game_mode_of(world)`, which
is what raises those events.

**Sessions — letting players find each other** (Unreal's Create / Find / Join / Destroy Session).
`gameplay::request_session(world, SessionOp::Create(SessionSettings { name, max_players, lan,
.. }), requester)` makes the game a listen server and advertises it — on the LAN through the
engine's built-in beacon by default, or through the project's online backend. `SessionOp::Find`
searches, `SessionOp::Join(result)` joins a row (the address is opaque: Steam's `steam://<steamid>`
joins over Valve's relay the same way), `SessionOp::Destroy` ends it, and
`SessionOp::InviteFriends` opens the platform's invite overlay (Steam's) for the current session.
The host answers with `gameplay::deliver_session_outcome`: a Blueprint's latent `Session/*` node
resumes on On Success / On Failure, and the requesting entity receives `Event/OnSessionComplete`
(Rhai `fn on_session_complete(ev)` with `ev.op`, `ev.success`, `ev.error`, `ev.results`). A joined
session that ends against the player's will (refused at login, kicked, banned, timed out, the link
lost) answers the join's requester once more with `op` `"network_failure"` and `error`
`"<code>: <reason>"` — `gameplay::NetworkFailure` (Unreal's `ENetworkFailure`) names the codes. The same
verbs exist as Rhai `host_session` / `find_sessions` / `join_session` / `destroy_session`. A
dedicated server answers every session verb with a failure (it is advertised by its operator, not
its gameplay). For a game with no front end of its own, the project setting `Project/Game`
`multiplayer_menu: true` (on in the `third_person` template) gives the player build the engine's
main menu (Play Solo / Host Game / Join Game / Server Browser / Join by Address / Quit), a Host Game
page (name, max players, LAN / online), Connecting and connection-failure screens, and a Host /
Leave row in its pause menu; `--listen` / `NGINE_LISTEN` still host from the command line.
Play Solo is a standalone world: the local player is logged in (`GameMode::post_login`) and, when
the match starts, spawned from `Ruleset::default_pawn` like a server's players — a mode whose
`ready_to_start_match` waits for 2 players therefore never starts solo unless it checks
`gameplay::NetMode::of(world) == NetMode::Standalone`. `Project/Game` `background_fps` (default
30, 0 = off) caps only the RENDER of an unfocused player window; the sim and net keep their rate.

**Replays** (Unreal's `StartRecordingReplay` / `StopRecordingReplay` / `PlayReplay`).
`gameplay::replay::request_replay(world, ReplayOp::StartRecording { name } | StopRecording |
Play { name })` — or Blueprint `Replay/StartRecording` / `StopRecording` / `PlayReplay`, Rhai
`start_recording(name)` / `stop_recording()` / `play_replay(name)`. A server (dedicated or listen)
records its replication stream plus checkpoints to a `.ngreplay` (`NGINE_REPLAY_DIR`, default
`Saved/Replays`; `NGINE_RECORD_REPLAY` / `-record` records a dedicated server from boot); the editor
or a player plays it back as a spectator client (pause, 0.25x–4x, scrub, follow a player). A
dedicated server refuses Play. Owner-only replicated fields are not recorded (the recording is a
spectator's view). Format: `ngine::gameplay::replay` docs.

**Steam and achievements.** The online backend is the project setting `Project/OnlineServices`
`bundle` — `local`, `lan`, `steam` or `none` — plus `steam_app_id` (480, Valve's test app, until
the game has its own). On `steam` every service above runs on Steamworks (lobbies, rich presence,
overlay invites, Steam Cloud) with no game-code change; if Steam cannot start the project runs on
LAN and `services.state` says why. Achievements and stats are the sixth service:
`gameplay::request_achievement(world, AchievementOp::Unlock { id } | Progress { id, current, max }
| SetStat { stat, value }, requester)` — or the `achievements` field of the `ngine::services::GameServices`
resource directly — answered like a session verb (`gameplay::deliver_achievement_outcome`:
the latent `Achievements/Unlock` / `WriteProgress` / `SetStat` node resumes, the entity receives
`Event/OnAchievementComplete`, Rhai `fn on_achievement_complete(ev)`); Rhai has
`unlock_achievement` / `achievement_progress` / `set_player_stat` / `invite_friends`. Write
achievements on the player's own process — a server answers every write with a failure. Setup,
shipping (`steam_api64.dll` beside the exe, `steam_appid.txt` in development builds only) and the
two-account test: `docs/ONLINE_STEAM.md`.

**Voice chat.** Built in, no SDK: the project setting `Project/Voice` (`enabled`, `mode`
push_to_talk / open_mic, `ptt_key`, `vad_threshold_db`, `channel` all / team / proximity,
`proximity_range_m`) turns it on for every network session; the server relays Opus packets on the
unreliable channel by channel and never feeds them to the sim. Game code mutes and reads talkers
with `gameplay::request_voice(world, VoiceOp::Mute { talker, muted } | SetVolume { talker, volume })`
and `gameplay::voice_is_talking(world, talker)` (`-1` = the local player), the Blueprint
`Voice/MuteTalker` / `Voice/SetTalkerVolume` / `Voice/IsTalking` / `Voice/IsLocalTalking` nodes and
`Event/OnTalkingChanged`, or Rhai `voice_mute` / `voice_set_volume` / `voice_is_talking` /
`voice_local_talking` and `fn on_talking_changed(ev)`. The talker list is the resource
`gameplay::VoiceTalkers`. Voice is presentation: never branch the simulation on it.

**Player settings.** Every game gets a pause menu with Options ▸ Graphics (quality level =
scalability, resolution scale), Audio (a volume per mixer bus), Controls (look sensitivity,
invert-Y, rebinding every digital action — keyboard and pad separately) and Accessibility pages,
pad-navigable, saved per player and applied live. Game code reads and writes the same settings by
KEY (`graphics.quality`, `graphics.resolution_scale`, `audio.<bus>`, `controls.sensitivity`,
`controls.invert_y`, `controls.key.<Action>`, `controls.pad.<Action>`, `access.*`): Rust
`gameplay::request_user_setting(world, key, &value)` / `gameplay::user_setting(world, key)`, the
Blueprint `Settings/SetUserSetting` / `Settings/GetUserSetting` nodes, or Rhai
`set_user_setting(key, value)` / `user_setting(key)`; `game.user_settings` lists every key. A write
applies next frame (and reads back then). Presentation: never branch the simulation on a setting.

**Effect parameters.** A VFX effect declares typed user parameters (a flame's length, a smoke
colour — `vfx.param {action:'list'}`); game logic drives a placed instance with
`gameplay::verbs::set_effect_param(world, requester, LogicTier::…, target, name, EffectParamValue)`
(or `vfxgraph::VfxSystem::set_param` directly), the Blueprint `VFX/SetEffectParameter` /
`VFX/GetEffectParameter` nodes (the node's `ty` types its Value pin), or Rhai
`set_effect_param([token,] name, value)` / `effect_param([token,] name)`. Writes queue on
`gameplay::EffectParamQueue` and apply after the tick; reads answer from the host-published
`gameplay::EffectParamView` (last frame's values). Presentation band and not replicated — each peer
sets its own; drive it from replicated state. The editor / player host drains and publishes it
(effects are stepped by the app's frame loop), and reports an undeclared name or wrong type in the
Message Log.

## Letting an agent play your game (the agent door)

Full loop, op table and pitfalls: [references/agent-playtest.md](references/agent-playtest.md).

Build the game with the `agent-door` feature and launch it with `NGINE_AGENT_DOOR=observe`
(read-only) or `=drive` (input, camera, travel, your own commands). Attach an MCP client with
`ngine mcp connect --game` — loopback + a per-run token, nothing to configure. The engine gives
every game one vocabulary — the same ops the editor's Play (`game.door`) and a dedicated server
serve: `game.info`, `game.match`, `game.players`, `world.query`, `events.tail`, `ui.tree`,
`screenshot`, `logs.tail` (Observe) and `input.action`, `input.aim_at`, `time.pause` / `time.step` /
`time.scale`, `ui.activate`, `console.run`, `game.travel` (Drive); `agent.commands` lists them all.
Add your own from setup: `register_agent_command(world, "mygame.give_ammo", "...", schema,
AgentHandler::Drive(|w, args| { ... Ok(json!({...})) }))` — an `Observe` handler gets `&World`
and cannot mutate. A Shipping export has no door at all (compiled out).

## Determinism is a hard requirement

The simulation is hashed and replayed. Multiplayer, replays, the golden tests and crash
reproduction all depend on two runs over the same inputs producing the same bytes — so a system
must never read the wall clock, use its own random source, or iterate an unordered collection.
The full rules, and the trap that catches large worlds, are in
**[references/determinism.md](references/determinism.md)**. Read it before writing your first
system; a desync found in a playtest costs far more than reading it now.

## Build and run

```bash
cargo test -p my-game              # your game's own tests, incl. the determinism test
ngine games --dir=<parent of my-game> --codegen   # after any game.toml change (from the engine checkout root)
NGINE_GAME=my-game <editor>        # Play it in the editor
```

Editing your game crate recompiles the game and relinks the host — it does **not** rebuild the
engine. Your crate sits above the engine in the dependency graph, never inside it.

The editor can also build for you: `build.run` / `build.status` / `build.errors` / `build.cancel`
compile in the background and stream diagnostics to a Build Output panel, so an agent can iterate
without leaving the session.

## Making a spawned entity VISIBLE

Your code has a `World` and no asset database, so you cannot build a `MeshRenderer` — it holds
asset handles only the host can mint. Ask for a visual instead, and the host resolves it into a
real renderer on its next frame:

```rust
world.insert(
    e,
    scene::PrimitiveVisual::new("cylinder", Vec3::new(0.3, 0.34, 0.31))
        .with_surface(0.0, 0.75)                        // metallic, roughness
        .with_emissive(Vec3::new(0.1, 0.2, 0.13)),      // make it glow
);
```

Kinds: `cube`, `sphere`, `plane`, `cylinder`, `cone`, `wedge`, `torus`. Colours are **linear RGB**.
Entities asking for the same look share one material, so a wave of forty enemies stays one draw
batch. An unknown kind draws nothing and logs — it never silently substitutes a cube.

A host with no asset database (the dedicated server, a headless test) simply never resolves it and
the entity stays logical. That is deliberate: it is what lets the same game code hash identically
on a server and a client. For a real authored mesh rather than a blockout, spawn a prefab.

## The three tiers, and when to use which

| Tier | Iterate by | Reach for it when |
|---|---|---|
| **Rust** (this skill) | rebuild + relaunch | you need real components, systems, or performance |
| **Rhai script** | live, no rebuild | per-entity behaviour you want to tweak while playing; sandboxed, deterministic, fuel-limited |
| **Blueprint** | live, no rebuild | designer-facing logic, event wiring, anything you want visible in a graph |

They compose: write the capability in Rust, expose it with `#[ngine::node]`, and let Blueprint
assemble the game out of it. That is the intended shape — see
**[references/blueprint-exposure.md](references/blueprint-exposure.md)** for how a Rust function
becomes a node, and for the ops that scaffold new code from inside a running editor.

## Rules

- **Depend only on `ngine`.** Naming an internal engine crate directly ties your game to
  internals that are explicitly not a semver promise. Everything a game needs is re-exported —
  `ecs`, `math`, `gameplay`, `runtime`, `scene`, `anim`, `physics_api`, `nav`, `net`, and more.
- **Physics is an interface, not an engine.** Author bodies as `scene::RigidBody` / `Collider` /
  `Joint`, query with `ngine::query::{raycast, sphere_overlap, box_overlap}` or by collision
  channel / preset with `ngine::query::{trace, trace_multi, overlap}` (a `scene::QueryFilter` from
  `scene::resolve_query_filter_in(world, "Visibility", "")`; presets are
  `scene::CollisionProfiles`, authored in World Settings ▸ Collision presets), push bodies with
  `scene::PhysicsCommands`. The engine underneath (Jolt by default, or Rapier — both first-class) is the
  PROJECT's choice (`Physics/PhysicsSettings.backend`, Project Settings ▸ Physics ▸ Physics engine);
  never assume one — read `ngine::physics_api::PhysicsCaps` (agents: `physics.caps`) before
  relying on an optional verb such as sleep state or state snapshots.
- **`ngine::prelude::*` is a pinned surface.** `World`, `Entity`, `Commands`, `Transform`,
  `DVec3`, `Quat`, `Reflect`, `AppBuilder`, `Plugin`, `Phase`, `Time`, `Name` and the query
  filters all arrive through the one glob.
- **Keep core simulation behaviour portable.** Apeiron targets native and the browser from one
  source. Quality and non-core features may differ per platform; simulation *semantics* may not.
- **`render`, `app` and `edit` are deliberately not re-exported.** A game does not draw; it places
  data and runs systems.
