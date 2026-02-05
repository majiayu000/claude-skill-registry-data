---
name: email-sender
description: Compose and send professional emails with optional attachments and formatting
version: 1.0.0
author: AgentSkills.NET Examples
tags:
  - communication
  - email
  - productivity
allowed-tools:
  - email
  - filesystem
---

# Email Sender

Compose and send professional emails with support for attachments, formatting, and multiple recipients.

## Purpose

This skill enables you to send emails when needed for communication, notifications, or automated workflows. Use it when the user requests email functionality or when a workflow requires email notification.

## Instructions

Follow this process when sending an email:

### 1. Gather Information

Collect all necessary information before composing:
- **Recipients**: Email addresses (To, CC, BCC)
- **Subject**: Clear, concise subject line
- **Body**: The message content
- **Attachments**: Optional file paths
- **Priority**: Normal, High, or Low
- **Format**: Plain text or HTML

### 2. Validate Input

Before sending, verify:
- All email addresses are valid format (user@domain.com)
- Subject line is not empty
- Body contains meaningful content
- Attachment paths exist (if specified)
- Total attachment size is reasonable (< 25 MB)

### 3. Compose the Email

Structure the email professionally:
- Use proper greeting ("Dear [Name]" or "Hi [Name]")
- Keep paragraphs concise
- Use clear, professional language
- Include call-to-action if needed
- End with appropriate closing ("Best regards", "Thank you")
- Include signature if appropriate

### 4. Review Before Sending

Double-check:
- Recipients are correct (no typos)
- Subject is descriptive
- Body is error-free
- Attachments are correct
- Tone is appropriate

### 5. Send the Email

Execute the send operation and report:
- Success confirmation with message ID
- Any errors encountered
- Retry strategy if sending fails

## Examples

### Example 1: Simple Email

**Input:**
- To: john.doe@example.com
- Subject: Meeting Tomorrow
- Body: Hi John, Just confirming our meeting tomorrow at 2 PM. See you then!

**Output:**
```
✓ Email sent successfully
Message ID: msg-12345
Sent to: john.doe@example.com
Subject: Meeting Tomorrow
```

### Example 2: Email with Attachment

**Input:**
- To: team@example.com
- CC: manager@example.com
- Subject: Monthly Report - December 2024
- Body: Please find attached the monthly report for your review.
- Attachments: /reports/december-2024.pdf

**Output:**
```
✓ Email sent successfully
Message ID: msg-12346
Sent to: team@example.com
CC: manager@example.com
Subject: Monthly Report - December 2024
Attachments: december-2024.pdf (2.3 MB)
```

### Example 3: HTML Formatted Email

**Input:**
- To: clients@example.com
- Subject: New Features Available
- Format: HTML
- Body:
  ```html
  <h1>Exciting Updates!</h1>
  <p>We're thrilled to announce new features:</p>
  <ul>
    <li>Dark mode support</li>
    <li>Advanced search</li>
    <li>Mobile app</li>
  </ul>
  <p>Learn more at <a href="https://example.com">our website</a>.</p>
  ```

**Output:**
```
✓ HTML email sent successfully
Message ID: msg-12347
Sent to: clients@example.com (distribution list)
Subject: New Features Available
```

## Error Handling

Handle these common errors gracefully:

### Invalid Email Address
```
❌ Error: Invalid email address 'not-an-email'
Suggestion: Check the email format (should be user@domain.com)
```

### Attachment Not Found
```
❌ Error: Attachment not found '/path/to/file.pdf'
Suggestion: Verify the file path exists and you have read permissions
```

### Send Failure
```
❌ Error: Failed to send email (SMTP timeout)
Suggestion: Retry in 30 seconds or check network connectivity
```

### Quota Exceeded
```
❌ Error: Daily email quota exceeded (limit: 100 emails/day)
Suggestion: Wait until tomorrow or contact administrator
```

## Best Practices

1. **Always validate recipients** - Prevent sending to wrong addresses
2. **Use descriptive subjects** - Help recipients identify important emails
3. **Keep it concise** - Respect recipient's time
4. **Format properly** - Use paragraphs, lists, and formatting
5. **Proofread** - Check for errors before sending
6. **Be mindful of attachments** - Large files may be blocked
7. **Respect privacy** - Use BCC for distribution lists
8. **Track important emails** - Log message IDs for reference

## Security Considerations

- Never send passwords or sensitive data in plain text emails
- Verify recipient addresses to prevent data leaks
- Use encryption for confidential information
- Be aware of phishing risks in email content
- Validate all user inputs to prevent injection attacks
- Respect opt-out requests and unsubscribe preferences

## Templates

### Professional Request
```
Subject: Request for [Resource/Information]

Dear [Name],

I hope this email finds you well.

I am writing to request [specific request]. This would help us [reason/benefit].

Would it be possible to [action requested] by [date/time]?

Please let me know if you need any additional information.

Thank you for your consideration.

Best regards,
[Your Name]
```

### Status Update
```
Subject: Status Update - [Project Name]

Hi [Name/Team],

Quick update on [project]:

Progress:
- ✓ Completed: [items]
- 🔄 In Progress: [items]
- 📋 Upcoming: [items]

Blockers: [any issues or none]

Next Steps: [what's coming]

Let me know if you have questions.

Thanks,
[Your Name]
```

### Meeting Confirmation
```
Subject: Confirming Meeting - [Date/Time]

Hi [Name],

Confirming our meeting:

📅 Date: [date]
🕐 Time: [time with timezone]
📍 Location: [location or video link]
📋 Agenda: [brief agenda]

Please let me know if you need to reschedule.

Looking forward to speaking with you.

Best,
[Your Name]
```

## Notes

- This skill requires email tool access (specified in allowed-tools)
- Actual email sending is performed by the host environment
- This skill provides guidance for proper email composition
- Always follow organizational email policies and guidelines
