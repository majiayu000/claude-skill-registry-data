---
name: settings
description: Read before adding an app's settings to Settings, or when someone asks where a setting is.
metadata:
  title: "Settings"
  subtitle: "Every app's settings, in one place"
  about: "Your devices, people, accounts, notifications, look and updates, and every app you have, in one place. Each app brings its own settings here."
  category: Utilities
---

Settings is one app where every app brings its settings, as macOS's System Settings has its panes. Its sidebar has
whoever's looking (Sign In & Security under their name), the sections apps add, in three groups, then every app they
have, A to Z, each with its own page: who it's for, whether it's trusted, its notifications, its update, and Remove
App. Updates is its own: Software Update for the network's servers, this device, and each app with an update ready.

- `sections` lists what the apps you have add, as below, each with its app's title and icon and its red count.
- `apps` lists the apps you have as the sidebar shows them; One Core's `apps` says the rest of each.
- `badge` is the red count on Settings' icon: what waits in its sections, together.

Each of its screens is a tool that only reads and its arguments, which a link names and a browser's address shows:
`section` (`one:settings#section&app=sign-in&section=devices`, /settings/sign-in/devices), `updates`
(/settings/updates), or `app`, an app's page (`one:settings#app&name=<name>&for=<who it's for>`, /settings/apps/<name>).
A link's other arguments are the section's own, which its component reads from `link()`: Vault's `request`
(`one:settings#section&app=vault&section=accounts&request=<id>`).

## Sections

An app adds to Settings by hooking into `settings.sections`, answering with its list of what it adds:

    @impl true
    def hooks, do: ["settings.sections"]

    @impl true
    def hook("settings.sections", _about, _call),
      do: [
        %{in: "settings", name: "Devices", component: "devices", icon: "client/icon.svg", group: "network", order: 1},
        %{in: "device", component: "awake", service: true}
      ]

- `component` is what draws it: a Solid component the app's client exports (`client/package.json`: `{"exports":
  {"./devices": "./devices.tsx"}}`), the module's default export. A trusted app's is drawn in Settings' page and acts
  with what Settings' page may do. An untrusted app's is its page `client/<component>.html` instead, in a frame of
  Settings' page (the UI library's `Frame`), the device after `#`, where it keeps what its own app may do; it says how
  tall it is (`sizeChanged({ height })`), which its group grows to, and is 150 points otherwise. It draws its own
  card, as a trusted one's is drawn in Settings' (`<ListStyle value="insetGrouped">`).
- `in` is where. `"settings"` is a section of the sidebar, for the apps a network starts with, which are trusted (an
  untrusted app's is left out): its `name`, its `icon`
  (a file of the app's `client/`), its `group`, `"you"` (the row with the person's name, which is Sign-In's),
  `"network"`, `"general"` or `"system"`, its `order` in the group, and a `badge`, if it has one: a tool of the app's
  that only reads, whose answer's `count` is the red count on its row and, added up, on Settings' icon. A section that
  has nothing to show on some devices says `needs`, a field of what `client()` says of the device (`login`): it's listed
  only where that isn't `null`, as a phone has no login to open the app at. Its component
  draws a whole `Screen`, with `back`, and is given `groups`, a component that draws what other apps add to a place
  it offers: `<props.groups in="device" device={id} />`.
- Any other `in` is a group in a page a section offers, headed by the adding app's icon and name, so it's clear which
  app brings what: `"device"`, a device's page in Devices, whose component is given `device`, the device's id, and
  `server`, the server it is or runs on, if any; or `"app"`, the app's own page in Settings' Apps. A device's group
  says where it applies, so no heading shows over nothing: `kinds`, the kinds of device it's for (`app`, `browser`,
  `assistant`, `server`), and `service: true` for only a server where the app's service runs (Stay Awake, on a Mac).
  A group's component draws only its rows (a `List`), never a `Screen`.

An app that can't answer is left out, as one whose answer doesn't say what it must is.
