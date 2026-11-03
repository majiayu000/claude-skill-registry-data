---
name: symfony-ai-agent
description: Reference for the Symfony AI Agent component (symfony/ai-agent) — Agent over a Platform, the tool-calling loop, Toolbox and #[AsTool], JSON-schema tool parameters, tool lifecycle events and human-in-the-loop denial, input/output processors, memory providers, MultiAgent handoffs (incl. a decision-model orchestrator), SpeechAgent, MockAgent, RAG via SimilaritySearch, the AI Bundle agent config, and the 0.12 vs 0.13 Execution rewrite. Use whenever the work involves Symfony\AI\Agent classes, tool calling from a Symfony app, agent processors, multi-agent routing, or wiring symfony/ai-agent into a project.
---

# Symfony AI — Agent component

`composer require symfony/ai-agent`. An `Agent` is a `Platform` plus: a fixed model, input/output processors, and the tool-calling loop. Everything under it is the Platform component — read `symfony-ai-platform` for `MessageBag`, `DeferredResult`, streaming deltas and options.

```php
use Symfony\AI\Agent\Agent;
use Symfony\AI\Platform\Bridge\OpenAi\Factory;

$agent = new Agent($platform, 'gpt-4o-mini');

echo $agent->call('Hello, how are you?')->getContent();
```

`call()` accepts a plain string, a `UserMessage`, or a `MessageBag` — the first two are normalized by `InputNormalizer::toMessageBag()`. `getName()` returns the agent's name (default `'agent'`), used for debugging and multi-agent routing.

## ⚠️ Two shapes — check `composer.lock` first

The constructor and return type changed in 0.13. Everything below is marked.

### 0.12 (and earlier)

```php
public function __construct(
    PlatformInterface $platform,
    string $model,
    iterable $inputProcessors = [],
    iterable $outputProcessors = [],
    string $name = 'agent',
);

public function call(string|MessageBag|UserMessage $input, array $options = []): ResultInterface;
```

Tool calling is wired as a processor pair — the same `AgentProcessor` instance in both slots:

```php
$processor = new AgentProcessor($toolbox, includeSources: true, maxToolCalls: 75);
$agent = new Agent($platform, $model, [$processor], [$processor]);
```

`call()` runs eagerly and returns a `ResultInterface`. `->getContent()` reads it.

### 0.13+

```php
public function __construct(
    PlatformInterface $platform,
    string $model,
    iterable $inputProcessors = [],
    iterable $outputProcessors = [],
    string $name = 'agent',
    ?ToolboxInterface $toolbox = null,
    ?ToolExecutorInterface $toolExecutor = null,   // default SequentialToolExecutor
    ?int $maxToolCalls = 50,
    bool $excludeToolMessages = false,
    bool $includeSources = false,
    ?EventDispatcherInterface $eventDispatcher = null,
);

public function call(string|MessageBag|UserMessage $input, array $options = []): Execution;
```

`Toolbox\AgentProcessor` and `Toolbox\StreamListener` are **gone**. Pass the toolbox to the agent:

```php
$agent = new Agent($platform, $model, toolbox: $toolbox, maxToolCalls: 75, includeSources: true);
```

Migration diff:

```diff
-$processor = new AgentProcessor($toolbox, includeSources: true, maxToolCalls: 75);
-$agent = new Agent($platform, $model, [$processor], [$processor]);
+$agent = new Agent($platform, $model, toolbox: $toolbox, maxToolCalls: 75, includeSources: true);
```

Consequences of the rewrite:

- The agent is **lazy** — it does not run until the execution is consumed. Side effects and exceptions surface at `getResult()`/`getContent()`/iteration, not at the `call()` line.
- `$agent->call(...) instanceof TextResult` no longer works; `getResult()` first.
- Output processors now see the final assembled result, and input processors run **once per agent call** instead of once per tool-calling round.
- A tool-calling round adds **one** assistant message per turn (text + thinking + tool calls together) instead of splitting it. Tests asserting on message-bag shape need updating.
- Custom `AgentInterface` implementations and decorators must return an `Execution`:

  ```php
  public function call(string|MessageBag|UserMessage $input, array $options = []): Execution
  {
      return new Execution(function (): \Generator {
          yield new Result($someResult);
      });
  }
  ```

## Execution (0.13+)

The execution *is* the result, plus an observation channel.

```php
$text   = $agent->call('Hello')->getContent();     // eager, unchanged from 0.12 in practice
$result = $agent->call('Hello')->getResult();
$answer = $agent->call('Hello')->asText();
```

