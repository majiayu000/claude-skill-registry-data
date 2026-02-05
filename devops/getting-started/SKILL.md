---
title: "Your First Skill"
description: "Build a complete task management skill from scratch"
---

## Build a Task Management Skill

Let's build a complete skill that manages tasks (create, list, complete, delete).

## Step 1: Initialize Project

```bash
mkdir task-management-skill
cd task-management-skill
lua init
```

Follow the prompts to create a new agent.

## Step 2: Clean Up Template

Remove unnecessary example files:

```bash
rm src/tools/ProductsTool.ts
rm src/tools/BasketTool.ts
rm src/tools/OrderTool.ts
rm src/tools/PaymentTool.ts
rm src/tools/GetWeatherTool.ts
```

## Step 3: Create Task Tool

Create `src/tools/TaskTool.ts`:

```typescript
import { LuaTool, Data } from "lua-cli";
import { z } from "zod";

export class CreateTaskTool implements LuaTool {
  name = "create_task";
  description = "Create a new task";
  
  inputSchema = z.object({
    title: z.string().describe("Task title"),
    description: z.string().optional(),
    priority: z.enum(['low', 'medium', 'high']).default('medium'),
    dueDate: z.string().optional()
  });

  async execute(input: z.infer<typeof this.inputSchema>) {
    const task = await Data.create('tasks', {
      ...input,
      status: 'pending',
      createdAt: new Date().toISOString()
    }, input.title + ' ' + (input.description || ''));
    
    return {
      taskId: task.id,
      message: `Task "${input.title}" created`
    };
  }
}

export class ListTasksTool implements LuaTool {
  name = "list_tasks";
  description = "List all tasks, optionally filtered by status";
  
  inputSchema = z.object({
    status: z.enum(['pending', 'in_progress', 'completed']).optional()
  });

  async execute(input: z.infer<typeof this.inputSchema>) {
    const filter = input.status ? { status: input.status } : {};
    const result = await Data.get('tasks', filter, 1, 50);
    
    return {
      tasks: result.data.map(entry => ({
        id: entry.id,
        ...entry.data
      })),
      count: result.pagination.totalCount
    };
  }
}

export class CompleteTaskTool implements LuaTool {
  name = "complete_task";
  description = "Mark a task as completed";
  
  inputSchema = z.object({
    taskId: z.string()
  });

  async execute(input: z.infer<typeof this.inputSchema>) {
    const task = await Data.getEntry('tasks', input.taskId);
    
    await Data.update('tasks', input.taskId, {
      ...task.data,
      status: 'completed',
      completedAt: new Date().toISOString()
    });
    
    return {
      success: true,
      message: `Task "${task.data.title}" marked as completed`
    };
  }
}

export class SearchTasksTool implements LuaTool {
  name = "search_tasks";
  description = "Search tasks by content";
  
  inputSchema = z.object({
    query: z.string()
  });

  async execute(input: z.infer<typeof this.inputSchema>) {
    const results = await Data.search('tasks', input.query, 20, 0.6);
    
    return {
      tasks: results.data.map(entry => ({
        id: entry.id,
        ...entry.data,
        relevance: entry.score
      }))
    };
  }
}
```

## Step 4: Create Agent with Skill

Update `src/index.ts` to use the **v3.0.0 LuaAgent pattern**:

```typescript
import { LuaAgent, LuaSkill } from "lua-cli";
import {
  CreateTaskTool,
  ListTasksTool,
  CompleteTaskTool,
  SearchTasksTool
} from "./tools/TaskTool";

// Create the task management skill
const taskSkill = new LuaSkill({
  name: "task-management-skill",
  description: "Manage tasks and to-do lists with creation, listing, completion, and search",
  context: `
    This skill helps users manage their tasks.
    
    - Use create_task when users want to add a new task
    - Use list_tasks to show all tasks or filter by status
    - Use complete_task when users finish a task
    - Use search_tasks to find tasks by content
    
    Always confirm task details before creating.
    When listing tasks, organize by priority and due date.
  `,
  tools: [
    new CreateTaskTool(),
    new ListTasksTool(),
    new CompleteTaskTool(),
    new SearchTasksTool()
  ]
});

// Create agent (v3.0.0 pattern)
export const agent = new LuaAgent({
  name: "task-assistant",
  
  persona: `You are a helpful task management assistant.
  
