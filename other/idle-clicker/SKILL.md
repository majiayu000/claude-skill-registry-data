---
name: idle-clicker
description: "Idle/clicker game architecture — big number math, offline progress, prestige/rebirth, upgrade trees, automation, currency systems, time-based rewards."
globs: ["**/Idle*.cs", "**/Clicker*.cs", "**/Currency*.cs", "**/Upgrade*.cs", "**/Prestige*.cs"]
---

# Idle / Clicker Game Patterns

## Big Number System

Standard float/double loses precision at large values. Use a custom big number or double with formatted display.

```csharp
public readonly struct BigNumber
{
    private readonly double _value;
    private readonly int _exponent;

    public BigNumber(double value, int exponent = 0)
    {
        _value = value;
        _exponent = exponent;
        // Normalize would be called here
    }

    public static BigNumber operator +(BigNumber a, BigNumber b)
    {
        if (a._exponent == b._exponent)
        {
            return new BigNumber(a._value + b._value, a._exponent);
        }
        int diff = a._exponent - b._exponent;
        if (diff > 15) return a; // b is negligible
        if (diff < -15) return b;
        if (diff > 0)
        {
            return new BigNumber(a._value + b._value / System.Math.Pow(10, diff), a._exponent);
        }
        return new BigNumber(b._value + a._value / System.Math.Pow(10, -diff), b._exponent);
    }

    public string ToFormattedString()
    {
        // 1.23K, 4.56M, 7.89B, 1.23T, etc.
        string[] suffixes = { "", "K", "M", "B", "T", "Qa", "Qi", "Sx", "Sp", "Oc", "No", "Dc" };
        int tier = _exponent / 3;
        if (tier < suffixes.Length)
        {
            double displayValue = _value * System.Math.Pow(10, _exponent % 3);
            return $"{displayValue:F2}{suffixes[tier]}";
        }
        return $"{_value:F2}e{_exponent}";
    }
}
```

## Currency System

```csharp
[CreateAssetMenu(menuName = "Idle/Currency Definition")]
public sealed class CurrencyDefinition : ScriptableObject
{
    [SerializeField] private string _currencyId;
    [SerializeField] private string _displayName;
    [SerializeField] private Sprite _icon;

    public string CurrencyId => _currencyId;
    public string DisplayName => _displayName;
    public Sprite Icon => _icon;
}

public sealed class CurrencyManager : MonoBehaviour
{
    private readonly Dictionary<string, double> _currencies = new();

    public event System.Action<string, double> OnCurrencyChanged;

    public double GetAmount(string currencyId)
    {
        _currencies.TryGetValue(currencyId, out double amount);
        return amount;
    }

    public bool CanAfford(string currencyId, double cost)
    {
        return GetAmount(currencyId) >= cost;
    }

    public void Add(string currencyId, double amount)
    {
        if (!_currencies.ContainsKey(currencyId))
        {
            _currencies[currencyId] = 0;
        }
        _currencies[currencyId] += amount;
        OnCurrencyChanged?.Invoke(currencyId, _currencies[currencyId]);
    }

    public bool Spend(string currencyId, double cost)
    {
        if (!CanAfford(currencyId, cost)) return false;
        _currencies[currencyId] -= cost;
        OnCurrencyChanged?.Invoke(currencyId, _currencies[currencyId]);
        return true;
    }
}
```

## Upgrade System

```csharp
[CreateAssetMenu(menuName = "Idle/Upgrade Definition")]
public sealed class UpgradeDefinition : ScriptableObject
{
    [SerializeField] private string _upgradeId;
    [SerializeField] private string _displayName;
    [SerializeField] private string _currencyId;
    [SerializeField] private double _baseCost = 10;
    [SerializeField] private float _costMultiplier = 1.15f;
    [SerializeField] private int _maxLevel = -1; // -1 = unlimited
    [SerializeField] private double _baseEffect = 1;
    [SerializeField] private float _effectMultiplier = 1.0f;

    public string UpgradeId => _upgradeId;
    public string DisplayName => _displayName;

    public double GetCost(int currentLevel)
    {
        return _baseCost * System.Math.Pow(_costMultiplier, currentLevel);
    }

    public double GetEffect(int currentLevel)
    {
        return _baseEffect + (_effectMultiplier * currentLevel);
    }

    public bool IsMaxed(int currentLevel)
    {
        return _maxLevel >= 0 && currentLevel >= _maxLevel;
    }
}
```

