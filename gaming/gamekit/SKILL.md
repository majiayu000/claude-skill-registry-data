---
name: gamekit
description: "Integrate Game Center features using GameKit. Use when authenticating players with GKLocalPlayer, submitting scores to leaderboards, unlocking achievements, implementing real-time or turn-based multiplayer matchmaking, showing the Game Center access point or dashboard, or adding challenges and friend invitations to iOS games."
---

# GameKit

Integrate Game Center features into iOS 26+ games using GameKit and Swift 6.3.
Provides player authentication, leaderboards, achievements, multiplayer
matchmaking, access point, dashboard, challenges, and saved games.

## Contents

- [Authentication](#authentication)
- [Access Point](#access-point)
- [Dashboard](#dashboard)
- [Leaderboards](#leaderboards)
- [Achievements](#achievements)
- [Real-Time Multiplayer](#real-time-multiplayer)
- [Turn-Based Multiplayer](#turn-based-multiplayer)
- [Common Mistakes](#common-mistakes)
- [Review Checklist](#review-checklist)
- [References](#references)

## Authentication

All GameKit features require the local player to authenticate first. Set the
`authenticateHandler` on `GKLocalPlayer.local` early in the app lifecycle.
GameKit calls the handler multiple times during initialization.

```swift
import GameKit

func authenticatePlayer() {
    GKLocalPlayer.local.authenticateHandler = { viewController, error in
        if let viewController {
            // Present so the player can sign in or create an account.
            present(viewController, animated: true)
            return
        }
        if let error {
            // Player could not sign in. Disable Game Center features.
            disableGameCenter()
            return
        }

        // Player authenticated. Check restrictions before starting.
        let player = GKLocalPlayer.local

        if player.isUnderage {
            hideExplicitContent()
        }
        if player.isMultiplayerGamingRestricted {
            disableMultiplayer()
        }
        if player.isPersonalizedCommunicationRestricted {
            disableInGameChat()
        }

        configureAccessPoint()
    }
}
```

Guard on `GKLocalPlayer.local.isAuthenticated` before calling any GameKit API.
For server-side identity verification, see [references/gamekit-patterns.md](references/gamekit-patterns.md).

## Access Point

`GKAccessPoint` displays a Game Center control in a corner of the screen. When
tapped, it opens the Game Center dashboard. Configure it after authentication.

```swift
func configureAccessPoint() {
    GKAccessPoint.shared.location = .topLeading
    GKAccessPoint.shared.showHighlights = true
    GKAccessPoint.shared.isActive = true
}
```

Hide the access point during gameplay and show it on menu screens:

```swift
GKAccessPoint.shared.isActive = false  // Hide during active gameplay
GKAccessPoint.shared.isActive = true   // Show on pause or menu
```

Open the dashboard to a specific state programmatically:

```swift
// Open directly to a leaderboard
GKAccessPoint.shared.trigger(
    leaderboardID: "com.mygame.highscores",
    playerScope: .global,
    timeScope: .allTime
) { }

// Open directly to achievements
GKAccessPoint.shared.trigger(state: .achievements) { }
```

## Dashboard

Present the Game Center dashboard using `GKGameCenterViewController`. The
presenting object must conform to `GKGameCenterControllerDelegate`.

```swift
final class GameViewController: UIViewController, GKGameCenterControllerDelegate {

    func showDashboard() {
        let vc = GKGameCenterViewController(state: .dashboard)
        vc.gameCenterDelegate = self
        present(vc, animated: true)
    }

    func showLeaderboard(_ leaderboardID: String) {
        let vc = GKGameCenterViewController(
            leaderboardID: leaderboardID,
            playerScope: .global,
            timeScope: .allTime
        )
        vc.gameCenterDelegate = self
        present(vc, animated: true)
    }

    func gameCenterViewControllerDidFinish(
        _ gameCenterViewController: GKGameCenterViewController
    ) {
        gameCenterViewController.dismiss(animated: true)
    }
}
```

Dashboard states: `.dashboard`, `.leaderboards`, `.achievements`, `.localPlayerProfile`.

## Leaderboards

Configure leaderboards in App Store Connect before submitting scores. Supports
classic (persistent) and recurring (time-limited, auto-resetting) types.

### Submitting Scores

Submit to one or more leaderboards using the class method:

```swift
func submitScore(_ score: Int, leaderboardIDs: [String]) async throws {
    try await GKLeaderboard.submitScore(
        score,
        context: 0,
        player: GKLocalPlayer.local,
        leaderboardIDs: leaderboardIDs
    )
}
```

### Loading Entries

```swift
func loadTopScores(
    leaderboardID: String,
    count: Int = 10
) async throws -> (GKLeaderboard.Entry?, [GKLeaderboard.Entry]) {
    let leaderboards = try await GKLeaderboard.loadLeaderboards(
        IDs: [leaderboardID]
    )
    guard let leaderboard = leaderboards.first else { return (nil, []) }

    let (localEntry, entries, _) = try await leaderboard.loadEntries(
        for: .global,
        timeScope: .allTime,
        range: 1...count
    )
    return (localEntry, entries)
}
```

`GKLeaderboard.Entry` provides `player`, `rank`, `score`, `formattedScore`,
`context`, and `date`. For recurring leaderboard timing, leaderboard images,
and leaderboard sets, see [references/gamekit-patterns.md](references/gamekit-patterns.md).

## Achievements

Configure achievements in App Store Connect. Each achievement has a unique
identifier, point value, and localized title/description.

### Reporting Progress

Set `percentComplete` from 0.0 to 100.0. GameKit only accepts increases;
setting a lower value than previously reported has no effect.

```swift
func reportAchievement(identifier: String, percentComplete: Double) async throws {
    let achievement = GKAchievement(identifier: identifier)
    achievement.percentComplete = percentComplete
    achievement.showsCompletionBanner = true
    try await GKAchievement.report([achievement])
}

// Unlock an achievement completely
func unlockAchievement(_ identifier: String) async throws {
    try await reportAchievement(identifier: identifier, percentComplete: 100.0)
}
```

### Loading Player Achievements

```swift
func loadPlayerAchievements() async throws -> [GKAchievement] {
    try await GKAchievement.loadAchievements() ?? []
}
```

If an achievement is not returned, the player has no progress on it yet. Create
a new `GKAchievement(identifier:)` to begin reporting. Use
`GKAchievement.resetAchievements()` to reset all progress during testing.

## Real-Time Multiplayer

Real-time multiplayer connects players in a peer-to-peer network for
simultaneous gameplay. Players exchange data directly through `GKMatch`.

### Matchmaking with GameKit UI

Use `GKMatchmakerViewController` for the standard matchmaking interface:

```swift
func presentMatchmaker() {
    let request = GKMatchRequest()
    request.minPlayers = 2
    request.maxPlayers = 4
    request.inviteMessage = "Join my game!"

    guard let matchmakerVC = GKMatchmakerViewController(matchRequest: request) else {
        return
    }
    matchmakerVC.matchmakerDelegate = self
    present(matchmakerVC, animated: true)
}
```

Implement `GKMatchmakerViewControllerDelegate`:

```swift
extension GameViewController: GKMatchmakerViewControllerDelegate {
    func matchmakerViewController(
        _ viewController: GKMatchmakerViewController,
        didFind match: GKMatch
    ) {
        viewController.dismiss(animated: true)
        match.delegate = self
        startGame(with: match)
    }

    func matchmakerViewControllerWasCancelled(
        _ viewController: GKMatchmakerViewController
    ) {
        viewController.dismiss(animated: true)
    }

    func matchmakerViewController(
        _ viewController: GKMatchmakerViewController,
        didFailWithError error: Error
    ) {
        viewController.dismiss(animated: true)
    }
}
```

### Exchanging Data

Send and receive game state through `GKMatch` and `GKMatchDelegate`:

```swift
extension GameViewController: GKMatchDelegate {
    func sendAction(_ action: GameAction, to match: GKMatch) throws {
        let data = try JSONEncoder().encode(action)
        try match.sendData(toAllPlayers: data, with: .reliable)
    }

    func match(_ match: GKMatch, didReceive data: Data, fromRemotePlayer player: GKPlayer) {
        guard let action = try? JSONDecoder().decode(GameAction.self, from: data) else {
            return
        }
        handleRemoteAction(action, from: player)
    }

    func match(_ match: GKMatch, player: GKPlayer, didChange state: GKPlayerConnectionState) {
        switch state {
        case .connected:
            checkIfReadyToStart(match)
        case .disconnected:
            handlePlayerDisconnected(player)
        default:
            break
        }
    }
}
```

Data modes: `.reliable` (TCP-like, ordered, guaranteed) and `.unreliable`
(UDP-like, faster, no guarantee). Use `.reliable` for critical game state and
`.unreliable` for frequent position updates. Register the local player as a
listener (`GKLocalPlayer.local.register(self)`) to receive invitations through
`GKInviteEventListener`. For programmatic matchmaking and custom match UI, see
[references/gamekit-patterns.md](references/gamekit-patterns.md).

## Turn-Based Multiplayer

Turn-based games store match state on Game Center servers. Players take turns
asynchronously and do not need to be online simultaneously.

### Starting a Match

```swift
let request = GKMatchRequest()
request.minPlayers = 2
request.maxPlayers = 4

let matchmakerVC = GKTurnBasedMatchmakerViewController(matchRequest: request)
matchmakerVC.turnBasedMatchmakerDelegate = self
present(matchmakerVC, animated: true)
```

### Taking Turns

Encode game state into `Data`, end the turn, and specify the next participants:

```swift
func endTurn(match: GKTurnBasedMatch, gameState: GameState) async throws {
    let data = try JSONEncoder().encode(gameState)

    // Build next participants list: remaining active players
    let nextParticipants = match.participants.filter {
        $0.matchOutcome == .none && $0 != match.currentParticipant
    }

    try await match.endTurn(
        withNextParticipants: nextParticipants,
        turnTimeout: GKTurnTimeoutDefault,
        match: data
    )
}
```

### Ending the Match

Set outcomes for all participants, then end the match:

```swift
func endMatch(_ match: GKTurnBasedMatch, winnerIndex: Int, data: Data) async throws {
    for (index, participant) in match.participants.enumerated() {
        participant.matchOutcome = (index == winnerIndex) ? .won : .lost
    }
    try await match.endMatchInTurn(withMatch: data)
}
```

### Listening for Turn Events

Register as a listener and implement `GKTurnBasedEventListener`:

```swift
GKLocalPlayer.local.register(self)

extension GameViewController: GKTurnBasedEventListener {
    func player(_ player: GKPlayer, receivedTurnEventFor match: GKTurnBasedMatch,
                didBecomeActive: Bool) {
        // Load match data and update UI
        loadAndDisplayMatch(match)
    }

    func player(_ player: GKPlayer, matchEnded match: GKTurnBasedMatch) {
        showMatchResults(match)
    }
}
```

### Match Data Size

`matchDataMaximumSize` is 64 KB. Store larger state externally and keep only
references in match data.

## Common Mistakes

### Not authenticating before using GameKit APIs

```swift
// DON'T
func submitScore() {
    GKLeaderboard.submitScore(100, context: 0, player: GKLocalPlayer.local,
                              leaderboardIDs: ["scores"]) { _ in }
}

// DO
func submitScore() async throws {
    guard GKLocalPlayer.local.isAuthenticated else { return }
    try await GKLeaderboard.submitScore(
        100, context: 0, player: GKLocalPlayer.local, leaderboardIDs: ["scores"]
    )
}
```

### Setting authenticateHandler multiple times

```swift
// DON'T: Set handler on every scene transition
override func viewDidAppear(_ animated: Bool) {
    super.viewDidAppear(animated)
    GKLocalPlayer.local.authenticateHandler = { vc, error in /* ... */ }
}

// DO: Set the handler once, early in the app lifecycle
```

### Ignoring multiplayer restrictions

```swift
// DON'T
func showMultiplayerMenu() { presentMatchmaker() }

// DO
func showMultiplayerMenu() {
    guard !GKLocalPlayer.local.isMultiplayerGamingRestricted else { return }
    presentMatchmaker()
}
```

### Not setting match delegate immediately

```swift
// DON'T: Set delegate in dismiss completion -- misses early messages
func matchmakerViewController(_ vc: GKMatchmakerViewController, didFind match: GKMatch) {
    vc.dismiss(animated: true) { match.delegate = self }
}

// DO: Set delegate before dismissing
func matchmakerViewController(_ vc: GKMatchmakerViewController, didFind match: GKMatch) {
    match.delegate = self
    vc.dismiss(animated: true)
}
```

### Not calling finishMatchmaking for programmatic matches

```swift
// DON'T
let match = try await GKMatchmaker.shared().findMatch(for: request)
startGame(with: match)

// DO
let match = try await GKMatchmaker.shared().findMatch(for: request)
GKMatchmaker.shared().finishMatchmaking(for: match)
startGame(with: match)
```

### Not disconnecting from match

```swift
// DON'T
func returnToMenu() { showMainMenu() }

// DO
func returnToMenu() {
    currentMatch?.disconnect()
    currentMatch?.delegate = nil
    currentMatch = nil
    showMainMenu()
}
```

## Review Checklist

- [ ] `GKLocalPlayer.local.authenticateHandler` set once at app launch
- [ ] `isAuthenticated` checked before any GameKit API call
- [ ] Player restrictions checked (`isUnderage`, `isMultiplayerGamingRestricted`, `isPersonalizedCommunicationRestricted`)
- [ ] Game Center capability added in Xcode signing settings
- [ ] Leaderboards and achievements configured in App Store Connect
- [ ] Access point configured and toggled appropriately during gameplay
- [ ] `GKGameCenterControllerDelegate` dismisses dashboard in `gameCenterViewControllerDidFinish`
- [ ] Match delegate set immediately when match is found
- [ ] `finishMatchmaking(for:)` called for programmatic matches; `disconnect()` and nil delegate on exit
- [ ] Turn-based match data stays under 64 KB
- [ ] Turn-based participants have outcomes set before `endMatchInTurn`
- [ ] Invitation listener registered with `GKLocalPlayer.local.register(_:)`
- [ ] Data mode chosen appropriately: `.reliable` for state, `.unreliable` for frequent updates
- [ ] `NSMicrophoneUsageDescription` set if using voice chat
- [ ] Error handling for all async GameKit calls

## References

- See [references/gamekit-patterns.md](references/gamekit-patterns.md) for voice chat, saved games, custom match
  UI, leaderboard images, challenge handling, and rule-based matchmaking.
- [GameKit documentation](https://sosumi.ai/documentation/gamekit)
- [GKLocalPlayer](https://sosumi.ai/documentation/gamekit/gklocalplayer)
- [GKAccessPoint](https://sosumi.ai/documentation/gamekit/gkaccesspoint)
- [GKLeaderboard](https://sosumi.ai/documentation/gamekit/gkleaderboard)
- [GKAchievement](https://sosumi.ai/documentation/gamekit/gkachievement)
- [GKMatch](https://sosumi.ai/documentation/gamekit/gkmatch)
- [GKTurnBasedMatch](https://sosumi.ai/documentation/gamekit/gkturnbasedmatch)
