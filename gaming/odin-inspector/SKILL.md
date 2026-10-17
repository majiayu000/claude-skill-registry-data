---
name: odin-inspector
description: "Odin Inspector & Serializer — SerializedMonoBehaviour, validation attributes, custom drawers, editor windows. Enhances Unity inspector with powerful serialization and UI."
globs: ["**/Odin*", "**/Sirenix*", "**/*Inspector*.cs"]
---

# Odin Inspector & Serializer

Odin Inspector (Sirenix) extends Unity's inspector with powerful serialization (dictionaries, interfaces, polymorphic types), validation attributes, layout control, and custom editor window tools. It dramatically reduces the need for custom editors.

## Serialization — SerializedMonoBehaviour & SerializedScriptableObject

Unity's default serializer cannot handle dictionaries, interfaces, abstract classes, or deeply nested polymorphic types. Odin's serializer can.

```csharp
using Sirenix.OdinInspector;
using Sirenix.Serialization;

// Inherit from SerializedMonoBehaviour instead of MonoBehaviour
public class EnemyData : SerializedMonoBehaviour
{
    // Dictionary — just works in the inspector
    public Dictionary<string, int> Stats = new Dictionary<string, int>
    {
        { "Health", 100 },
        { "Attack", 15 },
        { "Defense", 8 },
    };

    // Interface field — shows a polymorphic dropdown
    public IAbility PrimaryAbility;
    public List<IAbility> AbilityPool;

    // Nested complex types
    public Dictionary<DamageType, List<StatusEffect>> DamageEffects;
}
```

```csharp
// For ScriptableObjects
public class GameConfig : SerializedScriptableObject
{
    public Dictionary<string, EnemyWaveConfig> Waves;
    public Dictionary<ItemRarity, Color> RarityColors;
}
```

### When to Use Odin Serialization vs Unity Serialization

| Use Odin Serialization | Use Unity Serialization |
|------------------------|------------------------|
| Dictionaries, interfaces, polymorphism | Simple fields (int, float, string, Vector3) |
| Editor-time configuration data | Runtime hot-path data |
| Complex nested structures | Arrays/Lists of concrete types |
| Tool/editor windows | Prefabs and ScriptableObjects that must work without Odin |

### IMPORTANT: Migration Caution

Projects using `SerializedMonoBehaviour` or `SerializedScriptableObject` are **coupled to Odin**. If Odin is removed from the project, all data stored via Odin's extended serialization is **permanently lost**. Unity only reads its own serialized data. Plan accordingly.

## Validation Attributes

Catch configuration errors in the inspector before they become runtime bugs.

### Required Fields

```csharp
public class UIManager : MonoBehaviour
{
    [Required]
    [SerializeField] private Canvas _mainCanvas;

    [Required("Assign the health bar prefab!")]
    [SerializeField] private GameObject _healthBarPrefab;
}
```

### Value Validation

```csharp
public class EnemyConfig : ScriptableObject
{
    [MinValue(1)]
    public int Health = 100;

    [MaxValue(100)]
    public int SpawnChance = 50;

    [MinValue(0), MaxValue(1)]
    public float CriticalChance = 0.1f;

    [PropertyRange(0, 10)]
    public float MoveSpeed = 3f;

    [ValidateInput("IsPositive", "Damage must be positive")]
    public int Damage = 10;

    private bool IsPositive(int value) => value > 0;
}
```

### Asset Constraints

```csharp
[AssetsOnly]
public GameObject EnemyPrefab;         // Only accepts project assets, not scene objects

[SceneObjectsOnly]
public Transform SpawnPoint;            // Only accepts objects in the scene

[ChildGameObjectsOnly]
public Transform WeaponMount;           // Only accepts children of this object
```

### Custom Validation

```csharp
[ValidateInput("ValidateWaveConfig", "Wave must have at least one enemy type")]
public WaveConfig CurrentWave;

private bool ValidateWaveConfig(WaveConfig config)
{
    return config != null && config.EnemyTypes.Count > 0;
}
```

