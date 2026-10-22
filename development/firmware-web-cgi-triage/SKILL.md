---
name: firmware-web-cgi-triage
description: Use when analyzing embedded firmware web interfaces, CGI backends, httpd route tables, ASP/EJ/page references, hidden or unlinked CGI endpoints, NVRAM web routes, or mismatches between extracted rootfs web content and compiled route handlers. Especially useful for router firmware reverse engineering where source trees, object files, and rootfs binaries may not match exactly.
metadata:
  short-description: Map firmware web UI and CGI routes
---

# Firmware Web/CGI Triage

Use this skill for static route mapping in embedded firmware web stacks. Stay read-only unless the user explicitly asks for changes.

## Workflow

1. Establish layout and provenance.
   - Identify source tree web code, compiled httpd binaries, CGI objects/archives, and extracted rootfs `www/` paths.
   - Hash comparable binaries. If hashes differ, treat them as separate artifacts and avoid assuming route parity.

2. Harvest visible web references.
   - Search extracted web content for CGI/ASP/EJ/action references.
   - Prefer `rg -n`; if `rg` is unavailable, use `grep -RniE`.
   - Include JavaScript-generated routes, form actions, self-posting ASP pages, and upload forms when visible.

3. Harvest compiled routes.
   - Use `strings -td`, `nm -A`, `readelf -r`, and `objdump -Dr` on httpd binaries and CGI objects.
   - Look for route table strings adjacent to handler symbol relocations.
   - For stripped binaries, use `readelf -Ws`, dynamic imports, PLT/GOT call patterns, and dense strings to build candidate maps.
   - Separate source-tree routes from rootfs-binary routes when the binaries differ.

4. Build an endpoint table.
   - Columns: endpoint, artifact/source, handler/function, method/context if known, visible page references, confidence, notes.
   - Mark entries as `confirmed`, `candidate`, or `needs validation`.

5. Identify hidden or unlinked routes.
   - `hidden/candidate`: route string or route table entry exists, but no extracted `www/` page references it.
   - `visible-only`: page references a route not found in the compiled artifact being examined.
   - `rootfs-visible`: extracted pages reference a route in the deployed rootfs binary, even if absent from the source-tree route set.
   - Keep source-tree and rootfs comparisons separate.

## Useful Commands

```sh
file path/to/httpd path/to/cgi/*.o path/to/cgi/*.a
sha256sum path/to/httpd /tmp/rootfs/usr/sbin/httpd
nm -A path/to/cgi/*.o
strings -td path/to/httpd path/to/cgi/*.o
readelf -r path/to/cgi/all_cgis.o
objdump -Dr -b elf32-little -m mips:isa32 path/to/cgi/all_cgis.o
rg -n "([A-Za-z0-9_./-]+\.cgi|cgi-bin/|\.asp|<%|action=|submit|enctype=|nvram)" /tmp/rootfs/www src 2>/dev/null
# Fallback when rg is unavailable:
grep -RniE "([A-Za-z0-9_./-]+\.cgi|cgi-bin/|\.asp|<%|action=|submit|enctype=|nvram)" /tmp/rootfs/www src 2>/dev/null
```

## Reporting Rules

- Do not claim a route is reachable only because a string exists; call it a candidate unless table linkage or runtime routing is clear.
- Do not merge source and rootfs findings when their binaries differ.
- Preserve uncertainty around generated JavaScript routes, auth gates, model/SKU conditionals, and dead code.
