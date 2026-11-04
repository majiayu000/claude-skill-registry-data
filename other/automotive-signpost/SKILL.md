---
name: automotive-signpost
kind: signpost
description: "Signpost (not a knowledge pack) for the automotive standards landscape: ISO 26262, ASPICE, SAE J3016, UNECE R155, UNECE R156, and the NHTSA vehicle set. Contains NO source content: designation, edition, owner, status, and an official catalogue URL only. Use when you need to identify or locate an automotive standard. Most are paywalled or carry no redistribution grant and cannot be packaged; the one open path is the nhtsa-vehicle pack."
---

<!-- argument-hint: [standard designation or topic, e.g. ISO 26262 / ASPICE / J3016 / R155 / R156] -->

# Automotive Standards Landscape: Signpost (pointers only)

**This is a signpost, not a knowledge pack.** It carries **no source content**:
no reproduced clauses, no synthesised summaries of normative text. ISO 26262,
ASPICE, SAE J3016, and UNECE R155/R156 are Excluded under this repo's
`docs/SOURCE-VETTING.md` (paywalled or no redistribution grant), so none of them
can be reconstituted into a pack. What this skill does: tell you which automotive
standard you want, who owns it, whether it can be packaged, and where to get the
authentic copy.

## When to use
You need to identify, cite, or locate an automotive standard (e.g. "the
functional-safety standard?" → ISO 26262; "the cybersecurity regulation?" → UNECE
R155). This routes you to the authoritative source. The one genuinely open path in
this catalogue is the `nhtsa-vehicle` pack (US Government guidance, not an
equivalent of any excluded row).

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
| **ISO 26262** | 2018 series; catalogue anchor ISO 26262-1:2018 | ISO | 🔴 Excluded. `https://www.iso.org/standard/68383.html` | `mil-std-882` for system-safety process (not an equivalent); `nhtsa-vehicle` for US vehicle safety content |
| **ASPICE (Automotive SPICE PAM)** | 4.0 | VDA QMC | 🔴 Excluded. `https://vda-qmc.de/en/software-processes/automotive-spice/` | none in this catalogue |
| **SAE J3016** | 202104 | SAE | 🔴 Excluded. `https://www.sae.org/standards/content/j3016_202104/` | `nhtsa-vehicle` ADS chapter for the US vision document, which is not the J3016 level definitions |
| **UNECE R155** | UN Regulation No. 155, cyber security and CSMS | UNECE | 🔴 Excluded. `https://unece.org/transport/documents/2021/03/standards/un-regulation-no-155-cyber-security-and-cyber-security` | `nhtsa-vehicle` cyber chapter (US guidance, not R155) |
| **UNECE R156** | UN Regulation No. 156, software update and SUMS | UNECE | 🔴 Excluded. Hub `https://unece.org/transport/vehicle-regulations` · addenda index `https://unece.org/transport/vehicle-regulations-wp29/standards/addenda-1958-agreement-regulations-141-160` · exact document slug unconfirmed as of 2026-09-27 | none; no open SUMS pack exists in this catalogue |
| **NHTSA vehicle set** | Cyber 2022 final, ADS 2.0, FMVSS selections | NHTSA | 🟢 Open. No URL (the content pack carries no source URL, and neither does this row) | pack `nhtsa-vehicle` |

---
*Signpost content is original JG Systems Consulting Ltd. work, MIT licensed. Trademarks and standard designations are named for identification only.*