Typed narrowing accessors mirror `DeferredResult`: `asText()` `asObject()` `asBinary()` `asFile()` `asDataUri()` `asToolCalls()` `asStream()`, and they throw when the agent produced something else. A multi-part result holding a single part of the expected type (a reasoning part next to the answer) narrows to that part.

Observe a run:

```php
use Symfony\AI\Agent\Execution\Update\Progress;
use Symfony\AI\Agent\Execution\Update\Result;

foreach ($agent->call('What time is it?') as $update) {
    if ($update instanceof Progress) { echo $update->getMessage(); }   // "Invoking model.", 'Executing tool "clock".'
    if ($update instanceof Result)   { echo $update->getResult()->getContent(); }
}

// or without driving the loop yourself
$result = $agent->call('What time is it?')
    ->onProgress(fn (Progress $p) => $logger->info($p->getMessage()))
    ->getResult();
```

Callbacks fire however the execution is consumed, so they observe a run whose result is handled elsewhere. **Reading is idempotent; iterating is once-only** — an execution runs side effects, so call `call()` again for a new one.

Streaming:

```php
foreach ($agent->call('Tell me a story.', ['stream' => true])->asTextStream() as $delta) {
    echo $delta->getText();
}
```

`getContent()` under `stream` yields the platform's deltas. Once drained, the execution resolves normally — `getResult()` gives the assembled answer, `asObject()` works on a streamed structured output. Iterating instead reports each delta as a `Progress` of stage `delta` with the delta as payload. Streaming and tool calling compose: a streamed tool call is executed and the next round streams into the same execution.

## Tools

```php
use Symfony\AI\Agent\Toolbox\Attribute\AsTool;

#[AsTool('company_name', 'Provides the name of your company')]
final class CompanyName
{
    public function __invoke(): string { return 'ACME Corp.'; }
}

$toolbox = new Toolbox([new CompanyName()]);
$agent = new Agent($platform, $model, toolbox: $toolbox);          // 0.13
```

`AsTool` is repeatable, so one class can expose several tools via `method:`:

```php
#[AsTool(name: 'weather_current',  description: 'get current weather',  method: 'current')]
#[AsTool(name: 'weather_forecast', description: 'get weather forecast', method: 'forecast')]
final readonly class OpenMeteo { /* current(), forecast() */ }
```

Signature: `AsTool(string $name, string $description, string $method = '__invoke', array $metadata = [])`.

Return value must end as a string; arrays and `JsonSerializable` objects are JSON-encoded for you.

`maxToolCalls` caps iterations per agent call — default `50`, exceeded throws `MaxIterationsExceededException`, `null` disables the cap. The loop runs until the model answers without requesting more tools.

### Parameters and JSON Schema

The schema is derived from the method signature plus `@param` PHPDoc. Refine it with `#[Schema]` on arguments:

```php
use Symfony\AI\Platform\Contract\JsonSchema\Attribute\Schema;

public function __invoke(
    #[Schema(pattern: '^[a-z0-9]{5}$')] string $name,       // no PCRE delimiters
    #[Schema(minimum: 0, maximum: 10)] int $number,
    #[Schema(enum: ['tech', 'business', 'science'])] array $categories,
    #[Schema(ref: __DIR__.'/schema.json')] array $data,
): string
```

`#[Schema]` only *describes* the constraint to the model. To actually reject bad arguments, register `Toolbox\EventListener\ValidateToolCallArgumentsListener`.

### Tool factories

- `ReflectionToolFactory` (default) — reads `#[AsTool]`.
- `MemoryToolFactory` — register third-party classes you cannot annotate: `->addTool(Clock::class, 'clock', 'Get the current date and time', 'now')`.
- `ChainFactory` — combine them; **first factory wins**, so a `MemoryToolFactory` in front overrides an annotated tool's config.

```php
$toolbox = new Toolbox([...], new ChainFactory($metadataFactory, new ReflectionToolFactory()));
```

### Agent as a tool

```php
$subagent = new Subagent($agent);
$factory = (new MemoryToolFactory())->addTool($subagent, 'research_agent', 'Meaningful description');
$toolbox = new Toolbox([$subagent], $factory);
```

### Fault tolerance

`FaultTolerantToolbox` decorates a toolbox and converts exceptions (wrong tool name, runtime errors) into readable messages for the model instead of blowing up the request:

```php
$agent = new Agent($platform, $model, toolbox: new FaultTolerantToolbox($innerToolbox));
```

