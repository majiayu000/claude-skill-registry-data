---
name: creative-review-and-approval-queue
description: Manage creative intake, spec QA, legal or brand approval, platform review, trafficking readiness, rejection handling, swaps, expirations, and evidence for programmatic campaigns. Use when creative assets, VAST tags, HTML5, native, CTV, audio, DOOH, landing pages, click URLs, or approval statuses block launch or in-flight delivery.
---

# Creative review and approval queue

Creative is often the launch blocker that looks small until the day before go-live. This skill
gives operators a queue for asset intake, spec QA, platform approval, trafficking readiness,
rejections, and in-flight swaps across programmatic platforms.

Use platform-specific creative skills for exact specs. Use this skill to run the queue and make
sure each asset has a state, owner, evidence, and next action.

## When to use this skill

- A campaign needs creative intake, asset QA, or approval tracking.
- Creative review, rejection, spec failure, click URL issue, or VAST issue blocks launch.
- Assets need to be swapped, retired, refreshed, or mapped to line items.
- Legal, brand, medical, financial, or regulated-category approval is required.
- The user asks for a creative tracker or creative queue.

## Queue states

| State | Meaning |
| --- | --- |
| Requested | Asset needed but not received |
| Received | Asset received but not QA'd |
| Spec QA | Operator checking dimensions, duration, weight, format, text, URL, tags |
| Brand/legal review | Internal or client approval in progress |
| Platform review | Submitted to platform or publisher review |
| Approved | Cleared and ready to assign |
| Rejected | Rejected by spec, brand, legal, platform, publisher, or policy |
| Trafficked | Assigned to the correct entities |
| Live verified | Serving, click, tags, and reporting verified |
| Retired | Removed, expired, or replaced |

## Required fields

| Field | Requirement |
| --- | --- |
| Asset ID or file name | Stable identifier, not only a friendly title |
| Creative code | Joins to taxonomy and reporting |
| Format and size | Display, HTML5, video, CTV, audio, native, DOOH, etc. |
| Platform and placement | Where the asset will run |
| Landing page and click URL | Final URL, tracker, UTM, and redirect path |
| Approval owner | Brand, legal, client, platform, publisher, or internal owner |
| Review status | One of the queue states |
| Rejection reason | Exact reason and screenshot or policy text where available |
| Assigned entities | Campaign, line, ad group, placement, or creative shell IDs |
| Expiry or rotation rule | End date, refresh date, or replacement condition |

## Core process

1. **Intake against the plan.** Confirm every asset requested in the media plan or trafficking
   sheet has arrived, has a creative code, and maps to a platform, line item, placement, or ad
   group.
2. **Run spec QA.** Check file type, dimensions, duration, bitrate, audio, weight, safe zones,
   click URL, landing page, macros, VAST or tag response, SSL, and policy-sensitive claims.
3. **Check approval needs.** Regulated categories, claims, endorsements, financial language,
   health language, alcohol, political, and client legal processes may require approval before
   platform submission.
4. **Submit and track platform review.** Record platform review ID, submitted date, expected
   SLA, rejection reason, and appeal or resubmission path.
5. **Traffic only approved assets.** Assign assets to the correct entities, confirm rotations,
   weights, dates, and companion assets, then hand to launch QA.
6. **Verify live state.** After launch, confirm impressions, click URL, tag firing, creative
   preview, and reporting rows. Mark `Live verified` only with evidence.
7. **Manage swaps and expiry.** When assets fatigue, expire, reject, or need a legal update,
   create a swap ticket and run it through the same queue.

## Rejection handling

```text
Creative rejection
Asset:
Platform:
Entity IDs:
Rejected by:
Reason:
Policy or spec cited:
Screenshot or evidence:
Impact:
Owner:
Fix path:
Resubmission time:
Launch or delivery risk:
```

Do not describe a rejection as "platform issue" unless support is actually needed. Many
rejections are local spec, landing-page, claim, or targeting-policy issues.

## Decision rules

- Approved does not mean trafficked. Trafficked does not mean live verified.
- A click URL that redirects incorrectly is a launch blocker.
- A video asset that passes file spec but has an invalid VAST response is still blocked.
- Never swap creative without checking reporting and creative code continuity.
- Do not run unapproved claims while waiting on legal. Hold launch or substitute approved copy.

## Common pitfalls

- Tracking creative in email threads instead of a queue with states.
- Losing creative-code mapping during swaps, which breaks asset-level reads.
- Treating platform approval as brand approval.
- Forgetting companions, end cards, captions, click trackers, and landing-page redirects.
- Letting expired creative keep serving because it was approved earlier.

## Related artifacts

- `templates/ops/creative-review-tracker.csv`
- `direct-response-creative-testing`
- `dv360-creative-trafficking`
- `dv360-video-creative-specs`
- `ttd-creative-and-formats`
- `stackadapt-creative-and-formats`
- `cross-platform-launch-qa`
