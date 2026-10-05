---
name: langchain
description: Apply when building LangChain pipelines, LCEL chains, agents, or retrieval-augmented generation systems.
license: MIT
version: 1.0.0
tokens_target: 2200
triggers:
  - langchain
  - lcel chain
  - agent framework
loads_after: [python]
supersedes: []
---

# Sub-Skill: LangChain / Agent Framework Conventions

**Purpose:** Prevent common LangChain mistakes — deprecated chain classes, missing retry/timeout guards, unsafe prompt handling, and unobservable pipelines.

---

## Rules

### Chain Construction

1. **Use LCEL pipe syntax.** Always use the LCEL pipe operator (`|`) to compose runnables instead of deprecated constructor-based chain classes (`LLMChain`, `SequentialChain`, `TransformChain`). Reference: ERR-2026-026
2. **Avoid legacy chain imports.** Never import from `langchain.chains.llm` or `langchain.chains.sequential`; use `langchain_core.runnables` and `langchain_core.prompts` instead.
3. **Prefer RunnablePassthrough for identity steps.** Use `RunnablePassthrough` to thread context through a chain without mutation rather than writing a lambda that returns its input unchanged.
4. **Use RunnableParallel for fan-out.** Prefer `RunnableParallel` over manually calling multiple chains and merging dicts; it expresses intent and enables parallel execution.

### Prompts & Output Parsers

5. **Use typed output parsers.** Always attach an output parser (`PydanticOutputParser`, `JsonOutputParser`, `StrOutputParser`) to chains that produce structured data; never parse raw LLM strings manually downstream.
6. **Inject format instructions via partial.** Use `prompt.partial(format_instructions=parser.get_format_instructions())` to bind parser instructions into the prompt template rather than hard-coding them in the template string.
7. **Separate system and human messages.** Use `ChatPromptTemplate.from_messages([("system", ...), ("human", ...)])` instead of a single `PromptTemplate` for chat models; mixing roles in one string breaks structured output.

### Chat Models vs LLMs

8. **Prefer ChatModel over LLM.** Always use `ChatOpenAI`, `ChatAnthropic`, or equivalent chat-model classes for new code; the base `OpenAI` LLM class is deprecated for most use cases and lacks tool-calling support.
9. **Pin model name explicitly.** Never rely on the default model name in a chat model constructor; always pass `model="gpt-4o"` (or equivalent) so upgrades are intentional.

### Memory & State

10. **Use RunnableWithMessageHistory for stateful chains.** Prefer `RunnableWithMessageHistory` over manual history management or deprecated `ConversationChain`; it integrates cleanly with LCEL and supports async.
11. **Scope memory by session ID.** Always pass a `session_id` key when constructing `RunnableWithMessageHistory` to prevent cross-user memory leakage in multi-tenant services.

### Tools & Agents

12. **Define tools with @tool decorator.** Use the `@tool` decorator (or `StructuredTool.from_function`) with a typed signature and docstring; never pass raw callables to an agent without a schema.
13. **Use create_tool_calling_agent for modern agents.** Prefer `create_tool_calling_agent` + `AgentExecutor` over deprecated `initialize_agent`; it uses native tool-calling APIs and avoids ReAct string parsing.
14. **Cap agent iterations.** Always set `max_iterations` and `max_execution_time` on `AgentExecutor` to prevent runaway loops; default is unbounded.

### Retrieval & Vector Stores

15. **Use retrieval chains via LCEL.** Build RAG pipelines with `retriever | format_docs | prompt | llm | parser` rather than `RetrievalQA.from_chain_type`; the latter is deprecated and hides the retrieval step.
16. **Ensure document loaders are lazy.** Prefer `.lazy_load()` over `.load()` for large corpora to avoid loading all documents into memory at once.

### Reliability & Observability

17. **Wrap LLM calls with retry.** Use `.with_retry(stop_after_attempt=3, wait_exponential_jitter=True)` on any runnable that calls an external API; never let transient rate-limit errors propagate uncaught.
18. **Set request timeout.** Always pass `request_timeout` (or `timeout`) to chat model constructors; omitting it allows indefinitely hanging requests.
19. **Attach callbacks for observability.** Use `callbacks=[LangSmithTracer()]` or equivalent on chains in production; never ship a pipeline with no tracing so failures are diagnosable.
20. **Count tokens before sending.** Before sending large contexts, use `llm.get_num_tokens(text)` or a tiktoken counter to verify the payload fits within the model's context window.

### Security

21. **Sanitize user input before prompt injection.** Never interpolate raw user strings directly into system prompts; use a dedicated input variable in the prompt template and validate/strip control characters before binding.
22. **Disable dangerous tools in untrusted contexts.** Avoid giving agents tools with filesystem or shell access when processing untrusted input; scope tool permissions to the minimum required.

### Caching & Cost

23. **Enable semantic caching in dev.** Use `set_llm_cache(InMemoryCache())` during development and `SQLiteCache` in staging to avoid redundant API calls and reduce cost during iteration.

---

## See also

- `skills/python/SKILL.md`
- `skills/error-log/SKILL.md`

---
