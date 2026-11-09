---
name: figma-mcp
description: Use when reading a Figma file into code, or when the Figma MCP is missing.
version: 1.1.0
author: TimeLine
license: MIT
platforms: [macos]
metadata:
    hermes:
        tags: [figma, mcp, design, cdp, oauth, tokens]
---

# Figma MCP

The Figma remote MCP server is the one supported route from a design file into this repository. It
is a hosted endpoint at `https://mcp.figma.com/mcp`, authenticated by OAuth, and it is link-based: a
tool call names a file key and a node id, never a search phrase.

Two failures make it look broken when it is not, and both are covered below: the token an MCP client
stores carries the `mcp:connect` scope only, and a tool result above a few kilobytes is replaced in
the transcript by a marker whose content is not kept.

Nothing here names a machine, an account or an absolute path. A command reads its endpoint and its
token from the environment, so the same text works in every clone.

## The install

```sh
hermes mcp install figma          # registers the server with the client
hermes mcp test figma             # prints the transport, the auth and the tool count
```

`hermes mcp list` reports `figma https://mcp.figma.com/mcp all enabled`. A healthy test prints
`Auth: OAuth 2.0`, `Connected`, and `Tools discovered: 42`. Never hand-edit `mcp_servers` in the
client's configuration; the install command is the only writer, and a hand-written block skips the
OAuth registration that the authorize step performs.

The OAuth flow opens `figma.com/oauth/mcp` in a browser and redirects to a loopback callback. The
client writes the resulting token to its own store, at a path that is the client's business -
`mcp_call.py` takes that path in `MCP_TOKEN_FILE` rather than assuming it.

## The scope is the trap

`mcp:connect` is not `files:read`. The stored access token authenticates the MCP endpoint and
nothing else:

```sh
curl -s -H "Authorization: Bearer $TOKEN" https://api.figma.com/v1/me    # 403 Forbidden
```

A 403 here is the scope, not an expired token. The REST API needs a personal access token that this
repository does not keep, so every read goes through the MCP endpoint.

## A large result is lost, not merely shortened

A chat client replaces a tool result above a few kilobytes with a marker, and the marker for an MCP
result is not stored, so retrieving it answers `hash not found in session store`. A 24 KB
`get_metadata` reply arrives as a marker with nothing behind it.

The fix is to call the endpoint directly, so the payload is written to a file that can be read,
grepped and diffed locally:

```sh
export MCP_URL="https://mcp.figma.com/mcp"
export MCP_TOKEN_FILE="<the token file your client wrote>"

python3 mcp_call.py get_metadata '{"fileKey":"<KEY>","nodeId":"4-4"}' figma-meta.xml
python3 mcp_call.py get_design_context '{"fileKey":"<KEY>","nodeId":"4:5"}' figma-drawer.md
```

`mcp_call.py` performs the streamable-HTTP handshake (`initialize`, `notifications/initialized`,
`tools/call`) and prints a one-line summary plus the first 600 bytes. The full result is the output
file. It handles both `application/json` and `text/event-stream` replies, because the server answers
with either.

The node id spelling differs by tool: `get_metadata` accepts `4-4` and `get_design_context` accepts
`4:4`. A `node-id=4-4` URL parameter maps to `4:4` in the API, so both spellings reach the same
node.

## Finding the file when all you have is a name

The MCP is link-based and has no search-by-name tool. `whoami` returns every plan the authenticated
user belongs to with its team key, which is the only honest way to resolve a team name:

```sh
python3 mcp_call.py whoami '{}' figma-whoami.json
```

A team answers `team::<id>` with a `seat` field. The file itself is then found in the person's own
browser, because the file list is client-rendered and the only session that can see it is theirs:

```sh
node cdp-figma-click.js "https://www.figma.com/files/team/<TEAM_ID>/project/<FOLDER_ID>" "Main View"
```

That opens a background tab, clicks the card with real `Input.dispatchMouseEvent` presses, and
prints the resulting `location.href`. A synthetic `MouseEvent` does not open a Figma file card - the
card listens on the pointer pipeline - so the click has to go through the input domain.

The layers panel is a second source of node ids and needs no MCP call at all: every row carries
`data-testid="<id>-layers-panel-row"`. `cdp-figma-tree.js` expands the carets and dumps the tree,
but its caret toggle collapses as well as expands, so the row count oscillates between passes. Treat
the MCP `get_metadata` reply as the authoritative tree and this as a cross-check.

## Reading a design into components

1. `get_metadata` on the root frame, then parse the XML locally into an outline of id, name, size
   and position. The reply carries every descendant, so one call describes the whole composition.
2. `get_design_context` per section, written to its own file. It returns markup with utility
   classes, `data-node-id` attributes and temporary asset URLs.
3. `get_variable_defs` answers `{}` on a file with no local variables. That is a real answer: the
   composition's colours are literal fills, so the palette comes from the generated classes, not
   from a token set.
4. The asset URLs under `figma.com/api/mcp/asset/...` expire in seven days. Download anything the
   page needs and reference the local copy; a temporary URL in a component is a broken image next
   week.

The conversion rule the tool itself prints is the one to follow: the generated markup is a
description of the design, not the code to commit. This repository takes `.scss` with BEM nesting
and Solid `.tsx`, so the classes are translated into the component sheets under
`Source/Stylesheet/Component/` and the markup is rewritten as a Solid component.

## What the composition became

One frame held the whole workspace, and each of its four parts now has a component:

| Frame                | Node    | Component                                          |
| -------------------- | ------- | -------------------------------------------------- |
| `Timeline Selector`  | `4:289` | `Source/Component/Workspace/Provenance.tsx`        |
| `File Drawer`        | `4:5`   | `Drawer.tsx`, `DrawerColumn.tsx`, `DrawerItem.tsx` |
| `HR Separator`       | `4:153` | `Publish.tsx`                                      |
| `Blank bento layout` | `3:3`   | `Bento.tsx`                                        |

The drum in `Timeline Selector` is the part worth keeping: thirteen bands whose height, opacity,
marker size and corner radius ramp away from the selected stage. That ramp is a table indexed by
distance from the selection (`Ladder` in `Provenance.tsx`), so the rail holds any number of stages
without a new rule.

## Claim → test

| Claim                                           | Test                                                                                                                                  |
| ----------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| The server is registered and reachable          | `hermes mcp test figma` prints `Auth: OAuth 2.0`, `Connected` and a tool count                                                        |
| The stored token cannot read the REST API       | `curl -s -o /dev/null -w '%{http_code}' -H "Authorization: Bearer $TOKEN" https://api.figma.com/v1/me` prints `403`                   |
| A large reply survives as a file                | `python3 mcp_call.py get_metadata '{"fileKey":"<KEY>","nodeId":"4-4"}' figma-meta.xml` writes the file and prints its first 600 bytes |
| A file card opens only through the input domain | `node cdp-figma-click.js "<folder URL>" "<card name>"` prints `after:` with the resulting `location.href`                             |
| The layers panel is a cross-check, not a source | the row count printed by `cdp-figma-tree.js` matches the node count in the `get_metadata` reply                                       |

## References

| File                 | Covers                                                      |
| -------------------- | ----------------------------------------------------------- |
| `mcp_call.py`        | Direct MCP tool call, result written to a file              |
| `cdp-figma-find.js`  | Scan a Figma page for `design`/`file` links matching a name |
| `cdp-figma-click.js` | Open a file card with real input events, print the URL      |
| `cdp-figma-tree.js`  | Dump the layers panel tree with node ids                    |
| `cdp-page.js`        | Generic background-tab probe: anchors and text of one URL   |
