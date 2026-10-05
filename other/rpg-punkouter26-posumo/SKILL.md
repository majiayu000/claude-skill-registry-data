---
name: rpg
description: "RPG game architecture — stat system (base + modifiers), level/XP, skill trees, quest system, NPC interaction, turn-based and real-time combat patterns."
globs: ["**/RPG*.cs", "**/Stat*.cs", "**/Quest*.cs", "**/Skill*.cs", "**/Level*.cs"]
---

# RPG Game Patterns

## Stat System

```csharp
public enum StatModifierType { Flat, PercentAdd, PercentMultiply }

[System.Serializable]
public sealed class StatModifier
{
    public float Value;
    public StatModifierType Type;
    public int Order;
    public object Source;

    public StatModifier(float value, StatModifierType type, int order, object source)
    {
        Value = value;
        Type = type;
        Order = order;
        Source = source;
    }
}

[System.Serializable]
public sealed class CharacterStat
{
    [SerializeField] private float _baseValue;
    private readonly List<StatModifier> _modifiers = new();
    private float _cachedValue;
    private bool _isDirty = true;

    public float Value
    {
        get
        {
            if (_isDirty)
            {
                _cachedValue = CalculateFinalValue();
                _isDirty = false;
            }
            return _cachedValue;
        }
    }

    public void AddModifier(StatModifier mod)
    {
        _modifiers.Add(mod);
        _modifiers.Sort((a, b) => a.Order.CompareTo(b.Order));
        _isDirty = true;
    }

    public void RemoveAllModifiersFromSource(object source)
    {
        for (int i = _modifiers.Count - 1; i >= 0; i--)
        {
            if (_modifiers[i].Source == source)
            {
                _modifiers.RemoveAt(i);
                _isDirty = true;
            }
        }
    }

    private float CalculateFinalValue()
    {
        float finalValue = _baseValue;
        float percentAddSum = 0f;

        for (int i = 0; i < _modifiers.Count; i++)
        {
            StatModifier mod = _modifiers[i];
            switch (mod.Type)
            {
                case StatModifierType.Flat:
                    finalValue += mod.Value;
                    break;
                case StatModifierType.PercentAdd:
                    percentAddSum += mod.Value;
                    if (i + 1 >= _modifiers.Count || _modifiers[i + 1].Type != StatModifierType.PercentAdd)
                    {
                        finalValue *= 1f + percentAddSum;
                        percentAddSum = 0f;
                    }
                    break;
                case StatModifierType.PercentMultiply:
                    finalValue *= 1f + mod.Value;
                    break;
            }
        }

        return Mathf.Round(finalValue * 100f) / 100f;
    }
}
```

**Modifier ordering:** Flat (+5) → PercentAdd (+10% stacks additively) → PercentMultiply (+20% stacks multiplicatively).

## Level / XP System

```csharp
public sealed class LevelSystem
{
    private int _currentLevel = 1;
    private int _currentXP;
    private int _maxLevel = 99;

    public event System.Action<int> OnLevelUp;

    public int CurrentLevel => _currentLevel;
    public int CurrentXP => _currentXP;
    public int XPToNextLevel => GetXPForLevel(_currentLevel + 1) - GetXPForLevel(_currentLevel);
    public float XPProgress => (float)_currentXP / XPToNextLevel;

    public void AddXP(int amount)
    {
        _currentXP += amount;
        while (_currentXP >= XPToNextLevel && _currentLevel < _maxLevel)
        {
            _currentXP -= XPToNextLevel;
            _currentLevel++;
            OnLevelUp?.Invoke(_currentLevel);
        }
    }

    // Exponential XP curve
    private int GetXPForLevel(int level)
    {
        return Mathf.RoundToInt(100f * Mathf.Pow(level, 1.5f));
    }
}
```

## Quest System

```csharp
public enum ObjectiveType { Kill, Collect, Talk, Location, Custom }

[System.Serializable]
public sealed class QuestObjective
{
    public string Description;
    public ObjectiveType Type;
    public string TargetId;
    public int RequiredCount;
    [NonSerialized] public int CurrentCount;

    public bool IsComplete => CurrentCount >= RequiredCount;
}

[CreateAssetMenu(menuName = "RPG/Quest Definition")]
public sealed class QuestDefinition : ScriptableObject
{
    [SerializeField] private string _questId;
    [SerializeField] private string _title;
    [TextArea] [SerializeField] private string _description;
    [SerializeField] private List<QuestObjective> _objectives;
    [SerializeField] private int _xpReward;
    [SerializeField] private List<ItemDefinition> _itemRewards;
    [SerializeField] private QuestDefinition[] _prerequisites;

    public string QuestId => _questId;
    public string Title => _title;
    public IReadOnlyList<QuestObjective> Objectives => _objectives;
    public int XPReward => _xpReward;
}

public sealed class QuestTracker
{
    private readonly Dictionary<string, QuestDefinition> _activeQuests = new();

    public event System.Action<QuestDefinition> OnQuestCompleted;

    public void StartQuest(QuestDefinition quest)
    {
        _activeQuests[quest.QuestId] = quest;
    }

    public void ReportProgress(ObjectiveType type, string targetId, int count = 1)
    {
        foreach (KeyValuePair<string, QuestDefinition> kvp in _activeQuests)
        {
            QuestDefinition quest = kvp.Value;
            bool allComplete = true;

            for (int i = 0; i < quest.Objectives.Count; i++)
            {
                QuestObjective obj = quest.Objectives[i];
                if (obj.Type == type && obj.TargetId == targetId)
                {
                    obj.CurrentCount = Mathf.Min(obj.CurrentCount + count, obj.RequiredCount);
                }
                if (!obj.IsComplete) allComplete = false;
            }

            if (allComplete)
            {
                OnQuestCompleted?.Invoke(quest);
            }
        }
    }
}
```

## Skill Tree

- **SkillNode SO:** name, description, icon, prerequisites (list of SkillNode), stat modifiers, unlock cost
- **SkillTree:** graph of nodes, check prerequisites before unlock, apply modifiers on unlock
- **Respec:** remove all modifiers from skill source, reset unlock state

## Combat Patterns

### Real-Time (Action RPG)
- Abilities as ScriptableObjects: damage, cooldown, mana cost, animation trigger, VFX
- Combo system: track input sequence within time window
- Status effects: timed stat modifiers + tick damage/heal + VFX

### Turn-Based
- Turn order by Speed stat (or initiative roll)
- Action queue: select action → select target → execute → next turn
- Command pattern: each action is an ICommand with Execute/Undo
