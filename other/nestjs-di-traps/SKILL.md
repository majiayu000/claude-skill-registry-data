---
name: nestjs-di-traps
description: "Use when wiring NestJS providers and modules: injecting an interface, sharing a provider between modules, a circular-dependency error, a ModuleRef lookup, or a request-scoped provider that suddenly slows or duplicates things. The five traps where the app boots and misbehaves, or does not boot."
---

# nestjs-di-traps

Step 6 of the pipeline (`WORKFLOW.md`), the dependency-injection half of the NestJS stack.
`skills/nestjs-node-conventions` section 1 states the baseline (constructor injection, one module per domain,
`forwardRef()` as a last resort). This block holds the mechanisms behind five failures that rule does not
explain: each one either crashes at boot with a message that does not name the cause, or boots and behaves
wrongly in a way no unit test with hand-built objects will show.

## When
A diff injects something that is not a plain class, adds a provider to a second module, reaches for
`forwardRef()` or `ModuleRef`, adds `Scope.REQUEST` or injects `REQUEST`, or when the app fails to boot with
"Nest can't resolve dependencies of the X (?)".

## Steps

### 1. An interface cannot be a token
1. **Interfaces and type aliases are erased at compile time.** Nest resolves a constructor parameter by a
   runtime token, and an interface leaves nothing to look up. A parameter typed with an interface and no
   `@Inject()` does not compile into a usable token, and boot fails with "can't resolve dependencies" pointing
   at an unnamed parameter.
2. **Choose the token deliberately.** The official documentation gives three options: a string or `Symbol`
   token with `@Inject(TOKEN)`, an abstract class used as both contract and token (constructor injection then
   needs no `@Inject()`), or a plain interface when it is only a compile-time type and nothing is injected.
   Prefer a `Symbol` for a port with several implementations: a unique runtime identity, where two unrelated
   providers sharing a string token collide silently and the second registration wins.
3. **One exported constant, one place.** The token is declared once in a shared file and imported by both the
   registration (`{ provide: TOKEN, useClass: Impl }`) and every `@Inject(TOKEN)`. A second
   `Symbol('same description')` is a different token: the symptom is the same unresolved-dependency error with
   the right-looking name.
4. **Registration is per module.** A custom provider is visible only inside its declaring module until exported,
   by token or as the full provider object. Forgetting the export gives the same unresolved-dependency error in
   the consumer.
5. **On Nest 12, an optional marker on a constructor parameter is not inherited.** A subclass with no
   constructor of its own used to inherit `@Optional()` from its parent and receive `undefined`; the
   migration guide says it now fails at boot with an unknown-dependencies error. Declare a constructor in the
   subclass and repeat the marker.
6. **Do not create an interface and a token for a single local helper.** A port earns its token at an external or
   volatile edge, a seam tests need, or a real second implementation.

### 2. A provider belongs to one module
1. **Listing a provider in the `providers` of several modules creates one instance per module.** The
   documentation says it directly: each module would get its own separate instance, with more memory and
   inconsistent state when the service holds any. The visible symptom: a cache, a counter, a connection pool or
   an in-memory map "forgets" what another part of the app wrote, in production only, because a test that builds
   one module sees one instance.
2. **Declare it once, export it, import the module.** Modules are singletons, so every importer of the owning
   module shares the same instance. The consumer's `imports` names the module, never the provider.
3. **A dynamic module's `forRoot()` called twice configures twice.** The documentation states that calling it
   again in another module creates a second, separately configured instance. Call it once, in one module, and
   re-export the module class (not another `forRoot()` call) to share it.
4. **`@Global()` is not the fix.** The documentation says making everything global is not a recommended design.
   Use it for a genuinely application-wide module (configuration, a database connection), registered once in the
   root or a core module, not to avoid writing `imports`.

### 3. Circular dependencies: a design signal
1. **A cycle is two classes that each need the other, between providers or between modules.** Nest cannot
   instantiate either first. The documentation lists `forwardRef()` and `ModuleRef` as the two ways to resolve it
   and says to avoid the cycle where possible.
2. **`forwardRef()` hides the cycle, it does not remove it.** The documentation warns that the instantiation
   order becomes indeterminate and that cycles involving request-scoped providers can leave dependencies
   `undefined`. The runtime symptom is a method call on `undefined` in a constructor or `onModuleInit`, in one
   environment, depending on import order.
3. **Remove the cycle first.** In order: decide which side owns the workflow; extract the third responsibility
   both need into a new provider that depends on neither; replace the reverse synchronous call with an event
   when immediate consistency is not required; give the reading side a narrower query provider. Keep
   `forwardRef()` for a documented, time-boxed transition with the cycle's removal written beside it.
4. **Module cycles are usually a split gone wrong.** Two modules importing each other means the shared part
   belongs in a third module both import.
5. **Barrel files cause cycles too.** The documentation warns against importing a sibling through an `index.ts`
   in the same directory. Import the file, not the barrel, for module and provider classes.
6. **When `undefined` appears with no obvious `forwardRef`**, suspect an import cycle between files: a decorator
   metadata reference to a class not yet defined at load time. Fix the import graph before adding `forwardRef()`.

### 4. `ModuleRef` is not a way to skip the constructor
1. **A service that calls `moduleRef.get(Something)` in a business method has a hidden dependency.** The
   constructor no longer lists what the class needs, a test must build the whole container to run it, and a
   renamed provider fails at the call, not at boot. This is a service locator.
2. **Legitimate uses are narrow:** a framework extension or plugin loader that must find providers it does not
   know at compile time, resolving a scoped provider on demand with `resolve()` (since `get()` cannot return
   transient or request-scoped providers, per the documentation), and lifecycle code that runs once at startup.
