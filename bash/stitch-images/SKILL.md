---
name: stitch-images
description: Stitch two images together horizontally using OpenCV. Scales images to matching height before joining.
argument-hint: <left-image> <right-image> [output-path]
---

# Stitch Images Horizontally

The user wants to stitch two images side by side. Their arguments: $ARGUMENTS

## Important: Special Characters in Paths

macOS screenshot filenames contain a **narrow no-break space** (U+202F) before AM/PM, e.g. `Screenshot 2026-02-10 at 11.10.43\u202fAM.png`. This looks like a regular space but isn't, so shell quoting alone won't work.

**Always use `glob.glob()` in the Python script to resolve paths** rather than passing raw filenames through the shell. If the user provides partial filenames or paths with potential special characters, use glob patterns to match them (e.g. replace the space before AM/PM with `?` or `*`).

When passing paths as command-line arguments to the script, use `sys.argv` and avoid shell interpolation of the filenames.

## Steps

1. Parse the arguments to extract:
   - **left image path** (first argument, required)
   - **right image path** (second argument, required)
   - **output path** (third argument, optional — default to `stitched.png` in the current working directory)

2. Write a short Python script to a temporary file that does the following:
   - Accepts image paths via `sys.argv`
   - For each input path, if `os.path.exists()` fails, try `glob.glob()` on the path with the space before AM/PM replaced by a `?` wildcard — this handles the U+202F narrow no-break space in macOS screenshot names
   - Reads both images with `cv2.imread()`
   - Exits with a clear error if either image fails to load
   - If the images have different heights, scales the shorter one up (or taller one down) so both match the **larger** height, preserving aspect ratio
   - Joins them horizontally with `numpy.hstack()`
   - Saves the result with `cv2.imwrite()` to the output path
   - Prints the output path and final dimensions

3. Run the script with `python3`, passing paths as arguments. **Quote all paths with double quotes** to handle regular spaces.

4. Delete the temporary script file after it finishes.

5. If the run fails because `opencv-python` or `numpy` is not installed, offer to install them with `pip3 install opencv-python numpy` and retry.
