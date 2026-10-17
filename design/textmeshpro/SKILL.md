---
name: textmeshpro
description: "TextMeshPro text rendering — font asset creation, material presets, rich text tags, dynamic font fallback, sprite assets in text. Use for all text rendering in Unity."
globs: ["**/TMP_*.cs", "**/TextMesh*.cs", "**/*Text*.cs", "**/*.asset"]
---

# TextMeshPro — Advanced Text Rendering for Unity

TextMeshPro (TMP) is Unity's standard text solution, replacing the legacy Text component. It uses Signed Distance Field (SDF) rendering for resolution-independent, crisp text with support for rich text, outlines, shadows, and inline sprites.

## Component Types

| Component | Use Case | Namespace |
|-----------|----------|-----------|
| `TextMeshProUGUI` | Canvas UI text (most common) | `TMPro` |
| `TextMeshPro` | World-space 3D text (signs, name plates) | `TMPro` |

```csharp
using TMPro;

[SerializeField] private TextMeshProUGUI _uiText;     // Canvas text
[SerializeField] private TextMeshPro _worldText;       // 3D world text
```

## Font Asset Creation

Font assets are created from TTF/OTF font files via the Font Asset Creator window.

### Steps

1. **Window > TextMeshPro > Font Asset Creator**
2. Set **Source Font File** to your TTF/OTF font
3. Configure settings:
   - **Sampling Point Size**: Auto or specific (e.g., 64)
   - **Padding**: 5-9 (higher = better outlines/shadows but larger atlas)
   - **Packing Method**: Optimum
   - **Atlas Resolution**: 512x512 for small character sets, 2048x2048+ for CJK
   - **Character Set**: ASCII for English, Unicode Range for specific sets, Custom Characters for exact glyphs
   - **Render Mode**: SDFAA (default, best quality)
4. Click **Generate Font Atlas**, then **Save**

### SDF Rendering Modes

| Mode | Quality | Use Case |
|------|---------|----------|
| SDFAA | Best | Default for most fonts |
| SDF | Good | Slightly faster rendering |
| SDFAA_HINTED | Best + hinting | Small text sizes, pixel-perfect |
| Raster | Bitmap | Pixel art fonts only |

## Material Presets

Material presets add visual effects (outline, shadow, glow) without modifying the base font asset.

### Creating a Material Preset

1. Select the font asset in Project window
2. In Inspector, click the material field to see the base material
3. Right-click the font asset > **Create > Material Preset**
4. Adjust properties on the new material:
   - **Face**: Color, softness, dilate
   - **Outline**: Color, thickness
   - **Underlay** (shadow): Color, offset, dilate, softness
   - **Lighting**: Bevel for 3D effect
   - **Glow**: Inner/outer glow

### Applying Material Presets in Code

```csharp
[SerializeField] private Material _damageMaterial;  // Red outline preset
[SerializeField] private Material _defaultMaterial;

public void ShowDamageText()
{
    _uiText.fontSharedMaterial = _damageMaterial;
}

public void ResetTextAppearance()
{
    _uiText.fontSharedMaterial = _defaultMaterial;
}
```

**Important**: Use `fontSharedMaterial` (shared, no allocation) instead of `fontMaterial` (creates instance, allocates).

## Rich Text Tags

TMP supports extensive rich text markup within text strings.

### Basic Formatting

```
<b>Bold text</b>
<i>Italic text</i>
<u>Underline</u>
<s>Strikethrough</s>
<mark=#FFFF0044>Highlighted</mark>
<sup>Superscript</sup>
<sub>Subscript</sub>
```

### Color and Size

```
<color=#FF0000>Red</color>
<color="red">Named red</color>
<color=#FF000088>Semi-transparent red</color>
<size=24>Larger text</size>
<size=+10>Relative larger</size>
<size=-4>Relative smaller</size>
```

### Alignment and Spacing

