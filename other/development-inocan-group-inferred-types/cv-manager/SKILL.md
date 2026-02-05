---
name: cv-manager
description: Expert in managing professional candidate CVs and interview records. **Use this skill whenever the user mentions 'add a CV', 'add new professional interview', 'add an interview', 'view the CV', 'summarize a candidate', 'candidate summary', or requests to process recruitment-related documents and interview notes.** Handles CV upload to Google Drive, information extraction, interview transcription, and structured documentation in Google Docs. (project, gitignored)
---

# CV Manager

## Overview

Manage candidate CVs and interview records in a structured Google Drive/Docs system. Store CVs in a dedicated Drive folder and maintain a master tracking document with candidate profiles and interview summaries.

## Core Capabilities

This skill provides three main workflows:

1. **Add a CV** - Upload and process new candidate CVs
2. **Add an Interview** - Record and structure interview notes
3. **Summarize a Candidate** - Generate comprehensive candidate summaries

## Configuration

**Reference:** `references/configuration.md` for Google Drive folder IDs and document IDs.

**Key Resources:**
- CV Storage Folder: `1n5sMW4L_NHpnIFVogRD2I3jPvKk2WQUw`
- Interview Files Folder: `1fRRtK3TPxbTDSPw_KufOrYLHMNuelLp0` (audio recordings, attachments)
- Tracking Document: `1M83HrxnWIOYUGk_jtaaLS_eo5_-sIlHmi_1ZAwCdRWI`

## Document Structure

**Reference:** `references/document-structure.md` for detailed structure template.

**Master Document Structure:**
- **Heading 1 (Title):** CVs
- **Heading 2:** Table of content

**Per-Candidate Hierarchy:**
- **Heading 2:** Candidate Name
- **Heading 3:** Presentation (CV info, job title, 100-200 word description)
- **Heading 3:** Interview
- **Heading 4:** Interview Date
- **Heading 5:** Attendees
- **Heading 5:** Summary (interview content)

**Note:** Each candidate is a Heading 2 section within the master tracking document.

## Workflow 1: Add a CV

**Trigger:** User provides a local CV file (PDF, DOCX, etc.) and candidate name.

**Steps:**

1. **Receive the CV file**
   - User provides local file path to CV
   - Confirm candidate name

2. **Extract CV information**
   - Use `scripts/run.sh extract_cv <file_path>` to extract text from PDF
   - Use `pdf-extractor` skill for complex PDFs if needed
   - Analyze extracted text to identify:
     - Job title/role
     - Key skills and expertise
     - Experience highlights
     - Notable achievements

3. **Generate presentation content**
   - Draft **Job Title** summary
   - Write 100-200 word description with main skills
   - Present draft to user for review
   - If user requests, run `open <file_path>` to view original CV

4. **Upload CV to Google Drive**
   - Use `google-drive-manager` skill to upload file to CV Storage Folder
   - Folder ID: `1n5sMW4L_NHpnIFVogRD2I3jPvKk2WQUw`
   - File name format: `<Candidate Name> - CV.pdf`
   - Capture the returned Google Drive link

5. **Get formal validation**
   - Present complete entry to user:
     - Candidate name (Heading 2)
     - Presentation section with CV link, job title, description
   - Request approval before insertion

6. **Insert into tracking document**
   - Use `google-docs-manager` skill to:
     - Create new Heading 2 with candidate name
     - Add Presentation section (Heading 3)
     - Insert CV Link, Job Title, and description
     - Create empty Interview section (Heading 3)
   - Document ID: `1M83HrxnWIOYUGk_jtaaLS_eo5_-sIlHmi_1ZAwCdRWI`
   - Insert after "Table of content" section

7. **Cleanup**
   - Remove local CV file using `rm <file_path>`
   - Confirm completion to user

## Workflow 2: Add an Interview

**Trigger:** User provides interview notes and/or audio recordings for existing candidate.

**Steps:**

1. **Identify candidate**
   - User provides candidate name
   - Use `google-docs-manager` skill to verify candidate exists in tracking document
   - Locate their Interview section (Heading 3)

2. **Upload interview files to Drive (if provided)**
   - **If audio file or other attachments provided:**
     - Use `google-drive-manager` skill to upload file to Interview Files Folder
     - Folder ID: `1fRRtK3TPxbTDSPw_KufOrYLHMNuelLp0`
     - Files are backed up for future reference

