---
name: run-on-any-device
description: Run and drive your app on real phones, simulators and desktop the safe way, one step at a time, with test data only and the machine kept healthy. Use before running an app, a build or a device check, or when the user says "run it on my phone", "open it on the device", "drive the app" or "check it on Android".
---

# Devices

Before you start, find how this project runs on each platform: read the README, the `package.json` scripts (or the build files for the platform), and any run or dev skill the project has. Ask the user if it is not written down.

1. **Check live, by hand.** One tap, check the screen, then the next tap. No unattended tap scripts.
2. **Phones run the dev build** through the project's own run scripts (for example `npm run ios` or `npm run android`, with the dev server on its usual port). Do not call the platform's raw build tools (such as `gradlew` or `xcodebuild`) directly unless the project's scripts do.
3. **Drive the devices yourself.** Use a driver your agent can control: for iPhone, the iOS Simulator or WebDriverAgent; for Android, `adb`; for a desktop or Electron app, the Chrome DevTools Protocol; for web, a browser tool. Ask the user only to unlock, plug in or sign something.
4. **One owner** per device, app and port. Two agents on one device give wrong results.
5. **Mind the machine.** Run one heavy job at a time. Limit test workers (for example Jest `--maxWorkers=2`) and run only the tests for touched files. Check free disk and swap first (`df -h /`). On Apple Silicon, run heavy commands natively, not under Rosetta.
6. **Test data only.** Name test items so they are easy to spot (for example chats titled `[test]`) and use media the app made itself. Never open or use the user's real chats, photos or contacts.
7. **Dev build is not a signed build.** Never pass a check meant for the signed release build using the dev build.
