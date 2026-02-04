---
name: yoga-class-planner
description: Creates structured 60-minute beginner-friendly yoga class sequences with detailed pose instructions and timing
---

# Yoga Class Planner

A comprehensive skill for yoga teachers to create well-structured, beginner-friendly 60-minute yoga class sequences. This skill generates complete class plans with detailed pose instructions, timing, transitions, and teaching cues - without requiring themed classes or music suggestions.

## Purpose

This skill helps yoga teachers:
- Design balanced 60-minute beginner-friendly sequences
- Generate detailed pose-by-pose instructions with timing
- Create smooth transitions between poses
- Include appropriate warm-ups, peak poses, and cool-downs
- Provide teaching cues and modifications for beginners
- Structure classes with proper pacing and energy flow

## What This Skill Does

When invoked, this skill will:

1. **Generate Complete Class Structure**
   - Opening/centering (5 minutes)
   - Warm-up sequence (10-12 minutes)
   - Standing poses (15-18 minutes)
   - Peak pose section (10-12 minutes)
   - Cool-down/floor poses (12-15 minutes)
   - Savasana and closing (5-8 minutes)

2. **Provide Detailed Pose Instructions**
   - Sanskrit and English names
   - Step-by-step entry instructions
   - Key alignment cues
   - Beginner modifications
   - Breath integration
   - Hold duration

3. **Include Teaching Elements**
   - Transition cues between poses
   - Safety reminders
   - Common beginner mistakes to watch for
   - Props suggestions (blocks, straps, blankets)
   - Energy/intensity level indicators

4. **Ensure Beginner-Appropriate Content**
   - Accessible poses for all fitness levels
   - Clear, simple instructions
   - Adequate rest periods
   - Focus on foundational poses
   - Emphasis on safety and body awareness

## Instructions for Claude

When a user asks you to create a yoga class plan, follow this systematic approach:

### Step 1: Clarify Requirements (if needed)

If the user hasn't specified, ask about:
- **Focus area**: Full body, lower body, upper body, flexibility, strength, relaxation
- **Energy level**: Gentle, moderate, energizing
- **Special considerations**: Injuries, physical limitations, props available

### Step 2: Structure the 60-Minute Class

Create a balanced sequence following this timing framework:

**Opening (5 minutes)**
- Centering in easy seated or child's pose
- Breathing exercises (pranayama)
- Intention setting

**Warm-Up (10-12 minutes)**
- Gentle neck/shoulder rolls
- Cat-cow stretches
- Gentle twists
- Sun salutation modifications or foundational flow

**Standing Poses (15-18 minutes)**
- Mountain pose (Tadasana)
- Standing forward fold (Uttanasana)
- Warrior poses (Warrior I, II)
- Triangle pose (Trikonasana)
- Tree pose (Vrksasana) or other balance

**Peak Pose Section (10-12 minutes)**
- Build toward 1-2 main poses
- Include preparatory poses
- Offer modifications and variations
- Examples: Low lunge, pyramid pose, half splits, seated forward fold

**Cool-Down (12-15 minutes)**
- Seated poses (seated twists, forward folds)
- Supine poses (bridge, reclined twists)
- Hip openers (pigeon, happy baby)
- Gentle backbend (sphinx or supported fish)

**Closing (5-8 minutes)**
- Savasana (5-7 minutes)
- Gentle return to seated
- Brief closing meditation or gratitude
- Namaste

### Step 3: Format Each Pose Entry

For every pose in the sequence, provide:

```
**[English Name] (Sanskrit Name)** - [Duration]

Setup:
- [Step-by-step entry instructions]

Alignment Cues:
- [Key alignment points]
- [Breath guidance]

Beginner Modifications:
- [Easier variations]
- [Props to use]

Teaching Notes:
- [Common mistakes]
- [Safety considerations]
- [Transition to next pose]
```

### Step 4: Include Transition Language

