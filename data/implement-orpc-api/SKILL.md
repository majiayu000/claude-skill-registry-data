---
name: implement-orpc-api
description: Implement a new handler and attach to the oRPC router
license: MIT
compatibility: opencode
---

## What I do

- make sure you understand the all requirements and ask question about unclear or edge cases
- checkout database schema written with the Drizzle from the `packages/db/src` 
- checkout Drizzle version from packages/db/package.json and modify the schema if necessary.
- check available middewares from `apps/<package>/src/lib/server/orpc/base.ts` and use the appropriate middleware. If the middleware is not suitable with requirement, then create a new one.
- create handler file under `apps/<package>/src/lib/server/orpc/handlers/<scope>/<operation>.ts`. For example: `apps/website/src/lib/server/orpc/handlers/organizations/listMembers.ts`
- implement input schema using zod.
- attach the middleware after input, because some middleware need data from the import and have to typesafe.
- attach the handler to the router in `apps/<package>/src/lib/server/orpc/router.ts` 

**No need to run `npm run <script>`. I will run the necessary scripts and manually check the types for you.**


## When to use me

Use this when you are going to implement a feature and expose API as an oRPC.
Ask clarifying questions if the you are unclear.