3. **Process interview content**
   - **If audio file provided:**
     - Use `speech-to-text` skill to transcribe audio
     - Save transcription as interview notes
   - **If text notes provided:**
     - Use notes directly

4. **Extract interview information**
   - Identify interview date
   - Extract or confirm attendee list
   - Present attendee list to user for confirmation
   - Draft interview summary including:
     - **First paragraph:** Global feeling, strengths, weaknesses
     - **Main content:** Key discussion points, technical assessments, notable responses

5. **Get formal validation**
   - Present complete interview entry:
     - Interview date (Heading 4)
     - Attendees section (Heading 5) with plain text list
     - Summary section (Heading 5)
     - Overall assessment paragraph
     - Main interview discussion summary
   - Request user to provide final thoughts
   - Incorporate user feedback and re-present if needed

6. **Insert into document**
   - Use `google-docs-manager` skill to:
     - Navigate to candidate's Interview section (Heading 3)
     - Add new Heading 4 with interview date
     - Add Heading 5 "Attendees" with plain text list (not bullets)
     - Add Heading 5 "Summary"
     - Insert overall assessment paragraph
     - Insert main interview discussion summary
   - Document ID: `1M83HrxnWIOYUGk_jtaaLS_eo5_-sIlHmi_1ZAwCdRWI`

7. **Cleanup**
   - Automatically remove local interview files using `rm <file_path>`
   - Files are already backed up in Google Drive (Folder: `1fRRtK3TPxbTDSPw_KufOrYLHMNuelLp0`)
   - Confirm completion to user

## Workflow 3: Summarize a Candidate

**Trigger:** User requests summary or information about a specific candidate.

**Steps:**

1. **Locate candidate information**
   - User provides candidate name
   - Use `google-docs-manager` skill to read tracking document
   - Document ID: `1M83HrxnWIOYUGk_jtaaLS_eo5_-sIlHmi_1ZAwCdRWI`
   - Find candidate's Heading 2 section

2. **Extract all information**
   - Read candidate's Heading 2 section
   - Read Presentation section (Heading 3):
     - CV link
     - Job title
     - Description
   - Read all Interview sections (Heading 3):
     - Interview dates (Heading 4)
     - Attendees (Heading 5)
     - Summary content (Heading 5)
     - Overall assessments
     - Discussion points

3. **Generate comprehensive summary**
   - Candidate overview (from Presentation)
   - Interview history:
     - Number of interviews conducted
     - Dates and attendees
     - Key feedback from each interview
     - Overall strengths noted across interviews
     - Areas of concern noted across interviews
   - Recommendation or next steps (if applicable from interviews)

4. **Present summary to user**
   - Formatted, clear summary with all relevant details
   - Include CV link for reference

## Resources

### scripts/

**run.sh** - Generic script runner using `uv` for isolated Python environments
- Usage: `./run.sh <script_name> [args...]`
- Automatically loads environment variables from `.env` files
- Creates isolated Python environments for dependencies

**extract_cv.py** - Extract text from CV files
- Usage: `scripts/run.sh extract_cv <file_path>`
- Supports: PDF files
- Returns: Extracted text to stdout

### references/

**configuration.md** - Google Drive and Docs IDs, authentication setup
**document-structure.md** - Detailed template and example of document structure

## Integration with Other Skills

- **pdf-extractor**: Use for complex PDF extraction when `extract_cv.py` fails
- **google-docs-manager**: Primary tool for reading/writing tracking document
- **google-drive-manager**: Alternative for Drive operations if needed
- **speech-to-text**: Transcribe interview audio recordings
- **email-extractor**: Extract CV from email attachments if sent via email

## Important Notes

- Always get formal validation from user before inserting content into tracking document
- Respect the document structure hierarchy (Heading 2-5 for candidates) strictly
- One candidate can have multiple interviews but only one Presentation section
- Attendees are listed as plain text (not bullets) under the Attendees heading
- Summary section contains two paragraphs: overall assessment first, then detailed discussion
- Always insert new candidates after "Table of content" section
- Clean up local files after upload to Drive
- Use `open <file>` command when user wants to review the local CV before processing
- Each candidate is a Heading 2 section within the master tracking document
