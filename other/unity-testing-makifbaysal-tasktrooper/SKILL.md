---
name: unity-testing
category: testing
description: Use when writing or running Unity tests - Unity Test Framework EditMode vs PlayMode, test assembly definitions, testing plain C# and ScriptableObjects, PlayMode scene/physics/input tests, batchmode CLI with result XML, coverage, and the dotnet test fallback when no editor is installed.
tech_stack: Unity
source: informed by the Unity Test Framework, Input System testing and Code Coverage package docs; own wording
---
# Unity Testing

## Overview

The Unity Test Framework (NUnit 3 underneath) runs tests in two modes. EditMode tests run in the editor without entering Play mode — fast, ideal for plain C# rules, ScriptableObjects and editor tooling. PlayMode tests run the player loop — needed for scenes, physics, coroutines and input, and slower. Most tests should be EditMode tests against plain classes (testable-game-logic).

**Core principle:** EditMode first; PlayMode only for behaviour that needs the player loop. Read the result XML, not the log tail.

## Which mode

| Question | Mode | Typical setup |
|---|---|---|
| Does the damage/cooldown/inventory rule compute correctly? | EditMode | `new` the plain class |
| Is every shipped definition valid? | EditMode | `AssetDatabase.FindAssets` |
| Does a ScriptableObject-driven system behave? | EditMode | `ScriptableObject.CreateInstance<T>()` |
| Does the character land on the floor / trigger fire? | PlayMode | load a test scene, `WaitForFixedUpdate` |
| Does pressing Jump jump? | PlayMode | `InputTestFixture` |
| Does the coroutine/Awaitable sequence finish? | PlayMode | `[UnityTest]` yielding frames |

## Test assemblies

```json
{
  "name": "Tests.EditMode",
  "references": ["Game.Core", "Game.Runtime", "UnityEngine.TestRunner", "UnityEditor.TestRunner"],
  "includePlatforms": ["Editor"],
  "overrideReferences": true,
  "precompiledReferences": ["nunit.framework.dll"],
  "defineConstraints": ["UNITY_INCLUDE_TESTS"],
  "autoReferenced": false
}
```

PlayMode assemblies leave `includePlatforms` empty (any platform) and drop `UnityEditor.TestRunner` unless they need editor APIs. Tests live where the repository keeps them (often `Assets/Tests/EditMode` and `Assets/Tests/PlayMode`); follow its naming — `Method_Scenario_Expected` when there is none.

## EditMode examples

```csharp
public class InventoryTests {
    [Test] public void Add_BeyondStackLimit_OverflowsToNewSlot() {
        var potion = ScriptableObject.CreateInstance<ItemDefinition>();
        potion.Configure(id: "potion", maxStack: 5);
        var inv = new Inventory(slots: 4);

        inv.Add(potion, 7);

        Assert.That(inv.Slots[0].Count, Is.EqualTo(5));
        Assert.That(inv.Slots[1].Count, Is.EqualTo(2));
        Object.DestroyImmediate(potion);
    }

    [TestCase(0f, 100)] [TestCase(0.5f, 50)] [TestCase(1f, 0)]
    public void Damage_ByArmorFraction_ReducesLinearly(float armor, int expected) =>
        Assert.That(DamageMath.Apply(100, armor), Is.EqualTo(expected));
}
```

Destroy every object a test creates (`DestroyImmediate` in EditMode, `Destroy` in PlayMode, or in `[TearDown]`) — leaked objects leak into the next test.

## PlayMode examples

```csharp
public class PlayerPhysicsTests {
    [UnitySetUp] public IEnumerator Load() { yield return SceneManager.LoadSceneAsync("Test_FlatFloor"); }

    [UnityTest] public IEnumerator Player_DroppedAboveFloor_BecomesGrounded() {
        var player = Object.Instantiate(TestPrefabs.Player, new Vector3(0, 3, 0), Quaternion.identity);
        for (int i = 0; i < 100; i++) yield return new WaitForFixedUpdate();
        Assert.That(player.GetComponent<GroundCheck>().IsGrounded, Is.True);
    }
}

public class JumpInputTests : InputTestFixture {
    [UnityTest] public IEnumerator PressingSpace_MakesPlayerJump() {
        var keyboard = InputSystem.AddDevice<Keyboard>();
        var player = Object.Instantiate(TestPrefabs.Player);
        yield return null;
        Press(keyboard.spaceKey);
        yield return new WaitForFixedUpdate();
        Assert.That(player.GetComponent<Rigidbody>().linearVelocity.y, Is.GreaterThan(0f));
    }
}
```

