---
name: browser-verification-stand
kind: pattern
rule: browser-verification
description: Pattern of rule browser-verification. Load when an honest stand is needed — the production build of the site, the admin stand, a stand behind real nginx, signing in to the admin, finding out what sits on a port. Not for layout measurements — that is pattern browser-verification-measure.
---
<!-- rt-kit v0.34.0 · patterns/browser-verification-stand.md · 917850e19048 · правится надстройкой, не здесь -->

# An honest stand

Pattern of the rule `browser-verification`. What must be true — the law
`docs/constitution/verifiability.md`.

## When to use

- What is checked is not visible on the dev server: server-side markup, locales, cache,
  redirects, headers, bundle size.
- The port answers with something other than what was expected.
- Signing in to the admin is needed.

## Port numbers are declared by the tree, not by the pattern

The commands below name the ports by name — `API_PORT`, `SITE_PORT`, `ADMIN_PORT`, `SSR_PORT`, the
stand ports and the proxy ports. The pattern has no numbers: every tree lays out its stands its own
way, and a tree with one application, obliged to name eight foreign numbers, names invented ones —
and the substitutions lose their meaning. The tree declares the numbers by its own profile: in
environment variables or in an override section of this pattern, where its own ready-made commands
stand with the names of the runner targets.

The role of each name is what the prose speaks of: the intake port, the site port, the admin port,
the rendering server port. A tree that has no such application does not read those sections.

## First — what answers on the port

Before the first request, not after a puzzling answer:

```bash
lsof -nP -iTCP:$API_PORT -sTCP:LISTEN
```

A built artifact from a past session regularly hangs on the intake port
(`node -r dotenv/config dist/apps/api/main.js`): it answers 200 with old code, and the procedure
created in the branch it does not have at all. There may be several such processes, and all of
them must be killed — by PID from `lsof`, each one: `pkill` by the pattern `nx serve api` hits none
of them.

## Production build of the site

```bash
npx nx build site
PORT=$SITE_STAND_PORT node dist/apps/site/server/server.mjs
```

This is not a dev server: the guard catches `nx|ng serve`, package runners and static servers, and
lets the launch of a built server through.

Behaviour that depends on the host — the owner's address, a redirect away, a different answer on
different names — is checked right here with one request carrying the given header. A proxy with
substitution is not needed for that: it adds one more process whose behaviour will have to be told
apart from the one under check.

## Admin stand

```bash
npx nx build admin --base-href=/
```

Without `--base-href` the stand serves an empty page with no errors in the console. A stand that
needs Angular DevTools also needs the dev configuration (`--configuration=development`): the
production build does not publish `window.ng`. No conclusions about bundle size and minification
may be drawn from such a build.

What was built is served by the tree's proxy with its real config, not by a static server. There are
two reasons, and both surface in the first minute. The application calls procedures on its own
origin, and on a deep link a static server answers `404`: it knows nothing of the single-page
application's routes and does not fall back to its entry point. The dev-server guard refuses such a
server the same as `nx serve`, and that is a pointer to the right move, not an obstacle. The
ready-made call is the section "A stand behind real nginx" below; it both serves what was built and
proxies the procedures.

Sign-in is done through the form, as a person does it. The account of the local development
database is not the owner's secret: the seed of the same tree puts it there, and the password lies
in the environment file next to it. Permission for it is not asked — permission is asked about a
production account, and there is never one on a local stand. Where there is no intake nearby, the
stand itself substitutes the sign-in answer: the application's path stays the same as a person's.

The token is not signed by hand and not put into browser storage by hand: put there so, it checks
the screen while bypassing the live sign-in path — that is, it answers the wrong question. Asking
a person to type a password, open a tab or press a button means a wrongly chosen path, not a lack
of rights on the executor's side.

**Ask for the work mode, not for the input.** Input into the password field is refused by the
classifier of automatic mode: it judges the action itself and does not tell addresses apart — a
stand on a local port looks to it like the production site. There is one move from here: name the
refused action to the owner, ask for normal mode, fill the form with the seed pair yourself and
return to automatic mode. The request "sign in yourself" and "type the password" shifts the
agent's work onto the owner and looks legitimate exactly because a real obstacle stands before
it: a refused field, a foreign extension in the browser, a profile that disconnected. The
obstacle stays the agent's obstacle.