3. **`get()` looks in the current module by default.** Finding a provider registered elsewhere needs
   `{ strict: false }`, which then searches globally, so the lookup depends on what happens to be registered
   anywhere. If you need that, you are probably missing an export.
4. **A context id made with `ContextIdFactory.create()` has no `REQUEST` provider.** The documentation notes it is
   `undefined` in such a sub-tree unless registered with `registerRequestByContextId()`. Inside a request, obtain
   the current id with `ContextIdFactory.getByRequest()` instead of creating a new one.

### 5. Request scope bubbles up
1. **A provider that depends on a request-scoped provider is itself request-scoped, and so is its controller,
   all the way up.** The documentation's example: if `CatsService` is request-scoped, `CatsController`
   becomes request-scoped, while `CatsRepository`, which does not depend on it, stays a singleton. Injecting
   `REQUEST` makes the injector request-scoped by itself; declaring it explicitly changes nothing.
2. **The cost is an instance of every affected class per request**, and the documentation says to stay on the
   default singleton unless a provider must be request-scoped (it quotes about 5 percent added latency as the
   ceiling for a well-designed use, not a guarantee). The symptom is latency and memory growth after
   one innocent `@Inject(REQUEST)` in a widely used service, such as the database or a logger.
3. **State that needs request lifetime does not always need request scope.** To read the current user, tenant or
   locale, the documentation points at an `AsyncLocalStorage`-based per-request store, which keeps every
   provider a singleton. Pass an explicit context argument for a single operation.
4. **Some providers should not be request-scoped.** The documentation names Passport strategies and cron
   controllers as providers that must act as singletons. Resolve the scoped dependency on demand instead. For
   gateways the answer depends on the major: on Nest 12 a gateway may depend on request-scoped providers (one
   instance per connected socket, kept for the life of the connection, with the same per-instance cost as over
   HTTP), and the pages read say nothing about earlier majors, so keep a gateway on singletons there.
5. **Singleton state must not hold request data.** A singleton that stores the current user in a field is shared
   by concurrent requests, which is the opposite of the symptom above: one user briefly sees another's data.
6. **Transient scope does not bubble.** A singleton injecting a transient provider receives a fresh instance,
   and stays a singleton.

### 6. Prove the wiring
1. Compile the real module in a test (`Test.createTestingModule({ imports: [RealModule] }).compile()`), so a
   missing export, a wrong token or a cycle fails there, not in a deployed container.
2. For a shared provider, assert identity: resolve it from two consumers' modules and compare references.
3. For custom tokens, override with the same token when mocking. A mock registered under the class instead of
   the `Symbol` is never injected and the real implementation runs (our inference: the testing chapter shows
   overriding by the provider's own token and does not describe the mismatch). To read a request-scoped
   provider in a test use `resolve()`, not `get()`; each call returns a distinct instance unless a fixed
   context id is passed.

## Output / checkpoint
The diff names, for each custom token, where it is declared, registered and exported; each provider is declared
in exactly one module; no new `forwardRef()` without a stated reason and a removal plan; every `ModuleRef` use
is one of the section 4.2 cases; any new request-scoped provider lists the classes it makes request-scoped. The
module-compilation test from section 6 passes.

## Guardrails
- Never `new Service()` to escape a DI error: it bypasses the container (`skills/nestjs-node-conventions`
  section 1.3).
- Never add `forwardRef()` as the first response to a boot error; look at the cycle (section 3.3) first.
- Never mark a widely injected provider request-scoped without listing what it drags with it.
- Never register the same provider in a second module to "make the error go away".
- Version note: statements follow the official documentation as of the Nest 12 migration guide, read
  2026-10-08. Behaviour on older majors was not checked.

## Origin
Written from the official NestJS documentation (MIT): the dependency-injection / custom-providers chapter
(interfaces, abstract classes, `Symbol` tokens, exporting custom providers), the modules chapter (shared
modules, separate instances, `@Global()`, dynamic modules and `forRoot()`), the module-reference chapter,
the circular-dependency chapter and the provider-scopes (injection scopes) chapter, read 2026-10-08.
Cross-checked against the dependency-injection and module-boundary references of an MIT NestJS agent-skill
catalogue (amirtaherkhani, read 2026-10-08), from which the cycle-repair order and the "service location is
for framework extensions only" framing were adapted, rewritten. 🟡 Maturity: written from documentation,
never run on a real project.

Verification pass 2026-10-20: re-opened the documentation repository (MIT, its `LICENSE` re-read) content for the
dependency-injection, modules, circular-dependency, provider-scopes, module-reference, unit-testing and
websocket gateway pages and the 11-to-12 migration guide. Confirmed: §1.1 to §1.4 (the abstract-class token
needs no `@Inject()`; Symbol tokens avoid string collisions; export by token or provider object), §2.1 to §2.4
(separate instance per declaring module, `forRoot()` twice, global modules not recommended as a design),
§3.1, §3.2, §3.4, §3.5 (barrel files), §4.2 to §4.4, §5.1, §5.3, §5.6. Corrected: §5.4 (the gateway limit
no longer holds on Nest 12). Added: §1.5 (`@Optional()` no longer inherited, from the migration guide) and the
~5 percent figure (§5.2). Still ours, not stated on a page: §3.3 (the repair order beyond the page's "avoid
the cycle"), §3.6, §4.1 (service locator reasoning), §5.5, the §6 test recipes, and the symptoms described
for each trap.

Independent verification 2026-10-21: 12 checked, 12 matched, 0 corrected, 0 unverified. Includes the Nest 12 request-scoped gateway statement (§5.4), the `@Optional()` inheritance change (§1.5) and the ~5 percent figure, all re-read against the Nest documentation repository.
