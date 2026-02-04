---
name: business-english-game
description: |
  Create interactive learning games for business English practice.
  Supports multiple game types (quiz, simulation, drag-drop) across
  various business scenarios (emails, meetings, presentations, negotiations).
  Generate HTML/React-based games tailored to user's industry, job role,
  and proficiency level. Use when users request business English learning
  games, practice materials, interactive training content, or educational
  exercises for professional English communication.
---

# Business English Game

## Overview

Generate interactive HTML-based learning games for business English practice. This skill creates engaging, scenario-based exercises covering emails, meetings, presentations, negotiations, and industry-specific vocabulary. Games automatically adapt to user's proficiency level and professional context.

## When to Use This Skill

Use this skill when users request:
- Business English learning games or quizzes
- Interactive practice materials for professional English
- Training exercises for specific business scenarios (emails, meetings, presentations)
- Vocabulary games for industry-specific terms (IT, finance, marketing, etc.)
- Scenario-based simulations for business communication
- Educational content for workplace English

## Game Types

### 1. Multiple Choice Quiz
Create 4-choice quizzes testing business expressions, vocabulary, or appropriate usage in context.

**Example request**: "Create a business email vocabulary quiz"

**Process**:
- Load relevant expressions from `references/business_expressions.md`
- Select appropriate difficulty level
- Use `assets/templates/quiz-template.html`
- Generate 10-15 questions with explanations
- Include immediate feedback and scoring

### 2. Drag & Drop Matching
Create matching games connecting terms, definitions, or sentence components.

**Example request**: "Make a marketing terminology matching game"

**Process**:
- Load industry vocabulary from `references/vocabulary_by_industry.md`
- Use `assets/templates/drag-drop-template.html`
- Create 8-12 matching pairs
- Include visual feedback for correct/incorrect matches

### 3. Scenario Simulation
Create interactive dialogue simulations for business situations.

**Example request**: "Practice meeting discussion phrases with a simulation game"

**Process**:
- Load scenario from `references/scenarios.md`
- Use `assets/templates/scenario-template.html`
- Present branching dialogue choices
- Provide feedback on appropriateness and tone
- Suggest alternative expressions

### 4. Fill in the Blanks
Create cloze exercises with business expressions.

**Example request**: "Create email writing practice with fill-in-the-blanks"

**Process**:
- Select scenario-appropriate templates
- Remove key phrases/vocabulary
- Provide multiple-choice or type-in options
- Show correct answers with explanations

### 5. Sequence Ordering
Create games requiring correct ordering of dialogue or presentation flow.

**Example request**: "Practice presentation structure ordering"

**Process**:
- Present scrambled sequence of expressions
- User arranges in logical order
- Explain proper flow and transitions

## Difficulty Levels

### Beginner
- Common business phrases
- Basic email and meeting vocabulary
- Simple sentence structures
- Clear, formal language

### Intermediate
- Industry-specific terminology
- Nuanced expressions (suggestions, polite disagreement)
- Phrasal verbs and idioms
- Tone matching exercises

### Advanced
- Negotiation and persuasion language
- Cultural nuances and subtleties
- Complex sentence structures
- Executive communication styles

## Customization Parameters

When generating games, consider:
- **Industry**: IT, finance, marketing, HR, manufacturing, logistics, etc.
- **Job role**: Manager, individual contributor, executive, sales, support
- **Scenario**: Email, meeting, presentation, negotiation, networking
- **Skill focus**: Writing, speaking, listening comprehension
- **Time**: Adjust question count for desired play duration (5-30 minutes)

## Content Categories

Available in `references/` files:

1. **Email Writing** (formal/informal)
   - Subject lines
   - Opening/closing phrases
   - Request and response templates
   - Follow-up language

2. **Meeting Participation**
   - Starting meetings
   - Expressing opinions
   - Agreeing/disagreeing politely
   - Asking for clarification
   - Summarizing and closing

3. **Presentations**
   - Introduction and agenda
   - Transition phrases
   - Explaining visuals
   - Handling questions
   - Conclusion techniques

4. **Negotiation & Persuasion**
   - Making proposals
   - Compromising
   - Objection handling
   - Closing deals

5. **Networking & Small Talk**
   - Introductions
   - Industry conversation
   - Building rapport
   - Following up

6. **Phone & Video Calls**
   - Opening calls
   - Technical issues
   - Active listening phrases
   - Closing professionally

## Game Generation Workflow

1. **Understand Request**
   - Identify game type needed
   - Determine difficulty level
   - Note any specific industry/scenario requirements

