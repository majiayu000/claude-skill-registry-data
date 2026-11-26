---
name: downloads
description: Read when someone wants the network's app on a computer or phone, asks where to download it, or to set the network's public TestFlight link.
metadata:
  title: "Downloads"
  subtitle: "Get the app on every device"
  about: "Your network's download page, at its address /download: the app for the computer or phone it's opened on, and the rest under it."
  category: Admin
---

The network's download page is <address>/download, for whoever's signed in to the network: someone who isn't signs in
first and comes back to it. Send people there to get the network's app on a Mac, Windows, Linux or Android, or
on an iPhone through TestFlight. It offers what `list` says.

The installers are Software Update's: `tooling/release client` publishes the network's own
(`software-update publish_installer`), and the page serves each at <address>/download/<its name>.

An iPhone gets the app from TestFlight. With a public TestFlight link (`set_testflight_link`, as App Store Connect
gives it for an external group), the page offers that; without one, it opens TestFlight, where the app is listed for
whoever the network has invited as a tester.
