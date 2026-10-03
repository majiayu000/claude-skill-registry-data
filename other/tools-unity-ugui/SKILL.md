---
name: tools-unity-ugui
description: Unity UI patterns including Canvas optimization, list virtualization, and mobile-friendly UI.
---

# Unity uGUI

## Overview

Unity's uGUI system provides flexible UI but requires careful optimization to maintain performance, especially on mobile devices.

## When to Use

- Game menus and HUD
- Inventory and shop screens
- Scrolling lists
- Modal dialogs
- Health bars and floating text

## Canvas Optimization

### Canvas Splitting

```csharp
// WRONG: Everything on one canvas
// Every change causes full rebuild

// RIGHT: Split by update frequency
public class CanvasOrganizer : MonoBehaviour
{
    [Header("Static UI - Never changes")]
    [SerializeField] private Canvas _staticCanvas;  // Background, frames
    
    [Header("Semi-Dynamic - Changes occasionally")]
    [SerializeField] private Canvas _dynamicCanvas; // Buttons, icons
    
    [Header("Highly Dynamic - Changes every frame")]
    [SerializeField] private Canvas _hudCanvas;     // Health, mana, timers
    
    private void Start()
    {
        // Static canvas doesn't need updates
        _staticCanvas.GetComponent<GraphicRaycaster>().enabled = false;
    }
}
```

### Canvas Group for Visibility

```csharp
public class UIPanel : MonoBehaviour
{
    private CanvasGroup _canvasGroup;
    
    private void Awake()
    {
        _canvasGroup = GetComponent<CanvasGroup>();
    }
    
    // BETTER than SetActive - doesn't rebuild canvas
    public void Show()
    {
        _canvasGroup.alpha = 1f;
        _canvasGroup.interactable = true;
        _canvasGroup.blocksRaycasts = true;
    }
    
    public void Hide()
    {
        _canvasGroup.alpha = 0f;
        _canvasGroup.interactable = false;
        _canvasGroup.blocksRaycasts = false;
    }
    
    public async UniTask FadeIn(float duration)
    {
        _canvasGroup.interactable = true;
        _canvasGroup.blocksRaycasts = true;
        
        float elapsed = 0;
        while (elapsed < duration)
        {
            elapsed += Time.unscaledDeltaTime;
            _canvasGroup.alpha = elapsed / duration;
            await UniTask.Yield();
        }
        _canvasGroup.alpha = 1f;
    }
}
```

### Raycast Optimization

```csharp
public class RaycastOptimizer : MonoBehaviour
{
    // Disable Raycast Target on non-interactive elements
    public void OptimizeHierarchy()
    {
        var graphics = GetComponentsInChildren<Graphic>(true);
        
        foreach (var graphic in graphics)
        {
            // Only enable on actually clickable items
            bool isInteractive = 
                graphic.GetComponent<Button>() != null ||
                graphic.GetComponent<Toggle>() != null ||
                graphic.GetComponent<Slider>() != null ||
                graphic.GetComponent<ScrollRect>() != null;
            
            graphic.raycastTarget = isInteractive;
        }
    }
}
```

## List Virtualization

### Simple Virtual List

