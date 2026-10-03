---
name: supabase-mobile-auth
description: Supabase auth and data access from React Native. Use for Apple or Google sign-in with Supabase, sessions dropping or not refreshing, auth deep links, RLS blocking mobile queries, requests hanging on slow networks.
user-invocable: false
---

# Supabase in a mobile app, the parts the docs gloss over

## Native sign-in beats browser redirects

On mobile, prefer token-based native flows over web OAuth redirects. The user stays in the app, there is no browser handoff to break, and no deep-link dance:

- **Apple**: the native Sign in with Apple sheet returns an identity token; pass it to `signInWithIdToken`. Hash the nonce (SHA-256) into the Apple request and pass the raw nonce to Supabase, and remember Apple only returns the user's name on the FIRST authorization, so persist it immediately or lose it.
- **Google**: the native Google sign-in SDK returns an id token for `signInWithIdToken`. Check whether your chosen Google sign-in library supports a nonce parameter. Some do not, and then Supabase's nonce check fails; the "skip nonce check" switch in the Supabase dashboard exists for exactly that case. Prefer a nonce-capable library when starting fresh, and treat the skip switch as a documented tradeoff rather than a mystery setting.
- **Email**: OTP codes (`signInWithOtp` then `verifyOtp`) avoid deep links entirely, which on mobile removes a whole class of "the magic link opened the wrong thing" support tickets.

With only native flows, no URL detection is needed: `detectSessionInUrl: false`, and deep-link handling stays out of the auth path entirely.

## Session storage and refresh

- Supply an explicit storage adapter. Working choices: encrypted MMKV (fast, sturdy), AsyncStorage or an encrypted wrapper over it (Supabase's documented default), or SecureStore with care, since sessions are larger than what some iOS releases historically accepted per value.
- Refresh needs the app-state pattern: start auto-refresh when the app becomes active, stop it in the background. A refresh that fires while the app is suspended can rotate the token without persisting the result, and the next launch presents a stale refresh token, which trips refresh-token-reuse detection and signs the user out.
- Serialize concurrent refreshes. Two simultaneous `getSession` calls both trying to refresh is another reuse-detection trigger; a simple in-process mutex around refresh ends it.
- On sign-out, also clear the persisted session storage explicitly. Belt and suspenders, but a cached session resurrecting a signed-out account is a real bug class and clearing storage is one line.
- Copy-ready wiring for all of the above (storage adapter, refresh lifecycle, serial lock, fetch timeout) is in [reference.md](reference.md).

## Timeouts, aborts, and honest error reporting

Mobile networks hang in ways desktop dev machines never do. Without a timeout, a hung request means an infinite spinner.

- Give the client a global fetch timeout (an AbortController around fetch, 15 to 30 seconds), and tighter per-query timeouts where UX demands it via `abortSignal` on queries.
- Treat resulting AbortErrors as connectivity noise: warning-level telemetry with a fixed fingerprint, never one error event per stack trace, or your error tracker becomes unreadable the first week a user rides the subway.
- Render from cache first where you have one. A profile screen that shows last-known data instantly and refreshes silently survives a 20-second network stall; one that blocks on the fetch does not.

## RLS from the mobile perspective

- Baseline for user-owned rows: enable RLS, policy `auth.uid() = user_id` for select/insert/update/delete as appropriate. Test with the anon key, not the service key; the service key bypasses RLS and validates nothing.
- An RLS denial surfaces client-side as an empty result or a 403-class error, and it is indistinguishable from "no data" if you do not look. When mobile shows nothing and the table has rows, suspect RLS before suspecting the query.
- Never ship the service role key in the app. Anything requiring elevated rights belongs in an Edge Function or RPC with its own checks. Corollary: server-to-server webhook endpoints (payment providers and the like) cannot present a user JWT, so those functions need platform JWT verification off and a shared-secret check of their own, or the sender gets 401s forever.
- SECURITY DEFINER functions are the safe hatch for narrow privileged operations callable from the client: smallest possible scope, explicit grants, `set search_path` pinned.

## Debugging auth incidents, in order

1. What does the client actually hold? Log session presence and expiry (never the token itself) at the failure site.
2. Refresh races: two near-simultaneous refresh attempts in the log line up with reuse-detection sign-outs.
3. Provider-side config drift: bundle id / package name and client ids in the provider console must match the running binary; a dev-build applicationId suffix breaks Google sign-in configured only for the production id.
4. Clock skew on device breaks JWT validation in both directions; rare, but it explains the unexplainable once a year.
