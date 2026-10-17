---
name: add-dependency
description: Add a third-party library to Lodestone - pinned to an exact version, verified by hash, license-checked and documented. Use whenever new code needs a library that isn't fetched yet.
---

# Add a Dependency

1. **Check the license** - only permissive licenses are allowed: MIT, BSD, zlib, Apache 2.0, public domain or CC0. Anything else needs the user's decision first (see `AGENTS.md`). Check `docs/TechStack.md#libraries` - the library may already be planned, with a chosen version policy.
2. **Pick an exact version** - a release tag, or a specific commit when releases are stale (as for sol2). Never a branch.
3. **Hash the archive** - download the release archive (GitHub: `https://github.com/<owner>/<repo>/archive/refs/tags/<tag>.tar.gz`, or `.../archive/<commit>.tar.gz`) into an empty scratch directory, and compute its SHA256 (`sha256sum`, or `Get-FileHash` on Windows). If the project publishes checksums, compare against them.
4. **Declare it** in `cmake/Dependencies.cmake`:
   ```cmake
   # <name> - <what it's for> (<license>)
   ls_declare_dependency(<name>
   	URL <archive URL>
   	SHA256 <hash>
   )
   set(<OPTION> <value> CACHE BOOL "" FORCE)   # turn off the dependency's tests, examples and install rules
   ```
   and add it to `FetchContent_MakeAvailable()`. If it has no CMake build, define its target after `FetchContent_MakeAvailable()`, as Lua's is.
5. **Respect the layering** - link it only to the targets that need it. `LodestoneCore` must never link GLFW, nvrhi, miniaudio or anything that needs a window, GPU or audio device (`docs/Architecture.md#targets-and-layering`).
6. **Document it** - add the library, version, license, purpose and whether it ships in exported games to `THIRD_PARTY_LICENSES.md`, with the full license text from the archive. Add it to `docs/TechStack.md#libraries` if it isn't listed.
7. **Test it** - build every configuration on your platform and run the tests (`build-and-test` skill). CI checks the other platforms. If the library throws exceptions, catch them where Lodestone calls it and return `std::expected` errors (`docs/CodeStyle.md#error-handling`).