```
<align="center">Centered text</align>
<align="left">Left aligned</align>
<align="right">Right aligned</align>
<cspace=5>Character spacing</cspace>
<line-height=150%>Taller lines</line-height>
<indent=20>Indented text</indent>
<margin=10>Text with margin</margin>
<mspace=0.5em>Monospaced</mspace>
```

### Inline Sprites

```
Coins: <sprite name="coin"> x 100
Health: <sprite name="heart" tint=1>
<sprite index=0>  (by index in sprite asset)
```

### Links

```
Click <link="store">here</link> to open the store.
Visit <link="https://example.com">our site</link>.
```

### Other Tags

```
<font="OtherFontAsset">Different font</font>
<gradient="GradientPreset">Gradient text</gradient>
<rotate=15>Rotated</rotate>
<voffset=10>Vertical offset</voffset>
<width=50%>Constrained width</width>
<nobr>No line break here</nobr>
<page>Page break (for multi-page)</page>
```

## Dynamic Font Fallback

Chain font assets so missing characters fall through to other fonts. Essential for multi-language support.

### Setup

1. Select your primary font asset
2. In Inspector, expand **Fallback Font Asset List**
3. Add fallback fonts in priority order:
   - Primary: LatinFont (English, European)
   - Fallback 1: CJKFont (Chinese, Japanese, Korean)
   - Fallback 2: ArabicFont
   - Fallback 3: EmojiFont

TMP automatically searches fallback fonts when a glyph is not found in the primary font.

### Global Fallback (TMP Settings)

1. **Edit > Project Settings > TextMesh Pro > Settings**
2. Add fonts to **Fallback Font Assets** list
3. These apply to ALL TMP text components as a last resort

## Sprite Assets

Embed icons, emojis, or custom images inline with text.

### Creating a Sprite Asset

1. Create a sprite sheet texture (atlas of icons)
2. **Right-click texture > Create > TextMeshPro > Sprite Asset**
3. Define sprite regions in the Sprite Asset inspector
4. Name each sprite for easy reference

### Usage

```csharp
// In text strings
_uiText.text = "Gold: <sprite name=\"coin\"> 500";

// With tinting (inherits text color)
_uiText.text = "<sprite name=\"heart\" tint=1>";
```

## Code Access Patterns

### Setting Text Efficiently

```csharp
[SerializeField] private TextMeshProUGUI _scoreText;
[SerializeField] private TextMeshProUGUI _timerText;

// GOOD — SetText with format args avoids string allocation
_scoreText.SetText("Score: {0}", score);
_timerText.SetText("{0}:{1:00}", minutes, seconds);

// GOOD — SetText with float formatting
_scoreText.SetText("DPS: {0:2}", damagePerSecond); // 2 decimal places

// OK for infrequent updates
_scoreText.text = $"Score: {score}";

// BAD for frequent updates — allocates every frame
void Update()
{
    _scoreText.text = "FPS: " + (1f / Time.deltaTime).ToString("F1"); // Allocates
}

// GOOD for frequent updates
void Update()
{
    _scoreText.SetText("FPS: {0:1}", 1f / Time.deltaTime); // Zero alloc
}
```

### SetText Format Specifiers

```csharp
_text.SetText("{0}", intValue);          // Integer
_text.SetText("{0:1}", floatValue);      // 1 decimal place
_text.SetText("{0:2}", floatValue);      // 2 decimal places
_text.SetText("{0:00}", intValue);       // Zero-padded (use string format for this)
```

Note: `SetText` format is NOT the same as `string.Format`. The number after `:` is decimal places, not format specifier.

### Accessing Text Properties

```csharp
// Font and style
_text.font = myFontAsset;
_text.fontSize = 36;
_text.fontStyle = FontStyles.Bold | FontStyles.Italic;
_text.characterSpacing = 2f;
_text.lineSpacing = 10f;
_text.wordSpacing = 5f;

// Color
_text.color = Color.white;
_text.faceColor = new Color32(255, 255, 255, 200); // Face color with alpha
_text.outlineColor = Color.black;
_text.outlineWidth = 0.2f;

// Alignment
_text.alignment = TextAlignmentOptions.Center;
_text.alignment = TextAlignmentOptions.TopLeft;

// Overflow
_text.overflowMode = TextOverflowModes.Ellipsis;
_text.overflowMode = TextOverflowModes.Truncate;
_text.enableWordWrapping = true;

// Sizing
_text.enableAutoSizing = true;
_text.fontSizeMin = 12;
_text.fontSizeMax = 48;
```

