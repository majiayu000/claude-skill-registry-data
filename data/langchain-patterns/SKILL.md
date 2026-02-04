---
name: LangChain Patterns
description: Building LLM applications with LangChain - chains, agents, RAG, memory, and production patterns for AI-powered apps.
---

# LangChain Patterns

## Overview

LangChain เป็น framework สำหรับ building applications powered by LLMs ช่วยจัดการ complexity ของ prompt chaining, memory, retrieval, agents, และ tool use ทำให้สร้าง AI applications ได้เร็วขึ้น

## Why This Matters

- **Abstraction**: Unified interface สำหรับ LLM providers ต่างๆ
- **Composability**: Chain components เข้าด้วยกันได้ง่าย
- **RAG Ready**: Built-in retrieval และ vector store integrations
- **Production**: LangSmith สำหรับ monitoring และ debugging

---

## Core Concepts

### 1. Basic Setup

```typescript
// lib/langchain.ts
import { ChatOpenAI } from '@langchain/openai';
import { ChatAnthropic } from '@langchain/anthropic';
import { StringOutputParser } from '@langchain/core/output_parsers';
import { ChatPromptTemplate } from '@langchain/core/prompts';

// Initialize models
export const openai = new ChatOpenAI({
  modelName: 'gpt-4-turbo-preview',
  temperature: 0,
  openAIApiKey: process.env.OPENAI_API_KEY,
});

export const claude = new ChatAnthropic({
  modelName: 'claude-3-opus-20240229',
  temperature: 0,
  anthropicApiKey: process.env.ANTHROPIC_API_KEY,
});

// Simple chain
const prompt = ChatPromptTemplate.fromMessages([
  ['system', 'You are a helpful assistant that translates {input_language} to {output_language}.'],
  ['human', '{text}'],
]);

const chain = prompt.pipe(openai).pipe(new StringOutputParser());

// Usage
const result = await chain.invoke({
  input_language: 'English',
  output_language: 'Thai',
  text: 'Hello, how are you?',
});
```

### 2. Structured Output

```typescript
import { z } from 'zod';
import { StructuredOutputParser } from 'langchain/output_parsers';
import { ChatPromptTemplate } from '@langchain/core/prompts';

// Define schema
const productSchema = z.object({
  name: z.string().describe('Product name'),
  description: z.string().describe('Product description'),
  price: z.number().describe('Price in USD'),
  category: z.enum(['electronics', 'clothing', 'food', 'other']),
  tags: z.array(z.string()).describe('Product tags'),
});

const parser = StructuredOutputParser.fromZodSchema(productSchema);

const prompt = ChatPromptTemplate.fromMessages([
  ['system', `Extract product information from the text.
{format_instructions}`],
  ['human', '{text}'],
]);

const chain = prompt.pipe(openai).pipe(parser);

const result = await chain.invoke({
  text: 'New iPhone 15 Pro, amazing camera, $999, perfect for photography enthusiasts',
  format_instructions: parser.getFormatInstructions(),
});

// result: { name: 'iPhone 15 Pro', description: '...', price: 999, category: 'electronics', tags: ['photography', 'camera'] }
```

### 3. RAG (Retrieval-Augmented Generation)

```typescript
import { OpenAIEmbeddings } from '@langchain/openai';
import { SupabaseVectorStore } from '@langchain/community/vectorstores/supabase';
import { createClient } from '@supabase/supabase-js';
import { RecursiveCharacterTextSplitter } from 'langchain/text_splitter';
import { createRetrievalChain } from 'langchain/chains/retrieval';
import { createStuffDocumentsChain } from 'langchain/chains/combine_documents';

// Setup vector store
const supabase = createClient(
  process.env.SUPABASE_URL!,
  process.env.SUPABASE_SERVICE_KEY!
);

const embeddings = new OpenAIEmbeddings({
  openAIApiKey: process.env.OPENAI_API_KEY,
});

const vectorStore = new SupabaseVectorStore(embeddings, {
  client: supabase,
  tableName: 'documents',
  queryName: 'match_documents',
});

// Index documents
async function indexDocuments(documents: string[]) {
  const splitter = new RecursiveCharacterTextSplitter({
    chunkSize: 1000,
    chunkOverlap: 200,
  });

  const docs = await splitter.createDocuments(documents);
  await vectorStore.addDocuments(docs);
}

// Create RAG chain
const retriever = vectorStore.asRetriever({
  k: 5,
  searchType: 'similarity',
});

const qaPrompt = ChatPromptTemplate.fromMessages([
  ['system', `Answer the question based on the following context:

{context}