## Layout Attributes

Organize inspector fields into groups, tabs, and collapsible sections.

### Box Group

```csharp
[BoxGroup("Movement")]
public float MoveSpeed = 5f;

[BoxGroup("Movement")]
public float JumpHeight = 2f;

[BoxGroup("Combat")]
public int Damage = 10;

[BoxGroup("Combat")]
public float AttackRange = 1.5f;
```

### Tab Group

```csharp
[TabGroup("General")]
public string DisplayName;

[TabGroup("General")]
public Sprite Icon;

[TabGroup("Stats")]
public int Health = 100;

[TabGroup("Stats")]
public int Attack = 15;

[TabGroup("Audio")]
public AudioClip HitSound;

[TabGroup("Audio")]
public AudioClip DeathSound;
```

### Foldout Group

```csharp
[FoldoutGroup("Advanced Settings")]
public float GravityMultiplier = 1f;

[FoldoutGroup("Advanced Settings")]
public bool UseCustomPhysics;

[FoldoutGroup("Advanced Settings")]
public LayerMask CollisionLayers;
```

### Horizontal and Vertical Groups

```csharp
[HorizontalGroup("Row1")]
public int Health;

[HorizontalGroup("Row1")]
public int Mana;

[HorizontalGroup("Row1")]
public int Stamina;

// Nested groups
[VerticalGroup("Row2/Left")]
public float Speed;

[VerticalGroup("Row2/Left")]
public float JumpForce;

[VerticalGroup("Row2/Right")]
public int Armor;

[VerticalGroup("Row2/Right")]
public int MagicResist;
```

### Title and Header

```csharp
[Title("Player Configuration", "Adjust these values for game balance")]
public float MoveSpeed;

[Title("Visual Settings", bold: true, horizontalLine: true)]
public Color TrailColor;
```

## Display Attributes — Conditional Visibility

### Show/Hide Based on Conditions

```csharp
public bool UseCustomGravity;

[ShowIf("UseCustomGravity")]
public float CustomGravity = 9.81f;

[HideIf("UseCustomGravity")]
public string DefaultGravityNote = "Using Physics.gravity";

// Method-based condition
public EnemyType Type;

[ShowIf("IsBoss")]
public float EnrageThreshold = 0.3f;

private bool IsBoss() => Type == EnemyType.Boss;
```

### Enable/Disable

```csharp
[EnableIf("IsDebugMode")]
public bool ShowHitboxes;

[DisableIf("IsReleaseMode")]
public string DebugCommand;

public bool IsDebugMode;
private bool IsReleaseMode() => !IsDebugMode;
```

### Read Only

```csharp
[ReadOnly]
public string GeneratedId;

[DisplayAsString]
public string InfoMessage = "This is display-only text";

// Show in inspector but cannot edit
[ShowInInspector, ReadOnly]
public int CalculatedDPS => Damage * AttacksPerSecond;
```

### Preview and Inline Editor

```csharp
[PreviewField(75)]
public Sprite CharacterIcon;

[PreviewField(100, ObjectFieldAlignment.Left)]
public Texture2D SplashArt;

// Show full inspector of referenced ScriptableObject inline
[InlineEditor]
public EnemyConfig EnemySettings;

[InlineEditor(InlineEditorModes.FullEditor)]
public Material EffectMaterial;
```

## Button Attribute

Turn methods into inspector buttons for quick testing and tooling.

```csharp
public class LevelBuilder : MonoBehaviour
{
    public int Width = 10;
    public int Height = 10;

    [Button("Generate Level", ButtonSizes.Large)]
    private void GenerateLevel()
    {
        // Level generation logic
        Debug.Log($"Generating {Width}x{Height} level");
    }

    [Button]
    private void ClearLevel()
    {
        // Clear all tiles
    }

    [ButtonGroup("Actions")]
    private void Save() { /* ... */ }

    [ButtonGroup("Actions")]
    private void Load() { /* ... */ }

    [ButtonGroup("Actions")]
    private void Reset() { /* ... */ }

    // Button with parameters
    [Button]
    private void SpawnEnemies(EnemyType type, int count)
    {
        for (int i = 0; i < count; i++)
            SpawnEnemy(type);
    }
}
```

