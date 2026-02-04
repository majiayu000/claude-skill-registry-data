---
name: "Researching Features"
description: "Use this whenever a user wants to add a new feature or explitly states to research a feature/API or building a plan for a new feature. It itnerviews the user for feature details (if not provided), research the best API/service for their needs, confirm choice, then gather all implementation notes for their request and save them as a .claude/plans file. "
version: "1.0.0"
dependencies: ["context7", "mcp-api", "python>=3.8"]
allowed-tools: ["context7", "mcp", "file_write"]
---

# Feature Researcher

## Instructions
When requested to research a feature:


1. **User Interview**  
   - If the user's requirements are unclear, politely ask for more details (deatails on feature, free/paid API options, constraints).
   - If details are provided, proceed directly.

1. **Service & API Discovery**  
   - Take the user's answers and consider them in your search
   - You MUST use `context7` to identify the APIs/services/libraries that best match the user's requirements.
   - DO NOT use `web_search` - tell teh user to get `context7`
   - Only use `web_search` if the the user doesnt want to use `context7`
   - Go with the top 3 options that the tools return/suggest

3. **User Confirmation**  
   - Summarize every provider you found and suggest
   - After selecting the best API/service, briefly summarize your choice and reasons.
   - Ask the user to confirm before proceeding with implementation research.

4. **Implementation Notes Gathering**  
   - VERY IMPORTANT: Before you start, look at the `spec-sheet.md` for the specs for this projects and `claude.md` to understand the context - this way you know the tech stack to a build a plan for.
   - Once confirmed, use `Context7` to retrieve official docs, key endpoints, authentication steps, usage patterns, and constraints for the selected API/service.
   - Structure your notes clearly around:
      - Have page and UI elements to be built first before backend functions etc
     - Authentication  
     - Setup and Initialization  
     - Core Endpoints/Methods  
     - Example Requests/Responses  d
     - Error Handling  
     - Rate Limits or Pricing

5. **Save Implementation Plan**  
   - Compile all notes and implementation steps into a .md file.
   - Create a plan in `.claude/plans/plan-[feature-name].md`.
   - Notify the user where to find their plan.

## Examples
- **Input:** "I want live chat in my app. What service is best?"
  **Output:**  
  1. Interview user for scale, preferred integrations.
  2. Research providers (Twilio Conversations, Sendbird, CometChat).
  3. Suggest Sendbird based on docs and usage.
  4. After user approval, gather usage notes, endpoints, sample code.
  5. Save results to `.claude/plans/plan-feature-live-chat.md`.

- **Input:** "Add online payments (API/service of your choice)"
  **Output:**  
  Same flow, ending with a plan file like `.claude/plans/plan-feature-payments.md`
