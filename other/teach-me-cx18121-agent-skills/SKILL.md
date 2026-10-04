---
name: teach-me
description: Teach a topic in stages and check understanding before moving on.
disable-model-invocation: true
---

# Teach Me

Teach the named topic or the work from the current session in small stages. Start by asking the user to explain what they already understands. Use that answer to choose the first gap instead of giving a full lecture.

For each stage:

1. Explain the purpose and the concrete mechanism.
2. Use one real example when it helps.
3. Ask the user to restate the idea or answer a short question.
4. Correct the gap before moving on.

Use `ask_user_question` for multiple choice questions when the tool is available. Do not reveal the answer before submission. Explain why the chosen answer works and why the closest alternative does not.

Keep a short checklist in the conversation. Create a file only when the user asks for a durable learning guide. Cover the problem, the chosen solution, and the important downstream effect when they are relevant to the learning goal.

Match requested depth such as beginner, intern, or expert. Let the user ask questions and change pace.

Stop when the user demonstrates the requested understanding or chooses to stop. Do not require exhaustive mastery of every related topic before completing the lesson.
