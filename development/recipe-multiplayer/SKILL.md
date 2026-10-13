---
name: recipe-multiplayer
description: "A multiplayer game the Unreal way — Rust GameMode + replicated components, Blueprint/Rhai RPCs, RepNotify, sessions (LAN, Steam or the game relay by join code), invites, achievements, voice chat, proof on every peer."
---

# Multiplayer (recipe stub)

This is a **pointer**, not the recipe. The workflow lives in the engine and always matches the
build you are connected to, so load it from the running editor before you act:

    ngine.recipes {name: "gameplay/multiplayer"}

Follow the numbered steps it returns, and read its warnings first. Do not work from this stub
alone.

## Use it when

- making a multiplayer game
- testing a game with several players
- a blueprint or script rpc does nothing on the other players
- other players look wrong, fall through the floor or never animate
- replicating a variable or a game component to clients
- validating or rate-limiting what clients send (anti-cheat)
- hosting a game other players can find (a server browser, LAN play)
- joining a game without typing an address
- voice chat, push to talk or proximity voice between players

## Ops it names

`project.new`, `build.run`, `build.status`, `build.relaunch`, `game.set_ruleset`, `game.ruleset`, `place.actor`, `scene.add_component`, `blueprint.from_text`, `blueprint.validate`, `script.compile_check`, `script.set`, `game.play`, `game.stop`, `net.state`, `net.emulation`, `net.server_health`, `game.host_session`, `game.find_sessions`, `game.join_session`, `game.destroy_session`, `game.session_state`, `game.session_menu`, `net.relay_host`, `net.relay_join`, `game.invite_friends`, `game.achievement`, `services.state`, `voice.state`, `voice.set`, `voice.mute`, `settings.set`, `input.action`, `anim.state`, `scene.query`

Check each op's arguments with `ngine.describe` before the first call: the recipe is the
order and the discipline, the live schema is the spelling.

Start the session with `editor.context`. If `ngine.recipes` cannot be reached the editor is not
running or not connected: run `/apeiron:status`.
