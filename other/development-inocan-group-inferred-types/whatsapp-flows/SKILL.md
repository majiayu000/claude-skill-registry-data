---
name: whatsapp-flows
description: Authoring WhatsApp Business Flows with validation, component guidance, and server integration patterns. Use when building conversational experiences, collecting user data, implementing conditional logic, or integrating with backend endpoints.
---

# WhatsApp Flows Skill

Build conversational WhatsApp experiences with dynamic forms, conditional logic, and server integration.

## Quick Start

### What are WhatsApp Flows?

WhatsApp Flows are structured conversations that collect user input through a series of screens. Use them to:
- Collect information (forms, surveys)
- Implement conditional logic (eligibility checks, branching)
- Display dynamic data (products, prices, inventory)
- Validate user input server-side
- Complete multi-step processes

### 5 Key Concepts

1. **Screens** - Individual steps in your flow. Each has a unique ID and layout.
2. **Components** - Building blocks (TextInput, Dropdown, Footer, If, etc.)
3. **Form Data** - User input via `${form.field_name}` binding
4. **Server Data** - Dynamic data via `${data.field_name}` binding
5. **Actions** - What happens: navigate, data_exchange, complete, update_data, open_url

### Minimal Example

```json
{
  "version": "7.1",
  "screens": [
    {
      "id": "GREETING",
      "title": "Greeting",
      "layout": {
        "type": "SingleColumnLayout",
        "children": [
          {
            "type": "TextHeading",
            "text": "Welcome!"
          },
          {
            "type": "TextBody",
            "text": "Please tell us your name to proceed.",
            "markdown": true
          },
          {
            "type": "TextInput",
            "name": "name",
            "label": "What's your name?",
            "required": true
          },
          {
            "type": "Footer",
            "label": "Continue",
            "on-click-action": {
              "name": "navigate",
              "next": {
                "type": "screen",
                "name": "CONFIRMATION"
              }
            }
          }
        ]
      }
    },
    {
      "id": "CONFIRMATION",
      "title": "Confirmation",
      "terminal": true,
      "success": true,
      "layout": {
        "type": "SingleColumnLayout",
        "children": [
          {
            "type": "TextHeading",
            "text": "Hello ${screen.GREETING.form.name}!"
          },
          {
            "type": "Footer",
            "label": "Done",
            "on-click-action": {
              "name": "complete",
              "payload": {
                "name": "${screen.GREETING.form.name}"
              }
            }
          }
        ]
      }
    }
  ]
}
```

**Business 3.0 API Requirements:**
- Every screen MUST have a `title` property
- Action properties use `name` (not `action`) with nested structure

**When to add `data_api_version`:**
- Only include `"data_api_version": "3.0"` if your flow needs server integration (data validation, dynamic data, form submission to backend)
- If your flow is client-side only with no backend endpoints, omit this property
- See [server-integration.md](reference/server-integration.md) for details on setting up endpoints

---

## Business 3.0 API Requirements

WhatsApp Flows uses the Business 3.0 API which has specific requirements:

**Every screen MUST have:**
- `id` (required) - Unique screen identifier
- `title` (required) - Screen title for display and navigation

**Markdown formatting:**
- Only **TextBody** and **TextCaption** support markdown
- Set `"markdown": true` to enable formatting
- **TextHeading does NOT support markdown** (will cause validation error)
- Markdown is disabled by default if property omitted

**Optional server integration:**
- `data_api_version: "3.0"` - Only required if your flow calls backend endpoints
- `routing_model` - Only required with `data_api_version` for dynamic routing

**Minimal structure (no backend needed):**
```json
{
  "version": "7.1",
  "screens": [
    {
      "id": "SCREEN_ID",
      "title": "Screen Title",
      "layout": { ... }
    }
  ]
}
```

**With server integration (backend endpoints):**
```json
{
  "version": "7.1",
  "data_api_version": "3.0",
  "routing_model": { ... },
  "screens": [
    {
      "id": "SCREEN_ID",
      "title": "Screen Title",
      "layout": { ... }
    }
  ]
}
```

See **[constraints.md](reference/constraints.md)** for complete validation rules and **[server-integration.md](reference/server-integration.md)** for endpoint setup.

---

## Essential Constraints

| Item | Limit | Impact |
|------|-------|--------|
| Components per screen | 50 | Split into multiple screens if exceeded |
| Nesting depth (If/Switch) | 3 levels | Simplify logic or use separate screens |
| Flow JSON size | 10MB | Compress or split large flows |
| Text heading length | 80 chars | Be concise with titles (NO markdown) |
| Text body length | 4096 chars | Supports markdown v5.1+ (set `markdown: true`) |
| Dropdown options | 200 (static) | Use dynamic data for more options |
| Image max size | 300KB | Optimize images before including |
| Image count per screen | 3 | Limit media usage per screen |
| Screen title | Required | Business 3.0 API requirement |

