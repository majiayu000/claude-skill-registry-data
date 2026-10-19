---
name: unity-tests-without-asmdef
description: Add NUnit EditMode tests to a Unity project whose first-party code has no assembly definitions (everything compiles into Assembly-CSharp) - where the tests live, what compiles, how to test pure logic, static guards and MonoBehaviours outside Play Mode, how to run them headless with a JUnit report, and the PlayMode fallback. Use when a legacy Unity project needs automated tests without an asmdef refactor.
license: Unlicense
metadata:
  tags: "Unity, Testing, NUnit, Unity Test Framework"
  category: "testing-validation"
---

# EditMode tests without assembly definitions

## Where tests go

- `Assets/<Project>/Tests/Editor/*.cs` compiles into **Assembly-CSharp-Editor**, which references
  `nunit.framework`, `UnityEditor.TestRunner` and `UnityEngine.TestRunner` out of the box. It can see every
  type in Assembly-CSharp and in auto-referenced packages.
- PlayMode tests in the predefined assemblies need `playModeTestRunnerEnabled: 1` in
  `ProjectSettings/ProjectSettings.asset` ("Enable playmode tests for all assemblies"); use them only when
  the code truly needs the player loop.
- Namespace them (`<Project>.Tests`) and keep the folder name `Tests` so the migration to real test assemblies
  later is a move plus an asmdef.

## What to test first

1. Pure logic: state machines, mappers, parsers, calculators. Construct, feed inputs, assert outputs; observe
   transitions through events rather than private fields.
2. Static guards and domain-reload resets: read the private static through reflection
   (`typeof(T).GetField("isLoading", BindingFlags.Static | BindingFlags.NonPublic)`), invoke the
   `[RuntimeInitializeOnLoadMethod]` reset through reflection, assert the public property.
3. In-memory fakes of service interfaces (an `ICloudManager` that stores objects): defaults, storage semantics,
   listener behaviour, no-op writes.
4. MonoBehaviours outside Play Mode: `new GameObject().AddComponent<T>()` works in EditMode tests, but Awake,
   Start and the serializer do not run, so serialized fields (including `UnityEvent` fields) can be null;
   initialise them in the test and `Object.DestroyImmediate` the host in `[TearDown]`. Coroutines and
   `SceneManager.LoadSceneAsync` are Play Mode only.

## Pitfalls seen in practice

- State machines often fire the initial state's "enter" event on the first update; prime the machine with one
  neutral sample before attaching recorders.
- In-place mutation of objects returned by a getter defeats "did it change" comparisons against the stored
  instance; compare against a remembered value.
- Time-dependent logic that uses `Stopwatch`: sleep past the window (`Thread.Sleep(150)` for an 80 ms trigger);
  keep the total suite under a few seconds.
- `Debug.Log` in production code is fine in tests; `Debug.LogError` fails the test unless `LogAssert.Expect`.

## Run

```powershell
unity test <project> --mode EditMode --report-format junit --output TestResults/editmode.junit.xml --timeout 900 --no-banner
```

The project must be closed (the CLI spawns its own editor). Exit code 0 means every test passed; the JUnit
file lists each `testcase` with failures. From a live editor, the Meta XR bridge Test Runner tools or the Test
Runner window run the same tests. Ignore `TestResults/` in git and attach the report to the review as evidence.