```csharp
public class VirtualizedList<TData, TView> : MonoBehaviour 
    where TView : Component
{
    [SerializeField] private ScrollRect _scrollRect;
    [SerializeField] private RectTransform _content;
    [SerializeField] private TView _itemPrefab;
    [SerializeField] private float _itemHeight = 100f;
    
    private readonly List<TView> _visibleItems = new();
    private readonly Queue<TView> _recycledItems = new();
    private IList<TData> _dataSource;
    private Action<TView, TData> _bindAction;
    
    private int _firstVisibleIndex;
    private float _viewportHeight;
    
    public void Initialize(IList<TData> data, Action<TView, TData> bindAction)
    {
        _dataSource = data;
        _bindAction = bindAction;
        
        // Set content height
        _content.sizeDelta = new Vector2(
            _content.sizeDelta.x,
            data.Count * _itemHeight
        );
        
        _viewportHeight = _scrollRect.viewport.rect.height;
        
        _scrollRect.onValueChanged.AddListener(OnScroll);
        
        RefreshVisibleItems();
    }
    
    private void OnScroll(Vector2 _)
    {
        RefreshVisibleItems();
    }
    
    private void RefreshVisibleItems()
    {
        float scrollY = _content.anchoredPosition.y;
        
        int newFirstVisible = Mathf.Max(0, Mathf.FloorToInt(scrollY / _itemHeight));
        int visibleCount = Mathf.CeilToInt(_viewportHeight / _itemHeight) + 2;
        int lastVisible = Mathf.Min(newFirstVisible + visibleCount, _dataSource.Count);
        
        // Recycle items that scrolled out
        for (int i = _visibleItems.Count - 1; i >= 0; i--)
        {
            var item = _visibleItems[i];
            int itemIndex = GetItemIndex(item);
            
            if (itemIndex < newFirstVisible || itemIndex >= lastVisible)
            {
                RecycleItem(item);
                _visibleItems.RemoveAt(i);
            }
        }
        
        // Create/reuse items that scrolled in
        for (int i = newFirstVisible; i < lastVisible; i++)
        {
            if (!IsItemVisible(i))
            {
                var item = GetOrCreateItem();
                PositionItem(item, i);
                _bindAction(item, _dataSource[i]);
                _visibleItems.Add(item);
            }
        }
        
        _firstVisibleIndex = newFirstVisible;
    }
    
    private TView GetOrCreateItem()
    {
        if (_recycledItems.Count > 0)
        {
            var item = _recycledItems.Dequeue();
            item.gameObject.SetActive(true);
            return item;
        }
        
        return Instantiate(_itemPrefab, _content);
    }
    
    private void RecycleItem(TView item)
    {
        item.gameObject.SetActive(false);
        _recycledItems.Enqueue(item);
    }
    
    private void PositionItem(TView item, int index)
    {
        var rect = item.GetComponent<RectTransform>();
        rect.anchoredPosition = new Vector2(0, -index * _itemHeight);
        item.gameObject.name = $"Item_{index}";
    }
    
    private bool IsItemVisible(int index)
    {
        return _visibleItems.Any(v => GetItemIndex(v) == index);
    }
    
    private int GetItemIndex(TView item)
    {
        var rect = item.GetComponent<RectTransform>();
        return Mathf.RoundToInt(-rect.anchoredPosition.y / _itemHeight);
    }
}
```

### Usage Example

```csharp
public class InventoryScreen : MonoBehaviour
{
    [SerializeField] private VirtualizedList<ItemData, InventorySlot> _list;
    
    public void ShowInventory(List<ItemData> items)
    {
        _list.Initialize(items, BindSlot);
    }
    
    private void BindSlot(InventorySlot slot, ItemData data)
    {
        slot.SetIcon(data.Icon);
        slot.SetName(data.Name);
        slot.SetQuantity(data.Quantity);
        slot.OnClick = () => OnItemClicked(data);
    }
}
```

## Safe Text Updates

### Cached Text Component

```csharp
public class SafeText : MonoBehaviour
{
    private TMP_Text _text;
    private string _lastValue;
    
    private void Awake()
    {
        _text = GetComponent<TMP_Text>();
        _lastValue = _text.text;
    }
    
    // Only update if value changed
    public void SetText(string value)
    {
        if (_lastValue != value)
        {
            _text.text = value;
            _lastValue = value;
        }
    }
    
    public void SetTextFormat(string format, params object[] args)
    {
        var value = string.Format(format, args);
        SetText(value);
    }
}
```

### Zero-Allocation Number Display

```csharp
public class NumberDisplay : MonoBehaviour
{
    private TMP_Text _text;
    private int _lastValue = int.MinValue;
    private readonly char[] _buffer = new char[16];
    
    private void Awake()
    {
        _text = GetComponent<TMP_Text>();
    }
    
    public void SetValue(int value)
    {
        if (value == _lastValue) return;
        _lastValue = value;
        
        // Zero-allocation int to string
        int length = IntToChars(value, _buffer);
        _text.SetCharArray(_buffer, 0, length);
    }
    
    private int IntToChars(int value, char[] buffer)
    {
        if (value == 0)
        {
            buffer[0] = '0';
            return 1;
        }
        
        bool negative = value < 0;
        if (negative) value = -value;
        
        int index = buffer.Length;
        
        while (value > 0)
        {
            buffer[--index] = (char)('0' + value % 10);
            value /= 10;
        }
        
        if (negative)
        {
            buffer[--index] = '-';
        }
        
        int length = buffer.Length - index;
        Array.Copy(buffer, index, buffer, 0, length);
        return length;
    }
}
```

## Layout Optimization

### Manual Layout