See **[constraints.md](reference/constraints.md)** for complete reference.

---

## Core Reference Files

Navigate to these for detailed guidance:

### Components
**[reference/components.md](reference/components.md)** - All 22 components with syntax and examples
- Text: TextHeading, TextSubheading, TextBody, TextCaption, RichText
- Input: TextInput (7 types), TextArea, DatePicker
- Selection: Dropdown, CheckboxGroup, RadioButtonsGroup, OptIn, ChipsSelector, NavigationList
- Media: Image, ImageCarousel
- Actions: Footer, EmbeddedLink
- Logic: If, Switch

### Actions
**[reference/actions.md](reference/actions.md)** - Control flow progression
- `navigate` - Move to next screen
- `data_exchange` - Send to server, receive next screen
- `complete` - End flow with response
- `update_data` - Update screen state (v6.0+)
- `open_url` - Open external link (v6.0+)

### Data Binding
**[reference/data-binding.md](reference/data-binding.md)** - How to reference data
- Form data: `${form.field_name}`
- Server data: `${data.field_name}`
- Global references: `${screen.SCREEN_ID.form.field}`
- Nested expressions: `${`...`}` (v6.0+)

### Conditional Logic
**[reference/conditional-logic.md](reference/conditional-logic.md)** - If and Switch components
- Boolean conditions with If
- Multi-way branching with Switch
- Nested conditionals (max 3 levels)
- Conditional navigation and inputs

### Server Integration
**[reference/server-integration.md](reference/server-integration.md)** - Backend integration
- Routing models for flow control
- Data endpoints (request/response format)
- Dynamic data from server
- Error handling and validation

### Constraints & Validation
**[reference/constraints.md](reference/constraints.md)** - Limits and rules
- Character limits per component
- Component counts per screen
- Validation checklist
- Common errors and fixes

### Security & Best Practices
**[reference/security.md](reference/security.md)** - Secure flows
- Sensitive data handling
- HTTPS requirements
- Input validation patterns
- GDPR compliance

### Versions & Features
**[reference/versions.md](reference/versions.md)** - Feature matrix v4.0-7.1
- Component availability by version
- Breaking changes between versions
- Migration guide
- Version recommendations

### Navigation
**[reference/TABLE_OF_CONTENTS.md](reference/TABLE_OF_CONTENTS.md)** - Find what you need
- By topic, use case, component type
- Quick reference guides

---

## Examples

See **[examples.md](examples.md)** for 4 complete, working flows:

1. **Simple Multi-Screen Survey** - Basic form with navigation
2. **Conditional Age Verification** - If/Switch with routing decisions
3. **E-Commerce Product Selection** - Dynamic data from server
4. **Server Validation Flow** - Email validation with error handling

---

## Common Tasks

### I need to add formatted text (bold, lists, emphasis)

1. Use **TextBody** or **TextCaption** components (not TextHeading)
2. Add `"markdown": true` property to enable formatting
3. Use markdown syntax: `**bold**`, `*italic*`, `\n` for line breaks, `• item` for lists
4. Without `markdown: true`, markdown syntax displays as plain text
5. For rich formatting with headers/tables, use **RichText** instead
6. See [components.md](reference/components.md) text components section

**Example:**
```json
{
  "type": "TextBody",
  "text": "**Important:** Please read the following carefully.\n\n• First item\n• Second item",
  "markdown": true
}
```

### I need to collect user information

1. Create a screen with TextInput, TextArea, DatePicker components
2. Add Footer with navigate action to next screen
3. On confirmation screen, use global reference `${screen.FIRST_SCREEN.form.field_name}`
4. Make sure every screen has a `title` property (Business 3.0 requirement)
5. See [components.md](reference/components.md) input section

### I need conditional branching

1. Use If component for true/false decisions
2. Use Switch component for multiple options
3. Reference form data: `${form.field_name}` or `${screen.X.form.field}`
4. Maximum 3 levels of nesting allowed
5. See [conditional-logic.md](reference/conditional-logic.md)

### I need to validate with a backend

1. Add `data_api_version: "3.0"` and `routing_model` to flow
2. Add `data_exchange` action to Footer/DatePicker/selection component
3. Server receives form data in payload
4. Server validates and responds with next screen or errors
5. See [server-integration.md](reference/server-integration.md)

### I need to display dynamic data

