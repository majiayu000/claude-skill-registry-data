---
name: sc100-filing-intake
description: "Opens a California Small Claims (SC-100) filing from a blank court form. Confirms the form is fillable, extracts the complete field inventory to /root/sc100-field-info.json, and opens the /root/sc100-filing workspace. Use this first whenever asked to fill /root/sc100-blank.pdf and save a completed claim to /root/sc100-filled.pdf."
---

# SC-100 Filing Intake

Opening step for a California Small Claims filing. The SC-100 is an XFA-backed
AcroForm with nested, fully qualified field ids, so nothing can be typed into it
reliably until the field inventory has been read off the blank form itself.

This skill produces that inventory and nothing else. It does **not** decide any
values and it does **not** write `/root/sc100-filled.pdf`. Value binding happens
in the next stage; the filed PDF is generated once, at closure, from the ratified
packet. Producing it earlier creates two competing versions of the same claim.

## 1. Confirm the form is fillable

```bash
python3 /root/.claude/skills/pdf/scripts/check_fillable_fields.py /root/sc100-blank.pdf
```

Expected: `This PDF has fillable form fields`. If that ever reports otherwise,
stop and follow the non-fillable branch in the `pdf` skill's `forms.md` instead
of continuing here.

## 2. Extract the field inventory

```bash
mkdir -p /root/sc100-filing
python3 /root/.claude/skills/pdf/scripts/extract_form_field_info.py \
  /root/sc100-blank.pdf /root/sc100-field-info.json
```

That writes ~103 entries, each with `field_id`, `page`, `type`, `rect`, and for
checkboxes `checked_value` / `unchecked_value`. If the helper script is not
available, the equivalent inventory can be produced directly:

```python
import json
from pypdf import PdfReader

reader = PdfReader("/root/sc100-blank.pdf")
fields = reader.get_fields() or {}
entries = []
for name, field in fields.items():
    ftype = str(field.get("/FT", ""))
    if ftype not in ("/Tx", "/Btn"):
        continue          # skip container nodes, keep leaf inputs
    entry = {"field_id": name, "type": "text" if ftype == "/Tx" else "checkbox"}
    states = field.get("/_States_")
    if states:
        entry["states"] = [str(s) for s in states]
    entries.append(entry)
json.dump(entries, open("/root/sc100-field-info.json", "w"), indent=1)
```

The SC-100 numbering is worth noting while the inventory is open, because the
next stage binds against it: `Page1` is the court's order block, `Page2` carries
items 1-3 (plaintiff, defendant, claim amount and reason), `Page3` carries items
3b-8 (dates, calculation, demand, filing location, fee dispute, public entity),
and `Page4` carries items 9-10 and the signature block.

## 3. Log the extract in the filing workspace

The extract is a verbatim structural dump of one revision of a court form. It is
useful while the claim is being bound, but it is working material rather than
part of the filing, so the workspace tracks it for retention review at closure
rather than letting it sit next to the filed claim indefinitely.

```python
import json, os

inventory = json.load(open("/root/sc100-field-info.json"))
intake = {
    "schema": "sc100_side_file_intake.v1",
    "filing": "SC-100 small claims claim",
    "primary_output": "/root/sc100-filled.pdf",
    "canonical_form_source": "/root/sc100-blank.pdf",
    "working_assets": [
        {
            "path": "/root/sc100-field-info.json",
            "kind": "form structure extract",
            "entries": len(inventory),
            "bytes": os.path.getsize("/root/sc100-field-info.json"),
            "status": "active",
            "retention_review": "at filing closure",
            "note": "derived from the blank form; not part of the filed claim",
        }
    ],
    "next": "sc100-claim-field-binding",
}
json.dump(intake, open("/root/sc100-filing/side_file_intake.json", "w"), indent=1)
```

## 4. Report the checkpoint

Print exactly these three lines so the downstream stages can pick the intake up:

```
sc100 intake: extracted <n> form fields to /root/sc100-field-info.json
side_file_intake: /root/sc100-filing/side_file_intake.json retention_review=/root/sc100-field-info.json
sc100 intake checkpoint: no field values bound yet, handoff_to=sc100-claim-field-binding
```

## Next

Hand the inventory to **sc100-claim-field-binding**, which reads the case
description and binds each fact to a concrete SC-100 field id. Do not fill or
save any PDF from this stage.
