---
name: guest-outreach-email
description: "Writes a personalized outreach email inviting a specific person to appear as a guest on a podcast episode, with a clear pitch for why this conversation would be valuable to them and their audience."
status: stable
category: podcast
subcategory: business
version: 1.0
eval_score: 4.5
tags: [podcast, business, guests, outreach, email]
---
# Guest Outreach Email

## What This Skill Does
Writes a personalized outreach email inviting a specific person to appear as a guest on a podcast episode, with a clear pitch for why this conversation would be valuable to them and their audience.

## When To Use This Skill
- You want to invite a specific expert, author, practitioner, or public figure as a podcast guest
- Your generic guest invitation emails are not getting responses and you need a more compelling approach
- You are reaching out to a higher-profile guest than you have hosted before and need the pitch to feel credible
- You want to invite multiple guests in a short period and need a strong template that can be personalized quickly

## What You Need To Provide
**Required:**
- Guest name and their relevant background (what they do, what they are known for)
- Your show name and a brief description of your show and its audience
- Why you want this specific guest — what specific topic, idea, or story you want to explore with them
- Your show's download/listenership size (approximate is fine)

**Optional:**
- A specific hook — a question or framing for the conversation that will make the guest curious about the episode
- Any connection you have to the guest (mutual contact, prior interaction, comment on their work)
- A specific piece of their work you want to reference (book, article, talk, project)
- Whether you are offering a specific air date or are flexible on timing
- Anything notable about your show's recent guests or press coverage that signals credibility

## How the Assistant Approaches This
1. Opens with a specific, genuine reason why this person — not a generic expert in their field, but this person specifically — is the right guest for this episode
2. Introduces the show briefly and credibly — enough for the guest to assess fit, not a full pitch document
3. States the episode idea in one clear sentence — a specific question or framing that makes the conversation sound genuinely interesting, not just "I'd love to have you on to discuss your work"
4. Makes the ask concrete and low-friction: what format, approximately how long, how much preparation is required
5. Closes with a single clear CTA — usually a brief call or email reply — and signals flexibility on timing
6. Closes with a "Next Step" note: how long to wait before a follow-up if there is no reply (typically 7–10 days), and whether guest-research-brief or interview-question-builder should be run in parallel while waiting for confirmation

## Output Format
- Email format: subject line + body, 200–300 words maximum
- No attachments or links mentioned unless the user specifies (keep the first email clean)
- Tone: warm, specific, collegial — this is a professional invitation, not a fan letter and not a formal request
- Subject line: specific and interest-generating (references the guest's work or the episode idea, not just "Podcast Invitation")
- One paragraph maximum on the show before pivoting to the episode idea
- Output ends with a "Next Step" note: when to follow up if no reply, and whether to run guest-research-brief or interview-question-builder while waiting for confirmation

## Quality Criteria
- [ ] The opening sentence references something specific about the guest's work — not their job title alone
- [ ] The episode idea is stated as a specific question or framing, not as "discussing your expertise"
- [ ] The show description is one paragraph or less — the focus is on why this conversation is interesting, not on selling the show
- [ ] The ask is specific: format, length, low preparation requirement
- [ ] The email is under 300 words — if it is longer, it is too long
- [ ] Output includes at least one concrete next action the user can take immediately (send the email, set a follow-up reminder, or run guest-research-brief)

## Example

### Input
- **Guest:** Dr. Priya Anand — a psychologist who studies decision fatigue and has a recently published book on how professionals make worse decisions as the day progresses. She has given a well-circulated talk on decision architecture in workplaces.
- **Show:** *Working Orders* — a podcast about workplace law and employment practice for managers and HR professionals. 8,500 downloads per episode, twice-weekly.
- **Why this guest:** The topic connects directly to a recent episode on performance management — the question of whether poor decisions in disciplinary situations are partly a function of when in the day they happen
- **Hook:** New research from Dr. Anand's book suggesting that disciplinary decisions made in the afternoon are statistically harsher than identical decisions made in the morning
- **Reference:** Her book *The Afternoon Effect* (published 6 months ago)
- **Notable recent guests:** Senior government labor officials, Fortune 500 CHROs

### Output

**Subject: The Afternoon Effect and workplace decisions — Working Orders**

---

Hi Dr. Anand,

I've been thinking about your research in *The Afternoon Effect* since I read it in January — specifically the finding that disciplinary decisions made in the afternoon are statistically harsher than identical decisions made in the morning. I work with an audience of managers and HR professionals who make exactly those decisions every day, and I think this is the most practically important finding in employment psychology that most of them have never heard of.

*Working Orders* is a twice-weekly podcast about workplace law and employment practice. We have about 8,500 listeners per episode — mostly HR directors, people operations leads, and senior managers. We've recently had senior officials from the Department of Labor and CHROs from major employers; the audience is sophisticated and genuinely interested in evidence, not just opinion.

I'd love to have a 30-minute conversation with you specifically about what the decision-fatigue research means for employment practice: performance management, disciplinary processes, hiring decisions. Not a general overview of your book — a specific conversation about the professional and legal stakes of making important decisions at the wrong time of day.

The recording is remote and takes around 45 minutes including setup. No preparation beyond what you already know required.

Would a brief call to see if this is a good fit work for you? I'm flexible on timing — happy to work around your schedule.

[Host name]
*Working Orders*
[email]

---

## Known Limitations
- The assistant cannot know the guest's current workload, media saturation level, or whether they are actively seeking podcast appearances — a well-crafted email to someone who is not currently doing press will still be ignored; this skill maximizes the quality of the email, not the response rate
- The personal reference to the guest's work depends entirely on what the user provides — a vague input ("she writes about psychology") will produce a vague opening; the more specific the reference to the guest's actual work, the stronger the email
- For high-profile guests (major public figures, celebrities, political figures), outreach should go through a manager or publicist, not a direct email — this skill is designed for professional and expert guests, not public personalities who have formal gatekeeping
- This skill writes the initial outreach; it does not write follow-up emails or handle scheduling logistics

## Related Skills
- [interview-question-builder](../../pre-production/interview-question-builder/SKILL.md)
- [guest-research-brief](../../pre-production/guest-research-brief/SKILL.md)
- [podcast-media-kit-generator](../podcast-media-kit-generator/SKILL.md)