## Color and Enum Enhancements

```csharp
// Color palette picker
[ColorPalette("My Palette")]
public Color TeamColor;

// Enum as toggle buttons instead of dropdown
[EnumToggleButtons]
public Direction Facing;

// Custom value dropdown from method
[ValueDropdown("GetAvailableItems")]
public string SelectedItem;

private IEnumerable<string> GetAvailableItems()
{
    return new[] { "Sword", "Shield", "Potion", "Bow" };
}

// Dropdown with custom display names
[ValueDropdown("GetDifficultyOptions")]
public int DifficultyLevel;

private IEnumerable<ValueDropdownItem<int>> GetDifficultyOptions()
{
    return new[]
    {
        new ValueDropdownItem<int>("Easy", 1),
        new ValueDropdownItem<int>("Normal", 2),
        new ValueDropdownItem<int>("Hard", 3),
        new ValueDropdownItem<int>("Nightmare", 4),
    };
}
```

## ShowInInspector — Display Non-Serialized Data

```csharp
// Show properties and computed values in the inspector (read-only display, not saved)
[ShowInInspector]
public int CurrentHealth => _health;

[ShowInInspector]
private static int _instanceCount;

[ShowInInspector]
public float DamagePerSecond => Attack * AttackSpeed;

// Show non-serialized runtime state
[ShowInInspector, ReadOnly]
private FSMState _currentState;
```

## Editor Windows with Odin

### Simple Editor Window

```csharp
using Sirenix.OdinInspector;
using Sirenix.OdinInspector.Editor;
using UnityEditor;

public class GameBalanceTool : OdinEditorWindow
{
    [MenuItem("Tools/Game Balance")]
    private static void Open() => GetWindow<GameBalanceTool>();

    [InlineEditor]
    public List<EnemyConfig> Enemies;

    [Button("Auto-Balance All", ButtonSizes.Large)]
    private void AutoBalance()
    {
        foreach (var enemy in Enemies)
            BalanceEnemy(enemy);
    }
}
```

### Menu Tree Editor Window

```csharp
public class GameDataEditor : OdinMenuEditorWindow
{
    [MenuItem("Tools/Game Data")]
    private static void Open() => GetWindow<GameDataEditor>();

    protected override OdinMenuTree BuildMenuTree()
    {
        var tree = new OdinMenuTree();

        // Add all ScriptableObjects of specific types
        tree.AddAllAssetsAtPath("Enemies", "Assets/Data/Enemies", typeof(EnemyConfig));
        tree.AddAllAssetsAtPath("Items", "Assets/Data/Items", typeof(ItemConfig));
        tree.AddAllAssetsAtPath("Levels", "Assets/Data/Levels", typeof(LevelConfig));

        // Custom entries
        tree.Add("Settings/Audio", new AudioSettingsWrapper());
        tree.Add("Settings/Graphics", new GraphicsSettingsWrapper());

        return tree;
    }
}
```

## List and Collection Attributes

```csharp
// Searchable list
[Searchable]
public List<EnemyConfig> AllEnemies;

// Table display for list of structs/classes
[TableList]
public List<LootEntry> LootTable;

[System.Serializable]
public class LootEntry
{
    [TableColumnWidth(60, Resizable = false)]
    [PreviewField(50)]
    public Sprite Icon;

    public string ItemName;

    [PropertyRange(0, 100)]
    public float DropChance;

    [MinValue(1)]
    public int MinCount;

    [MinValue(1)]
    public int MaxCount;
}
```

## Performance Considerations

