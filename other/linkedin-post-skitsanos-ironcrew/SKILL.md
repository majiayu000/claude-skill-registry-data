---
name: linkedin-post
description: Draft a brief LinkedIn post about today's work. Use when the user asks for a LinkedIn update, progress post, build-in-public summary, or short professional post with relevant hashtags.
argument-hint: [optional-topic-or-tone]
user-invocable: true
---

# LinkedIn Post

Write a concise LinkedIn post about what we are working on today.

Arguments:

- `$ARGUMENTS` may include a topic, audience, or tone such as `technical`, `founder-style`, `launch prep`, or `more personal`.
- If no arguments are provided, use the current task context and recent work as the source material.

Requirements:

1. Keep the post to 1 to 3 short paragraphs total.
2. End with relevant hashtags.
3. Focus on concrete progress, what changed, what was learned, or why the work matters.
4. Keep the tone professional, natural, and specific. Avoid hype, emojis, and generic motivational language unless the user explicitly asks for it.
5. Do not use bullet points or headings unless the user asks for a different format.

Workflow:

1. Infer today's work from the current conversation, changed files, or explicit user instructions.
2. Pick the most relevant angle:
   - progress update
   - technical insight
   - product improvement
   - lesson learned
3. Write a short post that sounds like a real human update, not marketing copy.
4. Add 3 to 8 relevant hashtags on the final line.

Style rules:

- Prefer plain English and concrete nouns over buzzwords.
- Mention the actual task or outcome when it is clear.
- If the work is highly technical, make it readable to a professional audience outside the codebase.
- If context is too thin to write a credible post, ask for a one-line summary instead of inventing details.

Output:

- Return only the final LinkedIn post unless the user asks for multiple variants.