Between poses, provide smooth transition cues:
- "From [current pose], gently..."
- "On your next exhale, release and..."
- "Take a breath here, then when you're ready..."

### Step 5: Add Teaching Reminders

Throughout the sequence, include:
- **Breath reminders**: "Continue breathing deeply"
- **Rest options**: "Take child's pose anytime you need"
- **Pacing notes**: "Hold for 5 breaths" or "Stay for 30 seconds"
- **Safety cues**: "Listen to your body", "No pain"

### Step 6: Provide Class Summary

At the end, include:
- **Total duration**: Verify it sums to ~60 minutes
- **Intensity level**: Gentle, moderate, etc.
- **Props needed**: Blocks, straps, blankets, bolster
- **Key focus areas**: What body areas were emphasized
- **Suggested variations**: How to adjust for different levels

## Output Format

Structure your output as a complete, ready-to-teach class plan:

```markdown
# 60-Minute Beginner Yoga Class Plan
**Focus**: [Focus area]
**Energy Level**: [Gentle/Moderate/Energizing]
**Props Needed**: [List]

---

## Opening & Centering (5 minutes)

[Detailed instructions]

---

## Warm-Up Sequence (10-12 minutes)

[Pose-by-pose breakdown]

---

## Standing Poses (15-18 minutes)

[Pose-by-pose breakdown]

---

## Peak Pose Section (10-12 minutes)

[Pose-by-pose breakdown]

---

## Cool-Down & Floor Poses (12-15 minutes)

[Pose-by-pose breakdown]

---

## Savasana & Closing (5-8 minutes)

[Detailed instructions]

---

## Class Summary

**Total Duration**: 60 minutes
**Intensity**: [Level]
**Props**: [List]
**Focus Areas**: [Body areas]
**Teaching Notes**: [Any special considerations]
```

## Example Prompts

Users can invoke this skill with prompts like:

- "Create a beginner-friendly 60-minute yoga class focused on hip flexibility"
- "I need a gentle yoga class plan for beginners with lower back issues"
- "Design a 60-minute class emphasizing strength and balance for new students"
- "Generate a relaxing evening yoga sequence for beginners, 60 minutes"

## Key Principles

**Beginner-Friendly Focus**
- Use foundational poses
- Provide clear, simple instructions
- Offer modifications for all poses
- Emphasize safety and body awareness
- Allow adequate rest and recovery time

**No Themes or Music**
- Focus purely on physical practice
- Keep instructions practical and clear
- No narrative themes or stories
- No music playlist suggestions
- Straightforward, functional approach

**60-Minute Structure**
- Always total approximately 60 minutes
- Include all essential class components
- Provide specific timing for each section
- Allow flexibility for teacher pacing

**Comprehensive Teaching Support**
- Include everything a teacher needs to lead the class
- Provide alignment cues and modifications
- Include transition language
- Note common mistakes and safety considerations

## Limitations

This skill:
- Does NOT create themed classes (moon cycles, chakras, etc.)
- Does NOT suggest music or playlists
- Does NOT include advanced or intermediate poses
- Does NOT provide yoga philosophy or spiritual content
- FOCUSES purely on practical, beginner-appropriate physical sequences

## Tips for Best Results

1. **Be specific about focus**: Tell Claude what body area or quality (flexibility, strength, relaxation) to emphasize
2. **Mention constraints**: Let Claude know about injuries, physical limitations, or available props
3. **Request variations**: Ask for "gentle" or "moderate" intensity versions
4. **Iterate**: Ask Claude to adjust timing, swap poses, or modify difficulty as needed

## Customization

Teachers can customize generated class plans by asking Claude to:
- "Make this sequence more gentle"
- "Replace [pose] with something easier"
- "Add more hip openers"
- "Reduce standing poses, add more floor work"
- "Simplify the peak pose section"

---

**Version**: 1.0
**Created**: 2025-11-14
**Skill Type**: Prompt-based (no Python code required)
**Target Users**: Yoga teachers, yoga instructors, movement educators
