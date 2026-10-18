---
name: kling-video
description: Generate and retrieve ACT video assets through Kling's official hosted MCP connector in Claude, including the ten-second AIR sonic film. Use for Kling setup, authenticated discovery, video generation and task status; not ordinary website edits.
---

# Kling Video

Use Kling's official international MCP server at `https://kling.ai/mcp`, declared
in the repo's `.mcp.json`. No third-party wrapper or bespoke API client is used.
Read the Kling section of the root README for Claude Code and custom-connector
setup. A shared config alone does not mean a Claude account is connected.

## Authentication

Complete the connector's browser OAuth flow with the ACT Kling account. Claude
stores credentials outside this repo. Never extract browser tokens, print
credentials, commit them, or send Open API access/secret keys to this endpoint.
If tools are not available, have the user enable and authenticate the connector;
do not fall back to a different provider or a direct API wrapper.

## Generation

1. Discover the connected identity, credits, exposed tools and model parameters.
   Confirm the ACT account and distinguish discovery from a paid generation.
2. Use the current tool schemas rather than assuming model IDs or parameters.
   Run the README's single short text-to-video connectivity test only after
   authentication, and only when the user requests a test or generation.
3. For the AIR film, read [the ten-second brief](references/air-film.md). Confirm
   aspect ratio, duration, sound, and reference roles before submission.
4. Submit each approved task once. Retain its generation ID and query the same
   task no faster than every 15 seconds. Never resubmit after an ambiguous timeout.
   Stop on success or failure; report pending work after ten minutes.
5. Retrieve the output and verify actual playback, duration, framing and audio.
   Do not claim success based only on submission or unauthenticated reachability.

Composite the supplied AIR SVG during finishing to preserve its exact proportions
and typography. No music or voiceover for the AIR film. Keep review assets out of
`public/`; website placement and publication require the user's request.

Official setup: https://kling.ai/blog/claude-code-kling-mcp-food-promo-workflow?tab=ai-tools-creation