To surface a *specific* message, throw an exception implementing `ToolExecutionExceptionInterface::getToolCallResult(): string`.

### Filtering

Per call, by name:

```php
$agent->call($messages, ['tools' => ['tavily_search']]);
```

Or shape the toolset before it reaches the model using tool metadata:

```php
#[AsTool('delete_product', 'Delete a product', method: 'delete', metadata: ['needs_confirmation' => true])]

$readOnly = array_filter(
    iterator_to_array($toolbox->getTools()),
    static fn (Tool $tool): bool => false === $tool->getMetadataValue('needs_confirmation', true),
);
```

Metadata is arbitrary application data carried through to `Tool::getMetadata()` / `getMetadataValue()`. It **describes**, it does not enforce — a listener has to act on it, and should fail closed so a tool added later without metadata is not silently exempt.

### Lifecycle events

| Event | When | What you can do |
|---|---|---|
| `ToolCallRequested` | before execution | `$event->deny($reason)` blocks and returns the reason to the model; `$event->setResult(ToolResult)` skips execution with a custom result |
| `ToolCallArgumentsResolved` | args parsed | notify the client which tool is running |
| `ToolCallSucceeded` | after a call | read `$event->getResult()` |
| `ToolCallFailed` | on exception | read `$event->getException()` |
| `ToolCallsExecuted` | after the whole batch | `$event->setResult(...)` short-circuits the next model call entirely |

Human-in-the-loop is `ToolCallRequested` + `deny()`. `ToolCallsExecuted` + `setResult()` is how you skip a round-trip when a tool's output *is* the answer.

### Sources

Enable `includeSources: true` on the agent, then have the tool implement `HasSourcesInterface` with `HasSourcesTrait` and call `$this->addSource(new Source($name, $reference, $content))`. Read them back from result metadata:

```php
foreach ($result->getMetadata()->get('sources', []) as $source) { /* … */ }
```

### Keeping tool chatter out of the bag

`excludeToolMessages: true` removes the assistant-with-tool-calls and tool-result messages from *your* `MessageBag` after the call. The model still saw them; the history you persist stays clean.

## Input / output processors

```php
final class MyProcessor implements InputProcessorInterface
{
    public function processInput(Input $input): void
    {
        $options = $input->getOptions();
        $options['foo'] = 'bar';
        $input->setOptions($options);

        $input->getMessageBag()->append(Message::ofAssistant('…'));
    }
}
```

`Input` exposes `getModel()/setModel()`, `getMessageBag()/setMessageBag()`, `getOptions()/setOptions()`. `Output` exposes `getModel()`, `getResult()/setResult()`, `getMessageBag()`, `getOptions()` — the bag and options are read-only there.

A processor implementing `AgentAwareInterface` (with `AgentAwareTrait`) receives the agent, so it can call back into it.

Built-in: `SystemPromptInputProcessor` (accepts a string, `Stringable`, `TranslatableInterface` or a `File`; **skips injection if the bag already has a system message**; optionally appends tool definitions when given a toolbox), `ModelOverrideInputProcessor`, `MemoryInputProcessor`.

**The processor trick that matters:** `Chat::submit()` calls `Agent::call()` with no options, so an input processor is the only place to set per-call model options on the Agent path.

```php
final class DefaultInvocationOptions implements InputProcessorInterface
{
    public function __construct(private readonly array $defaults) {}

    public function processInput(Input $input): void
    {
        $input->setOptions([...$this->defaults, ...$input->getOptions()]);   // explicit wins
    }
}
```

In a Symfony app: `#[AsInputProcessor]` / `#[AsOutputProcessor]`, both taking an `agent:` argument to scope the processor to one agent.

## Memory

Memory providers inject context into the **system prompt** — they do not touch your application logic or the stored history.

```php
$memory = new MemoryInputProcessor([
    new StaticMemoryProvider([
        'The user is allergic to nuts',
        'The user prefers brief explanations',
    ]),
]);

$agent = new Agent($platform, $model, [$memory]);
```

Providers: `StaticMemoryProvider` (fixed facts), `EmbeddingProvider($platform, $embeddingsModel, $store)` (vector-store lookup keyed on the current user message). Implement `MemoryProviderInterface::load(Input $input): Memory[]` for your own.

Disable per call with `['use_memory' => false]`. The processor stashes the original system prompt in metadata under `memory_original_system_prompt`, so re-running on the same bag recombines rather than nesting.

## RAG

