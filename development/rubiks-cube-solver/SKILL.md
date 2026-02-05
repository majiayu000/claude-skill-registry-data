---
name: rubiks-cube-solver
description: Fast procedural Rubik's cube solver that requests photos, converts them to cube state string, and uses Python scripts to generate step-by-step solutions.
---

## Prerequisites

Before using this skill, ensure the required libraries are installed:
```bash
pip3 install kociemba
```

If the solver returns a dependency error during execution, install missing packages at that time.

## Procedure

Follow these steps in order. Each step contains all required information.

### Step 1: Request Photos
Request exactly 6 photos from the user, one of each cube face IN THIS SPECIFIC ORDER with correct orientation.

**Photos must be in JPEG or PNG format.**

**Display the text visualization for each requested face photo.**

**Instructions for User:**
- Take clear, well-lit photos following the exact order and orientation shown below
- **ORIENTATION IS CRITICAL**: All middle-layer faces (Orange, Green, Red, Blue) MUST have white on top
- For white face: Hold so blue is on top
- For yellow face: Hold so green is on top
- The center sticker indicates which face you're photographing
- Hold the cube steady and fill the frame with each face
- Make sure all 9 stickers are clearly visible in each photo
- Upload photos in PNG or JPEG format.

**Photo 1: White face (center) - Hold cube with BLUE on top**
```
      (Blue on top)
      ? ? ?
      ? W ?
      ? ? ?
```

**Photo 2: Orange face (center) - Hold cube with WHITE on top**
```
      (White on top)
      ? ? ?
      ? O ?
      ? ? ?
```

**Photo 3: Green face (center) - Hold cube with WHITE on top**
```
      (White on top)
      ? ? ?
      ? G ?
      ? ? ?
```

**Photo 4: Red face (center) - Hold cube with WHITE on top**
```
      (White on top)
      ? ? ?
      ? R ?
      ? ? ?
```

**Photo 5: Blue face (center) - Hold cube with WHITE on top**
```
      (White on top)
      ? ? ?
      ? B ?
      ? ? ?
```

**Photo 6: Yellow face (center) - Hold cube with GREEN on top**
```
      (Green on top)
      ? ? ?
      ? Y ?
      ? ? ?
```

### Step 2: Analyze and Review Colors with User

For each photo, analyze the colors and run the validation script. Don't show validation output to the user until all 6 faces are processed. Once all 6 faces are validated, show the user a single visualization for confirmation.

**Reading Order for Each Face** (left-to-right, top-to-bottom):
```
1 2 3
4 5 6
7 8 9
```

**Color codes to use:**
- **W** = White
- **R** = Red
- **G** = Green
- **Y** = Yellow
- **O** = Orange
- **B** = Blue

**For each photo:**

1. **Analyze the photo**: Read the 9 stickers in order (left-to-right, top-to-bottom) and create a 9-character string
   - **Example**: If you see White-White-Green / White-White-Blue / Red-Red-Red, the string is: **"WWGWWBRRR"**
   - **Example**: If you see all Green stickers, the string is: **"GGGGGGGGG"**

2. **Validate silently using the script** to cache the face:
   ```bash
   python3 scripts/solve_cube.py validate <9-char-color-string>
   ```
   - **Example**: `python3 scripts/solve_cube.py validate WWGWWBRRR`
   - The script will verify the string, detect which face it is from the center color, and cache it
   - Don't show validation output to user - continue processing all faces

3. If validation fails (format error), re-check your color reading and try again

4. Continue until all 6 faces are validated

**After all 6 faces are validated:**

1. **Render the complete cube state** for user review:
   ```bash
   python3 scripts/solve_cube.py render
   ```
   - This generates a markdown visualization showing all 6 faces with emoji
   - Shows both the colored cube state and position reference grid
   - Each sticker shows its position label (U1-U9, L1-L9, F1-F9, etc.)

2. **Show the visualization and ask user for confirmation**:
   Display the markdown output from the render command, then ask:

   "Please review the cube state above. Does this match your physical cube?

   - If correct, reply 'correct' or 'yes' and I'll solve it
   - If any sticker is wrong, tell me using this format:
     - 'U3 should be Red' (meaning Up face, position 3, should be Red)
     - 'F5 should be Blue' (meaning Front face, position 5, should be Blue)
     - 'L7 should be Orange'"

3. **After asking, STOP and wait for the user's next message**:
   - Do NOT run any more commands until the user responds
   - If user confirms it's correct, proceed to Step 3 (concatenate and solve)
   - If user provides corrections, update the affected face(s) and re-render

4. **If user reports corrections**:
   - Determine which face needs correction based on their reference (U/L/F/R/B/D or color name)
   - Reconstruct the complete corrected 9-character string for that face (use W, R, G, Y, O, B)
   - Re-validate that face: `python3 scripts/solve_cube.py validate <corrected-9-char-color-string>`
   - Render again to show the update: `python3 scripts/solve_cube.py render`
   - Ask user to confirm the correction

**Note**: While you should request photos in the order specified in Step 1, the validation script automatically detects each face from its center color, so you can process them in any order during validation.

### Step 3: Concatenate and Solve

Once all 6 faces are validated and cached:

1. **Concatenate faces**: `python3 scripts/solve_cube.py concat`
   - This combines all cached faces in the Kociemba solver order: U, R, F, D, L, B
   - Returns the 54-character cube string (already translated to solver format)
   - If any faces are missing, it will report which ones

2. **Solve the cube**: `python3 scripts/solve_cube.py solve <54-character-string>`
   - Use the string from the concat command
   - The script validates and solves the cube
   - Returns step-by-step text instructions

**If solve fails:**
- The cube state is likely impossible (wrong orientations or analysis errors)
- Proceed to Step 4 to review and correct the detected colors with the user

### Step 4: Review and Correct Colors (Only on Solve Failure)

If the solve command in Step 3 fails, review the cube state with the user to identify and correct errors:

1. **Render the current cube state** for visual review:
   ```bash
   python3 scripts/solve_cube.py render
   ```
   - This generates a markdown visualization with emoji showing the complete cube state
   - Shows both colored state and position reference grid

2. **Ask the user**: "Here's the current cube state. Please review and tell me any corrections needed:
   
   [Show the markdown output]
   
   Reference corrections by face and position number (e.g., 'U3 should be Red', 'F5 should be Blue')."

3. **If user reports corrections**:
   - Determine the complete corrected 9-character string for that face (use W, R, G, Y, O, B)
   - Re-validate that face: `python3 scripts/solve_cube.py validate <corrected-9-char-color-string>`
   - The script will detect the face from center color and update it automatically
   - Render again to show the update: `python3 scripts/solve_cube.py render`

4. **After making all corrections**:
   - Concatenate again: `python3 scripts/solve_cube.py concat`
   - Attempt to solve: `python3 scripts/solve_cube.py solve <54-character-string>`

5. **If still failing after corrections**:
   - Use `python3 scripts/solve_cube.py clear` to clear the cache
   - Go back to Step 1 and request photos again
   - Don't retry more than 3 times total

### Step 5: Deliver Solution

Once the solve succeeds in Step 3, present the solution to the user.

1. **The solve command outputs**:
   - Raw move notation (e.g., "R U R' F2 D' L2")
   - Translated step-by-step instructions in plain language

2. **Simply pass the solution output to the user**. Example format:
   ```
   SOLUTION:
   Raw moves: R U R' F2 D' L2
   
   SETUP: Hold cube with WHITE face on top and GREEN face toward you
   
   Step 1: Turn RIGHT face clockwise 90° [R]
   Step 2: Turn TOP face clockwise 90° [U]
   Step 3: Turn RIGHT face counterclockwise 90° [R']
   Step 4: Turn FRONT face 180° (either direction works) [F2]
   Step 5: Turn BOTTOM face counterclockwise 90° [D']
   Step 6: Turn LEFT face 180° (either direction works) [L2]
   ```

3. **User can**:
   - Follow the numbered steps in order
   - Refer to the setup orientation for consistency
   - Execute each move on their physical cube

4. **Clean up and return control**:
   - Return control to the user - the solve session is complete

**If you need to start over:**
- Clear the cache: `python3 scripts/solve_cube.py clear`
- This removes all cached face data so you can begin fresh

## Troubleshooting

### Common Issues and Solutions

**Face validation errors**
- "RE-VALIDATED": You're updating a face that was already cached (this is normal for corrections)
- "String must be exactly 9 characters": Face string is wrong length
  - Check that you're reading all 9 stickers (3x3 grid)
- "Invalid color": Non-standard color code detected
  - Only use: W (White), R (Red), G (Green), Y (Yellow), O (Orange), B (Blue)

**Concatenation errors**
- "Missing faces": Not all 6 faces have been validated
  - Check which faces are missing and validate them
  - Use `clear` command if you need to start over

**"Unable to solve cube" errors**
- Photos likely have orientation issues; request new photos with emphasis on consistent orientation
- Ensure all middle-layer faces (Orange, Green, Red, Blue) have white on top
- Ensure the white face has green facing you, and yellow face has green on top
- Clear the cache and restart from Step 1
- Verify the user is holding the cube exactly as instructed

**"Invalid cube configuration" errors**
- The cube string doesn't have all 6 faces or has duplicates
- This means photos may be duplicates or some faces weren't captured
- Check concat output to see which faces are present

**Repeated failures after 2-3 attempts**
- Ask user to verify their physical cube is actually solvable (not reassembled incorrectly)
- Some cubes can be physically taken apart and reassembled in impossible configurations
- Suggest the user try solving one face first to confirm the cube is in a valid state

### Command Reference

```bash
# Validate a face (script auto-detects which face from center color)
python3 scripts/solve_cube.py validate <9-char-color-string>

# Concatenate all cached faces into 54-char string
python3 scripts/solve_cube.py concat

# Render markdown visualization (from cached faces)
python3 scripts/solve_cube.py render

# Render markdown visualization (from specific cube string)
python3 scripts/solve_cube.py render <54-char-string>

# Solve from 54-character string
python3 scripts/solve_cube.py solve <54-char-string>

# Translate solution moves to friendly instructions
python3 scripts/solve_cube.py translate <solution-string>

# Clear all cached faces
python3 scripts/solve_cube.py clear
```