## Link Handling

Detect and respond to clicks on `<link>` tags.

```csharp
using TMPro;
using UnityEngine;
using UnityEngine.EventSystems;

public class LinkHandler : MonoBehaviour, IPointerClickHandler
{
    [SerializeField] private TextMeshProUGUI _text;

    public void OnPointerClick(PointerEventData eventData)
    {
        int linkIndex = TMP_TextUtilities.FindIntersectingLink(
            _text, eventData.position, null // null = main camera
        );

        if (linkIndex >= 0)
        {
            TMP_LinkInfo linkInfo = _text.textInfo.linkInfo[linkIndex];
            string linkId = linkInfo.GetLinkID();
            string linkText = linkInfo.GetLinkText();

            Debug.Log($"Clicked link: {linkId} ({linkText})");
            HandleLink(linkId);
        }
    }

    private void HandleLink(string linkId)
    {
        switch (linkId)
        {
            case "store":
                OpenStore();
                break;
            default:
                if (linkId.StartsWith("http"))
                    Application.OpenURL(linkId);
                break;
        }
    }
}
```

## Performance Best Practices

### Disable Raycast Target

Every TMP component with Raycast Target enabled participates in UI raycasting. Disable it when the text is not interactive.

```csharp
// In inspector: uncheck "Raycast Target" on non-interactive text
// Or in code:
_text.raycastTarget = false;
```

### Canvas Optimization

- Place frequently updating text on a **separate Canvas** to avoid rebuilding the entire UI batch
- Use `Canvas.willRenderCanvases` callback sparingly for text updates
- Group static text together, dynamic text on a different Canvas

### Avoid Per-Frame text Property Assignment

```csharp
// BAD — triggers mesh rebuild every frame even if value has not changed
void Update()
{
    _scoreText.text = $"Score: {_score}";
}

// GOOD — only update when value changes
private int _lastDisplayedScore = -1;
void Update()
{
    if (_score != _lastDisplayedScore)
    {
        _lastDisplayedScore = _score;
        _scoreText.SetText("Score: {0}", _score);
    }
}
```

### Text Info Access

```csharp
// Access character, word, and line info after text is set
_text.ForceMeshUpdate(); // Ensure text info is current

TMP_TextInfo textInfo = _text.textInfo;
int charCount = textInfo.characterCount;
int wordCount = textInfo.wordCount;
int lineCount = textInfo.lineCount;

// Access individual character info
TMP_CharacterInfo charInfo = textInfo.characterInfo[0];
Vector3 bottomLeft = charInfo.bottomLeft;
Vector3 topRight = charInfo.topRight;
bool isVisible = charInfo.isVisible;
```

## Localization Considerations

- Use string keys and a localization system — never hardcode user-facing text
- Set up font fallback chains to cover all target languages
- CJK fonts need large atlases (4096x4096 or dynamic atlas)
- Right-to-left languages (Arabic, Hebrew) require TMP's RTL support enabled
- Test overflow and auto-sizing with the longest translation strings
- Some languages expand 30-50% compared to English — design UI with flexible layouts

## Common Issues

### Missing Characters (Rectangles)

- Character not in font atlas. Add to character set or use fallback fonts.

### Blurry Text

- Atlas resolution too low. Regenerate with higher resolution.
- Padding too low for the outline/shadow being used.
- Canvas Scaler reference resolution mismatch.

### Text Not Updating

- Call `ForceMeshUpdate()` if reading textInfo immediately after setting text.
- Check that the component is enabled and the Canvas is active.
