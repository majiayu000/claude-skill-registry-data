---
name: unity
description: Unity Engine game development. Use for Unity projects, C# scripting, scene setup, GameObject systems, 2D/3D development, physics, animation, UI, shaders, VR/AR, or any Unity-specific questions.
---

# Unity Engine Development Skill

Comprehensive assistance with Unity game development, covering C# scripting, scene management, physics, rendering, animation, UI, and platform-specific features.

## When to Use This Skill

This skill should be triggered when working with:
- Unity Engine projects (2D/3D game development)
- C# scripting in Unity (MonoBehaviour, Coroutines, ScriptableObjects)
- Scene setup and GameObject hierarchy management
- Physics systems (Rigidbody, Colliders, Joints, Character Controllers)
- Animation and Animator systems (Animation Clips, Blend Trees, State Machines)
- Rendering pipelines (Built-in, URP, HDRP) and shaders (ShaderLab, Shader Graph)
- UI development (UI Toolkit, UGUI, Canvas, TextMeshPro)
- XR/VR/AR development (XR Interaction Toolkit)
- Asset management and optimization
- Platform-specific builds (iOS, Android, WebGL, PC/Console)
- Editor extensions and custom tools

## Unity-MCP Integration

**This skill can be combined with Unity-MCP for live Unity Editor control!**

**Unity Skill (Documentation)** + **Unity-MCP (Actions)** = Complete AI-powered development

- **Unity Skill**: Provides documentation, patterns, and best practices (3,367 pages)
- **Unity-MCP**: Executes code, creates assets, and automates workflows in your Unity Editor
- **Together**: Learn patterns from docs → Apply instantly to your project

**See [UNITY_MCP_INTEGRATION.md](UNITY_MCP_INTEGRATION.md) for complete setup guide.**

## Quick Reference

### Essential Unity Patterns

#### 1. MonoBehaviour Lifecycle
```csharp
using UnityEngine;

public class GameController : MonoBehaviour
{
    // Called once when script instance is being loaded
    void Awake()
    {
        // Initialize references and setup before Start()
    }

    // Called once before first frame update
    void Start()
    {
        // Initialization logic that depends on other objects
    }

    // Called every frame
    void Update()
    {
        // Input handling and frame-based logic
    }

    // Called at fixed time intervals (physics)
    void FixedUpdate()
    {
        // Physics-related code (Rigidbody forces, etc.)
    }

    // Called after all Update functions
    void LateUpdate()
    {
        // Camera following, post-processing logic
    }

    // Called when object becomes enabled/active
    void OnEnable() { }

    // Called when object becomes disabled/inactive
    void OnDisable() { }

    // Called when MonoBehaviour will be destroyed
    void OnDestroy()
    {
        // Cleanup logic (unsubscribe events, etc.)
    }
}
```

#### 2. Coroutines for Asynchronous Operations
```csharp
using System.Collections;
using UnityEngine;

public class CoroutineExample : MonoBehaviour
{
    void Start()
    {
        StartCoroutine(DelayedAction());
        StartCoroutine(FadeOut(GetComponent<SpriteRenderer>(), 2.0f));
    }

    // Simple delay
    IEnumerator DelayedAction()
    {
        yield return new WaitForSeconds(2.0f);
        Debug.Log("Executed after 2 seconds");
    }

    // Fade out over time
    IEnumerator FadeOut(SpriteRenderer sprite, float duration)
    {
        float elapsed = 0f;
        Color startColor = sprite.color;

        while (elapsed < duration)
        {
            elapsed += Time.deltaTime;
            float alpha = Mathf.Lerp(1f, 0f, elapsed / duration);
            sprite.color = new Color(startColor.r, startColor.g, startColor.b, alpha);
            yield return null; // Wait for next frame
        }
    }
}
```