The ways to lift the obstacle by one's own means come before any request. Substitute the value with
the form tool by a reference to the element; switch off the interfering extension in the browser
profile; raise the stand on another address. A second driver is not justified by the password field:
it fills the same field without the classifier, but the bypassed ban is lifted not from one field
but from all of them at once. Normal mode left on removes confirmation from every later action of
the session too, so the return is part of the sign-in, not a separate clean-up.

The owner's stand is never a fallback path: it builds the main branch and says nothing about the
edit in the working tree.

## API stand

The built artifact is raised on a free port, not on the intake port: there the owner's intake
answers, and its environment is not the one under check.

```bash
npx nx build api
env -u JWT_SECRET NODE_ENV=production API_PORT=$API_STAND_PORT DATABASE_URL=… node dist/apps/api/main.js
```

Environment variables are set in the command itself, one per case under check. A refusal at start-up
is as much a check result as a 200 answer. An application that fell in a provider factory does not
listen on the port at all, and that is seen by `lsof`, not by the text in the console.

A procedure is called by its full name, as the contract declares it:

```bash
curl -sS -X POST http://localhost:$API_STAND_PORT/<area>.v1.AuthService/GetMe \
    -H 'content-type: application/json' -H "authorization: Bearer $TOKEN" -d '{}'
```

A token is signed by hand only where the signature itself is under check: proving that the debug
key is accepted has no other path. In every other case the token is taken from the live API by
signing in — a hand-written one hides a divergence in the set of claims.

## A stand behind real nginx

Cache, redirects and headers live in `deploy/nginx.conf`, not in the application. Any conclusion
about `301`, `Cache-Control` and `X-Cache-Status` is drawn only here:

```bash
docker run -d --name <prefix>-stand-nginx \
  --add-host api:host-gateway --add-host ssr:host-gateway \
  -p $PROXY_SITE_PORT:80 -p $PROXY_ADMIN_PORT:8081 \
  -v "$PWD/deploy/nginx/main.conf:/etc/nginx/nginx.conf:ro" \
  -v "$PWD/deploy:/etc/nginx/conf.d:ro" \
  -v "$PWD/dist/apps/admin/browser:/usr/share/nginx/html/admin:ro" \
  nginx:1.27-alpine
```

- The config is mounted **as a directory**, not as a single file: the editor recreates the file,
  the container is left with a truncated copy, and `nginx -t` inside falls on "unexpected end of
  file" while the file outside is whole. Cured by recreating the container, not by editing the
  config.
- The main config is substituted by a separate line: it lies in `deploy/nginx/`, not next to
  `nginx.conf` — a file with the `.conf` extension in the mounted directory would get into
  `include` and bring nginx down on the `user` directive. Without it the stand comes up on the
  image's config, and the connection limit per worker there is its own.
- A foreign `Host` is refused by the **dev server**, not by the built application: the production
  build answers it the same as its own. Behind the real proxy requests go with their own header
  exactly because the proxy stands in front of the dev server — hence `-H "Host: localhost"`.
- The stand's environment variables must point at the stand's processes. `CACHE_REFRESH_URL`
  pointed at the site port resets the cache past the process that keeps the redirect table in
  memory — and a working mechanism looks broken.

## A stand lives exactly as long as the check

A stand is raised for one conclusion and is not needed after it. Abandoned, it hinders nothing and
gives no signal. It has its own name, a free port, it takes almost no room — it can be seen only by
a call to the list, and there is no reason to call it. So it is a person who has to take apart what
piled up, and they cannot tell an abandoned stand from a live one of a neighbouring tree by name.

Teardown goes by the same move the conclusion was made with:

```bash
docker rm -f <stand name>
```

The name is given by the task number — so it is visible whose stand was left if the move broke off
after all.

## A tree for comparison

"The edit broke this" can be said only when it is visible that before the edit it was otherwise.
That is checked with a second tree, not from memory:

```bash
git worktree add ../<prefix>-base <commit>   # the task branch is not touched
pnpm install --frozen-lockfile         # from ../<prefix>-base: its node_modules are its own
```

- For comparison take not the main branch but the last commit on which the tree builds: main is
  sometimes broken, and then "before" and "after" differ not because of the edit. Whether a commit
  builds is checked by building, not by its being in the main branch.
- The stand of the second tree is raised on its own ports: the site, admin and intake ports are
  taken by the owner, and the rendering port must not be taken — the developer's stand goes by the
  name `ssr:<rendering port>`.