1. Declare data schema on screen with `__example__` values
2. Use data_exchange action to fetch from server
3. Reference with `${data.field_name}` in Dropdown, NavigationList, text
4. See [data-binding.md](reference/data-binding.md)

### I need to validate my Flow JSON

```bash
# Full validation
python scripts/validate_flow.py your-flow.json

# Component-specific validation
python scripts/validate_components.py your-flow.json
```

Validators check:
- JSON syntax
- Required properties
- Component counts
- Character limits
- Field name matching

---

## Best Practices

### Form Design
1. Keep screens focused - one question per screen is ideal
2. Use clear, concise labels
3. Provide helpful validation messages
4. Show progress through multi-step flows
5. Make required fields obvious

### Data Handling
1. Always validate on server (never trust client)
2. Use global references `${screen.X.form.field}` instead of payloads
3. Mark sensitive fields with `sensitive: true`
4. Never expose sensitive data in error messages
5. Use HTTPS for all external URLs

### Conditional Logic
1. Keep conditions simple (one or two checks)
2. Use Switch instead of nested If for many options
3. Test all branches thoroughly
4. Provide feedback for conditional content
5. Document complex logic with comments

### Performance
1. Keep JSON under 1MB when possible
2. Optimize image sizes (max 300KB)
3. Limit components per screen (max 50)
4. Use server pagination for large datasets
5. Cache dynamic data when appropriate

### Mobile Considerations
1. Design for small screens (320px width)
2. Keep text concise and readable
3. Test on actual devices
4. Use larger touch targets (buttons)
5. Minimize scrolling

---

## Troubleshooting

### "condition is always false"
- Check field name matches component `name` property (case-sensitive)
- Verify field exists before referencing
- Use `${form.field}` not `${form.Field}`

### "Field validation errors don't appear"
- Ensure server returns errors with matching field names
- Check response format includes `errors` object
- Verify field names match input component `name` properties

### "Dynamic data not showing"
- Check data schema includes `__example__` for all properties
- Verify server response includes the data
- Use correct binding syntax: `${data.field_name}`
- Check component supports dynamic data (Dropdown, NavigationList)

### "Navigation not working"
- Verify next_screen exists in screens array
- Check screen IDs are unique (case-sensitive)
- For data_exchange, ensure routing_model includes path
- Verify action is in correct component (Footer, EmbeddedLink, etc.)

### "JSON validation fails"
- Run `python scripts/validate_flow.py` for error details
- Check required properties present (version, screens, layout)
- Verify no undefined component types
- Check screen ID and field name rules (alphanumeric + underscore)

See **[constraints.md](reference/constraints.md)** for complete validation rules and common errors.

---

## Version Information

Currently supports **WhatsApp Flow JSON v4.0 - v7.1**.

**For new flows, use v7.1** with `data_api_version: "3.0"`.

Key features by version:
- v4.0: Core flows, components, basic validation
- v5.0: RichText component
- v6.0: Nested expressions, update_data, open_url actions
- v6.2: NavigationList component
- v6.3: ChipsSelector, ImageCarousel
- v7.0+: Performance improvements

See **[versions.md](reference/versions.md)** for complete feature matrix and migration guide.

---

## Security Checklist

Before deploying flows with sensitive data:

- [ ] All URLs use HTTPS (no HTTP)
- [ ] Sensitive fields marked with `sensitive: true`
- [ ] All user input validated server-side
- [ ] Errors don't leak information
- [ ] Sensitive data not in logs
- [ ] Rate limiting enabled on endpoints
- [ ] Flow token validation implemented
- [ ] GDPR compliance verified

See **[security.md](reference/security.md)** for detailed security practices.

---

## Getting Help

- Check **[reference/TABLE_OF_CONTENTS.md](reference/TABLE_OF_CONTENTS.md)** for navigation by topic or use case
- See **[examples.md](examples.md)** for working flows you can adapt
- Run validation tools: `python scripts/validate_flow.py`
- Review **[constraints.md](reference/constraints.md)** for limits and rules
- Check **[versions.md](reference/versions.md)** if using older Flow versions

---

## Next Steps

1. **Read examples** - See [examples.md](examples.md) for working flows
2. **Choose your components** - See [components.md](reference/components.md)
3. **Plan your actions** - See [actions.md](reference/actions.md)
4. **Design data flow** - See [data-binding.md](reference/data-binding.md)
5. **Validate your flow** - Run `python scripts/validate_flow.py your-flow.json`
6. **Test thoroughly** - All screens, all navigation paths, all conditions
7. **Deploy** - Upload to WhatsApp Business API