#### 3. ScriptableObjects for Data Management
```csharp
using UnityEngine;

[CreateAssetMenu(fileName = "New Weapon", menuName = "Game/Weapon")]
public class WeaponData : ScriptableObject
{
    public string weaponName;
    public int damage;
    public float fireRate;
    public Sprite icon;
    public GameObject projectilePrefab;
}

// Usage in MonoBehaviour
public class WeaponSystem : MonoBehaviour
{
    [SerializeField] private WeaponData currentWeapon;

    public void Fire()
    {
        if (currentWeapon != null)
        {
            GameObject projectile = Instantiate(
                currentWeapon.projectilePrefab,
                transform.position,
                transform.rotation
            );
        }
    }
}
```

#### 4. Physics-Based Movement
```csharp
using UnityEngine;

[RequireComponent(typeof(Rigidbody))]
public class PlayerMovement : MonoBehaviour
{
    [SerializeField] private float moveSpeed = 5f;
    [SerializeField] private float jumpForce = 10f;
    [SerializeField] private LayerMask groundLayer;

    private Rigidbody rb;
    private bool isGrounded;

    void Awake()
    {
        rb = GetComponent<Rigidbody>();
    }

    void FixedUpdate()
    {
        // Check if grounded
        isGrounded = Physics.Raycast(
            transform.position,
            Vector3.down,
            1.1f,
            groundLayer
        );

        // Movement
        float horizontal = Input.GetAxis("Horizontal");
        float vertical = Input.GetAxis("Vertical");

        Vector3 movement = new Vector3(horizontal, 0f, vertical);
        rb.AddForce(movement * moveSpeed);
    }

    void Update()
    {
        // Jump
        if (Input.GetButtonDown("Jump") && isGrounded)
        {
            rb.AddForce(Vector3.up * jumpForce, ForceMode.Impulse);
        }
    }
}
```

#### 5. Object Pooling Pattern
```csharp
using System.Collections.Generic;
using UnityEngine;

public class ObjectPool : MonoBehaviour
{
    [SerializeField] private GameObject prefab;
    [SerializeField] private int poolSize = 20;

    private Queue<GameObject> pool = new Queue<GameObject>();

    void Start()
    {
        for (int i = 0; i < poolSize; i++)
        {
            GameObject obj = Instantiate(prefab);
            obj.SetActive(false);
            pool.Enqueue(obj);
        }
    }

    public GameObject GetObject()
    {
        if (pool.Count > 0)
        {
            GameObject obj = pool.Dequeue();
            obj.SetActive(true);
            return obj;
        }
        else
        {
            // Expand pool if needed
            GameObject obj = Instantiate(prefab);
            return obj;
        }
    }

    public void ReturnObject(GameObject obj)
    {
        obj.SetActive(false);
        pool.Enqueue(obj);
    }
}
```

#### 6. Singleton Pattern
```csharp
using UnityEngine;

public class GameManager : MonoBehaviour
{
    private static GameManager _instance;

    public static GameManager Instance
    {
        get
        {
            if (_instance == null)
            {
                _instance = FindObjectOfType<GameManager>();

                if (_instance == null)
                {
                    GameObject go = new GameObject("GameManager");
                    _instance = go.AddComponent<GameManager>();
                }
            }
            return _instance;
        }
    }

    void Awake()
    {
        if (_instance != null && _instance != this)
        {
            Destroy(gameObject);
            return;
        }

        _instance = this;
        DontDestroyOnLoad(gameObject);
    }
}
```

#### 7. Event System Pattern
```csharp
using System;
using UnityEngine;

public class EventManager : MonoBehaviour
{
    public static event Action OnGameStart;
    public static event Action<int> OnScoreChanged;
    public static event Action OnGameOver;

    public static void TriggerGameStart()
    {
        OnGameStart?.Invoke();
    }

    public static void TriggerScoreChanged(int newScore)
    {
        OnScoreChanged?.Invoke(newScore);
    }

    public static void TriggerGameOver()
    {
        OnGameOver?.Invoke();
    }
}

// Usage: Subscribe and unsubscribe
public class UIController : MonoBehaviour
{
    void OnEnable()
    {
        EventManager.OnScoreChanged += UpdateScoreDisplay;
        EventManager.OnGameOver += ShowGameOverScreen;
    }

    void OnDisable()
    {
        EventManager.OnScoreChanged -= UpdateScoreDisplay;
        EventManager.OnGameOver -= ShowGameOverScreen;
    }

    void UpdateScoreDisplay(int score)
    {
        // Update UI
    }

    void ShowGameOverScreen()
    {
        // Show game over
    }
}
```