- **Odin serialization is slower than Unity's built-in serializer.** Do not use `SerializedMonoBehaviour` for objects that are instantiated frequently at runtime (e.g., bullets, particles).
- **Odin attributes are editor-only.** They have zero runtime cost. Layout, buttons, and validation attributes do not affect build size or performance.
- **Use `SerializedScriptableObject` freely** for configuration data loaded once at startup.
- For runtime data containers that need dictionaries, consider manual serialization (JSON, MessagePack) instead of Odin serialization.

## Common Attribute Combinations

### Configuration ScriptableObject

```csharp
[CreateAssetMenu(fileName = "NewEnemyConfig", menuName = "Game/Enemy Config")]
public class EnemyConfig : SerializedScriptableObject
{
    [Title("Identity")]
    [Required]
    public string DisplayName;

    [PreviewField(50)]
    public Sprite Icon;

    [Title("Stats")]
    [PropertyRange(1, 1000)]
    public int Health = 100;

    [PropertyRange(1, 100)]
    public int Attack = 10;

    [PropertyRange(0, 20)]
    public float MoveSpeed = 3f;

    [Title("Abilities")]
    [ListDrawerSettings(ShowFoldout = true)]
    public List<IAbility> Abilities;

    [Title("Loot")]
    [TableList]
    public List<LootEntry> LootTable;

    [Title("Debug", bold: false)]
    [Button("Test Spawn")]
    private void TestSpawn()
    {
        Debug.Log($"Would spawn {DisplayName} with {Health} HP");
    }
}
```

### Inspector-Friendly MonoBehaviour

```csharp
public class TurretController : MonoBehaviour
{
    [BoxGroup("Targeting")]
    [Required]
    public Transform FirePoint;

    [BoxGroup("Targeting")]
    [PropertyRange(1, 50)]
    public float Range = 10f;

    [BoxGroup("Targeting")]
    [EnumToggleButtons]
    public TargetPriority Priority;

    [BoxGroup("Combat")]
    [MinValue(0.1f)]
    public float FireRate = 1f;

    [BoxGroup("Combat")]
    [AssetsOnly, Required]
    public GameObject ProjectilePrefab;

    [FoldoutGroup("Advanced")]
    public AnimationCurve DamageFalloff;

    [FoldoutGroup("Advanced")]
    [ShowIf("@Priority == TargetPriority.Custom")]
    public float CustomPriorityWeight;

    [ShowInInspector, ReadOnly]
    [BoxGroup("Runtime")]
    private Transform _currentTarget;

    [ShowInInspector, ReadOnly]
    [BoxGroup("Runtime")]
    [ProgressBar(0, 1)]
    private float _reloadProgress;
}
```

## Odin Attribute Quick Reference

| Category | Attributes |
|----------|-----------|
| **Validation** | `[Required]`, `[ValidateInput]`, `[AssetsOnly]`, `[SceneObjectsOnly]`, `[MinValue]`, `[MaxValue]`, `[PropertyRange]` |
| **Layout** | `[BoxGroup]`, `[TabGroup]`, `[FoldoutGroup]`, `[HorizontalGroup]`, `[VerticalGroup]`, `[Title]` |
| **Visibility** | `[ShowIf]`, `[HideIf]`, `[EnableIf]`, `[DisableIf]`, `[ReadOnly]`, `[ShowInInspector]` |
| **Display** | `[PreviewField]`, `[InlineEditor]`, `[ProgressBar]`, `[DisplayAsString]`, `[MultiLineProperty]` |
| **Interaction** | `[Button]`, `[ButtonGroup]`, `[EnumToggleButtons]`, `[ValueDropdown]`, `[ColorPalette]` |
| **Lists** | `[TableList]`, `[Searchable]`, `[ListDrawerSettings]` |
| **Info** | `[InfoBox]`, `[DetailedInfoBox]`, `[GUIColor]`, `[PropertyOrder]`, `[PropertySpace]` |
