---
name: spark-create-component
description: Create a new component in the Modules folder from template with proper documentation and placeholders replacement.
---

# Add New Component to Modules Folder

## Overview & Prerequisites

This skill helps you create a new component in the Modules folder using the template-based approach.

❗️ This skill should be used from the root of the monorepo project ❗️

The skill will:
1. Copy the component template
2. Update documentation files with correct metadata
3. Replace all placeholders in filenames and file contents
4. Handle anatomy image setup

## Input Parameters

When executing this skill, gather the required parameters one by one. Check if the user has already provided each piece of information. If not, ask the user for each parameter individually in a conversational message.

**Required Parameters (ask one at a time):**

1. **Component Name** (PascalCase format)
   - Examples: Button, Avatar, Chip, SegmentedControl
   - Ask: "What is the component name? (PascalCase format, e.g., Button, Avatar, Chip)"

2. **Description** (Brief description for documentation)
   - Examples: "A customizable button component", "User profile image component"
   - Ask: "What is the component description? (Brief description for documentation)"

3. **Figma Link** (URL to the Figma design)
   - Example: https://www.figma.com/design/0QchRdipAVuvVoDfTjLrgQ/Spark-Component-Specs?node-id=643-21226
   - Ask: "What is the Figma link? (URL to the Figma design)"

4. **Zeroheight Link** (URL to the Zeroheight specifications)
   - Example: https://zeroheight.com/1186e1705/p/17568d-chip
   - Ask: "What is the Zeroheight link? (URL to the Zeroheight specifications)"

5. **Anatomy Image Path** (Local path to the anatomy image file)
   - Example: /Users/username/Desktop/anatomy.png
   - Ask: "What is the anatomy image path? (Local path to the anatomy image file)"

**Important:**
   - Do NOT use `AskUserQuestion` tool for gathering these parameters
   - Ask for ONE parameter at a time in a conversational message
   - Wait for the user to respond before asking for the next parameter
   - Only proceed to the workflow steps once ALL parameters have been collected

## Workflow

### Step 1: Validate Parameters

Confirm you have all required parameters:
- [ ] Component Name (PascalCase)
- [ ] Description
- [ ] Figma Link
- [ ] Zeroheight Link
- [ ] Anatomy Image Path (verify file exists)

### Step 2: Prepare Component Names

From the component name (e.g., "Button", "Avatar"), generate:
- **COMPONENT_NAME_PASCAL**: PascalCase (e.g., "button")
- **COMPONENT_NAME_LOWER**: Lowercase (e.g., "button")
- **REMOVE SPARK MENTION**: Remove all *Spark* or *SparkComponent* in the name (e.g, "SparkButton" must be "Button" ; "SparkComponentButton" must be "Button" ; )

### Step 3: Copy Template to Modules

Copy the template to create the new component directory:

```bash
cp -r .template/component/ "Modules/Components/${COMPONENT_NAME_PASCAL}/"
```

### Step 4: Handle Anatomy Image

- [ ] Copy anatomy image into the *.github/assets*.
- [ ] Rename image to `sparkcomponent-{component_name_lower}-anatomy.png`

### Step 5: Update documentation.json

Read `Modules/Components/{ComponentName}/documentation.json` and update:
- [ ] `title`: Set to component name + "SparkComponent" in prefix (e.g., "SparkComponentButton")
- [ ] `description`: Set to the user-provided description
- [ ] `figma`: Set to the Figma link
- [ ] `zeroheight`: Set to the Zeroheight link
- [ ] `image`: Set to "spark" + component name in lowercase (e.g., "sparkbutton")

### Step 6: Update Documentation.md

Read `Modules/Components/{ComponentName}/Sources/Core/Documentation.docc/Documentation.md` and:
- [ ] Replace `TODO` in Zeroheight link with actual URL
- [ ] Replace `TODO` in Figma link with actual URL

### Step 7: Replace All Placeholders

**IMPORTANT**: Replace these exact placeholders in all files:
- `__COMPONENT_NAME___` (2 underscores prefix, 3 suffix) → PascalCase name
- `___component_name___` (3 underscores each side) → lowercase name
- `___COMPONENT_NAME___` (3 underscores each side) → PascalCase name

**Files to process:**
- [ ] `README.md`
- [ ] `documentation.json`
- [ ] `Sources/Core/Documentation.docc/Documentation.md`
- [ ] `Sources/Core/Spark__COMPONENT_NAME___.swift`
- [ ] `Sources/Testing/Spark__COMPONENT_NAME___Testing.swift`
- [ ] `Tests/UnitTests/Spark__COMPONENT_NAME___Tests.swift`
- [ ] `Tests/SnapshotTests/Spark__COMPONENT_NAME___SnapshotsTests.swift`
- [ ] `.sourcery.yml`
- [ ] Any other files containing placeholders

**Process:**
1. Update file contents first using Edit tool
2. Rename files with placeholders in names using `mv` command

### Step 8: Verify Component Structure

After all replacements:
- [ ] List files in the new component directory
- [ ] Read `documentation.json` to verify all fields are set
- [ ] Read `README.md` to confirm no placeholders remain
- [ ] Search for any remaining placeholder strings

### Step 9: Update Import.swift

Update the main Spark module to export the new component:

**File:** `spark-ios/Spark/Sources/Core/Import.swift`

- [ ] Read the Import.swift file to see the current list of imports
- [ ] Add `@_exported import SparkComponent{ComponentName}` to the file
- [ ] Insert the new import in alphabetical order among the other component imports
- [ ] Ensure the import follows the format: `@_exported import SparkComponent{ComponentName}` (with comment syntax as shown in the file)