#### 8. 2D Character Controller
```csharp
using UnityEngine;

[RequireComponent(typeof(Rigidbody2D))]
public class CharacterController2D : MonoBehaviour
{
    [SerializeField] private float moveSpeed = 5f;
    [SerializeField] private float jumpForce = 10f;
    [SerializeField] private Transform groundCheck;
    [SerializeField] private LayerMask groundLayer;

    private Rigidbody2D rb;
    private bool isGrounded;
    private bool facingRight = true;

    void Awake()
    {
        rb = GetComponent<Rigidbody2D>();
    }

    void Update()
    {
        // Ground check
        isGrounded = Physics2D.OverlapCircle(
            groundCheck.position,
            0.2f,
            groundLayer
        );

        // Movement input
        float moveInput = Input.GetAxis("Horizontal");
        rb.velocity = new Vector2(moveInput * moveSpeed, rb.velocity.y);

        // Flip character
        if (moveInput > 0 && !facingRight)
            Flip();
        else if (moveInput < 0 && facingRight)
            Flip();

        // Jump
        if (Input.GetButtonDown("Jump") && isGrounded)
        {
            rb.velocity = new Vector2(rb.velocity.x, jumpForce);
        }
    }

    void Flip()
    {
        facingRight = !facingRight;
        Vector3 scale = transform.localScale;
        scale.x *= -1;
        transform.localScale = scale;
    }
}
```

#### 9. UI Toolkit (Runtime UI)
```csharp
using UnityEngine;
using UnityEngine.UIElements;

public class UIController : MonoBehaviour
{
    private UIDocument uiDocument;
    private Label scoreLabel;
    private Button startButton;

    void OnEnable()
    {
        uiDocument = GetComponent<UIDocument>();
        var root = uiDocument.rootVisualElement;

        // Query elements
        scoreLabel = root.Q<Label>("score-label");
        startButton = root.Q<Button>("start-button");

        // Register callbacks
        startButton.clicked += OnStartButtonClicked;
    }

    void OnDisable()
    {
        startButton.clicked -= OnStartButtonClicked;
    }

    void OnStartButtonClicked()
    {
        Debug.Log("Game started!");
    }

    public void UpdateScore(int score)
    {
        scoreLabel.text = $"Score: {score}";
    }
}
```

#### 10. Basic Shader (ShaderLab)
```shaderlab
Shader "Custom/SimpleTextureShader"
{
    Properties
    {
        _MainTex ("Texture", 2D) = "white" {}
        _Color ("Tint Color", Color) = (1,1,1,1)
        _Brightness ("Brightness", Range(0, 2)) = 1
    }

    SubShader
    {
        Tags { "RenderType"="Opaque" }
        LOD 100

        Pass
        {
            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag
            #include "UnityCG.cginc"

            struct appdata
            {
                float4 vertex : POSITION;
                float2 uv : TEXCOORD0;
            };

            struct v2f
            {
                float2 uv : TEXCOORD0;
                float4 vertex : SV_POSITION;
            };

            sampler2D _MainTex;
            float4 _MainTex_ST;
            float4 _Color;
            float _Brightness;

            v2f vert (appdata v)
            {
                v2f o;
                o.vertex = UnityObjectToClipPos(v.vertex);
                o.uv = TRANSFORM_TEX(v.uv, _MainTex);
                return o;
            }

            fixed4 frag (v2f i) : SV_Target
            {
                fixed4 col = tex2D(_MainTex, i.uv);
                col *= _Color * _Brightness;
                return col;
            }
            ENDCG
        }
    }
}
```

