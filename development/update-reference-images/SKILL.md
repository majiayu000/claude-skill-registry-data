---
name: update-reference-images
description: Add a reference-image test to Lodestone, or deliberately update reference images after an intended rendering change. Use when a rendering feature needs image coverage, or a reference-image test fails because rendering was meant to change.
---

# Add or Update Reference Images

Reference images are the expected output of rendering tests, compared on lavapipe at the Mesa version pinned in `tools/lavapipe.env` (see `docs/Testing.md#reference-images` and `docs/Decisions/0009-lavapipe.md`). They live in `Tests/ReferenceImages` and are stored with Git LFS.

**Never regenerate a reference image to make a failing test pass.** Update one only when rendering is meant to change, and only after confirming the new image is right. If a test fails and the change wasn't meant to alter rendering, the code is wrong, not the image.

## Prerequisites
lavapipe must be available, or reference-image tests are skipped: on Windows CMake downloads it; on Linux build it with `tools/build-lavapipe.sh` and reconfigure. macOS can't create or check reference images - use Windows or Linux.

## Add a reference-image test
1. Write the test in `Tests/Render` (in `LodestoneRenderTests`), in the `ReferenceImages` test suite so it's left out where lavapipe isn't available:
   ```cpp
   TEST_CASE("Shadows soften with distance" * doctest::test_suite("ReferenceImages"))
   {
   	// Render offscreen into a texture, then:
   	const auto image = ReadTexture(nvrhiDevice, target);
   	REQUIRE_MESSAGE(image.has_value(), fmt::format("{}", image.error()));
   	Testing::CheckReferenceImage("SoftShadows", *image);
   	CHECK(device->GetValidationErrorCount() == 0);
   }
   ```
   Use small, fixed image sizes (256x256 is plenty for most features), and a fixed camera, time and random seed, so the image is deterministic.
2. Keep the default tolerance (`ImageTolerance`) unless the feature needs another, and say why in a comment if it does.
3. Generate the image (below), look at it, and commit it with the test.

## Generate or update images
1. Build, then run the rendering tests with `LS_UPDATE_REFERENCE_IMAGES=1`. Limit the run to the tests whose images should change:
   ```sh
   cmake --build --preset debug
   LS_UPDATE_REFERENCE_IMAGES=1 ctest --preset debug -L render -R "<test name pattern>"
   ```
   In PowerShell: `$env:LS_UPDATE_REFERENCE_IMAGES = '1'`, run `ctest`, then `Remove-Item Env:LS_UPDATE_REFERENCE_IMAGES`.
2. Look at every new or changed image in `Tests/ReferenceImages` (`git status`). Check it shows exactly what the feature should render - this is the only review the image gets.
3. Run the rendering tests again without the variable; they must pass.
4. Commit the images with the code change. The commit message says which images changed and why (for a Mesa update: the old and new versions).

## When a reference-image test fails
The test writes `<name>.actual.png` and `<name>.difference.png` (mismatched pixels in red) to `build/<preset>/RenderOutput`; CI uploads the same files as an artifact (`gh run download <run id>`). Look at both before deciding whether the code or the image is wrong.
