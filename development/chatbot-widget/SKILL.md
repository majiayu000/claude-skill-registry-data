---
name: chatbot-widget
description: Build embeddable chatbot widgets for web applications. Use when creating chat UIs, iframe embeds, or widget-based AI interfaces.
allowed-tools: Read, Write, Grep, Glob
---

# Chatbot Widget Theming Skill

Style AI chatbot to match Cloodle design system.

## Trigger
- Chatbot UI customization
- Widget embedding requests
- Chat interface styling

## Chainlit Theming
Create `/opt/cloodle/tools/ai/multi_agent_rag_system/.chainlit/config.toml`:

```toml
[UI]
name = "Cloodle Assistant"
description = "AI-powered learning assistant"
default_theme = "light"

[UI.theme]
primary_color = "#6e66cc"
background_color = "#ffffff"
paper_color = "#f7f7f7"
font_family = "Outfit, sans-serif"
```

## Custom CSS
Create `public/custom.css`:
```css
:root {
    --cloodle-primary: #6e66cc;
    --cloodle-radius: 12px;
}

.message {
    border-radius: var(--cloodle-radius);
    font-family: "Outfit", sans-serif;
}

.user-message {
    background-color: var(--cloodle-primary);
    color: white;
}

.assistant-message {
    background-color: #f7f7f7;
    border: 1px solid #dedbe0;
}

.chat-input {
    border-radius: var(--cloodle-radius);
    border-color: #dedbe0;
}

.chat-input:focus {
    border-color: var(--cloodle-primary);
}

.send-button {
    background-color: var(--cloodle-primary);
    border-radius: 500px;
}
```

## Moodle Embedding
```html
<div id="cloodle-chatbot" class="cloodle-chat-widget">
    <iframe
        src="https://chat.cloodle.example/widget"
        style="border: none; border-radius: 12px;"
        width="400"
        height="600">
    </iframe>
</div>
```

## Widget Position CSS
```css
.cloodle-chat-widget {
    position: fixed;
    bottom: 20px;
    right: 20px;
    z-index: 9999;
    box-shadow: rgba(77,77,77,0.1) 0 4px 12px;
    border-radius: 12px;
    overflow: hidden;
}
```

## Toggle Button
```html
<button class="cloodle-chat-toggle" onclick="toggleChat()">
    <svg><!-- Chat icon --></svg>
</button>
```
