---
name: intl-news-report
description: Generates a structured report for international news events. Use when a user asks for a detailed summary or investigation of international conflicts, diplomatic events, or global crises.
---

# International News Report Skill

This skill provides a standardized format for reporting on complex international events, ensuring all critical aspects from basic facts to international organizational responses are covered.

## Workflow

When triggered by a request for international news analysis or a report:

1.  **Research**: Use available tools (e.g., `google_web_search`, `newscli`) to gather comprehensive and up-to-date information on the event.
2.  **Synthesis**: Organize the gathered information into the following four mandatory sections.
3.  **Refinement**: Ensure the tone is professional, neutral, and senior-engineer-like (direct and high-signal).

## Report Structure

The report MUST follow this exact structure:

### 1. エグゼクティブサマリー (Executive Summary)
- Provide a concise (1-2 paragraph) high-level summary of the entire situation.
- Include the most critical recent developments and the overall gravity of the event.

### 2. 基本概要情報 (Basic Overview)
- List the fundamental facts: Who, What, When, Where, Why.
- Include key figures (leaders, organizations), specific locations, and a timeline of events.
- Quantify the scale of the event (e.g., number of casualties, scale of military force, economic impact) if available.

### 3. 国際社会の対応 (International Response)
- Detail the reactions and actions of major world powers (e.g., USA, China, Russia, EU, UK, Japan).
- Group responses by "Supportive/Aligned," "Critical/Opposed," and "Neutral/Concerned."
- Mention specific diplomatic statements, sanctions, or military movements.

### 4. 国連および国際機関の対応 (UN and International Organization Response)
- Report on actions by the UN Security Council, UN Secretary-General, and specialized agencies (e.g., IAEA, WHO, WTO).
- Include details of emergency meetings, resolutions (passed or proposed), and official statements.
- Mention any legal proceedings (e.g., at the ICJ or ICC) if applicable.

## Guidelines

- **Objectivity**: Present information from multiple perspectives, especially when reports are conflicting.
- **Timeliness**: Prioritize the most recent 24-48 hours of information but provide context if needed.
- **Clarity**: Use bullet points and clear headings to make the report easily skimmable.
- **Source Citation**: While not mandatory to list every URL, ensure the information is grounded in reliable reporting found during research.
