---
name: puzzle
description: "Mobile puzzle game architecture — grid/board logic, undo system, hint system, level packs, star ratings, touch drag-and-drop, tutorial overlays."
globs: ["**/Puzzle*.cs", "**/Board*.cs", "**/Grid*.cs", "**/Hint*.cs", "**/Undo*.cs"]
---

# Mobile Puzzle Patterns

## Undo System (Command Pattern)

```csharp
public interface IGameCommand
{
    void Execute();
    void Undo();
}

public sealed class UndoManager
{
    private readonly Stack<IGameCommand> _undoStack = new();
    private readonly int _maxUndoSteps;

    public UndoManager(int maxSteps = 50)
    {
        _maxUndoSteps = maxSteps;
    }

    public int UndoCount => _undoStack.Count;

    public void Execute(IGameCommand command)
    {
        command.Execute();
        _undoStack.Push(command);
        if (_undoStack.Count > _maxUndoSteps)
        {
            // Trim oldest — would need a different data structure for efficiency
        }
    }

    public bool Undo()
    {
        if (_undoStack.Count == 0) return false;
        IGameCommand command = _undoStack.Pop();
        command.Undo();
        return true;
    }

    public void Clear()
    {
        _undoStack.Clear();
    }
}

// Example: move a piece
public sealed class MovePieceCommand : IGameCommand
{
    private readonly Piece _piece;
    private readonly Vector2Int _fromPos;
    private readonly Vector2Int _toPos;

    public MovePieceCommand(Piece piece, Vector2Int from, Vector2Int to)
    {
        _piece = piece;
        _fromPos = from;
        _toPos = to;
    }

    public void Execute() { _piece.MoveTo(_toPos); }
    public void Undo() { _piece.MoveTo(_fromPos); }
}
```

## Level Pack System

```csharp
[CreateAssetMenu(menuName = "Puzzle/Level Pack")]
public sealed class LevelPack : ScriptableObject
{
    [SerializeField] private string _packId;
    [SerializeField] private string _displayName;
    [SerializeField] private Sprite _icon;
    [SerializeField] private PuzzleLevel[] _levels;
    [SerializeField] private bool _isLocked;
    [SerializeField] private int _starsToUnlock;

    public string PackId => _packId;
    public string DisplayName => _displayName;
    public IReadOnlyList<PuzzleLevel> Levels => _levels;
    public bool IsLocked => _isLocked;
    public int StarsToUnlock => _starsToUnlock;
}

[CreateAssetMenu(menuName = "Puzzle/Level")]
public sealed class PuzzleLevel : ScriptableObject
{
    [SerializeField] private string _levelId;
    [SerializeField] private int _parMoves; // 3 stars if completed in this many moves
    [SerializeField] private int _maxMoves; // fail if exceeded (0 = unlimited)
    [SerializeField] private float _parTime; // 3 stars if completed in this time
    [SerializeField] private TextAsset _levelData; // JSON or custom format

    public string LevelId => _levelId;
    public int ParMoves => _parMoves;
    public int MaxMoves => _maxMoves;
}
```

## Star Rating

```csharp
public sealed class StarCalculator
{
    public static int Calculate(PuzzleLevel level, int movesTaken, float timeTaken)
    {
        int stars = 1; // completing = 1 star minimum

        if (level.ParMoves > 0 && movesTaken <= level.ParMoves)
        {
            stars = 3;
        }
        else if (level.ParMoves > 0 && movesTaken <= level.ParMoves * 1.5f)
        {
            stars = 2;
        }

        return stars;
    }

    public static int GetTotalStars(string packId)
    {
        // Sum all stars earned across levels in pack
        int total = 0;
        // Read from save data...
        return total;
    }
}
```

## Hint System