If you don't know the answer, say "I don't have enough information to answer that."`],
  ['human', '{input}'],
]);

const documentChain = await createStuffDocumentsChain({
  llm: openai,
  prompt: qaPrompt,
});

const ragChain = await createRetrievalChain({
  combineDocsChain: documentChain,
  retriever,
});

// Usage
const response = await ragChain.invoke({
  input: 'What is our refund policy?',
});

console.log(response.answer);
console.log(response.context); // Source documents
```

### 4. Conversational Memory

```typescript
import { BufferMemory, ConversationSummaryMemory } from 'langchain/memory';
import { ConversationChain } from 'langchain/chains';
import { UpstashRedisChatMessageHistory } from '@langchain/community/stores/message/upstash_redis';

// Simple buffer memory
const bufferMemory = new BufferMemory({
  returnMessages: true,
  memoryKey: 'history',
});

// Redis-backed memory (for production)
const redisMemory = new BufferMemory({
  chatHistory: new UpstashRedisChatMessageHistory({
    sessionId: `user-${userId}-session-${sessionId}`,
    config: {
      url: process.env.UPSTASH_REDIS_URL!,
      token: process.env.UPSTASH_REDIS_TOKEN!,
    },
  }),
  returnMessages: true,
  memoryKey: 'history',
});

// Summary memory (for long conversations)
const summaryMemory = new ConversationSummaryMemory({
  llm: openai,
  returnMessages: true,
});

// Conversation chain with memory
const conversationChain = new ConversationChain({
  llm: openai,
  memory: redisMemory,
  verbose: true,
});

// Multi-turn conversation
await conversationChain.call({ input: 'My name is John' });
await conversationChain.call({ input: 'What is my name?' }); // Remembers "John"
```

### 5. Agents with Tools

```typescript
import { ChatOpenAI } from '@langchain/openai';
import { createOpenAIFunctionsAgent, AgentExecutor } from 'langchain/agents';
import { DynamicTool, DynamicStructuredTool } from '@langchain/core/tools';
import { pull } from 'langchain/hub';
import { z } from 'zod';

// Define tools
const searchTool = new DynamicTool({
  name: 'search',
  description: 'Search the web for current information',
  func: async (query: string) => {
    // Implement search logic
    const results = await searchWeb(query);
    return JSON.stringify(results);
  },
});

const calculatorTool = new DynamicStructuredTool({
  name: 'calculator',
  description: 'Perform mathematical calculations',
  schema: z.object({
    expression: z.string().describe('Mathematical expression to evaluate'),
  }),
  func: async ({ expression }) => {
    try {
      const result = eval(expression); // Use a safe math parser in production
      return `Result: ${result}`;
    } catch (error) {
      return `Error: Invalid expression`;
    }
  },
});

const databaseTool = new DynamicStructuredTool({
  name: 'query_database',
  description: 'Query the product database',
  schema: z.object({
    query: z.string().describe('Search query for products'),
    category: z.string().optional().describe('Filter by category'),
    maxPrice: z.number().optional().describe('Maximum price filter'),
  }),
  func: async ({ query, category, maxPrice }) => {
    const products = await prisma.product.findMany({
      where: {
        name: { contains: query, mode: 'insensitive' },
        ...(category && { category }),
        ...(maxPrice && { price: { lte: maxPrice } }),
      },
      take: 5,
    });
    return JSON.stringify(products);
  },
});

// Create agent
const tools = [searchTool, calculatorTool, databaseTool];
const prompt = await pull<ChatPromptTemplate>('hwchase17/openai-functions-agent');

const agent = await createOpenAIFunctionsAgent({
  llm: openai,
  tools,
  prompt,
});

const agentExecutor = new AgentExecutor({
  agent,
  tools,
  verbose: true,
  maxIterations: 5,
});

// Usage
const result = await agentExecutor.invoke({
  input: 'Find me a laptop under $1000 and calculate the price with 10% tax',
});
```

### 6. Streaming

```typescript
import { ChatOpenAI } from '@langchain/openai';
import { StringOutputParser } from '@langchain/core/output_parsers';

const model = new ChatOpenAI({
  modelName: 'gpt-4-turbo-preview',
  streaming: true,
});

// Stream with callbacks
const stream = await model.stream('Write a story about a robot');

for await (const chunk of stream) {
  process.stdout.write(chunk.content);
}

// Stream in Next.js API route
// app/api/chat/route.ts
import { StreamingTextResponse, LangChainStream } from 'ai';

