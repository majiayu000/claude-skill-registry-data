---
name: functional-safety-signpost
kind: signpost
description: "Signpost (not a knowledge pack) for the functional safety standards landscape: IEC 61508, ISO 26262, ISO/SAE 21434, UL 4600, SAE J3016, and ASPICE. Contains NO source content: designation, edition, owner, status, and an official catalogue URL only. Use when you need to identify or locate a functional safety standard. All six are paywalled or carry no redistribution grant and cannot be packaged; open paths point at US Government packs, which are not equivalents."
---

<!-- argument-hint: [standard designation or topic, e.g. IEC 61508 / ISO 26262 / 21434 / UL 4600 / J3016 / ASPICE] -->

# Functional Safety Standards Landscape: Signpost (pointers only)

**This is a signpost, not a knowledge pack.** It carries **no source content**:
no reproduced clauses, no synthesised summaries of normative text. IEC 61508,
ISO 26262, ISO/SAE 21434, UL 4600, SAE J3016, and ASPICE are Excluded under
this repo's `docs/SOURCE-VETTING.md` (paywalled or no redistribution grant), so
none of them can be reconstituted into a pack. What this skill does: tell you
which functional safety standard you want, who owns it, whether it can be
packaged, and where to get the authentic copy.

## When to use
You need to identify, cite, or locate a functional safety standard (e.g. "the
functional safety standard?" → IEC 61508; "the automotive variant?" → ISO
26262). This routes you to the authoritative source. The genuinely open paths
in this catalogue are the `mil-std-882` and `nhtsa-vehicle` packs (US
Government practice, not equivalents of any excluded row).

**Prerequisites:** none. Plain Markdown.

## How to use
Find your standard below. The **Status** column tells you whether it is
redistributable:
- 🔴 **Excluded**: paywalled or no redistribution grant; buy/download from the
  owner. Cannot be packaged here.
- 🟢 **Open**: an installable pack exists (named in the row).

Where a licence permits citation, the owner's official catalogue page is given in
the Status cell.

## The standards

| Designation | Edition to cite | Owner | Status | Open path |
|---|---|---|---|---|
| **IEC 61508** | IEC 61508-1:2010 as series anchor | IEC | 🔴 Excluded. `https://webstore.iec.ch/en/publication/5515` | `mil-std-882` (DoD system safety practice, not an IEC equivalent) |
| **ISO 26262** | 2018 series; catalogue anchor ISO 26262-1:2018 | ISO | 🔴 Excluded. `https://www.iso.org/standard/68383.html` | `mil-std-882`; `nhtsa-vehicle` for US vehicle content |
| **ISO/SAE 21434** | 2021 | ISO/SAE | 🔴 Excluded. `https://www.iso.org/standard/70918.html` | `nhtsa-vehicle` cyber chapter (US guidance, not 21434) |
| **UL 4600** | Evaluation of Autonomous Products | UL | 🔴 Excluded. `https://www.shopulstandards.com/ProductDetail.aspx?productId=UL4600` | `nhtsa-vehicle` ADS chapter (US vision, not a UL evaluation) |
| **SAE J3016** | 202104 | SAE | 🔴 Excluded. `https://www.sae.org/standards/content/j3016_202104/` | see `automotive-signpost` and `nhtsa-vehicle`; level definitions are not restated here |
| **ASPICE PAM** | 4.0 | VDA QMC | 🔴 Excluded. `https://vda-qmc.de/en/software-processes/automotive-spice/` | none in this catalogue |

`fda-med-device` is a live pack in this catalogue (FDA device software guidance and the QMSR). It is not an open path for IEC 61508, ISO 26262, or ISO/SAE 21434.

---
*Signpost content is original JG Systems Consulting Ltd. work, MIT licensed. Trademarks and standard designations are named for identification only.*