```php
$retriever = new Retriever($store, $vectorizer);
$toolbox = new Toolbox([new SimilaritySearch($retriever)]);
$agent = new Agent($platform, $model, toolbox: $toolbox);
```

Pair it with a system prompt that forbids answering outside the tool ("answer only using the similarity_search tool; if you cannot find an answer, say so"), or the model will happily fill gaps from its own weights. Needs `symfony/ai-store`.

## MultiAgent

```php
$multi = new MultiAgent(
    orchestrator: $analyzerAgent,
    handoffs: [
        new Handoff(to: $technicalAgent, when: ['code', 'debug', 'refactor']),
        new Handoff(to: $billingAgent,   when: ['payment', 'invoice', 'subscription']),
    ],
    fallback: $generalAgent,
    name: 'customer-service',
);
```

The orchestrator is called once with a built selection prompt (`User question: "…"`, one `- <agent name>: <when, when>` line per handoff, a last line for the fallback) and `response_format: Handoff\Decision::class` (`agentName`, `reasoning`). `when` is a keyword list — prompt material, not a matcher. At least one handoff is required or the constructor throws. What happens next:

| Orchestrator result | Who answers | With what input |
|---|---|---|
| not a `Decision` object | the orchestrator itself | full original messages |
| `Decision` with `agentName: ''` | `fallback` | full original messages |
| name matching no handoff's `getName()` | `fallback` | full original messages |
| name of a handoff target | that agent (`Progress` stage `handoff`) | **only the first user message** — history, later turns and system messages are dropped |

"First" is literal: `MultiAgent` uses `MessageBag::getUserMessage()`, which returns the **first** `UserMessage`. Behind `Chat` (full history in the bag) both routing and the handoff see turn one, not the new question. For multi-turn routing, call `MultiAgent` with only the latest user message, or route yourself.

`MultiAgent` implements `AgentInterface`, so it composes anywhere an agent does — and the orchestrator can be any `AgentInterface`, not only an LLM `Agent`.

### Decision-model orchestrator

A decision model (`symfony-ai-platform` skill → Decision models) cannot be an agent's model, but it can route: wrap it in a small `AgentInterface` that turns the selection prompt into a `ChoiceQuestion` and returns a `Decision`. Faster and cheaper than an LLM picking, and it comes with a confidence to gate on.

```php
final class DecisionOrchestrator implements AgentInterface
{
    public function __construct(private PlatformInterface $platform, private string $model, private float $minConfidence = 0.6) {}

    public function call(string|MessageBag|UserMessage $input, array $options = []): Execution
    {
        return new Execution(function () use ($input): \Generator {
            $prompt = InputNormalizer::toMessageBag($input)->getUserMessage()->asText();
            // ponytail: parses MultiAgent's prompt text; a change there breaks this, so cover it with a test that runs a real MultiAgent
            preg_match('/User question: "(.*)"\n\nAvailable agents/s', $prompt, $question);
            preg_match_all('/^- ([^:\n]+): (.+)$/m', $prompt, $agents);

            $choice = $this->platform->invoke($this->model, new Evaluation(['request' => $question[1]], [
                'agent' => new ChoiceQuestion('Which agent should handle `request`?', array_combine($agents[1], $agents[2])),
            ]))->asObject(Answers::class)->getChoice('agent');

            $name = $choice->getConfidence() >= $this->minConfidence ? $choice->getChoice() : '';   // '' → fallback
            yield new ResultUpdate(new ObjectResult(new Decision($name, sprintf('confidence %.2f', $choice->getConfidence()))));
        });
    }

    public function getName(): string { return 'decision_orchestrator'; }
}
```

The fallback line is one of the options, so the model can pick it directly; low confidence also lands there. The bundle prefixes every `multi_agent` orchestrator/handoff/fallback name with `ai.agent.` unless it already starts with it, so a plain class id does not resolve: give the service an `ai.agent.` id (`#[AsAlias('ai.agent.decision_orchestrator')]`) and set `orchestrator: 'decision_orchestrator'`, or construct `MultiAgent` yourself. Test it with `MockPlatformFactory` returning `new ObjectResult(new Answers(['agent' => new ChoiceAnswer(…)]))`: one test at high confidence (routes to the handoff), one at low (fallback).

## SpeechAgent

Decorator adding STT on input and/or TTS on output to any agent.