## Reference Files

This skill includes comprehensive documentation organized by topic in `references/`:

### Core Topics
- **[getting_started.md](references/getting_started.md)** - Installation, project setup, and Unity basics (4 pages)
- **[scripting.md](references/scripting.md)** - C# scripting, MonoBehaviour, coroutines, assemblies (8 pages)
- **[scene_management.md](references/scene_management.md)** - Scene creation, GameObjects, Transforms, Prefabs (38 pages)

### 2D/3D Development
- **[2d.md](references/2d.md)** - Sprites, Tilemaps, 2D physics, 2D animation (85 pages)
- **[3d.md](references/3d.md)** - 3D meshes, terrain, ProBuilder, lighting (30 pages)

### Systems
- **[physics.md](references/physics.md)** - Rigidbody, Colliders, Joints, Character Controllers (114 pages)
- **[animation.md](references/animation.md)** - Animation clips, Animator, Timeline, Blend Trees (11 pages)
- **[audio.md](references/audio.md)** - AudioSource, AudioMixer, spatial audio (32 pages)

### Rendering & Graphics
- **[rendering.md](references/rendering.md)** - Cameras, lighting, post-processing, VFX (45 pages)
- **[shaders.md](references/shaders.md)** - ShaderLab, Shader Graph, URP, HDRP, materials (631 pages)

### UI & Interface
- **[ui.md](references/ui.md)** - UI Toolkit, UGUI, Canvas, TextMeshPro (16 pages)

### Advanced Topics
- **[xr.md](references/xr.md)** - VR/AR development, XR Interaction Toolkit (238 pages)
- **[editor.md](references/editor.md)** - Custom editors, EditorWindows, MenuItem (8 pages)
- **[optimization.md](references/optimization.md)** - Profiling, memory management, best practices (34 pages)

### Platform & Services
- **[platform.md](references/platform.md)** - iOS, Android, WebGL, build settings (16 pages)
- **[assets.md](references/assets.md)** - Asset workflow, AssetBundles, Addressables (27 pages)
- **[networking.md](references/networking.md)** - Multiplayer, Netcode, networking systems (19 pages)
- **[services.md](references/services.md)** - Unity Services, Analytics, Cloud Build (9 pages)

### Additional Resources
- **[other.md](references/other.md)** - Miscellaneous topics and advanced features (1,707 pages)
- **[index.md](references/index.md)** - Complete documentation index

**Total Documentation:** 3,367 pages from official Unity Manual and Scripting API

Use the `view` tool to read specific reference files when detailed information is needed.

## Working with This Skill

### For Beginners
1. Start with [references/getting_started.md](references/getting_started.md) for Unity installation and basics
2. Review MonoBehaviour lifecycle pattern above
3. Learn GameObject and Transform basics in [references/scene_management.md](references/scene_management.md)
4. Explore simple scripting examples in [references/scripting.md](references/scripting.md)

### For Intermediate Developers
1. Study physics systems in [references/physics.md](references/physics.md)
2. Implement animation systems using [references/animation.md](references/animation.md)
3. Build UI with [references/ui.md](references/ui.md)
4. Optimize performance with [references/optimization.md](references/optimization.md)

### For Advanced Developers
1. Create custom shaders: [references/shaders.md](references/shaders.md)
2. Build custom editor tools: [references/editor.md](references/editor.md)
3. Develop VR/AR experiences: [references/xr.md](references/xr.md)
4. Optimize for specific platforms: [references/platform.md](references/platform.md)

### For Specific Tasks
- **2D game:** Check [references/2d.md](references/2d.md) for Sprites, Tilemaps, 2D Physics
- **3D game:** Review [references/3d.md](references/3d.md) and [references/rendering.md](references/rendering.md)
- **Mobile game:** See [references/platform.md](references/platform.md) for iOS/Android
- **Multiplayer:** Explore [references/networking.md](references/networking.md)
- **VR/AR:** Study [references/xr.md](references/xr.md)

