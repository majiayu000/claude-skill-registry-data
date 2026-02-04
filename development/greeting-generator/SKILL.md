---
name: Greeting Generator
description: Generate personalized, context-aware greetings for developers at different times of day and moods
---

# Greeting Generator

## Purpose

This skill helps create warm, personalized greetings for developers based on:
- Time of day
- Current mood/energy level
- Programming context
- Recent activity

## When to Use

Invoke this skill when:
- User starts a coding session
- User needs motivation or encouragement
- Creating personalized welcome messages
- Setting a positive tone for collaboration

## Instructions

### Step 1: Gather Context

Determine the following:
1. **Time of Day**: Morning (5am-12pm), Afternoon (12pm-5pm), Evening (5pm-10pm), Night (10pm-5am)
2. **User Mood**: Energetic, Focused, Tired, Frustrated, Curious
3. **Programming Language**: Based on recent files or user specification
4. **Current Task**: What the user is working on (if available)

### Step 2: Select Greeting Style

Choose an appropriate greeting style:
- **Energetic**: Enthusiastic, emoji-rich, exclamation points
- **Professional**: Calm, focused, task-oriented
- **Humorous**: Include programming jokes or puns
- **Supportive**: Encouraging, empathetic, motivating

### Step 3: Generate Greeting

Create a greeting that includes:
1. **Time-appropriate salutation**
2. **Programming context reference**
3. **Optional programming joke or fun fact**
4. **Invitation to share what they're working on**
5. **Offer of assistance**

### Step 4: Add Value

Include one of the following:
- Programming tip relevant to their language/framework
- Motivational quote from a famous developer
- Keyboard shortcut or productivity tip
- Fun fact about programming history

## Examples

### Morning Greeting (Energetic)

```
Good morning! Ready to write some beautiful code today?

Here's a fun fact: The first computer bug was an actual moth found in
Harvard's Mark II computer in 1947.

What are you building today? I'm here to help make it awesome!
```

### Afternoon Greeting (Professional)

```
Good afternoon! Hope your coding session is going well.

Quick tip: Use `git commit --amend` to modify your last commit message
without creating a new commit.

What can I help you with today?
```

### Evening Greeting (Supportive)

```
Good evening! Still coding strong, I see.

Remember: "First, solve the problem. Then, write the code." - John Johnson

What challenge are you tackling tonight? Let's solve it together!
```

### Night Greeting (Humorous)

```
Burning the midnight oil? You're in good company!

Programming joke: Why do programmers prefer dark mode?
Because light attracts bugs!

What late-night project are you working on? I'm here to help!
```

## Templates

### Time-Based Greetings

**Morning**:
- "Good morning, {name}! Ready to tackle some code?"
- "Morning! Let's make today's commits count!"
- "Rise and code! What's on your agenda today?"

**Afternoon**:
- "Good afternoon! Hope your coding is flowing smoothly."
- "Afternoon check-in! How's the code coming along?"
- "Afternoon! Time to turn coffee into code."

**Evening**:
- "Good evening! Still going strong!"
- "Evening! Let's wrap up the day with some solid commits."
- "Good evening! What are we building tonight?"

**Night**:
- "Burning the midnight oil? Let's make it count!"
- "Night owl coder detected! What are we creating?"
- "Late night coding session activated!"

### Programming Jokes

- "Why do Java developers wear glasses? Because they don't C#!"
- "How many programmers does it take to change a light bulb? None, that's a hardware problem."
- "A SQL query walks into a bar, walks up to two tables and asks, 'Can I join you?'"
- "There are 10 types of people: those who understand binary and those who don't."

### Developer Quotes

- "Talk is cheap. Show me the code." - Linus Torvalds
- "First, solve the problem. Then, write the code." - John Johnson
- "Code is like humor. When you have to explain it, it's bad." - Cory House
- "Make it work, make it right, make it fast." - Kent Beck

## Best Practices

1. **Be Authentic**: Greetings should feel genuine, not robotic
2. **Match Energy**: Adapt tone to time of day and user context
3. **Be Brief**: Don't overwhelm with a wall of text
4. **Add Value**: Include a tip, joke, or fact that's actually useful
5. **Encourage Engagement**: Ask what they're working on
6. **Offer Help**: Make it clear you're there to assist

## Output Format

```
[Time-based salutation]

[Optional: Programming joke/fact/tip]

[Question about their work]

[Offer of assistance]
```

## Error Handling

If context is unavailable:
- Use a neutral, friendly greeting
- Keep it simple and professional
- Focus on offering help

## Related Skills

- `motivation-generator`: For ongoing encouragement
- `farewell-generator`: For session endings
- `code-review-opener`: For starting code reviews with positivity
