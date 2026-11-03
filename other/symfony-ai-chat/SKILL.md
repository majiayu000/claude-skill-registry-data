---
name: symfony-ai-chat
description: Reference for the Symfony AI Chat component (symfony/ai-chat) — Chat over an Agent with persisted conversation history, MessageStoreInterface and ManagedStoreInterface, the bundled stores (session, cache, Doctrine DBAL, Redis, MongoDB, Meilisearch, SurrealDB, Cloudflare KV, Pogocache, InMemory), writing a custom store, streaming persistence, the ai:message-store console commands, and the 0.12 vs 0.13 stream() change. Use whenever the work involves Symfony\AI\Chat classes, persisting an LLM conversation, or building a chat history store in a Symfony app.
---

# Symfony AI — Chat component

`composer require symfony/ai-chat`. Thin layer: an `Agent` plus a message store. It owns the load → append → call → append → save cycle so your controller does not.

```php
use Symfony\AI\Agent\Agent;
use Symfony\AI\Chat\Chat;
use Symfony\AI\Chat\InMemory\Store as InMemoryStore;
use Symfony\AI\Platform\Message\Message;

$agent = new Agent($platform, 'gpt-4o-mini');
$chat  = new Chat($agent, new InMemoryStore());

$chat->initiate(new MessageBag(Message::forSystem('You are a helpful assistant.')));

$assistantMessage = $chat->submit(Message::ofUser('Hello'));
```

## The interfaces

```php
interface ChatInterface
{
    public function initiate(MessageBag $messages): void;
    public function submit(UserMessage $message): AssistantMessage;
    public function stream(UserMessage $message): \Generator;   // yields DeltaInterface
}

interface MessageStoreInterface
{
    public function save(MessageBag $messages): void;
    public function load(): MessageBag;
}

interface ManagedStoreInterface
{
    public function setup(array $options = []): void;
    public function drop(): void;
}
```

`Chat::__construct(AgentInterface $agent, MessageStoreInterface&ManagedStoreInterface $store)` — the **intersection type is required**, so a store passed to `Chat` must implement both. A store used only for reading and writing can implement `MessageStoreInterface` alone, but it will not fit `Chat`.

`initiate()` is `drop()` then `save()` — it **wipes the conversation**. Call it once when starting a new one, never per request, or the history is destroyed on every message.

## What submit() actually does

```php
public function submit(UserMessage $message): AssistantMessage
{
    $messages = $this->store->load();
    $messages->add($message);

    $result = $this->agent->call($messages);          // 0.13: ->getResult()

    $assistantMessage = Message::ofAssistant($result);
    $assistantMessage->getMetadata()->merge($result->getMetadata());
    $messages->add($assistantMessage);

    $this->store->save($messages);

    return $assistantMessage;
}
```

Two things follow:

1. **`save()` receives the whole bag, every time.** A store that appends will duplicate; a store that replaces is the model the component expects. If your store rewrites rows, `save()` after `submit()` is a full rewrite of the conversation — do not also save the bag yourself afterwards.
2. **`Agent::call()` is invoked with no options.** There is nowhere in `Chat` to pass `temperature`, `num_ctx`, `think`, or anything else. The only place to set them is an `InputProcessorInterface` on the agent:

   ```php
   final class DefaultInvocationOptions implements InputProcessorInterface
   {
       public function __construct(private readonly array $defaults) {}

       public function processInput(Input $input): void
       {
           $input->setOptions([...$this->defaults, ...$input->getOptions()]);
       }
   }
   ```

## Streaming

```php
foreach ($chat->stream(Message::ofUser('Tell me a story')) as $delta) {
    if ($delta instanceof TextDelta) { echo $delta; }
}
```

Once the stream is **fully consumed**, the assistant message is persisted automatically along with the user message — no extra code, but also no persistence if the client disconnects mid-stream or you `break` out of the loop.

The persisted turn is what the provider produced, thinking blocks and signatures included, so the stored conversation replays correctly on a later turn. From 0.13 that means a stored assistant message can hold structured content, not just text — **code reading persisted history must expect that**.

> Streaming with the HttpFoundation `Session` store is explicitly **not recommended** — the session is written at the end of the request, which does not fit a long-lived streamed response.

### 0.12 vs 0.13

| | 0.12 | 0.13 |
|---|---|---|
| `stream()` mechanism | `$result` is a `StreamResult`; a `ChatStreamListener` is attached to it and persists on completion | `Chat` consumes the agent's `Execution` itself: `yield from $execution->asStream()`, then builds and saves the assistant message |
| `ChatStreamListener` | exists | **removed** |
| `submit()` | `$this->agent->call($messages)` returns a `ResultInterface` | `$this->agent->call($messages)->getResult()` |

The public `ChatInterface` is unchanged, so calling code is unaffected — only a custom `ChatInterface` implementation or anything touching `ChatStreamListener` breaks.

## Bundled stores

