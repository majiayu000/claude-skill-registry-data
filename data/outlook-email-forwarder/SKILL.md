---
name: "Outlook Email Forwarder"
description: "A skill that checks Outlook 365 company mail, finds specific emails, checks for attachments, and forwards them to another email address."
---

# Outlook Email Forwarder Skill

## Purpose
This skill allows Claude to connect to Outlook 365 company mail, search for specific emails based on criteria, check if they have attachments, and forward them to another email address.

## Prerequisites
- Microsoft 365 account with appropriate permissions
- Azure AD application with required API permissions (Mail.Read, Mail.ReadWrite, Mail.Send)
- Client ID, Client Secret, and Tenant ID for authentication
- User must provide these credentials when prompted

## Usage Instructions
1. Claude will prompt for required authentication parameters if not already provided
2. User specifies search criteria for the email (subject, sender, date range, etc.)
3. User specifies the recipient email address for forwarding
4. Claude will search for the email, check for attachments, and forward the email

## Parameters
- `search_criteria`: String containing search criteria (e.g., "subject:Quarterly Report from:manager@company.com")
- `recipient_email`: Email address to forward the message to
- `include_attachments`: Boolean indicating whether to include attachments (default: true)

## Process
1. Authenticate with Microsoft Graph API
2. Search for emails matching the criteria
3. If email found, check for attachments
4. Forward the email to the specified recipient
5. Return confirmation of the forwarding action

## Security Considerations
- All credentials are handled securely
- Only emails from the authenticated user's inbox can be accessed
- Forwarding is limited to the specified recipient