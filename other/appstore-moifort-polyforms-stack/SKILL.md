---
name: appstore
description: Use when preparing an App Store or TestFlight step of a Polyforms app (listing, captures and panels, first subscription submission, release notes, signing secrets) or when App Store Connect refuses something. The long form of stack rule 07-appstore.
---

# App Store Connect

## The release, in order

1. `bun run deprecations`, remove what is removable, floor raised by the script's value.
2. Notes in `CHANGELOG.md` and each `CHANGELOG.<lang>.md` (rule 06), French shown and
   approved in the conversation.
3. Push `main`, watch Deploy.
4. Captures and panels only if the person asked.
5. `git tag ios-v<version> && git push origin ios-v<version>`; watch Release to the end.

## Secrets the iOS workflows read

| Secret | What |
|---|---|
| `ASC_KEY_ID`, `ASC_ISSUER_ID`, `ASC_KEY_P8` | The team's App Store Connect API key |
| `IOS_DIST_CERT_P12`, `IOS_DIST_CERT_PASSWORD` | The Apple Distribution certificate, base64 |
| `IOS_PROVISION_PROFILE` | The App Store profile named `<App> App Store`, base64 |
| `IOS_GOOGLE_SERVICE_INFO_PLIST` | The Firebase plist, base64 |
| `IOS_SENTRY_DSN`, `SENTRY_AUTH_TOKEN` | Reporting and dSYM upload |

## What has no API

Done once, in the built-in browser, signed in as the person: the app record, the price
schedule, the App Privacy answers, accepting a new agreement (account holder only).

## First subscription

The API refuses every direct route (`FIRST_SUBSCRIPTION_MUST_BE_SUBMITTED_ON_VERSION`,
`SUBSCRIPTION_GROUP_SUBMISSION_NOT_ALLOWED`). The sequence that works:
1. API: create a draft `reviewSubmission` (platform IOS), add the `appStoreVersion` as an item.
2. Browser: the subscription group's page, "Add for review" is a dropdown, pick the draft;
   then each subscription's page, same dropdown, same draft.
3. The draft's "Submit for review" becomes active; submit.
Cancelling takes a minute; a draft without items cannot be cancelled, delete its items.

## Listing traps

- A name held by another account in a locale answers 409: "Name: What it does".
- Keywords: 100 characters, checked by App Store Connect.
- A locale with release notes but no listing is created empty and the submission is refused:
  add a locale's `infra/fastlane/metadata/<locale>/` before its notes.
- The product page header (16:9) is dragged in by hand: there is no API for it.

## TestFlight

Adding a tester who belongs to another app's group answers 409: create the tester with
`POST /v1/betaTesters` carrying the group relationship.
