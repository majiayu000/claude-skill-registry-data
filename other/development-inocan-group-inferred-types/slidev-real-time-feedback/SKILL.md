---
id: slidev-feedback
name: Slidev Real-time Feedback
version: 1.0.0
description: Enable live audience reactions and feedback during Slidev presentations with WebSocket-powered real-time updates
icon: 📊
category: engagement
author: Amagen Skill Exchange
tags:
  - slidev
  - presentation
  - feedback
  - realtime
  - websocket
  - audience-engagement
contexts:
  - dashboard
  - embedded
  - universal
executionMode: realtime
features:
  realtime: true
  ai: false
  adaptive: true
  analytics: true
  collaborative: true
  offline: false
  requiresAuth: false
parameters:
  - name: presentationTitle
    type: string
    required: true
    description: Title of your presentation
    defaultValue: "My Presentation"
    validation:
      minLength: 3
      maxLength: 100
  - name: totalSlides
    type: number
    required: true
    description: Total number of slides in your presentation
    defaultValue: 20
    validation:
      min: 1
      max: 500
  - name: allowedReactions
    type: array
    required: true
    description: Emoji reactions allowed for audience feedback
    defaultValue:
      - "👍"
      - "❤️"
      - "🔥"
      - "🤔"
      - "👏"
    validation:
      minItems: 1
      maxItems: 10
  - name: enableQuestions
    type: boolean
    required: false
    description: Allow audience to submit text questions
    defaultValue: true
  - name: requireAuth
    type: boolean
    required: false
    description: Require user authentication to participate
    defaultValue: false
  - name: sessionDuration
    type: number
    required: false
    description: Auto-close session after N hours (0 = manual close)
    defaultValue: 0
    validation:
      min: 0
      max: 24
  - name: moderateQuestions
    type: boolean
    required: false
    description: Review questions before displaying to presenter
    defaultValue: false
  - name: theme
    type: string
    required: false
    description: Widget color theme
    defaultValue: "auto"
    validation:
      enum:
        - light
        - dark
        - auto
storage:
  backend: cloudflare-durable-objects
  durableObjects:
    - name: FEEDBACK_DO
      className: SlidevFeedbackDO
pricing:
  creditsPerUse: 10
  model: per-session
requiresDurableObjects: true
manifestPath: ./dist/manifest.js
examples:
  - title: "Workshop Feedback"
    description: "Interactive workshop with questions and understanding checks"
    config:
      presentationTitle: "React Hooks Deep Dive"
      totalSlides: 30
      allowedReactions: ["✅", "❓", "💡", "👏"]
      enableQuestions: true
      requireAuth: false
      moderateQuestions: false
      sessionDuration: 2
      theme: "auto"
  - title: "Corporate Presentation"
    description: "Business presentation with moderated Q&A"
    config:
      presentationTitle: "Q4 Sales Strategy"
      totalSlides: 25
      allowedReactions: ["👍", "💼", "📊", "🎯"]
      enableQuestions: true
      requireAuth: true
      moderateQuestions: true
      sessionDuration: 1
      theme: "dark"
  - title: "Conference Talk"
    description: "Large audience with quick reactions only"
    config:
      presentationTitle: "The Future of Web Development"
      totalSlides: 45
      allowedReactions: ["❤️", "🔥", "🚀", "🤯", "👏"]
      enableQuestions: false
      requireAuth: false
      moderateQuestions: false
      sessionDuration: 0
      theme: "auto"
---

# Slidev Real-time Feedback Skill

Transform your Slidev presentations into interactive experiences with real-time audience feedback and reactions.

## Instructions

This skill creates a real-time feedback system for Slidev presentations. When imported:

1. **Configure** your presentation details (title, slide count, allowed reactions)
2. **Deploy** the skill to generate a unique widget URL and QR code
3. **Embed** the widget in your Slidev presentation or share the URL with your audience
4. **Monitor** live reactions and questions through the presenter dashboard
5. **Export** analytics after your presentation for detailed insights

The skill uses WebSocket-powered Durable Objects for real-time synchronization between presenter and audience. All configuration is done through the 8 parameters defined in the frontmatter above.

## Overview

The Slidev Real-time Feedback skill enables presenters to gather live reactions, questions, and engagement metrics from their audience during presentations. Built on Cloudflare Durable Objects for scalable real-time performance, this skill provides instant feedback loops that help presenters adjust their delivery on the fly.

## Features

### ✨ Real-time Audience Engagement
- **Live Emoji Reactions**: Customizable emoji reactions for instant audience sentiment
- **Question Submission**: Allow audience to ask questions without interrupting
- **Slide Synchronization**: Automatic slide tracking for contextual feedback
- **Participant Counter**: See how many people are actively engaged

### 📊 Presenter Dashboard
- **Live Reaction View**: See reactions as they happen, organized by slide
- **Question Management**: Review, moderate, and respond to audience questions
- **Analytics Export**: Download detailed engagement data for post-presentation analysis
- **Navigation Controls**: Control slide progression and pause for Q&A

### 🎨 Embeddable Widget
- **Responsive Design**: Works on any device - desktop, tablet, or mobile
- **Theme Support**: Light, dark, and auto themes to match your presentation
- **QR Code Access**: Generate QR codes for easy audience access
- **Anonymous or Authenticated**: Choose whether to require login

### 🔒 Enterprise Features
- **Question Moderation**: Review questions before displaying to audience
- **Session Timeouts**: Auto-close sessions after a specified duration
- **Access Control**: Require authentication for sensitive presentations
- **Data Privacy**: All data stored securely with automatic cleanup

## How It Works

### For Presenters (Dashboard Mode)

