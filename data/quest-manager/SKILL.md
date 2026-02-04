---
name: quest-manager
description: Create, manage, and track quests for Ezra. Use when adding quests, checking progress, updating categories, or managing prerequisites.
allowed-tools: Read, Edit, Write, Grep, Glob
---

# Quest Manager Skill

## 20 Categories

### Academic Core (6)
| Code | Category |
|------|----------|
| L | Literacy - Reading, Writing, Phonics |
| M | Mathematics - Numbers, Logic |
| S | Science - Nature, Experiments |
| T | Technology - Digital Skills, Coding |
| H | History & Culture - Past, Traditions |
| LC | Language & Communication - Speaking, Listening |

### Physical Development (4)
| Code | Category |
|------|----------|
| PF | Physical Fitness - Exercise, Sports |
| YM | Yoga & Mindful Movement - Stretching, Breathing |
| GM | Gross Motor Skills - Running, Jumping |
| FM | Fine Motor Skills - Hand-Eye, Precision |

### Emotional & Social (4)
| Code | Category |
|------|----------|
| ER | Emotional Regulation - Feelings, Tantrums, Coping |
| SS | Social Skills - Friends, Sharing, Empathy |
| SC | Self-Care & Hygiene - Personal Care |
| MM | Meditation & Mindfulness - Focus, Stillness |

### Life Skills (4)
| Code | Category |
|------|----------|
| HS | Household Skills - Chores, Cleaning |
| SA | Safety & Awareness - Personal Safety |
| MR | Money & Responsibility - Financial Basics |
| TM | Time Management - Schedules, Planning |

### Creative (2)
| Code | Category |
|------|----------|
| VA | Visual Arts - Drawing, Painting, Crafts |
| MP | Music & Performing Arts - Singing, Dance |

## Quest ID Format
XX### where XX is category code, ### is 001-999

Example: ER015 = Emotional Regulation quest #15

## Difficulty Levels & Prerequisites

| Level | ID Range | Unlock Requirement |
|-------|----------|-------------------|
| 1 | X001-X099 | None (starting quests) |
| 2 | X100-X199 | 80% of Level 1 |
| 3 | X200-X299 | 80% of Levels 1-2 |
| 4 | X300-X399 | 80% of Levels 1-3 |
| 5 | X400-X499 | 80% of Levels 1-4 |
| 6 | X500+ | All previous + special |

## XP & Gold by Difficulty

| Level | XP Range | Gold Range |
|-------|----------|------------|
| 1 | 10-20 | 5-10 |
| 2 | 20-40 | 10-20 |
| 3 | 40-60 | 20-30 |
| 4 | 60-80 | 30-40 |
| 5 | 80-100 | 40-50 |
| 6 | 100-150 | 50-75 |
| Boss | 200+ | 100+ |

## Key Files
- ~/repos/phoenix-forge-ecosystem/1_EzrasQuest/QUEST_CATEGORY_MASTER.md
- ~/repos/phoenix-forge-ecosystem/1_EzrasQuest/data/

## When Adding Quests
1. Validate category code (must be one of 20)
2. Assign correct difficulty range based on complexity
3. Set XP and Gold within level guidelines
4. Define prerequisites if level 2+
5. Write clear, age-appropriate description (Ezra is 6)
6. Consider cross-category prerequisites for advanced quests