## Key Concepts

### Unity Architecture
- **GameObjects:** Container objects that hold Components
- **Components:** Modular behaviors (Transform, Rigidbody, scripts, etc.)
- **Prefabs:** Reusable GameObject templates
- **Scenes:** Levels or sections of your game
- **Assets:** Files used in your project (textures, models, audio, etc.)

### Scripting Best Practices
- Use Awake() for initialization, Start() for setup
- Physics code goes in FixedUpdate()
- Use coroutines for time-based operations
- Avoid FindObjectOfType() in Update loops (cache references)
- Use object pooling for frequently instantiated objects
- Implement proper event cleanup (unsubscribe in OnDisable/OnDestroy)
- Use ScriptableObjects for game data
- Follow naming conventions (PascalCase for public, camelCase for private)

### Performance Optimization
- Enable Static Batching for static objects
- Use Dynamic Batching for moving objects
- Implement Level of Detail (LOD) for distant objects
- Use occlusion culling to skip rendering hidden objects
- Profile with Unity Profiler to identify bottlenecks
- Optimize draw calls by sharing materials
- Use object pooling instead of Instantiate/Destroy
- Minimize GetComponent calls (cache components)
- Avoid empty Update methods

### Physics Tips
- Use layers and layer collision matrix to optimize collision detection
- Choose appropriate collision detection mode (Discrete vs. Continuous)
- Use FixedUpdate for physics operations
- Raycasts are cheaper than colliders for simple checks
- Use Physics.OverlapSphere instead of trigger colliders when possible
- Avoid moving objects with Transform when using physics (use Rigidbody)

### Rendering Pipeline Comparison
- **Built-in:** Legacy, full-featured, good compatibility
- **URP (Universal):** Modern, optimized, mobile-friendly, flexible
- **HDRP (High Definition):** High-end graphics, PC/Console only

## Resources

### Official Documentation
- Unity Manual: https://docs.unity3d.com/Manual/
- Scripting API: https://docs.unity3d.com/ScriptReference/

### Learning Resources
- Unity Learn: Official tutorials and courses
- Unity Blog: Latest features and best practices
- Unity Forum: Community help and discussions

### Useful Packages
- **Input System** (com.unity.inputsystem): Modern input handling
- **Cinemachine** (com.unity.cinemachine): Advanced camera system
- **ProBuilder** (com.unity.probuilder): In-editor 3D modeling
- **TextMeshPro**: Advanced text rendering
- **XR Interaction Toolkit**: VR/AR interactions
- **Netcode for GameObjects**: Multiplayer networking
- **Universal RP / HDRP**: Render pipelines
- **Timeline**: Cinematic sequencing
- **Addressables**: Advanced asset management

### Common Namespaces
```csharp
using UnityEngine;              // Core Unity classes
using UnityEngine.UI;           // UGUI components
using UnityEngine.UIElements;   // UI Toolkit
using UnityEngine.SceneManagement; // Scene loading
using System.Collections;       // IEnumerator for coroutines
using System.Collections.Generic; // Lists, Dictionaries
```

## scripts/
Add helper scripts here for common automation tasks and utilities.

## assets/
Add templates, boilerplate code, or example Unity project files here.

## Notes

- This skill covers Unity 2023.2+ (Unity 6.x compatible)
- All code examples follow Unity C# coding standards
- Reference files link to official Unity documentation
- Script Reference API included for detailed class information
- URP (Universal Render Pipeline) is the recommended pipeline for new projects
- Always test on target platforms early in development

## Updating

To refresh this skill with updated Unity documentation:
1. Update the Unity config with the latest version URL
2. Re-run the scraper: `skill-seekers scrape --config configs/unity.json`
3. The skill will be rebuilt with the latest Unity documentation

---

*This skill was generated from official Unity documentation (Manual + Scripting API) covering 3,367 pages of comprehensive Unity Engine information.*