- Use dedicated small test scenes (`Test_*.unity`) added to the test build, not production levels.
- Wait on conditions with a cap (`for` up to N fixed updates) instead of `WaitForSeconds` guesses.
- `Time.timeScale` can speed slow sequences, but physics results change with the step — assert outcomes, not exact positions.

## Running headless

```sh
UNITY="/Applications/Unity/Hub/Editor/$(sed -n 's/m_EditorVersion: //p' ProjectSettings/ProjectVersion.txt)/Unity.app/Contents/MacOS/Unity"
mkdir -p /tmp/tt-<task key>
"$UNITY" -batchmode -nographics -projectPath . -runTests -testPlatform EditMode \
  -testResults /tmp/tt-<task key>/editmode.xml -logFile /tmp/tt-<task key>/editmode.log
"$UNITY" -batchmode -projectPath . -runTests -testPlatform PlayMode \
  -testResults /tmp/tt-<task key>/playmode.xml -logFile /tmp/tt-<task key>/playmode.log
```

- Do not add `-quit` with `-runTests`; the editor quits when the run ends.
- Drop `-nographics` for PlayMode tests that render or capture (game-visual-self-review).
- `-testFilter "Game.Tests.InventoryTests"` or `-testCategory` narrows a run while iterating.
- The project must not be open in another editor instance (the lock fails the run).
- Read the result: `grep -o 'result="[A-Za-z]*" total="[0-9]*" passed="[0-9]*" failed="[0-9]*"' editmode.xml | head -1`, and `grep 'error CS' editmode.log` for compile errors (a compile error means zero tests ran, which is not a pass). A non-zero exit code is a failure.
- Licence errors in the log ("No valid Unity Editor license") mean the run never started — report it as not run.

Coverage, when the Code Coverage package is installed: add `-enableCodeCoverage -coverageResultsPath /tmp/tt-<task key>/coverage -coverageOptions "generateAdditionalMetrics;assemblyFilters:+Game.*"`.

## No editor on this machine

1. Keep the rules in `Game.Core` (`noEngineReferences: true`).
2. Build a throwaway test project outside the repo:

```xml
<!-- /tmp/tt-<task key>/core-tests/CoreTests.csproj -->
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup><TargetFramework>net8.0</TargetFramework><Nullable>disable</Nullable></PropertyGroup>
  <ItemGroup>
    <Compile Include="<repo>/Assets/Scripts/Core/**/*.cs" />
    <Compile Include="<repo>/Assets/Tests/EditMode/Core/**/*.cs" />
    <PackageReference Include="Microsoft.NET.Test.Sdk" Version="17.*" />
    <PackageReference Include="NUnit" Version="3.*" />
    <PackageReference Include="NUnit3TestAdapter" Version="4.*" />
  </ItemGroup>
</Project>
```

3. `dotnet test /tmp/tt-<task key>/core-tests` — Unity's C# language version is older than .NET 8's default, so set `<LangVersion>9.0</LangVersion>` if the repo targets it, to avoid using features Unity cannot compile.
4. Report both: `RAN: dotnet test (Core) 18/18` and `NOT RUN: EditMode/PlayMode — Unity <version> not installed`.

## Common Mistakes

- PlayMode tests for pure rules — slow and flaky for no gain.
- Tests that depend on production scenes or on execution order between tests.
- Objects created in a test and never destroyed.
- Reading "Exiting batchmode successfully" as "tests passed" while the XML says failed or the log shows `error CS`.

## Red Flags

- A new gameplay rule with only a PlayMode test.
- `WaitForSeconds(2)` as the synchronisation in a test.
- A test assembly that references `Game.UI` to test gameplay.
