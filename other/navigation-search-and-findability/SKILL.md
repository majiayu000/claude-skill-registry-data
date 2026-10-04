---
name: navigation-search-and-findability
kind: skill
status: ready
provenance:
  principles:
  - P013
  - P014
  - P020
  - P031
  - P033
  - P034
  - P044
  - P063
  - P069
  claims:
  - C00530
  - C00531
  - C01107
  - C01108
  - C00254
  - C00255
  - C00049
  - C00050
  - C00220
  - C00221
  - C00269
  - C00270
  - C00154
  - C00155
  - C01095
  - C01096
  - C00201
  - C00202
  evidence:
  - E00297
  - E00298
  - E00445
  - E00446
  - E00150
  - E00151
  - E00031
  - E00032
  - E00142
  - E00143
  - E00159
  - E00160
  - E00107
  - E00108
  - E00433
  - E00434
  - E00136
  - E00137
  source_anchors:
  - 861e11e30d6e-c0022
  - c0958e02bc38-c0002
  - 861e11e30d6e-c0012
  - 861e11e30d6e-c0003
  - 861e11e30d6e-c0011
  - 861e11e30d6e-c0013
  - 861e11e30d6e-c0008
  - c0958e02bc38-c0001
  - 861e11e30d6e-c0010
  authored_from_digest: ae05fb2be539e5de7d07d913c2398f255aa41726be2ac4f355ddf986c558a5d1
---

# Navigation, Search, and Findability

Make an environment findable: persistent navigation and place cues, integrated search-and-browse
behavior, results and link ordering by task, and click difficulty (not raw click count) as the
measure.

## When this applies

- Designing automated or semi-automated links between content objects (P013).
- Configuring search ranking, matching, stemming, spelling, fields, or expansion tools (P020).
- Users may explore, refine, refind, research exhaustively, or enter through multiple paths (P031).
- The system is large, hierarchical, complex, or supports varied finding needs (P033).
- Ordering or grouping retrieval results (P034).
- Creating in-content links, headings, or process-step labels (P044).
- Users can arrive from search engines, deep links, or unfamiliar pages (P069).

## Procedure

Apply these principles to the situation under review; for each, name the user need at stake and the trade-off the choice carries.

1. Validate and improve content-model links with user research, gap analysis, entry-point identification, and metadata-backed linking logic. (P013)
2. Treat navigation as effectively being the site: since people will not use a site they cannot find their way around, provide persistent (global) navigation in a consistent place, follow navigation conventions so elements are easy to locate and recognize, and remember navigation also reveals content, teaches how to use the site, and builds trust. (P014)
3. Choose retrieval algorithms, stemming, query builders, and structured-field search according to the user's recall-versus-precision needs. (P020)
4. Support integrated, iterative finding behavior by letting users move fluidly among search, browse, asking, similar-item paths, and subsite-level navigation. (P031)
5. Provide supplemental navigation such as sitemaps, indexes, guides, configurators, and search as backup paths because taxonomies and embedded navigation will not satisfy every user or task. (P033)
6. Select sorting, ranking, best bets, popularity, ratings, paid placement, or clustering based on task, content heterogeneity, available metadata, and user trust implications. (P034)
7. Design contextual links and headings around user expectations, surrounding context, visual hierarchy, and process sequence rather than ad hoc author preference. (P044)
8. Judge navigation by how hard each click is rather than the raw count: keep every click a mindless, unambiguous choice with a strong 'scent of information', use progressive disclosure to avoid confronting users with everything at once, and give just-enough (brief, timely, unavoidable) guidance only when a hard choice cannot be eliminated. (P063)
9. Respect established navigation conventions and provide clear place cues so users know where they are, what the environment is, and where they can go after deep entry. (P069)

## Principles applied

- **P013** (medium) — grounded in claims/evidence and chunk anchors in `sources/`.
- **P014** (high) — grounded in claims/evidence and chunk anchors in `sources/`.
- **P020** (medium) — grounded in claims/evidence and chunk anchors in `sources/`.
- **P031** (medium) — grounded in claims/evidence and chunk anchors in `sources/`.
- **P033** (medium) — grounded in claims/evidence and chunk anchors in `sources/`.
- **P034** (medium) — grounded in claims/evidence and chunk anchors in `sources/`.
- **P044** (medium) — grounded in claims/evidence and chunk anchors in `sources/`.
- **P063** (high) — grounded in claims/evidence and chunk anchors in `sources/`.
- **P069** (medium) — grounded in claims/evidence and chunk anchors in `sources/`.

## Provenance

Grounded in principles P013, P014, P020, P031, P033, P034, P044, P063, P069, their backing claims
and evidence records, and paragraph-level source anchors under `sources/anchors/`. Every cited id
resolves into this package's distilled spine; see `provenance-ledger.md` and `reports/faithfulness-
report.yaml`.
