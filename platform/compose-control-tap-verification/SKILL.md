---
name: compose-control-tap-verification
description: "Use when an adb tap on a Compose control does nothing or a count does not change after tapping, when a uiautomator dump disagrees with the code or a validation gate or toggle looks wrong on device, or before claiming a control or an on-device state check works."
---

# Verifying a Compose control on a device

A uiautomator dump splits one Compose control across nodes: the **label** sits
on a child (an icon, or a `TextView`), while the **click target and its state**
(`enabled`, `selected`, `checked`) sit on the node that owns the semantics —
usually the clickable ancestor. Guessed coordinates are the #1 cause of false
"this control is broken" reports; reading state off the label's node is what
produces false "nothing is ever disabled" ones. Device mechanics (auth, wake,
install, basic dump and tap) live in `android-usb-verify`.

## 1. Target by label, never by guessed coordinates

A tap that lands 20px off silently hits a sibling — often a whole-card
`clickable` that navigates away — and the evidence looks identical to a dead
button. Text nodes whose content is a bare number (`"3"`) are ambiguous: a stat
strip value and a like count look the same in a dump, and filtering by "small
node near the left edge" picks the wrong one.

Target by **accessibility label**, which is stable across redesigns:

```python
import xml.etree.ElementTree as ET, subprocess, os, re
ADB = os.path.expandvars(r"%LOCALAPPDATA%\Android\Sdk\platform-tools\adb.exe")
def sh(*a): return subprocess.run([ADB,"-s",SERIAL,*a],capture_output=True,text=True,errors="replace").stdout
def dump():
    sh("shell","uiautomator","dump","/sdcard/ui.xml"); return sh("shell","cat","/sdcard/ui.xml")

for n in dump().split("<node")[1:]:
    d = re.search(r'content-desc="([^"]*)"', n)
    b = re.search(r'bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"', n)
    if d and d.group(1) in ("Like", "Liked") and b:
        print(d.group(1), tuple(map(int, b.groups())), 'clickable="true"' in n)
```

Split on `<node`, not `<` — splitting on `<` shreds attributes across fragments
and every `content-desc` comes back empty.

If the filter returns nothing, **confirm which screen you are on first**. An
empty result usually means the control isn't on the current screen, not that it
lacks a label. Scroll to the control before judging absence: a dump only
contains what is currently composed.

## 2. The label is on a child; the click and the state are on the ancestor

In Compose, `Modifier.clickable` usually sits on the **parent** `Row`/`Box`,
while the `Icon` only carries the `contentDescription`. So the labelled node
reports `clickable=false`:

```
('Like', (152, 1035, 194, 1077), False)   <- icon: labelled, not clickable
```

That is normal. Tap the **centre of the labelled node anyway** — the parent's
hit rect encloses it. `clickable=false` on the icon is not a defect. Only treat
it as a finding when *no* ancestor is clickable: dump the clickable nodes and
check whether any encloses the icon's bounds. If none does, the tap target was
genuinely lost in a redesign.

State follows the same split. A regex over the whole XML that matches the label
and grabs the nearest attribute reads the *child*, which reports
`enabled="true"` / `selected="false"` no matter what the control is doing.
Symptom: the dump contradicts code you have just read, in the direction of
"nothing is ever disabled / nothing is ever selected". Parse the dump as XML and
walk **up** from the labelled node to the first clickable ancestor:

```python
def state_of(label, attr="enabled"):
    root = ET.fromstring(dump())
    parents = {c: p for p in root.iter() for c in p}
    for n in root.iter("node"):
        if n.get("text") == label:
            cur = parents.get(n)
            while cur is not None:
                if cur.get("clickable") == "true":
                    return cur.get(attr)
                cur = parents.get(cur)
    return "absent"
```

Print the ancestor chain once when a result surprises you — it shows
immediately which node carries what:

```python
chain = [(c.get("class","").split(".")[-1], c.get("clickable"), c.get("enabled"), (c.get("text") or "")[:12])]
```

The ancestor's `enabled`/`selected`/`checked` are what to read. Field *values*
are not: dumps often omit them, so confirm those with a screenshot. A dump can
also be stale — check its byte size changes (`android-usb-verify`).

## 3. Prove the state check can fail

A state check that only ever reports the good value is worthless. Drive the
control to both states in one run and print both:

| entry | expected |
|---|---|
| empty required field | disabled |
| valid value | enabled |
| out-of-range value | **disabled** |
| back to valid | enabled |

If every row reads the same, the measurement is wrong before the app is.

## 4. Confirm the effect against ground truth, not the UI

Optimistic UI updates can show success while the network write failed, and a
rollback can hide a real failure. Read the backing store either side of the tap:

```bash
PG() { docker run --rm -i -e PGPASSWORD="$PGPW" postgres:17-alpine \
  psql "$CONN" -tAc "$1" 2>&1 | tail -1; }
echo "before: $(PG "select count(*) from session_likes where user_id='<uid>'")"
adb shell input tap <cx> <cy>; sleep 5
echo "after:  $(PG "select count(*) from session_likes where user_id='<uid>'")"
```

A toggle is stateful: read the current row first so you know whether the
expected outcome is +1 or −1. Pair the DB delta with a screenshot so you have
both the write and the render.

## 5. Attribute a "nothing happened" result correctly

Before reporting a control as broken, rule out in order:

1. **Wrong screen** — dump and check a known label is present.
2. **Missed target** — tap centre was outside the reported bounds, or an open
   keyboard sat over it (`compose-layout-device-traps`).
3. **Hit a sibling** — took a screenshot and the app navigated somewhere else;
   that is a greedy parent `clickable`, not a dead control.
4. **Fired but failed** — UI reverted and the store is unchanged; now it is
   real, and the error copy (if any) is the next thing to check.

Only #4 is a bug in the control.

## Traps that make the check vacuous

- **A negative grep proves nothing** until the positive case is located. Search
  for the setter the UI actually calls, not for an enum's literal values — a
  control built from `Enum.entries` spells none of them.
- **Instrumented Gradle runs uninstall the app afterwards**, so a check started
  straight after one drives a launcher, not your app. Check `pm path <pkg>`
  first, and seed live-database fixtures with `am instrument` rather than the
  Gradle task (`android-jank-attribution-noise-floor`).
- **A forced device setting can silently do nothing** (`debug.force_rtl`, a
  per-app pseudolocale): prove it moved a geometry probe against the unforced
  run before trusting any result under it — see `android-rtl-layout-verification`.
