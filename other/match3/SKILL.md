---
name: match3
description: "Match-3 puzzle game architecture — grid system, tile matching, cascade/gravity, special tiles, combo chains, level objectives, lives/energy system."
globs: ["**/Match*.cs", "**/Grid*.cs", "**/Tile*.cs", "**/Board*.cs", "**/Puzzle*.cs"]
---

# Match-3 Puzzle Patterns

## Grid System

```csharp
public sealed class Board : MonoBehaviour
{
    [SerializeField] private int _width = 7;
    [SerializeField] private int _height = 9;
    [SerializeField] private float _cellSize = 1f;
    [SerializeField] private TileDefinition[] _tileTypes;

    private Tile[,] _grid;

    private void Awake()
    {
        _grid = new Tile[_width, _height];
    }

    public Vector3 GridToWorld(int x, int y)
    {
        float offsetX = (_width - 1) * 0.5f;
        float offsetY = (_height - 1) * 0.5f;
        return new Vector3((x - offsetX) * _cellSize, (y - offsetY) * _cellSize, 0f);
    }

    public bool IsValidPosition(int x, int y)
    {
        return x >= 0 && x < _width && y >= 0 && y < _height;
    }

    public Tile GetTile(int x, int y)
    {
        if (!IsValidPosition(x, y)) return null;
        return _grid[x, y];
    }

    public void SetTile(int x, int y, Tile tile)
    {
        _grid[x, y] = tile;
        if (tile != null)
        {
            tile.GridX = x;
            tile.GridY = y;
        }
    }
}
```

## Tile Definition

```csharp
[CreateAssetMenu(menuName = "Match3/Tile Definition")]
public sealed class TileDefinition : ScriptableObject
{
    [SerializeField] private string _tileId;
    [SerializeField] private Sprite _sprite;
    [SerializeField] private Color _color = Color.white;
    [SerializeField] private TileType _type = TileType.Normal;

    public string TileId => _tileId;
    public Sprite Sprite => _sprite;
    public Color Color => _color;
    public TileType Type => _type;
}

public enum TileType
{
    Normal,
    StripedHorizontal,
    StripedVertical,
    Wrapped,
    ColorBomb,
    Blocker,
    Ice,
    Chain
}
```

## Swap & Match Detection

```csharp
public sealed class MatchDetector
{
    private readonly Board _board;
    private readonly List<MatchResult> _matchBuffer = new(16);

    public MatchDetector(Board board) { _board = board; }

    public List<MatchResult> FindAllMatches()
    {
        _matchBuffer.Clear();
        FindHorizontalMatches();
        FindVerticalMatches();
        return _matchBuffer;
    }

    private void FindHorizontalMatches()
    {
        for (int y = 0; y < _board.Height; y++)
        {
            int matchStart = 0;
            for (int x = 1; x <= _board.Width; x++)
            {
                bool matches = x < _board.Width &&
                    _board.GetTile(x, y) != null &&
                    _board.GetTile(matchStart, y) != null &&
                    _board.GetTile(x, y).Definition.TileId ==
                    _board.GetTile(matchStart, y).Definition.TileId;

                if (!matches)
                {
                    int length = x - matchStart;
                    if (length >= 3)
                    {
                        MatchResult match = new MatchResult();
                        match.Direction = MatchDirection.Horizontal;
                        for (int mx = matchStart; mx < x; mx++)
                        {
                            match.Tiles.Add(_board.GetTile(mx, y));
                        }
                        _matchBuffer.Add(match);
                    }
                    matchStart = x;
                }
            }
        }
    }

    private void FindVerticalMatches()
    {
        for (int x = 0; x < _board.Width; x++)
        {
            int matchStart = 0;
            for (int y = 1; y <= _board.Height; y++)
            {
                bool matches = y < _board.Height &&
                    _board.GetTile(x, y) != null &&
                    _board.GetTile(x, matchStart) != null &&
                    _board.GetTile(x, y).Definition.TileId ==
                    _board.GetTile(x, matchStart).Definition.TileId;

                if (!matches)
                {
                    int length = y - matchStart;
                    if (length >= 3)
                    {
                        MatchResult match = new MatchResult();
                        match.Direction = MatchDirection.Vertical;
                        for (int my = matchStart; my < y; my++)
                        {
                            match.Tiles.Add(_board.GetTile(x, my));
                        }
                        _matchBuffer.Add(match);
                    }
                    matchStart = y;
                }
            }
        }
    }
}
```