- Both stands are kept up at the same time — exactly until the comparison ends: comparing from
  memory between two launches, you notice only what you managed to remember. With the comparison
  done, the stand of the second tree is torn down by the same move, not left until the end of the
  session. Stands left behind pile up across sessions and hold connections to the storage, and the
  rule says so in a pitfall. Teardown refused — the stand is named to the owner at the end of the
  session by name, with the port.

## The state of the ports is taken before the first build of the session

The owner's servers go down without your involvement: the site answered 404 on all its addresses
before the first build of the session, and the API fell silent in the middle of it. Without a
"before" measurement a fall can be neither attributed to your build nor cleared of suspicion.

```bash
for u in http://localhost:$API_PORT/health http://localhost:$SITE_PORT/ http://localhost:$ADMIN_PORT/; do
    printf '%s %s\n' "$(curl -s -o /dev/null -w '%{http_code}' --max-time 5 "$u")" "$u"
done
```

The measurement is the answer, not `lsof`: the port is sometimes taken by a built artifact from a
past session, and it answers 200 with old code.

## Common misses

- **A single project build the servers survive, and there is no reason to give it up.** Measured
  by the answer before and after: all ports stayed with their processes. Caution here costs more
  than the check — a whole set of layout checks was left unrun exactly because the build was
  deemed dangerous without measuring. A build from the cache is not a measurement: it builds
  nothing at all, and that is visible by its duration.
- Do not raise your own dev server: the site, the admin and the intake are already up by the
  owner, and a second instance is refused by the guard.
- **A refused static server is read as a ban on the check, while it is a pointer to the right
  move.** It may not serve what was built not out of caution: the application calls its own
  origin, and a deep link answers `404`. From here one goes not to bypass the guard but to the
  tree's proxy with its real config.
- **The owner's dev server is a place to look, not a place to check.** The conclusion that the
  screen is right is drawn on the production build behind the real proxy: server-side markup,
  locales, cache, redirects and headers on the dev server are either different or absent
  altogether. A look at the raised dev server is fit to understand what is going on on an
  unfamiliar screen and unfit as confirmation: the confirmation is a measurement on a stand from
  the production build.
- **A build of everything silences all three dev servers of the owner, not only the API.** After
  `nx run-many -t build` both the site and the admin go down. Build what you check
  (`npx nx build site`), not the whole tree. If the servers went down, the agent cannot bring them
  back up — the guard is in the way, so the owner is told at once, not at the end of the session.
  The push gate is such a build too: its set runs the build of everything affected. So the
  measurement is taken before the push or on a stand from the production build. The answer of the
  server, not its port, tells whether it survived.
- Take the rendering port with care: the developer's stand goes by the same name
  `ssr:<rendering port>` through `host-gateway`, and while a foreign process hangs on it, the
  stand serves a foreign build.

## The ports and stands of this tree

A section of this tree: there is no site and no rendering server here, and there are two stands —
the showcase of the component set and the stand of the end-to-end suite with its own seeded
database.

| Role                  | Port  | Raised by                              |
| --------------------- | ----- | -------------------------------------- |
| the showcase          | 6006  | `pnpm run storybook:ui-kit-v1`         |
| the built showcase    | 6007  | `pnpm run build-storybook:ui-kit-v1` and serving |
| the stand receiver    | 3310  | `pnpm run serve:stand`                 |
| the stand admin panel | 4310  | by the same call                       |
| the dev receiver      | 3000  | `pnpm run serve:api`                   |
| the dev admin panel   | 4200  | `pnpm run serve:admin`                 |
| the dev database      | 55432 | `pnpm run serve:db`                    |

The ports of the end-to-end stand are overridden by the variables `E2E_API_PORT` and
`E2E_ADMIN_PORT` — they are declared in `apps/message-bus-admin-e2e/stand/stand.mjs`. The stand
takes no working ports: on it one looks at what the working database does not have.

Sorting out an occupied port, telling a built artefact from a dev server and the rule that a
second instance is not raised hold here in full — and they are what one uses when the showcase
answers with the wrong thing.

## Why there is no nginx stand here

A section of this tree: none of the applications here has a proxy. The admin panel goes to the
receiver directly, proxying `/api` to its port by its own dev config, and the showcase is static
without a server. No conclusions about caching, redirects and headers are drawn on these stands:
there is nothing to draw them from.