1. **Create Session**: Configure your presentation details and allowed reactions
2. **Share Widget**: Get an embed code or QR code to share with your audience
3. **Monitor Feedback**: Watch reactions and questions appear in real-time
4. **Control Flow**: Navigate slides and moderate content as needed
5. **Export Data**: Download analytics for future reference

### For Audience (Embedded Widget Mode)

1. **Scan QR Code**: Access the feedback widget on any device
2. **React to Slides**: Tap emoji reactions to provide instant feedback
3. **Ask Questions**: Submit text questions without interrupting
4. **Stay Synced**: Widget automatically updates with current slide
5. **See Engagement**: View how many others are participating

## Use Cases

### 📚 Educational Lectures
- **Student Comprehension**: Quick polls on understanding ("Got it" vs "Confused")
- **Pace Control**: Adjust speed based on real-time feedback
- **Question Queue**: Organize student questions by topic/slide

### 💼 Business Presentations
- **Stakeholder Engagement**: Gauge executive interest and concerns
- **Sales Demos**: Capture prospect reactions to different features
- **Training Sessions**: Check understanding and collect improvement feedback

### 🎤 Conference Talks
- **Large Audiences**: Scalable to hundreds of simultaneous participants
- **Engagement Metrics**: Identify which slides resonate most
- **Q&A Management**: Organize questions for post-talk sessions

### 🧪 Research Presentations
- **Peer Feedback**: Collect colleague reactions to methodology
- **Interest Tracking**: Identify which findings generate most interest
- **Collaboration**: Facilitate discussion in virtual or hybrid settings

## Technical Architecture

### Real-time Infrastructure
```
┌─────────────┐         WebSocket         ┌──────────────────┐
│  Presenter  │◄──────────────────────────►│                  │
│  Dashboard  │                            │  Durable Object  │
└─────────────┘                            │   (Persistent    │
                                           │     State)       │
┌─────────────┐         WebSocket         │                  │
│  Audience   │◄──────────────────────────►│                  │
│   Widget    │                            └──────────────────┘
└─────────────┘
```

**Durable Object Benefits:**
- Single source of truth for session state
- Automatic connection management
- Built-in WebSocket handling
- Global low-latency access
- Persistent across restarts

### Data Flow
1. Presenter creates session → Durable Object instance spawned
2. Audience joins → WebSocket connection established
3. Reactions submitted → Broadcast to all connected clients
4. Slide changes → Synchronized across all participants
5. Session ends → Data exported, connections gracefully closed

## Configuration Examples

**Common Configurations:**
- **Workshop/Training**: Enable questions, moderate if needed, 2-hour auto-close, reactions like ✅❓💡
- **Business Presentation**: Require auth, moderate questions, professional reactions like 👍💼📊
- **Conference Talk**: Disable questions (use Q&A later), open access, engaging reactions like ❤️🔥🚀

All parameters are configured through the widget creation interface. See the 8 parameters in the frontmatter above for full customization options.

## Analytics & Insights

### What You Can Track
- **Engagement Rate**: Reactions per slide
- **Peak Interest**: Slides with most reactions
- **Audience Size**: Participant count over time
- **Question Themes**: Common topics and concerns
- **Session Duration**: Actual vs planned timing
- **Reaction Distribution**: Sentiment analysis per slide

### Export Formats
- JSON (full data export)
- CSV (spreadsheet analysis)
- Analytics Dashboard (visual charts)

## Security & Privacy

### Data Protection
- ✅ Anonymous participation by default
- ✅ Optional authentication for sensitive content
- ✅ No personal data stored without consent
- ✅ Automatic data cleanup after session
- ✅ Encrypted WebSocket connections
- ✅ GDPR compliant

### Access Control
- Session-based tokens for anonymous users
- Email verification for authenticated sessions
- Presenter-only access to raw data
- Public analytics opt-in

## Installation

### Import from GitHub
1. Go to "Add Skill" in your Amagen dashboard
2. Select "Import from GitHub"
3. Enter repository URL: `https://github.com/amagen-skill-exchange/slidev-feedback-skill`
4. Click "Import Skill"

### Create Widget (10 Credits)
1. Navigate to "My Skills"
2. Find "Slidev Real-time Feedback"
3. Click "Create Widget"
4. Configure presentation settings
5. Get embed code and QR code

## Integration

After creating a widget, you'll receive:
- **Widget URL**: `https://widgets.amagen.app/widget/YOUR_WIDGET_ID`
- **QR Code**: For easy mobile access
- **Embed Code**: Ready-to-use iframe snippet

**Quick Embed** (works in Slidev, HTML, or any webpage):
```html
<iframe src="https://widgets.amagen.app/widget/YOUR_WIDGET_ID"
        width="400" height="600" frameborder="0">
</iframe>
```

Share the widget URL or display the QR code during your presentation for audience access.

## Support & Resources

- 📖 [Full Documentation](https://docs.amagen.app/skills/slidev-feedback)
- 💬 [Community Discord](https://discord.gg/amagen)
- 🐛 [Report Issues](https://github.com/amagen-skill-exchange/slidev-feedback-skill/issues)
- ✉️ [Email Support](mailto:support@amagen.app)

## License

MIT License - See LICENSE file for details

## Credits

Built with:
- [Cloudflare Durable Objects](https://developers.cloudflare.com/durable-objects/) - Real-time infrastructure
- [React](https://react.dev/) - UI framework
- [TypeScript](https://www.typescriptlang.org/) - Type safety
- [Zod](https://zod.dev/) - Schema validation
- [@amagen/ui](https://github.com/amagen-skill-exchange/ui) - Component library

Created by the Amagen Skill Exchange community.
