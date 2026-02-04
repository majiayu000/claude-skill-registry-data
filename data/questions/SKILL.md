---
name: questions
description: Generate 20 fun League of Legends trivia questions based on player data. Use when creating entertaining French questions about LoL performance, champions, and player stats.
---

# /questions - LoL Trivia Question Generator

Generate 20 fun trivia questions about the group based on their League of Legends data.

## Langue

**Toutes les questions et réponses doivent être rédigées en français.**

## Tone

**You are a true entertainer.** This is a fun game played with the boys. Hit the sweet spot between pop culture humour, fine language, perfectly well-mannered and subtle allusions. Make us smile and shout!

## Instructions

### Step 1: Refresh Indicators
```bash
python run-before-question-skill.py
```

### Step 2: Invent 3 Dynamic Indicators

Pick a random inspiration (movie, meme, theme...) and create 3 new indicators that will surface interesting data. Be creative!

Example:
```bash
python run-before-question-skill.py --add-indicator '{
  "name": "tilted_tower",
  "type": "trend",
  "description": "Death increase in recent games",
  "params": {"stat": "deaths", "recent_games": 15}
}'
```

Run one command per indicator. These persist to cache for future sessions.

### Step 3: Read the Indicators Cache

Read `data/indicators_cache.json` - this contains all the statistical summaries you need. **NEVER read the raw player JSON files.**

### Step 4: Generate 20 Unique Questions

Create 20 questions that are:
- **Data-driven**: Based on real stats from the indicators
- **Varied in format**: Mix riddles, superlatives, comparisons, "would you rather", roasts, awards, predictions
- **Entertaining**: Playful, witty, with pop culture references when fitting
- **Answerable**: Each question has a definitive answer from the data

**Question categories to draw from:**
- Champion mastery & one-tricks
- Extreme records (highest kills, most deaths, longest game)
- Win rates & performance trends
- Role-specific stats (jungle mains, support aggression)
- Hidden patterns (hidden mains, cheese picks)
- Comparisons between players
- Percentile achievements (top 1% damage games)
- Your dynamic indicators!

### Step 5: Write Questions File

Create `questions/` folder if needed, then write all 20 questions to:
```
questions/session_YYYYMMDD_HHMMSS.txt
```

Format:
```
SESSION: [Your theme/inspiration for this session]
Generated: YYYY-MM-DD HH:MM:SS

---

Q1. [Question text]

Q2. [Question text]

...

Q20. [Question text]
```

### Step 6: Write Individual Answer Files

Create `answers/` folder if needed, then write each answer to a separate file:
- `answers/answer1.txt`
- `answers/answer2.txt`
- ... through `answers/answer20.txt`

Each answer file format:
```
Question: [The question]

Answer: [The answer]

Stats: [Supporting data that proves the answer]
```

### Step 7: Present to User

Tell the user:
- Where the questions file is located
- That answers are in individual files to avoid spoilers
- Invite them to start the game!

## Important Rules

1. **NEVER read raw data files** - Only use `data/indicators_cache.json`
2. **Keep answers SECRET** in separate files - no spoilers in the questions file!
3. **Make each session unique** - Different theme, different question styles, different angles
4. **Be specific** - Use real numbers, real player names, real champion names
5. **Have fun** - This is entertainment, not a statistics exam!

## Example Question Styles

- "Who among you holds the shameful record of 18 deaths in a single game? We call this the 'Grey Screen Appreciation Award'."
- "One of you has been secretly practicing Teemo with over 80k mastery points but hasn't touched the little devil in months. Who's the closet yordle main?"
- "If we ranked everyone by average damage dealt, who would be crowned the DPS Overlord?"
- "Would you rather: Have CoCoWan's highest kill game (32 kills) or MoRellOu's longest game (58 minutes of suffering)?"
- "Someone here has a 72% win rate on their best champion but only 52% overall. Who's been carried by their pocket pick?"
