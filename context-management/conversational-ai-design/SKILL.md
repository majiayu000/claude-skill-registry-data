---
name: conversational-ai-design
description: "Design conversational AI with Rasa NLU, dialogue management, and LangChain memory patterns."
context: fork
globs: []
alwaysApply: false
---

# Conversational AI Design

Design conversational AI systems with Rasa 3.x NLU pipelines, dialogue management, and LLM-based chatbot patterns.

---

## Rasa NLU Pipeline

### Configuration
```yaml
language: en
pipeline:
  - name: WhitespaceTokenizer
  - name: RegexFeaturizer
  - name: LexicalSyntacticFeaturizer
  - name: CountVectorsFeaturizer
  - name: DIETClassifier
    epochs: 100
  - name: EntitySynonymMapper
  - name: ResponseSelector
    epochs: 100
```

### Intent & Entity Design
- **Intents**: User goals (e.g., `greet`, `book_flight`, `check_status`)
- **Entities**: Data to extract (e.g., `date`, `location`, `order_id`)
- **Minimum 10 examples per intent** for reliable classification

---

## Dialogue Management

### Policy Stack
```yaml
policies:
  - name: RulePolicy          # Handle explicit rules
  - name: TEDPolicy           # ML-based dialogue
    epochs: 100
  - name: MemoizationPolicy   # Exact conversation matches
    max_history: 5
```

### Conversation Patterns
- **Form-based**: Collect structured data (bookings, orders)
- **FAQ-style**: Direct question → answer
- **Multi-turn**: Context-aware follow-ups
- **Fallback**: Handoff to human when confidence < threshold

---

## LLM Chatbot Patterns (LangChain)

### Conversational Memory
```python
from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True,
    max_token_limit=2000
)
```

### RAG for Chatbots
```python
from langchain.chains import RetrievalQA

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vector_store.as_retriever(),
    chain_type="stuff",
    memory=memory
)
```

---

## Best Practices

- **Always confirm** before destructive actions
- **Provide options** not open-ended questions when possible
- **Handle fallbacks** gracefully ("I didn't understand. Try: X, Y, Z")
- **Log conversations** for analysis and improvement
- **Test with real users** — not just developers
- **Set expectations** — tell users what the bot can/can't do

---

## Anti-Patterns

- ❌ No fallback handling
- ❌ Overly long responses
- ❌ Pretending to be human
- ❌ Ignoring context in multi-turn
- ❌ No escape hatch to human agent
