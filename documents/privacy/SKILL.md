---
name: privacy
description: Read before adding what your app keeps of people's data to the network's privacy page, or when someone asks what the page at /privacy says and where each part comes from.
metadata:
  title: "Privacy"
  subtitle: "What your network keeps, and who answers for it"
  about: "The network's privacy page, which anyone can open at its address, /privacy, without signing in: who runs the network and what its apps keep, each said by the app that keeps it."
  category: Utilities
---

The network's privacy page is at `<address>/privacy`, open to everyone, since an outside service's consent screen
(Google's OAuth) links to it. Each app that keeps people's data in a way worth stating says so itself, as an app
adds its settings to Settings: the page shows only the apps the network has installed.

`sections` lists what they add, as the page has it.

## Sections

An app adds to the page by hooking into `privacy.sections`, answering with its list of what it adds:

    @impl true
    def hooks, do: ["privacy.sections"]

    @impl true
    def hook("privacy.sections", _about, _call),
      do: [%{heading: "Your photos", order: 4, text: "Photos are kept in the network's own storage, and shown only to the people you share them with."}]

- `text` is what it says, in Markdown: paragraphs, lists and links.
- `heading` is the heading it's under. Sections with the same heading share it, in their `order`, so an app adds a
  line to another's heading by using its words. With none, it's the page's opening.
- `order` places it, lowest first, as a number: Sign-In's say who runs the network (0 to 2), what apps keep is 3 to 7,
  and how to ask is last (8, 9).
