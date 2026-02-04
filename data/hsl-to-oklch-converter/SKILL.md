---
name: hsl-to-oklch-converter
description: This skill converts HSL color values to OKLCH color values. It can process single or multiple colors, provided either directly by the user or from a specified file.
---

This skill automates the conversion of HSL color definitions to the OKLCH color space, leveraging Playwright to interact with the oklch.com web tool. It handles both individual color strings and batch conversions from files, replacing original HSL values with their OKLCH equivalents.

## When to Use This Skill
Use this skill when:
- You need to convert one or more HSL color values to OKLCH.
- You have a file containing HSL color definitions that need to be updated to OKLCH.
- You want to ensure color consistency and leverage the perceptually uniform properties of OKLCH.

## How to Use This Skill

To use this skill, follow these steps:

1.  **Launch Playwright and Navigate:**
    - Use the Playwright tool to navigate to `https://oklch.com`.

2.  **Select HSL Input Mode:**
    - Click the dropdown to select the HSL input format.

3.  **Perform Color Conversion:**
    - **For direct HSL input:**
        - Use the Playwright tool to type the HSL color value into the input field.
        - Use the Playwright tool to read the OKLCH output from the result field.
        - **Format OKLCH Output:** If the OKLCH value is like `oklch(38.927493438 193.48 124.936836)`, truncate the numerical components to two decimal places (e.g., `oklch(38.92 193.48 124.93)`).
        - Return the OKLCH value to the user.

    - **For file input:**
        - Read the file content using the `Read` tool.
        - Use the `Grep` tool with a regular expression to find all HSL color values in the file.
        - For each found HSL value:
            - Use the Playwright tool to type the HSL color into the input field (as described for direct input above).
            - Use the Playwright tool to read the OKLCH output (as described for direct input above).
            - Use the `Edit` tool to replace the original HSL value with the new OKLCH value in the file.
        - After all conversions, inform the user that the file has been updated.

4.  **Repeat for Multiple Colors:** If there are more colors to convert, repeat step 3 for each color. If processing a file, the iteration will be handled within the file processing logic.