Your role:
- Help users create and organize their tasks
- Keep track of todos and deadlines
- Search for tasks when needed
- Mark tasks as complete

Communication style:
- Friendly and encouraging
- Clear and concise
- Confirm actions before executing
- Provide helpful summaries

Capabilities:
- Create new tasks with title, description, priority, and due date
- List all tasks or filter by status
- Search tasks semantically
- Mark tasks as completed

Always confirm task details with users before creating them.`,

  
  skills: [taskSkill]
});
```

<Note>
**New in v3.0.0:** Use `LuaAgent` to configure your agent with persona, welcome message, and skills in one place.
</Note>

## Step 5: Test Your Tools

### Test Individual Tools

```bash
lua test
```

Select tools and test:
- **create_task**: Create a task to buy milk
- **list_tasks**: View all pending tasks
- **complete_task**: Mark a task as done
- **search_tasks**: Find tasks about "meeting"

### Test Conversationally

```bash
lua chat
```

Try these in the chat:
- "Create a task to buy milk"
- "Show me my pending tasks"
- "Mark the milk task as done"
- "Find all tasks about meetings"

<Check>
Your task management skill is now working!
</Check>

## Step 6: Deploy

When you're satisfied with your skill:

```bash
# Upload to server
lua push

# Deploy to production
lua deploy
```

## Step 7: Test on Real Channels (Optional)

Want to test your agent on WhatsApp, Facebook, Instagram, or other platforms?

<Card
  title="Quick Testing Channels"
  icon="mobile"
  href="/channels/quick-testing"
  horizontal
>
  Link your agent to existing Lua channels for instant testing without channel setup
</Card>

**Example for WhatsApp:**
```
https://wa.me/13023778932?text=link-me-to:YOUR_AGENT_ID
```

Replace `YOUR_AGENT_ID` with your agent ID from `lua.skill.yaml`

## What You Built

<CardGroup cols={2}>
  <Card title="4 Tools" icon="wrench">
    Create, list, complete, and search tasks
  </Card>
  <Card title="Custom Data" icon="database">
    Uses Lua's Data API for storage
  </Card>
  <Card title="Vector Search" icon="magnifying-glass">
    Semantic search for finding tasks
  </Card>
  <Card title="Type Safe" icon="shield">
    Full TypeScript with Zod validation
  </Card>
</CardGroup>

## Next Steps

<Steps>
  <Step title="Add More Features">
    - Delete tasks
    - Update task details  
    - Set reminders
    - Add tags
  </Step>
  
  <Step title="Improve User Experience">
    - Better error messages
    - Confirmation prompts
    - Progress indicators
  </Step>
  
  <Step title="Explore Other Examples">
    <Card
      title="Tool Examples"
      icon="layer-group"
      href="/examples/overview"
    >
      See 30+ working examples
    </Card>
  </Step>
</Steps>

## Common Patterns Used

### Pattern: Data Storage

```typescript
await Data.create('collection', data, searchableText);
```

Creates entries with optional vector search indexing.

### Pattern: Semantic Search

```typescript
await Data.search('collection', query, limit, threshold);
```

Finds similar items based on meaning, not just exact matches.

### Pattern: CRUD Operations

```typescript
await Data.get('collection', filter);
await Data.getEntry('collection', id);
await Data.update('collection', id, data);
await Data.delete('collection', id);
```

### Pattern: Input Validation

```typescript
inputSchema = z.object({
  title: z.string(),
  status: z.enum(['pending', 'completed']).optional()
});
```

Zod schemas provide runtime validation and TypeScript types.

## Troubleshooting

<AccordionGroup>
  <Accordion title="Cannot find module 'lua-cli'">
    Install dependencies:
    ```bash
    npm install
    ```
  </Accordion>

  <Accordion title="Task not found error">
    Make sure you're using the correct task ID from the list_tasks response.
  </Accordion>

  <Accordion title="Search returns no results">
    - Lower the score threshold: `0.6` instead of `0.7`
    - Check that tasks have searchable text
    - Try broader search terms
  </Accordion>
</AccordionGroup>

