---
$schema: https://gist.githubusercontent.com/remorses/9f3737a6f516c01f4bdb612045c64072/raw/agent-skill.schema.json
name: boox
description: >
  how to send documents to the user boox e ink tablet. Use when the user
  mentions boox, eink, e-ink tablet, USB file transfer to the tablet, or
  wants a PDF on the Boox. Also use for BooxDrop (Wi-Fi transfer) and
  finding the Boox IP on the local network.
---

# boox

Send files to Tommy's **ONYX Boox Go 10.3**. Prefer USB when the tablet is
plugged in. Use BooxDrop over Wi-Fi when it is not. Use Google Drive last.

## USB upload with gphoto2

macOS **Finder does not mount** the Boox. It uses **MTP**. Do not wait for a
volume in `/Volumes`.

Check the tablet is on USB:

```bash
ioreg -p IOUSB -l -w0 | awk -F'"' '/USB Product Name|USB Vendor Name/ {print $4}'
```

A connected Go 10.3 shows vendor **ONYX**. Product name is often
`KHAJE-IDP _SN:...`. libmtp/gphoto2 may label it `Google Inc Nexus/Pixel (MTP)`.

Upload into **Books**:

```bash
gphoto2 --folder '/store_00010001/Books' --upload-file "/path/to/file.pdf"
gphoto2 --folder '/store_00010001/Books' --list-files
```

`gphoto2` is on Homebrew (`brew install gphoto2`). Install it if missing.

### USB gotchas

- Unlock the tablet. Keep the screen on. Set USB to **File Transfer**.
- Use a **data** cable. Plug **direct into the Mac**, not a hub.
- If File Transfer is missing: Developer Options → Default USB configuration
  → File Transfer.
- `mtp-sendfile` / `mtp-connect --sendfile` fail on this device
  (`PTP Invalid Object Handle`). Always use **gphoto2**.
- `adb` only works if USB debugging is on. Do not depend on it.
- If `ioreg` has no ONYX device, USB is not enumerating. Switch cable or
  skip to Drive.

## Wi-Fi upload with BooxDrop

Use this when **no Boox is on USB**, or when the user asks for **BooxDrop**.
The user must open BooxDrop on the tablet, on the same Wi-Fi as the Mac.

```bash
bun ~/.config/opencode/skills/boox/booxdrop.ts find
bun ~/.config/opencode/skills/boox/booxdrop.ts send /path/to/file.pdf
bun ~/.config/opencode/skills/boox/booxdrop.ts send a.epub b.pdf --dir /storage/emulated/0/Books
bun ~/.config/opencode/skills/boox/booxdrop.ts send file.pdf --url http://192.168.1.50:8085
```

- The script tries the cached URL in `~/.cache/booxdrop.json`, then scans each
  LAN `/24` on port **8085** with `GET /api/device` (VPN tunnels are skipped).
- Upload is `POST /api/storage/upload` (multipart `file`, optional `dir`).
  Default folder is `Books`. Output shows the saved path on the device.
- The IP comes from router DHCP. It is usually stable, but it can change.
- If the scan finds nothing: ask the user for the URL that BooxDrop shows on
  screen and pass `--url`. The tablet turns Wi-Fi off when it sleeps, so keep
  the screen on. Guest networks with client isolation block the scan.

## Google Drive fallback

If USB and BooxDrop both fail, copy PDFs to:

`/Users/morse/Documents/googledrive/`

Drive syncs them. Example with critique:

```bash
critique --pdf /Users/morse/Documents/googledrive/changes-name.pdf
```