```csharp
public sealed class HintSystem : MonoBehaviour
{
    [SerializeField] private float _autoHintDelay = 15f; // show hint after N seconds idle
    [SerializeField] private int _freeHints = 3;

    private int _hintsRemaining;
    private float _idleTimer;
    private bool _hintShowing;

    public event System.Action<HintData> OnShowHint;
    public event System.Action OnHideHint;

    private void Update()
    {
        if (_hintShowing) return;

        _idleTimer += Time.deltaTime;
        if (_idleTimer >= _autoHintDelay)
        {
            ShowAutoHint();
        }
    }

    public void OnPlayerAction()
    {
        _idleTimer = 0f;
        if (_hintShowing)
        {
            _hintShowing = false;
            OnHideHint?.Invoke();
        }
    }

    public bool UseHint()
    {
        if (_hintsRemaining <= 0) return false;
        _hintsRemaining--;
        ShowExplicitHint();
        return true;
    }

    private void ShowAutoHint()
    {
        // Subtle hint — highlight possible move
        _hintShowing = true;
    }

    private void ShowExplicitHint()
    {
        // Obvious hint — animate the solution move
        _hintShowing = true;
    }
}
```

## Touch Drag-and-Drop

```csharp
public sealed class DragHandler : MonoBehaviour
{
    [SerializeField] private Camera _camera;
    [SerializeField] private LayerMask _draggableLayer;
    [SerializeField] private float _dragOffset = 0.5f; // lift piece while dragging

    private Piece _draggedPiece;
    private Vector3 _dragStartWorldPos;
    private Vector2Int _dragStartGridPos;

    private void Update()
    {
        if (UnityEngine.InputSystem.Touchscreen.current == null) return;

        UnityEngine.InputSystem.Controls.TouchControl touch =
            UnityEngine.InputSystem.Touchscreen.current.primaryTouch;

        if (touch.press.wasPressedThisFrame)
        {
            TryStartDrag(touch.position.ReadValue());
        }
        else if (touch.press.isPressed && _draggedPiece != null)
        {
            UpdateDrag(touch.position.ReadValue());
        }
        else if (touch.press.wasReleasedThisFrame && _draggedPiece != null)
        {
            EndDrag(touch.position.ReadValue());
        }
    }

    private void TryStartDrag(Vector2 screenPos)
    {
        Ray ray = _camera.ScreenPointToRay(screenPos);
        if (Physics2D.Raycast(ray.origin, ray.direction, 100f, _draggableLayer))
        {
            // Start dragging the hit piece
        }
    }

    private void UpdateDrag(Vector2 screenPos)
    {
        Vector3 worldPos = _camera.ScreenToWorldPoint(new Vector3(screenPos.x, screenPos.y, 10f));
        _draggedPiece.transform.position = new Vector3(worldPos.x, worldPos.y + _dragOffset, 0f);
    }

    private void EndDrag(Vector2 screenPos)
    {
        // Snap to nearest valid grid position or return to start
        _draggedPiece = null;
    }
}
```

## Tutorial Overlay

- **First-time only** — check PlayerPrefs flag per tutorial step
- **Dim background** — semi-transparent overlay, spotlight on target element
- **Animated hand** — show tap/drag gesture on the target
- **Progressive** — teach one mechanic per level, not all at once
- **Skippable** — always allow dismissing

## Puzzle Game Types

| Type | Core Mechanic | Examples |
|------|--------------|----------|
| Slide puzzle | Move tiles to solve | 15-puzzle, Unblock Me |
| Match puzzle | Match/connect similar | Match-3, Dots |
| Physics puzzle | Aim/launch objects | Angry Birds, Cut the Rope |
| Word puzzle | Form words from letters | Wordle, Word Cookies |
| Logic puzzle | Deduce solution | Sudoku, Nonograms |
| Spatial puzzle | Fit shapes | Tetris, Block Puzzle |

## Performance

- Puzzle games are rarely GPU-bound — focus on clean input and smooth animations
- Pool popup effects and particles
- Pre-calculate valid moves for hint system at level start
- Save progress per-level to avoid data loss on app kill
