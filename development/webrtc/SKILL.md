---
name: webrtc
description: Read before making an app stream a screen or other live video to a person's app over WebRTC, or when a live view says it couldn't connect.
metadata:
  title: "WebRTC"
  subtitle: "Live video of your screens"
  about: "Shows the screens your apps open, like a browser you sign in on or your AI's desktop, as smooth live video you can click and type on, through Cloudflare's relays."
  category: Admin
---

WebRTC gives an app's code `ice_servers` for one stream: TURN credentials from Cloudflare Realtime, short-lived,
which both ends use with `iceTransportPolicy: "relay"`. A person or an agent can't call any of its tools: the app
streaming is what decides who may watch. A screen's tool takes the action `stream`: with no `offer` it answers these
ICE servers, and with the app's whole SDP `offer` its own `{"answer": <sdp>}`. The UI library's `LiveScreen` does the
app's end. The screen's end is WebRTC's sender, one program for every kind of screen: `sender` gives its build for
each kind of machine, which the app's code there downloads once, checks and runs (`server/bin/stream/src/main.rs`
says what it takes).

Cloudflare Realtime's SFU is there too, for a stream it carries rather than TURN's two ends: `sfu_session` makes a
session, `sfu_tracks` adds tracks to it, `sfu_renegotiate` renegotiates after tracks change, and `sfu_close` closes
tracks. A session takes nothing: its offer goes with its tracks. `sfu_tracks` and `sfu_close` take an SDP
`sessionDescription` (its `type` and `sdp`) where they have one, and answer with Cloudflare's response:
`sfu_renegotiate` takes the answer to the SFU's offer, the others an offer of the app end's. A `sessionId`
is letters, digits, dashes and underscores.

It needs the item `Cloudflare TURN` in the Vault of whoever it's installed for (the network's, most often): `key_id`
(not secret) and `api_token`, a TURN key's id and secret from Cloudflare (Realtime › TURN, or the API's
`/accounts/<id>/calls/turn_keys`), with `rtc.live.cloudflare.com` its site, switched on for `webrtc`. The SFU needs
`Cloudflare SFU` there too: `app_id`, a Realtime app's id, and `app_token`, its API token, with the same site and
also switched on for `webrtc`. Ask for either with `vault_request` and `app: webrtc`, which puts it in that Vault;
never in the chat. Without it, a live view says so, and that its owners add it.