Under `Symfony\AI\Chat\Bridge\<Name>` (plus `Chat\InMemory\Store`). Separate Composer packages where marked.

| Store | Package | Lifetime |
|---|---|---|
| `InMemory\Store` | `symfony/ai-chat` | current process |
| `Bridge\Session\MessageStore` | `symfony/ai-session-message-store` | current HTTP session |
| `Bridge\Cache\MessageStore` | `symfony/ai-cache-message-store` | cache TTL |
| `Bridge\Doctrine\DoctrineDbalMessageStore` | `symfony/ai-doctrine-message-store` | long-term |
| `Bridge\Redis` `Bridge\MongoDb` `Bridge\Meilisearch` `Bridge\SurrealDb` `Bridge\Cloudflare` `Bridge\Pogocache` | `symfony/ai-chat` | long-term |

```php
new SessionStore($requestStack);
new CacheStore(new FilesystemAdapter(), 'chat', 3600);
new DoctrineDbalMessageStore($connection, 'chat_messages');
```

Constructor arguments differ per bridge — read the class rather than guessing.

## Writing your own store

The realistic reason to write one: the bundled stores serialize a `MessageBag` as an opaque blob. If you need the conversation as **queryable rows** — list a user's conversations, show titles, paginate — you write your own over your entities.

```php
class ConversationStore implements MessageStoreInterface, ManagedStoreInterface
{
    private ?Conversation $conversation = null;

    public function setup(array $options = []): void
    {
        // $options is yours: conversation_id, system_prompt, user id, …
        // load an existing conversation or create one
    }

    public function drop(): void   { /* delete messages, then the conversation */ }
    public function save(MessageBag $messages): void { /* replace all rows */ }
    public function load(): MessageBag { /* rebuild Message objects from rows */ }
}
```

Points that bite when hand-rolling one:

- **`setup()` takes an arbitrary options array** and the component never inspects it. That is the hook for "which conversation" — `Chat` itself has no concept of conversation identity.
- **Rebuild the right message class on load.** `Message::forSystem()` / `ofUser()` / `ofAssistant()` / `ofToolCall()` by stored role; a bag of user messages is not a conversation.
- **Multimodal content does not survive a `TEXT` column.** `UserMessage` content is a list of `Text`/`Image`/`Audio` objects. Either give the row a JSON column with a discriminated shape, or store a tagged payload and reconstruct with `Image::fromDataUrl()` / `Audio::fromDataUrl()` on load. Flattening to a string silently drops every attachment on the next turn.
- **Doctrine associations must be set on the owning side.** Use the entity's `addMessage()` helper (which sets both sides) rather than only `$message->setConversation()`, or the in-memory collection reads back empty and `drop()` hits the FK.
- **`save()` replaces.** Delete the existing rows before writing the incoming bag, and take the collection snapshot (`->toArray()`) before mutating it.
- Persisting each turn is a full rewrite. Fine for chat-sized histories; if it stops being fine, diff against the loaded bag instead of adding an append path the component will not use.

## Console commands (AI Bundle)

```yaml
ai:
    message_store:
        cache:
            symfonycon:
                service: 'cache.app'
                key: 'youtube'
    chat:
        youtube:
            agent: 'ai.agent.youtube'
            message_store: 'ai.message_store.cache.youtube'
```

```bash
php bin/console ai:message-store:setup symfonycon
php bin/console ai:message-store:drop symfonycon
```

Service ids: `ai.message_store.<type>.<name>`, `ai.chat.<name>`. The commands call `ManagedStoreInterface::setup()` / `drop()`, so a store that needs a table or index gets one without a migration.

## Debugging

`TraceableChat` and `TraceableMessageStore` decorate for the profiler. `MessageNormalizer` is the serializer the bridges use to turn a `MessageBag` into a storable payload — reuse it in a custom store rather than inventing a format, unless you specifically want queryable columns.

## Gotchas

- **`initiate()` drops everything.** New conversations only.
- **`Chat` requires `MessageStoreInterface&ManagedStoreInterface`.** Both.
- **No options reach the model through `Chat`.** Input processor on the agent, or use the Platform directly.
- **Streaming persists only on full consumption.** A disconnected client loses the turn.
- **Session store + streaming don't mix.**
- **`save()` gets the entire bag.** Replace, don't append.
- **0.13 stores structured assistant content** (thinking parts), not just text — a store that assumes `string` will break on upgrade.
- Skipping `Chat` entirely and driving `$platform->invoke()` plus your own store is a legitimate choice when you want SSE with your own frame shape and per-request options; you then own the append-and-save cycle, which is about ten lines.

## Siblings

`symfony-ai-agent` skill (the layer below: tool calling, processors, memory), `symfony-ai-platform` skill (messages, results, streaming).

Examples in the monorepo: `examples/chat/persistent-chat*.php` (one per backend), `examples/chat/stream-chat.php`, `examples/commands/message-stores.php`.