## Cascade / Gravity

After matches are cleared:
1. Remove matched tiles (play destroy animation)
2. Gravity: tiles above empty spaces fall down
3. Refill: new tiles spawn from top
4. Re-check for new matches (chain combo)
5. Repeat until no matches remain

```csharp
// Coroutine-based cascade loop
private IEnumerator CascadeLoop()
{
    List<MatchResult> matches = _detector.FindAllMatches();
    int comboCount = 0;

    while (matches.Count > 0)
    {
        comboCount++;
        yield return StartCoroutine(DestroyMatches(matches, comboCount));
        yield return StartCoroutine(ApplyGravity());
        yield return StartCoroutine(RefillBoard());
        matches = _detector.FindAllMatches();
    }

    CheckLevelObjective();
    EnableInput();
}
```

## Special Tile Rules

| Match | Creates |
|-------|---------|
| 4 in a row | Striped tile (clears row or column) |
| L or T shape | Wrapped tile (explodes 3x3 area) |
| 5 in a row | Color bomb (clears all of one color) |

| Combo | Effect |
|-------|--------|
| Striped + Striped | Cross clear (row + column) |
| Striped + Wrapped | 3-row or 3-column clear |
| Wrapped + Wrapped | 5x5 explosion |
| Color bomb + any | Clears all tiles of that color |
| Color bomb + Color bomb | Clears entire board |

## Touch Input for Swap

- Drag threshold: 0.5 cells (half the cell size)
- Only allow horizontal/vertical swaps (snap to nearest direction)
- Invalid swap: animate swap then swap back
- Disable input during cascade animation

## Level Objectives

- **Score target:** reach N points in M moves
- **Clear blockers:** destroy all ice/chain tiles
- **Collect items:** match next to items to collect them
- **Reach bottom:** guide special tile to bottom row

## Lives / Energy System

```csharp
public sealed class LivesSystem : MonoBehaviour
{
    [SerializeField] private int _maxLives = 5;
    [SerializeField] private int _regenMinutes = 30;

    private int _currentLives;
    private System.DateTime _lastLifeLostTime;

    public int CurrentLives => _currentLives;
    public bool HasLives => _currentLives > 0;

    public void UseLive()
    {
        if (_currentLives <= 0) return;
        _currentLives--;
        if (_currentLives < _maxLives)
        {
            _lastLifeLostTime = System.DateTime.UtcNow;
        }
        Save();
    }

    public void CheckRegen()
    {
        if (_currentLives >= _maxLives) return;
        System.TimeSpan elapsed = System.DateTime.UtcNow - _lastLifeLostTime;
        int livesRegened = (int)(elapsed.TotalMinutes / _regenMinutes);
        if (livesRegened > 0)
        {
            _currentLives = Mathf.Min(_maxLives, _currentLives + livesRegened);
            _lastLifeLostTime = _lastLifeLostTime.AddMinutes(livesRegened * _regenMinutes);
            Save();
        }
    }

    private void Save()
    {
        PlayerPrefs.SetInt("Lives", _currentLives);
        PlayerPrefs.SetString("LastLifeLost", _lastLifeLostTime.ToBinary().ToString());
        PlayerPrefs.Save();
    }
}
```

## Performance Notes

- Pool all tiles — never Instantiate/Destroy during gameplay
- Use SpriteRenderer or UI Image, not 3D meshes
- Pre-calculate match possibilities for hint system
- Animate with DOTween for smooth tile movement