```php
$speechAgent = new SpeechAgent(
    $agent,
    new SpeechConfiguration(ttsModel: 'eleven_multilingual_v2', ttsOptions: ['voice' => '…'], sttModel: 'whisper-1'),
    speechToTextPlatform: $openAiPlatform,
    textToSpeechPlatform: $elevenLabsPlatform,
);

$answer = $speechAgent->call(new MessageBag(Message::ofUser(Audio::fromFile('audio.mp3'))));

echo $answer->getMetadata()->get('text');   // the LLM's text
$answer->asFile('/tmp/speech.mp3');         // the audio
```

STT only fires when the latest user message actually carries audio content. With TTS configured the return value is the `BinaryResult` — **the text is only in metadata under `text`**, which is the easy thing to miss.

## Testing

```php
$agent = new MockAgent([
    'What is Symfony?'      => 'Symfony is a PHP web framework',
    'Tell me about caching' => 'Symfony provides powerful caching',
]);

$agent->assertCallCount(1);
$agent->assertCalledWith('What is Symfony?');
$agent->getCalls(); $agent->getLastCall(); $agent->reset();
```

Also `MockResponse` objects and callables for dynamic answers. For platform-level doubles (`MockPlatformFactory`, cassettes; `InMemoryPlatform` is gone in 0.15) see the `symfony-ai-platform` skill.

## In a Symfony app (AI Bundle)

```yaml
ai:
    agent:
        rag:
            platform: 'ai.platform.azure.gpt_deployment'
            model: 'gpt-4o-mini'
            memory: 'You have access to conversation history and user preferences'
            prompt:
                text: 'You are a helpful assistant.'
                include_tools: true
            tools:
                - 'Symfony\AI\Agent\Bridge\SimilaritySearch\SimilaritySearch'   # #[AsTool] service
                - service: 'App\Agent\Tool\CompanyName'                          # un-annotated service
                  name: 'company_name'
                  description: 'Provides the name of your company'
                  method: 'foo'
                - agent: 'research'                                              # an agent as a tool
                  name: 'wikipedia_research'
                  description: 'Can research on Wikipedia'
        research:
            platform: 'ai.platform.anthropic'
            model: 'claude-3-7-sonnet-latest'
            tools: ['Symfony\AI\Agent\Bridge\Wikipedia\Wikipedia']
            fault_tolerant_toolbox: false      # default true
            max_tool_calls: 75                 # default 50; null disables
            exclude_tool_messages: true        # default false
    multi_agent:
        customer_service:
            orchestrator: 'analyzer'
            handoffs:
                tech_support: ['error', 'bug', 'crash']
                billing: ['payment', 'invoice']
            fallback: 'general_support'
```

Service id is `ai.agent.<key>`. Orchestrator, handoff and fallback names are auto-prefixed with `ai.agent.` (unless already prefixed). **Tools are opt-in** — an agent with no `tools:` key gets none; `tools: true` injects all, `tools: false` is explicit none.

Bundle rename in 0.13: `keep_tool_messages` → `exclude_tool_messages`. The old name was inverted against its behavior since 0.4, so `keep_tool_messages: true` was in fact *excluding* them.

## Gotchas

- **0.13 `call()` is lazy.** A result never read means the agent never ran — including its tool side effects.
- **The toolbox is not a processor any more** (0.13). Passing `new AgentProcessor(...)` will fatal; passing `toolbox:` on 0.12 will be ignored.
- **`SystemPromptInputProcessor` is a no-op when the bag already has a system message.** Intended, and a common "my prompt is ignored" report.
- **`maxToolCalls` is per agent call, not per conversation.** The default 50 is a runaway guard, not a budget.
- **`#[Schema]` does not validate.** Register `ValidateToolCallArgumentsListener`.
- **`FaultTolerantToolbox` hides real bugs** as friendly text to the model. Useful in production, painful while developing a tool — unwrap it when debugging.
- **`ChainFactory` order is priority.** First factory wins.
- **Tool metadata does not gate anything.** Only a `ToolCallRequested` listener does.
- **`Message::ofAssistant($result)`** — pass the result object, not `->getContent()`, so thinking blocks and provider signatures survive into the next turn.
- **Streaming + `Chat`**: see the `symfony-ai-chat` skill; `Chat::stream()` changed shape in 0.13.

## Siblings

`symfony-ai-platform` skill (the layer below: messages, results, streaming, contracts), `symfony-ai-chat` skill (conversation persistence on top). Also `symfony/ai-store` (vector stores, RAG), `symfony/ai-bundle` (DI), `symfony/mcp-bundle`.

Examples in the monorepo: `examples/agent/`, `examples/toolbox/`, `examples/multi-agent/`, `examples/memory/`, `examples/rag/`, `examples/speech/`.