## Offline Progress

```csharp
public sealed class OfflineProgressCalculator : MonoBehaviour
{
    [SerializeField] private float _offlineEfficiency = 0.5f; // 50% of online rate
    [SerializeField] private float _maxOfflineHours = 8f;

    private const string LAST_PLAYED_KEY = "LastPlayedTime";

    public double CalculateOfflineEarnings(double perSecondRate)
    {
        string lastPlayed = PlayerPrefs.GetString(LAST_PLAYED_KEY, "");
        if (string.IsNullOrEmpty(lastPlayed)) return 0;

        long binary = long.Parse(lastPlayed);
        System.DateTime lastTime = System.DateTime.FromBinary(binary);
        System.TimeSpan elapsed = System.DateTime.UtcNow - lastTime;

        double seconds = System.Math.Min(elapsed.TotalSeconds, _maxOfflineHours * 3600);
        return perSecondRate * seconds * _offlineEfficiency;
    }

    public void SaveExitTime()
    {
        PlayerPrefs.SetString(LAST_PLAYED_KEY, System.DateTime.UtcNow.ToBinary().ToString());
        PlayerPrefs.Save();
    }

    private void OnApplicationPause(bool paused)
    {
        if (paused) SaveExitTime();
    }

    private void OnApplicationQuit()
    {
        SaveExitTime();
    }
}
```

## Prestige / Rebirth System

```csharp
public sealed class PrestigeSystem : MonoBehaviour
{
    [SerializeField] private double _prestigeThreshold = 1000000;
    [SerializeField] private string _primaryCurrencyId = "gold";
    [SerializeField] private string _prestigeCurrencyId = "gems";

    [SerializeField] private CurrencyManager _currencyManager;

    public int PrestigeCount { get; private set; }

    public double CalculatePrestigeReward()
    {
        double total = _currencyManager.GetAmount(_primaryCurrencyId);
        if (total < _prestigeThreshold) return 0;
        return System.Math.Floor(System.Math.Sqrt(total / _prestigeThreshold));
    }

    public bool CanPrestige()
    {
        return CalculatePrestigeReward() > 0;
    }

    public void DoPrestige()
    {
        double reward = CalculatePrestigeReward();
        if (reward <= 0) return;

        // Award prestige currency
        _currencyManager.Add(_prestigeCurrencyId, reward);
        PrestigeCount++;

        // Reset primary progress
        ResetProgress();
    }

    private void ResetProgress()
    {
        // Reset primary currency, upgrades, and generators
        // Keep prestige currency and prestige upgrades
    }
}
```

## Game Loop

```
Launch → Check offline progress → Show earnings popup
    → Main screen (tap to earn + automated income)
        → Buy upgrades (increase tap/auto income)
            → Prestige when progress slows
                → Restart with permanent bonuses
```

## Key Design Rules

- **Exponential growth** — costs and rewards both scale exponentially
- **Multiple income sources** — tap income, auto generators, prestige bonuses
- **Clear next goal** — always show what the player is working toward
- **Satisfying numbers** — big numbers going up is the core reward
- **Offline progress** — player must feel rewarded for coming back
- **No skill required** — progress is time + decisions, not reflexes

## Mobile-Specific

- **Battery friendly** — cap at 30fps, reduce Update frequency for idle generators
- **Background handling** — `OnApplicationPause` saves state immediately
- **Notification hooks** — "Your generators have earned 1M gold!" after offline period
- **Minimal UI updates** — update currency display every 0.1s, not every frame