```csharp
public class OptimizedGrid : MonoBehaviour
{
    [SerializeField] private int _columns = 4;
    [SerializeField] private float _cellWidth = 100f;
    [SerializeField] private float _cellHeight = 100f;
    [SerializeField] private float _spacing = 10f;
    
    private RectTransform _rect;
    
    private void Awake()
    {
        _rect = GetComponent<RectTransform>();
    }
    
    // Call once after adding/removing children
    public void RefreshLayout()
    {
        int index = 0;
        
        foreach (Transform child in transform)
        {
            if (!child.gameObject.activeSelf) continue;
            
            int row = index / _columns;
            int col = index % _columns;
            
            var childRect = child.GetComponent<RectTransform>();
            childRect.anchoredPosition = new Vector2(
                col * (_cellWidth + _spacing),
                -row * (_cellHeight + _spacing)
            );
            childRect.sizeDelta = new Vector2(_cellWidth, _cellHeight);
            
            index++;
        }
        
        // Update content size
        int totalRows = Mathf.CeilToInt((float)index / _columns);
        _rect.sizeDelta = new Vector2(
            _rect.sizeDelta.x,
            totalRows * (_cellHeight + _spacing)
        );
    }
}
```

### Disable Auto Layout

```csharp
public class LayoutDisabler : MonoBehaviour
{
    private LayoutGroup _layout;
    private ContentSizeFitter _sizeFitter;
    
    private void Start()
    {
        _layout = GetComponent<LayoutGroup>();
        _sizeFitter = GetComponent<ContentSizeFitter>();
        
        // Disable after initial layout
        StartCoroutine(DisableAfterFrame());
    }
    
    private IEnumerator DisableAfterFrame()
    {
        yield return null;
        
        if (_sizeFitter != null)
            _sizeFitter.enabled = false;
            
        if (_layout != null)
            _layout.enabled = false;
    }
    
    public void ForceRefresh()
    {
        if (_layout != null)
        {
            _layout.enabled = true;
            LayoutRebuilder.ForceRebuildLayoutImmediate(GetComponent<RectTransform>());
            _layout.enabled = false;
        }
    }
}
```

## Modal Dialog System

### Dialog Manager

```csharp
public class DialogManager : MonoBehaviour
{
    public static DialogManager Instance { get; private set; }
    
    [SerializeField] private Canvas _dialogCanvas;
    [SerializeField] private GameObject _backdrop;
    
    private readonly Stack<UIPanel> _dialogStack = new();
    
    private void Awake()
    {
        Instance = this;
    }
    
    public async UniTask<T> ShowDialog<T>(UIPanel dialogPrefab) where T : UIPanel
    {
        var dialog = Instantiate(dialogPrefab, _dialogCanvas.transform);
        _dialogStack.Push(dialog);
        
        UpdateBackdrop();
        await dialog.FadeIn(0.2f);
        
        return (T)dialog;
    }
    
    public async UniTask CloseTopDialog()
    {
        if (_dialogStack.Count == 0) return;
        
        var dialog = _dialogStack.Pop();
        await dialog.FadeOut(0.15f);
        Destroy(dialog.gameObject);
        
        UpdateBackdrop();
    }
    
    public async UniTask CloseAllDialogs()
    {
        while (_dialogStack.Count > 0)
        {
            var dialog = _dialogStack.Pop();
            Destroy(dialog.gameObject);
        }
        
        UpdateBackdrop();
    }
    
    private void UpdateBackdrop()
    {
        _backdrop.SetActive(_dialogStack.Count > 0);
    }
}
```

## Best Practices

1. **Split canvases** by update frequency
2. **Disable Raycast Target** on non-interactive elements
3. **Use CanvasGroup** for visibility, not SetActive
4. **Virtualize long lists** - Only render visible items
5. **Avoid Layout Groups** in dynamic content
6. **Cache text components** and avoid redundant updates
7. **Pool UI elements** - Don't instantiate frequently
8. **Use sprite atlases** for UI images
9. **Avoid transparency overdraw** - Minimize overlapping alpha
10. **Profile with Frame Debugger** - Check batch counts

## Troubleshooting

| Issue | Solution |
|-------|----------|
| High SetPass calls | Use sprite atlases |
| Canvas rebuild every frame | Split canvases, check hierarchy |
| Scroll stuttering | Virtualize list |
| Touch unresponsive | Check Raycast Target, Canvas order |
| Layout jitter | Disable auto layout, use manual |
| Memory from UI | Pool elements, unload unused atlases |
