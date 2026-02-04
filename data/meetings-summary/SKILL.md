---
name: meetings-summary
description: Generate comprehensive summary of meeting. **Use this skill when the user requests to 'create meeting summary', 'summarize the meeting', 'generate meeting email'.
---

# Meetings Summary

## Overview

Generate professional HTML email summaries of meetings that include attendees, main topics discussed, decisions taken, and actions decided. The skill integrates with existing skills to process audio recordings, calendar events, and additional attachments into a structured, validated email summary.

**IMPORTANT:** Email summaries are NEVER sent automatically. They must be validated by the user before sending.

## Workflow

### Step 1: Gather Meeting Inputs

Collect the following inputs from the user:

1. **Audio Recording:** Use audio-recorder skill.
   - If audio recording used, ensure it does exist by listing records
   - If not provided, list available recordings and try to figure out the correct recording according to user input. If unsure to identify properly the records, present recordings to user and ask which one to use
   - If user explicitly says "no record", don't try to find a record

1. **Calendar Event:** Use o365-manager skill.
   - If an audio recording is identified at the previous step, use the date of this audio to list event of this day to find a recording with a similar input.
   - If no audio recording are identified and a date of the meeting is provided by the user, try to find event with input maching user information.
   - In any case when identifying the calendar relevant event, if unsure, present the most relevant meeting and if unsure at all, present all the meeting of the day.
   - If event is idenfitied, event details (to get subject, attendees list, date/time of event, agenda) and download attachments

If you find all the relevant information, you can continue the process, but if you are not sure about the event or recording to use, ask for user confirmation.

**IMPORTANT:** If no record nor calendar event is provided, the user must provide clear input to fill the email (meeting name, date, agenda, list of attendees, and minutes of the meeting at least).

### Step 2: Process Recording

If a recording is provided:

1. **Transcribe the audio** using speech-to-text skill: this will provide the discovered attendees list and the minutes of the meeting

2. **Analyze the transcript** to extract:
   - **Attendees**: List of participants identified from transcript and event
   - **Topics discussed**: Discussed topics with details of discussion and important information
   - **Decisions**: Concrete decisions made during the meeting
   - **Actions**: Action items decided with owners if mentioned

**IMPORTANT:** Mentioned attendees must not be part of the attendees list. They can be part of the topics information, decisions or actions, but not in the attendees list.

### Step 3: Merge Data

Combine data from all sources:

1. **Merge attendees** from transcript, event, and possibly provided by user input.
2. **Use event subject** as meeting title (fallback to transcript title and as last resort, as user input)
3. **Use event date/time** for accuracy
4. **Include agenda** from event if available

### Step 4: Generate HTML Summary

With all the information rate the HTML email. The email is composed of 5 sections

The global style to apply to the email is the following:
```html
    <meta charset="UTF-8">
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
        }
        h1 {
            color: #0078d4;
            font-size: 1.5em
            border-bottom: 3px solid #0078d4;
            padding-bottom: 10px;
        }
        h2 {
            font-size: 1.2em
            color: #106ebe;
            margin-top: 25px;
        }
        ul {
            margin: 10px 0;
        }
        li {
            margin: 8px 0;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
        }
        th {
            background-color: #0078d4;
            color: white;
            padding: 12px;
            text-align: left;
        }
        td {
            border: 1px solid #ddd;
            padding: 10px;
        }
        tr:nth-child(even) {
            background-color: #f9f9f9;
        }
        strong {
            color: #106ebe;
        }
    </style>

```

The summary must content:
1. **Meeting information**: Must content the information about the meeting: title, date and agenda, something like:
```html
<h1>📅 Meeting Information</h1>
<strong>Meeting: {meeting title}</strong>
<strong>Date: {meeting date}</stong>
<strong>
```

2. **Attendees Section**: List of participants (bullet point style). When someone was not present in the meeting add `(abs)` after his name and put his name and the word `(abs)` in italic.
```html
<h1>👥 Attendees</h1>
<li>Attendee 1</li>
<li>Attendee 2</li>
<li>Attendee 3</li>
<li><i>Attendee 4 (abs></i></li>
```

3. **Topics discussed Section**: On sub-section per topic, with discussion summarized.
```html
<h1>💬 Topics discussed</h1>
<h2>Topic One</h2>
bla bla bla
<h2>Topic two</h2>
bla bla bla
```

4. **✅ Decisions Section**: List of decisions or "*No decision*" in italic if none was clearly identified (bullet point style). You can add fancy icon to illustrate.
```html
<h1>✅ Decisions</h1>
<li>Decision bla bla</li>
<li>Decision bli bli</li>
<li>Decision blo blo</li>
```

If no decision:
```html
<h1>✅ Decisions</h1>
<i>No decision</i>
```

5. **🎯 Actions Section**: List of actions or "*No action*" in italic if none was clearly identified (a table with the following columns: Label, Owner, ETA. If not ETA is provided write "*not provided*" in italic, same for owner).
```html
<h1>🎯 Actions</h1>
<table>
    <tr>
        <th>Label</th>
        <th>Owner</th>
        <th>ETA</th>
    </tr>
    <tr>
        <td>Action 1</td>
        <td>Toto KLOK</td>
        <td><i>not provided</i></td>
    </tr>
    <tr>
        <td>Action 2</td>
        <td>Tito MAROU</td>
        <td>December 2025</td>
    </tr>
</table>
```

If no actions:
```html
<h1>🎯 Actions</h1>
<i>No decision</i>
```

**NB:** If attachements where provided in the meeting of by the user, add them in the email.

Add as recipient all the attendees of the meeting.
Add as recipient or CC any user mentioned in the actions or decisions plan or provided in the user input. If the input are not emails use relevant the btdp-it-masterdata-retrieval skill to ensure the email address.

Then open the file with the `open` command for user validation.

### Step 5: Final validation

**NEVER send the email** automatically - user must explicitly request sending

When the user review the HTML you must propose:
- Leave the email as draft to sent it manually
- Send it automatically

You need a CLEAR answer to move forward. If modifications are requested, you modify the same file and tell the requester. You don't open it again, you just mention that the file already open can refreshed to see the modification.