export async function POST(req: Request) {
  const { messages } = await req.json();
  
  const { stream, handlers } = LangChainStream();
  
  const chain = prompt.pipe(model).pipe(new StringOutputParser());
  
  chain.invoke(
    { messages },
    { callbacks: [handlers] }
  );
  
  return new StreamingTextResponse(stream);
}
```

### 7. Document Loaders

```typescript
import { PDFLoader } from 'langchain/document_loaders/fs/pdf';
import { CSVLoader } from 'langchain/document_loaders/fs/csv';
import { WebBaseLoader } from 'langchain/document_loaders/web/web_base';
import { NotionAPILoader } from 'langchain/document_loaders/web/notionapi';
import { GithubRepoLoader } from 'langchain/document_loaders/web/github';

// Load PDF
const pdfLoader = new PDFLoader('path/to/document.pdf', {
  splitPages: true,
});
const pdfDocs = await pdfLoader.load();

// Load CSV
const csvLoader = new CSVLoader('path/to/data.csv', {
  column: 'text', // Column to use as page content
});
const csvDocs = await csvLoader.load();

// Load from web
const webLoader = new WebBaseLoader('https://example.com/article');
const webDocs = await webLoader.load();

// Load from Notion
const notionLoader = new NotionAPILoader({
  clientOptions: {
    auth: process.env.NOTION_API_KEY,
  },
  id: 'page-or-database-id',
  type: 'page',
});
const notionDocs = await notionLoader.load();

// Load from GitHub repo
const githubLoader = new GithubRepoLoader(
  'https://github.com/username/repo',
  {
    branch: 'main',
    recursive: true,
    unknown: 'warn',
    accessToken: process.env.GITHUB_TOKEN,
  }
);
const repoDocs = await githubLoader.load();
```

### 8. LangSmith Integration (Production Monitoring)

```typescript
// Enable tracing
process.env.LANGCHAIN_TRACING_V2 = 'true';
process.env.LANGCHAIN_API_KEY = 'your-langsmith-api-key';
process.env.LANGCHAIN_PROJECT = 'my-project';

// Or configure programmatically
import { Client } from 'langsmith';
import { LangChainTracer } from 'langchain/callbacks';

const client = new Client({
  apiKey: process.env.LANGSMITH_API_KEY,
});

const tracer = new LangChainTracer({
  projectName: 'my-project',
  client,
});

// Use with any chain
const result = await chain.invoke(
  { input: 'Hello' },
  { callbacks: [tracer] }
);

// Evaluate runs
import { evaluate } from 'langsmith/evaluation';

await evaluate(
  (input) => chain.invoke(input),
  {
    data: 'my-dataset-name',
    evaluators: [
      // Custom evaluators
      async ({ run, example }) => {
        const score = calculateScore(run.outputs, example.outputs);
        return { key: 'accuracy', score };
      },
    ],
  }
);
```

## Quick Start

1. **Install packages:**
   ```bash
   npm install langchain @langchain/openai @langchain/community
   ```

2. **Set environment variables:**
   ```bash
   OPENAI_API_KEY=sk-...
   LANGCHAIN_TRACING_V2=true
   LANGCHAIN_API_KEY=ls-...
   ```

3. **Create a simple chain:**
   ```typescript
   import { ChatOpenAI } from '@langchain/openai';
   import { ChatPromptTemplate } from '@langchain/core/prompts';
   
   const chain = ChatPromptTemplate
     .fromTemplate('Tell me a joke about {topic}')
     .pipe(new ChatOpenAI())
     .pipe(new StringOutputParser());
   
   const joke = await chain.invoke({ topic: 'programming' });
   ```

## Production Checklist

- [ ] LangSmith tracing enabled
- [ ] Error handling and retries configured
- [ ] Rate limiting implemented
- [ ] Caching layer for embeddings
- [ ] Token usage monitoring
- [ ] Fallback models configured
- [ ] Input validation
- [ ] Output validation/guardrails

## Anti-patterns

1. **No streaming for long responses**: Always stream for better UX
2. **Ignoring token limits**: Monitor and handle context length
3. **No error handling**: LLM calls can fail - handle gracefully
4. **Hardcoded prompts**: Use prompt templates and versioning

## Integration Points

- **Vector Stores**: Pinecone, Supabase, Chroma, Weaviate
- **LLMs**: OpenAI, Anthropic, Google, Cohere, local models
- **Memory**: Redis, PostgreSQL, in-memory
- **Tools**: Custom APIs, databases, search engines

## Further Reading

- [LangChain Documentation](https://js.langchain.com/docs)
- [LangSmith](https://smith.langchain.com/)
- [LangChain Templates](https://github.com/langchain-ai/langchain/tree/master/templates)
