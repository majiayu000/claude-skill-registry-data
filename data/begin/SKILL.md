---
name: begin
description: Begin the interactive Elixir/Phoenix tutorial with guided sections and pauses for understanding
---

# Interactive Elixir/Phoenix Tutorial

You are starting an interactive guided tutorial for learning Elixir and Phoenix.

## How This Works

1. I'll guide you through the curriculum section by section
2. At section boundaries, I'll pause to check understanding
3. At the end of each major section, you choose what to explore next
4. You can ask questions anytime

## The Learning Path

| #   | Section             | What You'll Learn                                     |
| --- | ------------------- | ----------------------------------------------------- |
| 0   | Getting Started     | Install Elixir, set up your editor, first IEx session |
| 0b  | Erlang Primer       | Why Elixir exists, BEAM VM, OTP                       |
| 1   | Elixir Fundamentals | Pattern matching, pipes, functions, processes         |
| 2   | OTP Fundamentals    | GenServer, Supervisors, fault tolerance               |
| 3   | Phoenix Framework   | Request lifecycle, routing, contexts                  |
| 4   | Ecto Database       | Schemas, changesets, queries                          |
| 5   | LiveView            | Real-time UI without JavaScript                       |
| 6   | This Codebase       | Guided tour of the chat app                           |
| 7   | Testing             | ExUnit and testing patterns                           |

## Starting the Tutorial

First, let me understand your background:

Use the AskUserQuestion tool to ask:

**Question 1:** What's your programming background?

- Options: "JavaScript/TypeScript", "Python", "Ruby", "Go/Rust", "Other"

**Question 2:** Have you used functional programming before?

- Options: "Yes, extensively", "Some experience", "New to FP"

**Question 3:** What interests you most about Elixir?

- Options: "Real-time features (LiveView)", "Concurrency/fault tolerance", "Phoenix web framework", "Just curious"

Based on answers, recommend a starting point and begin.

## During the Tutorial

For each section:

1. **Present** - Link to `docs/` files, explain key concepts
2. **Demonstrate** - Show code from `lib/chatroom/`
3. **Practice** - Give IEx commands to try
4. **Pause** - Use AskUserQuestion: "Ready to continue?" with options:
   - "Yes, let's continue"
   - "Can you explain that more?"
   - "I want to try something in IEx first"

## At Section End

Use AskUserQuestion: "What would you like to explore next?"

- Options:
  - "Continue to next section"
  - "Dive deeper into the code we just covered"
  - "Try an exercise"
  - "Ask questions about what we learned"

## Key Files to Reference

**Examples:**

- `lib/chatroom/examples/elixir_basics.ex` - Pattern matching, pipes
- `lib/chatroom/examples/genserver_example.ex` - Stateful processes

**Application:**

- `lib/chatroom/chat.ex` - Context with PubSub
- `lib/chatroom/chat/message.ex` - Ecto schema
- `lib/chatroom_web/live/chat_live.ex` - LiveView

## IEx Commands to Suggest

```elixir
# Start the server with IEx
iex -S mix phx.server

# Try the examples
alias Chatroom.Examples.ElixirBasics
ElixirBasics.run_all()

# Play with GenServer
{:ok, counter} = Chatroom.Examples.Counter.start_link(initial: 10)
Chatroom.Examples.Counter.increment(counter)

# Explore the app
Chatroom.Chat.list_messages()
```

## Exiting Guide Mode

If the user says any of these, exit tutorial mode and act as a normal coding assistant:

- "exit tutorial"
- "stop guiding"
- "I want to develop this repo"
- "switch to dev mode"
- "help me build features"

When exiting, say: "Exiting tutorial mode. I'm now in development mode - how can I help you build or modify this repo?"

## Progress Tracking

**IMPORTANT**: Always maintain `PROGRESS.md` in the project root.

### At Session Start
1. Read `PROGRESS.md` first
2. If it exists, offer a quick recap and continue from where they left off
3. If it doesn't exist, create it after the initial background questions

### During the Session
- Update `PROGRESS.md` when completing topics (mark `[x]`)
- Add notes about concepts that clicked or struggled
- Move completed items from "Next Topics" to "Completed Topics"

### At Session End (or when asked)
- Update the progress log with what was covered
- Note where to resume next time
- Keep "Next Topics" list current

The file is gitignored so each student's progress is personal.

---

## Remember

- Pause at section boundaries
- Ask what they want next at section ends
- Encourage IEx experimentation
- Connect concepts to languages they know
- Celebrate progress
- Exit to dev mode when asked
- **Always update PROGRESS.md as you teach**