**Example:**
```
@_exported import SparkCommon
@_exported import SparkComponentAvatar
@_exported import SparkComponentBadge
@_exported import SparkComponentButton
...
@_exported import SparkTheming
```

### Step 10: Update Package.swift

Add the new component to the root Package.swift file:

**File:** `spark-ios/Package.swift`

For each new component, you need to add:

1. **Package Dependency** (in `dependencies` array):
   - [ ] Add `.package(path: "Modules/Components/{ComponentName}")` in alphabetical order

2. **Products** (in `products` array, after main Spark product):
   - [ ] Add main component library product:
     ```swift
     .library(
         name: "SparkComponent{ComponentName}",
         targets: ["SparkComponent{ComponentName}"]
     ),
     ```
   - [ ] Add testing library product:
     ```swift
     .library(
         name: "SparkComponent{ComponentName}Testing",
         targets: ["SparkComponent{ComponentName}Testing"]
     ),
     ```

3. **Main Spark Target Dependency** (in main Spark target's `dependencies` array):
   - [ ] Add `.product(name: "SparkComponent{ComponentName}", package: "Component{ComponentName}")`

4. **Component Targets** (in `targets` array, after core targets, before demo targets):
   - [ ] Add main component target:
     ```swift
     .target(
         name: "SparkComponent{ComponentName}",
         dependencies: [
             "SparkCommon",
             "SparkTheming",
             // Add other component dependencies as needed
         ],
         path: "Modules/Components/{ComponentName}/Sources/Core"
     ),
     ```
   - [ ] Add testing target:
     ```swift
     .target(
         name: "SparkComponent{ComponentName}Testing",
         dependencies: [
             "SparkComponent{ComponentName}",
             "SparkCommon",
             "SparkCommonTesting",
             "SparkThemingTesting",
             "SparkTheme"
         ],
         path: "Modules/Components/{ComponentName}/Sources/Testing"
     ),
     ```

5. **Test Targets** (in `targets` array, in test targets section):
   - [ ] Add unit test target:
     ```swift
     .testTarget(
         name: "SparkComponent{ComponentName}UnitTests",
         dependencies: [
             "SparkComponent{ComponentName}",
             "SparkComponent{ComponentName}Testing",
             "SparkCommonTesting",
             "SparkThemingTesting"
         ],
         path: "Modules/Components/{ComponentName}/Tests/UnitTests"
     ),
     ```
   - [ ] Add snapshot test target:
     ```swift
     .testTarget(
         name: "SparkComponent{ComponentName}SnapshotTests",
         dependencies: [
             "SparkComponent{ComponentName}",
             "SparkComponent{ComponentName}Testing",
             "SparkCommonSnapshotTesting",
         ],
         path: "Modules/Components/{ComponentName}/Tests/SnapshotTests"
     ),
     ```

**Important Notes:**
- Maintain alphabetical ordering within each section
- Ensure proper indentation (4 spaces per level)
- Add dependencies based on what the component actually needs (check the template or similar components)

## Placeholder Details

Pay careful attention to underscores:

| Placeholder | Underscores | Replace With | Example |
|------------|-------------|--------------|---------|
| `__COMPONENT_NAME___` | 2 prefix, 3 suffix | PascalCase | SegmentedControl |
| `___component_name___` | 3 each side | lowercase | segmentedcontrol |
| `___COMPONENT_NAME___` | 3 each side | PascalCase | SegmentedControl |

## Example Usage

**User Request:**
```
Add a new component SparkButton with:
- Description: "A customizable button component"
- Figma: "https://figma.com/design/..."
- Zeroheight: "https://zeroheight.com/..."
- Anatomy image: "./assets/button-anatomy.png"
```

**Expected Result:**
- ✅ Directory created: `Modules/Components/Button/`
- ✅ `documentation.json` populated with correct values
- ✅ All placeholders replaced: "Button" or "button"
- ✅ Anatomy image: `sparkcomponent-button-anatomy.png`
- ✅ Documentation links updated
- ✅ Files renamed: `SparkButton.swift`, `SparkButtonTests.swift`, etc.

## Error Handling

If any step fails:
1. Stop the process immediately
2. Report the specific error to the user
3. Provide the step that failed
4. Suggest corrective action if applicable

## Completion Checklist

Before finishing:
- [ ] All placeholders replaced in file contents
- [ ] All files with placeholder names renamed correctly
- [ ] `documentation.json` has all fields filled (no "TODO")
- [ ] `Documentation.md` has all fields filled (no "TODO")
- [ ] Anatomy image renamed and in correct location
- [ ] Component directory structure matches template
- [ ] `Import.swift` updated with new component export
- [ ] `Package.swift` updated with:
  - [ ] Package dependency added
  - [ ] Products added (main + testing)
  - [ ] Main Spark target dependency added
  - [ ] Component targets added (main + testing)
  - [ ] Test targets added (unit + snapshot)
- [ ] No errors reported during execution

## Final Output

When complete, provide the user with:
1. ✅ Success message
2. 📁 Path to new component: `Modules/Components/{ComponentName}/`
3. 📝 Summary of modified files:
   - Component files created
   - `Import.swift` updated
   - `Package.swift` updated
4. ➡️ Next steps:
   - Implement component logic in `Sources/Core/{ComponentName}.swift`
   - Review and customize generated files
   - Run `swift package resolve` to verify package configuration
   - Run any required build/test commands