2. **Select Content**
   - Grep relevant expressions from `references/business_expressions.md`
   - Find matching scenarios from `references/scenarios.md`
   - Load industry vocabulary if specified

3. **Choose Template**
   - Select appropriate HTML template from `assets/templates/`
   - Templates are self-contained with CSS and JavaScript

4. **Generate Game**
   - Use `scripts/game_generator.py` to inject content into template
   - Customize based on user parameters
   - Ensure proper feedback and explanations

5. **Output**
   - Save as standalone HTML file
   - Provide brief usage instructions
   - Suggest variations or follow-up exercises

## Feedback Design

All games should include:
- **Immediate feedback**: Show correct/incorrect immediately
- **Explanations**: Why an answer is correct/incorrect
- **Alternative expressions**: Show other valid options
- **Usage examples**: Demonstrate in realistic context
- **Encouragement**: Positive reinforcement for learning

## Technical Implementation

### Templates Structure
All templates in `assets/templates/` are:
- Self-contained HTML files with embedded CSS and JavaScript
- Responsive design (mobile-friendly)
- Accessible (WCAG 2.1 AA compliant)
- No external dependencies required
- Progress tracking built-in
- Built-in pronunciation features with Web Speech API

### Pronunciation Features
Games include interactive audio pronunciation for learning correct speech:

**Features**:
- 🔊 **Listen to Questions**: Hear the full question read aloud
- 🔊 **Listen to Choices**: Each answer option has a speaker button
- ⚙️ **Accent Selection**: Choose between American, British, or Australian English
- ⏱️ **Speed Control**: Adjust playback speed (0.75x, 1x, 1.25x)
- 🔄 **Toggle On/Off**: Click speaker icon again to stop playback

**Technology**:
- Uses Web Speech API (built into modern browsers)
- No external API calls or audio files needed
- Works offline once page is loaded
- Supports multiple English accents

**Usage in Games**:
- Students can hear proper pronunciation of business expressions
- Useful for non-native speakers
- Helps with listening comprehension
- Reinforces correct pronunciation patterns

### Scripts
`scripts/game_generator.py` provides:
- Template loading and rendering
- Content injection from references
- Difficulty adjustment
- HTML output generation

Use as:
```bash
python scripts/game_generator.py --type quiz --topic email --level intermediate --count 15
```

## Resources

### scripts/
- `game_generator.py`: Main game generation script with template rendering
- `difficulty_analyzer.py`: Analyze and adjust content difficulty

### references/
- `business_expressions.md`: 500+ expressions categorized by scenario and difficulty
- `scenarios.md`: 30+ business scenario templates with learning objectives
- `vocabulary_by_industry.md`: Industry-specific terminology with examples
- `game_design_patterns.md`: Best practices for educational game design

### assets/
- `templates/`: HTML game templates (quiz, drag-drop, scenario, etc.)
- `styles/`: Common CSS styling
- `icons/`: SVG icons for feedback (correct, wrong, hint)

## Examples

### Example 1: Simple Quiz Request
**User**: "Create a business email vocabulary quiz"

**Output**: 10-question multiple choice quiz with common email phrases, beginner level, ~5 minute play time

### Example 2: Industry-Specific Game
**User**: "I need a marketing terminology matching game for my team"

**Output**: Drag-and-drop game with 12 marketing terms (ROI, KPI, CTR, etc.), intermediate level

### Example 3: Scenario Simulation
**User**: "Help me practice disagreeing politely in meetings with a simulation"

**Output**: Interactive dialogue game with 6-8 meeting scenarios, multiple choice responses, feedback on tone and appropriateness

### Example 4: Customized for Role
**User**: "Create a presentation skills game for IT product managers, advanced level"

**Output**: Mixed-format game (ordering, fill-blanks, scenarios) focused on technical product presentations, 20 minutes

## Tips for Effective Games

- **Context is key**: Always provide realistic business scenarios
- **Mix difficulty**: Include easier questions to build confidence
- **Explain why**: Don't just mark wrong, explain the better choice
- **Cultural notes**: Mention US/UK differences when relevant
- **Encourage practice**: Suggest related scenarios for continued learning
- **Track progress**: Show improvement over time when possible

## Extending Content

To add new content:
1. Add expressions to `references/business_expressions.md` with difficulty tags
2. Create new scenarios in `references/scenarios.md` following existing format
3. Update `vocabulary_by_industry.md` for new industries
4. Templates are reusable - no need to modify unless adding new game types
