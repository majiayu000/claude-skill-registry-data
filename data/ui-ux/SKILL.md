---
name: ui-ux
description: Implements UI/UX systems including responsive design, animations, input handling, HUD elements, and menu systems. Use when building game interfaces, menus, HUDs, or any user-facing UI.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Roblox UI/UX Systems

When implementing UI systems, follow these patterns for responsive and polished interfaces.

## Professional UI Design Consensus

Based on official Roblox documentation and community best practices, these are the key principles for professional Roblox UI design.

### Mobile-First Design (Critical)

**70%+ of Roblox players are on mobile devices.** Design for mobile first, then scale up for desktop.

```lua
-- GOOD: Mobile-first sizing with Scale
local button = Instance.new("TextButton")
button.Size = UDim2.new(0.8, 0, 0.12, 0)  -- 80% width, 12% height
button.Position = UDim2.new(0.5, 0, 0.5, 0)
button.AnchorPoint = Vector2.new(0.5, 0.5)

-- BAD: Fixed pixel sizes don't scale
local button = Instance.new("TextButton")
button.Size = UDim2.new(0, 300, 0, 50)  -- Looks tiny on mobile, huge on 4K
```

### Scale vs Offset Best Practices

| Use Case | Recommendation |
|----------|----------------|
| Main containers | **Scale** (0.8, 0) for responsiveness |
| Padding/margins | **Offset** (0, 10) for consistent spacing |
| Icon sizes | **Offset** with UISizeConstraint for crisp icons |
| Text containers | **Scale** width, auto-height via TextBounds |
| Buttons | **Scale** with UISizeConstraint min/max |

```lua
-- Hybrid approach: Scale with pixel constraints
local panel = Instance.new("Frame")
panel.Size = UDim2.new(0.6, 0, 0.7, 0)  -- Responsive

local sizeConstraint = Instance.new("UISizeConstraint")
sizeConstraint.MinSize = Vector2.new(300, 400)   -- Never too small
sizeConstraint.MaxSize = Vector2.new(800, 900)   -- Never too large
sizeConstraint.Parent = panel
```

### Typography Standards

**Gotham is the standard Roblox font family:**

| Font | Use Case |
|------|----------|
| `GothamBold` | Headers, titles, important labels |
| `GothamMedium` | Subheadings, button text |
| `Gotham` | Body text, descriptions |
| `GothamBlack` | Hero text, splash screens |

```lua
local title = Instance.new("TextLabel")
title.Font = Enum.Font.GothamBold
title.TextSize = 24  -- Use TextScaled sparingly
title.TextColor3 = Color3.fromRGB(255, 255, 255)

-- For responsive text, prefer RichText with fixed sizes
title.RichText = true
title.Text = '<font size="24">Title</font>'
```

**Text sizing guidelines:**
- Headers: 20-28px
- Body text: 14-18px
- Small labels: 12-14px
- Minimum readable: 12px (especially mobile)

### Modern UI Styling Components

**Every professional UI should use these:**

```lua
-- UICorner: Rounded corners (standard: 8-12px)
local corner = Instance.new("UICorner")
corner.CornerRadius = UDim.new(0, 12)
corner.Parent = frame

-- UIStroke: Border/outline for contrast
local stroke = Instance.new("UIStroke")
stroke.Thickness = 2
stroke.Color = Color3.fromRGB(255, 255, 255)
stroke.Transparency = 0.8
stroke.ApplyStrokeMode = Enum.ApplyStrokeMode.Border
stroke.Parent = frame

-- UIGradient: Depth and visual interest
local gradient = Instance.new("UIGradient")
gradient.Color = ColorSequence.new({
    ColorSequenceKeypoint.new(0, Color3.fromRGB(60, 60, 80)),
    ColorSequenceKeypoint.new(1, Color3.fromRGB(40, 40, 60))
})
gradient.Rotation = 90
gradient.Parent = frame

-- UIPadding: Consistent internal spacing
local padding = Instance.new("UIPadding")
padding.PaddingTop = UDim.new(0, 16)
padding.PaddingBottom = UDim.new(0, 16)
padding.PaddingLeft = UDim.new(0, 16)
padding.PaddingRight = UDim.new(0, 16)
padding.Parent = frame

-- UIListLayout: Automatic arrangement
local layout = Instance.new("UIListLayout")
layout.SortOrder = Enum.SortOrder.LayoutOrder
layout.Padding = UDim.new(0, 8)
layout.HorizontalAlignment = Enum.HorizontalAlignment.Center
layout.Parent = container
```

### Color and Contrast Guidelines

```lua
-- Professional dark theme palette
local Colors = {
    -- Backgrounds (darkest to lightest)
    Background = Color3.fromRGB(25, 25, 35),      -- Main background
    Surface = Color3.fromRGB(35, 35, 50),         -- Cards, panels
    SurfaceHover = Color3.fromRGB(45, 45, 65),    -- Hover states

    -- Text (high contrast)
    TextPrimary = Color3.fromRGB(255, 255, 255),  -- Main text
    TextSecondary = Color3.fromRGB(180, 180, 200),-- Descriptions
    TextMuted = Color3.fromRGB(120, 120, 140),    -- Hints

    -- Accents (brand colors)
    Primary = Color3.fromRGB(0, 170, 255),        -- Main action
    Success = Color3.fromRGB(50, 200, 100),       -- Positive
    Warning = Color3.fromRGB(255, 200, 50),       -- Caution
    Error = Color3.fromRGB(255, 80, 80),          -- Negative
    Premium = Color3.fromRGB(255, 200, 50),       -- Premium/gold
}

-- Ensure 4.5:1 contrast ratio for accessibility
-- White text on dark backgrounds is standard
```

### Animation Best Practices

**Animation durations: 0.2-0.35 seconds** (community consensus)

```lua
local TweenService = game:GetService("TweenService")

-- Standard UI animation durations
local DURATIONS = {
    instant = 0.1,      -- Button press feedback
    quick = 0.2,        -- Hover states, small transitions
    standard = 0.3,     -- Panel open/close
    smooth = 0.5,       -- Large transitions, page changes
}

-- Recommended easing styles
local EASING = {
    bounce = TweenInfo.new(0.3, Enum.EasingStyle.Back, Enum.EasingDirection.Out),
    smooth = TweenInfo.new(0.25, Enum.EasingStyle.Quart, Enum.EasingDirection.Out),
    snap = TweenInfo.new(0.15, Enum.EasingStyle.Quad, Enum.EasingDirection.Out),
}

-- Button feedback pattern
local function setupButtonFeedback(button)
    local originalSize = button.Size

    button.MouseButton1Down:Connect(function()
        TweenService:Create(button, EASING.snap, {
            Size = originalSize - UDim2.new(0.02, 0, 0.02, 0)
        }):Play()
    end)

    button.MouseButton1Up:Connect(function()
        TweenService:Create(button, EASING.bounce, {
            Size = originalSize
        }):Play()
    end)
end
```

### Visual Hierarchy Principles

**Size, color, space, and proximity establish hierarchy:**

```lua
-- 1. SIZE: Larger = more important
local heroTitle = Instance.new("TextLabel")
heroTitle.TextSize = 32
heroTitle.Font = Enum.Font.GothamBlack

local subtitle = Instance.new("TextLabel")
subtitle.TextSize = 18
subtitle.Font = Enum.Font.GothamMedium

-- 2. COLOR: Brighter/accent = more attention
local primaryButton = Instance.new("TextButton")
primaryButton.BackgroundColor3 = Colors.Primary  -- Draws attention

local secondaryButton = Instance.new("TextButton")
secondaryButton.BackgroundColor3 = Colors.Surface  -- Less prominent

-- 3. SPACE: More padding = more importance
local heroSection = Instance.new("Frame")
local heroPadding = Instance.new("UIPadding")
heroPadding.PaddingTop = UDim.new(0, 32)  -- Generous spacing
heroPadding.Parent = heroSection

-- 4. PROXIMITY: Related items grouped together
local rewardGroup = Instance.new("Frame")  -- Contains: icon + label + amount
-- All reward info in one visual unit
```

### UX Best Practices

**Clean UX with minimal clutter:**

1. **One primary action per screen** - Don't overwhelm with choices
2. **Clear feedback** - Every interaction should have visual/audio response
3. **Consistent patterns** - Same actions look the same everywhere
4. **Forgiving design** - Confirm destructive actions, allow undo
5. **Progressive disclosure** - Show basic first, details on demand

```lua
-- Feedback example: Button state changes
local function createActionButton(text, onClick)
    local button = Instance.new("TextButton")
    button.Text = text
    button.BackgroundColor3 = Colors.Primary

    -- Visual states
    button.MouseEnter:Connect(function()
        button.BackgroundColor3 = Colors.Primary:Lerp(Color3.new(1,1,1), 0.1)
    end)

    button.MouseLeave:Connect(function()
        button.BackgroundColor3 = Colors.Primary
    end)

    button.Activated:Connect(function()
        -- Immediate feedback
        button.Text = "..."
        button.BackgroundColor3 = Colors.Surface

        onClick()

        -- Success feedback
        button.Text = "✓"
        task.wait(0.5)
        button.Text = text
        button.BackgroundColor3 = Colors.Primary
    end)

    return button
end
```

### Touch Target Sizes (Mobile Critical)

**Minimum touch target: 44x44 pixels** (Apple HIG standard)

```lua
-- Ensure buttons are large enough for touch
local touchButton = Instance.new("TextButton")
touchButton.Size = UDim2.new(0.3, 0, 0, 48)  -- At least 48px height

local sizeConstraint = Instance.new("UISizeConstraint")
sizeConstraint.MinSize = Vector2.new(44, 44)  -- Never smaller than touch target
sizeConstraint.Parent = touchButton

-- For icon buttons, use padding to increase touch area
local iconButton = Instance.new("ImageButton")
iconButton.Size = UDim2.new(0, 24, 0, 24)  -- Visual size

local clickArea = Instance.new("TextButton")
clickArea.Size = UDim2.new(0, 48, 0, 48)  -- Touch area
clickArea.BackgroundTransparency = 1
clickArea.Parent = iconButton.Parent
clickArea.Position = iconButton.Position - UDim2.new(0, 12, 0, 12)
```

## Responsive Design

### UIAspectRatioConstraint
```lua
-- Maintain aspect ratio regardless of screen size
local frame = Instance.new("Frame")
frame.Size = UDim2.new(0.5, 0, 0.5, 0)  -- Will be adjusted

local aspectRatio = Instance.new("UIAspectRatioConstraint")
aspectRatio.AspectRatio = 16/9
aspectRatio.AspectType = Enum.AspectType.FitWithinMaxSize
aspectRatio.DominantAxis = Enum.DominantAxis.Width
aspectRatio.Parent = frame
```

### UISizeConstraint
```lua
-- Limit min/max size
local sizeConstraint = Instance.new("UISizeConstraint")
sizeConstraint.MinSize = Vector2.new(100, 50)
sizeConstraint.MaxSize = Vector2.new(500, 300)
sizeConstraint.Parent = frame
```

### Screen Size Detection
```lua
local camera = workspace.CurrentCamera

local function getScreenCategory()
    local viewportSize = camera.ViewportSize

    if viewportSize.X < 600 then
        return "mobile"
    elseif viewportSize.X < 1200 then
        return "tablet"
    else
        return "desktop"
    end
end

local function updateLayout()
    local category = getScreenCategory()

    if category == "mobile" then
        mainFrame.Size = UDim2.new(0.95, 0, 0.9, 0)
        fontSize = 14
    elseif category == "tablet" then
        mainFrame.Size = UDim2.new(0.8, 0, 0.8, 0)
        fontSize = 16
    else
        mainFrame.Size = UDim2.new(0.6, 0, 0.7, 0)
        fontSize = 18
    end
end

camera:GetPropertyChangedSignal("ViewportSize"):Connect(updateLayout)
```

### Safe Area (Notch/Button Handling)
```lua
local GuiService = game:GetService("GuiService")

local function getSafeInsets()
    local insets = GuiService:GetGuiInset()
    return insets
end

-- Apply safe area padding
local topInset = getSafeInsets()
mainFrame.Position = UDim2.new(0.5, 0, 0, topInset.Y + 10)
```

## UI Animation

### TweenService for UI
```lua
local TweenService = game:GetService("TweenService")

local function animateIn(frame)
    frame.Position = UDim2.new(0.5, 0, 1.5, 0)  -- Start below screen
    frame.Visible = true

    local tween = TweenService:Create(
        frame,
        TweenInfo.new(0.5, Enum.EasingStyle.Back, Enum.EasingDirection.Out),
        {Position = UDim2.new(0.5, 0, 0.5, 0)}
    )
    tween:Play()
    return tween
end

local function animateOut(frame)
    local tween = TweenService:Create(
        frame,
        TweenInfo.new(0.3, Enum.EasingStyle.Back, Enum.EasingDirection.In),
        {Position = UDim2.new(0.5, 0, 1.5, 0)}
    )
    tween:Play()
    tween.Completed:Connect(function()
        frame.Visible = false
    end)
    return tween
end
```

### Spring Animation
```lua
local function springAnimation(frame, targetSize, stiffness, damping)
    stiffness = stiffness or 200
    damping = damping or 20

    local currentSize = {frame.Size.X.Scale, frame.Size.Y.Scale}
    local velocity = {0, 0}
    local target = {targetSize.X.Scale, targetSize.Y.Scale}

    local conn
    conn = RunService.RenderStepped:Connect(function(dt)
        for i = 1, 2 do
            local displacement = target[i] - currentSize[i]
            local springForce = displacement * stiffness
            local dampingForce = velocity[i] * damping
            local acceleration = springForce - dampingForce

            velocity[i] = velocity[i] + acceleration * dt
            currentSize[i] = currentSize[i] + velocity[i] * dt
        end

        frame.Size = UDim2.new(currentSize[1], 0, currentSize[2], 0)

        -- Check if settled
        local totalVelocity = math.abs(velocity[1]) + math.abs(velocity[2])
        local totalDisplacement = math.abs(target[1] - currentSize[1]) + math.abs(target[2] - currentSize[2])

        if totalVelocity < 0.001 and totalDisplacement < 0.001 then
            frame.Size = targetSize
            conn:Disconnect()
        end
    end)
end
```

### Stagger Animation
```lua
local function staggerChildren(parent, delay, animateFunc)
    delay = delay or 0.1

    local children = parent:GetChildren()
    for i, child in ipairs(children) do
        task.delay((i - 1) * delay, function()
            animateFunc(child)
        end)
    end
end

-- Usage
staggerChildren(menuFrame, 0.05, function(button)
    button.Position = button.Position + UDim2.new(0.1, 0, 0, 0)
    button.BackgroundTransparency = 1

    TweenService:Create(button, TweenInfo.new(0.3), {
        Position = button.Position - UDim2.new(0.1, 0, 0, 0),
        BackgroundTransparency = 0
    }):Play()
end)
```

## Input Handling

### Button Interactions
```lua
local function setupButton(button)
    local originalSize = button.Size
    local originalColor = button.BackgroundColor3

    -- Hover
    button.MouseEnter:Connect(function()
        TweenService:Create(button, TweenInfo.new(0.1), {
            Size = originalSize + UDim2.new(0.02, 0, 0.02, 0),
            BackgroundColor3 = originalColor:Lerp(Color3.new(1, 1, 1), 0.1)
        }):Play()
    end)

    button.MouseLeave:Connect(function()
        TweenService:Create(button, TweenInfo.new(0.1), {
            Size = originalSize,
            BackgroundColor3 = originalColor
        }):Play()
    end)

    -- Click
    button.MouseButton1Down:Connect(function()
        TweenService:Create(button, TweenInfo.new(0.05), {
            Size = originalSize - UDim2.new(0.01, 0, 0.01, 0)
        }):Play()
    end)

    button.MouseButton1Up:Connect(function()
        TweenService:Create(button, TweenInfo.new(0.1), {
            Size = originalSize
        }):Play()
    end)
end
```

### Drag and Drop
```lua
local function makeDraggable(frame)
    local dragging = false
    local dragStart
    local startPos

    frame.InputBegan:Connect(function(input)
        if input.UserInputType == Enum.UserInputType.MouseButton1 or
           input.UserInputType == Enum.UserInputType.Touch then
            dragging = true
            dragStart = input.Position
            startPos = frame.Position

            input.Changed:Connect(function()
                if input.UserInputState == Enum.UserInputState.End then
                    dragging = false
                end
            end)
        end
    end)

    frame.InputChanged:Connect(function(input)
        if input.UserInputType == Enum.UserInputType.MouseMovement or
           input.UserInputType == Enum.UserInputType.Touch then
            if dragging then
                local delta = input.Position - dragStart
                frame.Position = UDim2.new(
                    startPos.X.Scale,
                    startPos.X.Offset + delta.X,
                    startPos.Y.Scale,
                    startPos.Y.Offset + delta.Y
                )
            end
        end
    end)
end
```

### Scroll Handling
```lua
local scrollingFrame = Instance.new("ScrollingFrame")
scrollingFrame.Size = UDim2.new(0.5, 0, 0.5, 0)
scrollingFrame.CanvasSize = UDim2.new(0, 0, 0, 0)  -- Will be auto-sized
scrollingFrame.AutomaticCanvasSize = Enum.AutomaticSize.Y
scrollingFrame.ScrollBarThickness = 8
scrollingFrame.ScrollBarImageColor3 = Color3.fromRGB(100, 100, 100)

-- List layout for automatic sizing
local listLayout = Instance.new("UIListLayout")
listLayout.SortOrder = Enum.SortOrder.LayoutOrder
listLayout.Padding = UDim.new(0, 5)
listLayout.Parent = scrollingFrame

-- Smooth scrolling
local function smoothScrollTo(targetPosition)
    local tween = TweenService:Create(
        scrollingFrame,
        TweenInfo.new(0.3, Enum.EasingStyle.Quad, Enum.EasingDirection.Out),
        {CanvasPosition = Vector2.new(0, targetPosition)}
    )
    tween:Play()
end
```

## HUD Systems

### Health Bar
```lua
local function createHealthBar(parent)
    local container = Instance.new("Frame")
    container.Size = UDim2.new(0.3, 0, 0, 30)
    container.Position = UDim2.new(0.02, 0, 0.05, 0)
    container.BackgroundColor3 = Color3.fromRGB(30, 30, 30)
    container.Parent = parent

    local fill = Instance.new("Frame")
    fill.Size = UDim2.new(1, 0, 1, 0)
    fill.BackgroundColor3 = Color3.fromRGB(0, 200, 0)
    fill.Parent = container

    -- Delayed damage indicator
    local delayedFill = Instance.new("Frame")
    delayedFill.Size = UDim2.new(1, 0, 1, 0)
    delayedFill.BackgroundColor3 = Color3.fromRGB(200, 0, 0)
    delayedFill.ZIndex = fill.ZIndex - 1
    delayedFill.Parent = container

    local function updateHealth(current, max)
        local ratio = current / max
        local targetSize = UDim2.new(ratio, 0, 1, 0)

        -- Instant fill update
        fill.Size = targetSize

        -- Delayed red bar
        TweenService:Create(delayedFill, TweenInfo.new(0.5), {
            Size = targetSize
        }):Play()

        -- Color based on health
        if ratio > 0.5 then
            fill.BackgroundColor3 = Color3.fromRGB(0, 200, 0)
        elseif ratio > 0.25 then
            fill.BackgroundColor3 = Color3.fromRGB(200, 200, 0)
        else
            fill.BackgroundColor3 = Color3.fromRGB(200, 0, 0)
        end
    end

    return {container = container, update = updateHealth}
end
```

### Minimap
```lua
local function createMinimap(parent, worldSize, minimapSize)
    local container = Instance.new("Frame")
    container.Size = UDim2.new(0, minimapSize, 0, minimapSize)
    container.Position = UDim2.new(1, -minimapSize - 10, 0, 10)
    container.BackgroundColor3 = Color3.fromRGB(20, 20, 20)
    container.ClipsDescendants = true
    container.Parent = parent

    -- Player marker
    local playerMarker = Instance.new("Frame")
    playerMarker.Size = UDim2.new(0, 10, 0, 10)
    playerMarker.AnchorPoint = Vector2.new(0.5, 0.5)
    playerMarker.BackgroundColor3 = Color3.fromRGB(0, 200, 0)
    playerMarker.Parent = container

    Instance.new("UICorner", playerMarker).CornerRadius = UDim.new(1, 0)

    local function worldToMinimap(worldPos)
        local x = (worldPos.X / worldSize + 0.5) * minimapSize
        local y = (worldPos.Z / worldSize + 0.5) * minimapSize
        return UDim2.new(0, x, 0, y)
    end

    local function update()
        local character = Players.LocalPlayer.Character
        if not character then return end

        local pos = character.PrimaryPart.Position
        playerMarker.Position = worldToMinimap(pos)

        -- Rotate marker based on facing
        local lookVector = character.PrimaryPart.CFrame.LookVector
        local angle = math.atan2(lookVector.X, lookVector.Z)
        playerMarker.Rotation = math.deg(angle)
    end

    RunService.RenderStepped:Connect(update)

    return container
end
```

### Cooldown Indicator
```lua
local function createCooldownIndicator(button, duration)
    local overlay = Instance.new("Frame")
    overlay.Size = UDim2.new(1, 0, 1, 0)
    overlay.BackgroundColor3 = Color3.new(0, 0, 0)
    overlay.BackgroundTransparency = 0.5
    overlay.ZIndex = button.ZIndex + 1
    overlay.Parent = button

    local gradient = Instance.new("UIGradient")
    gradient.Rotation = -90
    gradient.Transparency = NumberSequence.new({
        NumberSequenceKeypoint.new(0, 0),
        NumberSequenceKeypoint.new(0.5, 0),
        NumberSequenceKeypoint.new(0.501, 1),
        NumberSequenceKeypoint.new(1, 1)
    })
    gradient.Parent = overlay

    local cooldownText = Instance.new("TextLabel")
    cooldownText.Size = UDim2.new(1, 0, 1, 0)
    cooldownText.BackgroundTransparency = 1
    cooldownText.TextColor3 = Color3.new(1, 1, 1)
    cooldownText.TextScaled = true
    cooldownText.ZIndex = overlay.ZIndex + 1
    cooldownText.Parent = overlay

    local startTime = os.clock()

    local conn
    conn = RunService.RenderStepped:Connect(function()
        local elapsed = os.clock() - startTime
        local remaining = duration - elapsed

        if remaining <= 0 then
            overlay:Destroy()
            conn:Disconnect()
            return
        end

        -- Update sweep
        local progress = elapsed / duration
        gradient.Offset = Vector2.new(0, progress * 2 - 1)

        -- Update text
        cooldownText.Text = string.format("%.1f", remaining)
    end)
end
```

## Menu Systems

### Page Navigation
```lua
local MenuController = {}
MenuController.pageStack = {}

function MenuController.pushPage(pageName)
    local currentPage = MenuController.pageStack[#MenuController.pageStack]
    if currentPage then
        currentPage.Visible = false
    end

    local newPage = Pages[pageName]
    newPage.Visible = true
    table.insert(MenuController.pageStack, newPage)
end

function MenuController.popPage()
    if #MenuController.pageStack <= 1 then return end

    local currentPage = table.remove(MenuController.pageStack)
    currentPage.Visible = false

    local previousPage = MenuController.pageStack[#MenuController.pageStack]
    previousPage.Visible = true
end

function MenuController.goToPage(pageName)
    -- Clear stack and go to specific page
    for _, page in ipairs(MenuController.pageStack) do
        page.Visible = false
    end
    MenuController.pageStack = {}
    MenuController.pushPage(pageName)
end

-- Back button
backButton.MouseButton1Click:Connect(function()
    MenuController.popPage()
end)
```

### Modal Dialog
```lua
local function showModal(title, message, buttons)
    -- Darken background
    local backdrop = Instance.new("Frame")
    backdrop.Size = UDim2.new(1, 0, 1, 0)
    backdrop.BackgroundColor3 = Color3.new(0, 0, 0)
    backdrop.BackgroundTransparency = 0.5
    backdrop.ZIndex = 100
    backdrop.Parent = ScreenGui

    local modal = Instance.new("Frame")
    modal.Size = UDim2.new(0.4, 0, 0.3, 0)
    modal.Position = UDim2.new(0.5, 0, 0.5, 0)
    modal.AnchorPoint = Vector2.new(0.5, 0.5)
    modal.BackgroundColor3 = Color3.fromRGB(40, 40, 40)
    modal.ZIndex = 101
    modal.Parent = backdrop

    local titleLabel = Instance.new("TextLabel")
    titleLabel.Text = title
    titleLabel.Size = UDim2.new(1, 0, 0.2, 0)
    titleLabel.BackgroundTransparency = 1
    titleLabel.TextColor3 = Color3.new(1, 1, 1)
    titleLabel.TextScaled = true
    titleLabel.Parent = modal

    local messageLabel = Instance.new("TextLabel")
    messageLabel.Text = message
    messageLabel.Size = UDim2.new(0.9, 0, 0.4, 0)
    messageLabel.Position = UDim2.new(0.05, 0, 0.25, 0)
    messageLabel.BackgroundTransparency = 1
    messageLabel.TextColor3 = Color3.new(0.8, 0.8, 0.8)
    messageLabel.TextWrapped = true
    messageLabel.Parent = modal

    local buttonContainer = Instance.new("Frame")
    buttonContainer.Size = UDim2.new(0.9, 0, 0.25, 0)
    buttonContainer.Position = UDim2.new(0.05, 0, 0.7, 0)
    buttonContainer.BackgroundTransparency = 1
    buttonContainer.Parent = modal

    local listLayout = Instance.new("UIListLayout")
    listLayout.FillDirection = Enum.FillDirection.Horizontal
    listLayout.HorizontalAlignment = Enum.HorizontalAlignment.Center
    listLayout.Padding = UDim.new(0, 10)
    listLayout.Parent = buttonContainer

    local result = nil

    for _, buttonData in ipairs(buttons) do
        local btn = Instance.new("TextButton")
        btn.Size = UDim2.new(0, 100, 1, 0)
        btn.Text = buttonData.text
        btn.BackgroundColor3 = buttonData.color or Color3.fromRGB(60, 60, 60)
        btn.TextColor3 = Color3.new(1, 1, 1)
        btn.Parent = buttonContainer

        btn.MouseButton1Click:Connect(function()
            result = buttonData.value
            backdrop:Destroy()
        end)
    end

    -- Wait for result
    while not result and backdrop.Parent do
        task.wait()
    end

    return result
end

-- Usage
local choice = showModal("Confirm", "Are you sure?", {
    {text = "Yes", value = true, color = Color3.fromRGB(0, 150, 0)},
    {text = "No", value = false, color = Color3.fromRGB(150, 0, 0)}
})
```

## Shop UI System

### Complete Shop Implementation

```lua
local TweenService = game:GetService("TweenService")
local Players = game:GetService("Players")

local player = Players.LocalPlayer
local playerGui = player:WaitForChild("PlayerGui")

-- Shop Configuration
local ShopConfig = {
    categories = {
        {name = "Pets", icon = "rbxassetid://123456", items = {}},
        {name = "Gear", icon = "rbxassetid://123457", items = {}},
        {name = "Boosts", icon = "rbxassetid://123458", items = {}},
        {name = "Special", icon = "rbxassetid://123459", items = {}},
    },
    items = {
        {id = "speed_pet", name = "Speed Cat", category = "Pets", price = 500, currency = "coins", icon = "rbxassetid://..."},
        {id = "sword_basic", name = "Starter Sword", category = "Gear", price = 100, currency = "coins", icon = "rbxassetid://..."},
        {id = "2x_coins", name = "2x Coins (1hr)", category = "Boosts", price = 50, currency = "gems", icon = "rbxassetid://..."},
    }
}

local function createShopUI()
    local screenGui = Instance.new("ScreenGui")
    screenGui.Name = "ShopUI"
    screenGui.ResetOnSpawn = false

    -- Main container
    local mainFrame = Instance.new("Frame")
    mainFrame.Size = UDim2.new(0, 700, 0, 500)
    mainFrame.Position = UDim2.new(0.5, 0, 0.5, 0)
    mainFrame.AnchorPoint = Vector2.new(0.5, 0.5)
    mainFrame.BackgroundColor3 = Color3.fromRGB(25, 25, 40)
    mainFrame.Parent = screenGui

    Instance.new("UICorner", mainFrame).CornerRadius = UDim.new(0, 16)

    -- Header with title and close button
    local header = Instance.new("Frame")
    header.Size = UDim2.new(1, 0, 0, 60)
    header.BackgroundColor3 = Color3.fromRGB(35, 35, 55)
    header.Parent = mainFrame
    Instance.new("UICorner", header).CornerRadius = UDim.new(0, 16)

    local title = Instance.new("TextLabel")
    title.Size = UDim2.new(0.5, 0, 1, 0)
    title.Position = UDim2.new(0.02, 0, 0, 0)
    title.BackgroundTransparency = 1
    title.Text = "🛒 SHOP"
    title.TextColor3 = Color3.new(1, 1, 1)
    title.TextSize = 28
    title.Font = Enum.Font.GothamBold
    title.TextXAlignment = Enum.TextXAlignment.Left
    title.Parent = header

    -- Currency display
    local currencyFrame = Instance.new("Frame")
    currencyFrame.Size = UDim2.new(0, 200, 0, 40)
    currencyFrame.Position = UDim2.new(1, -260, 0.5, 0)
    currencyFrame.AnchorPoint = Vector2.new(0, 0.5)
    currencyFrame.BackgroundColor3 = Color3.fromRGB(45, 45, 65)
    currencyFrame.Parent = header
    Instance.new("UICorner", currencyFrame).CornerRadius = UDim.new(0, 8)

    -- Category tabs (left sidebar)
    local categorySidebar = Instance.new("Frame")
    categorySidebar.Size = UDim2.new(0, 120, 1, -70)
    categorySidebar.Position = UDim2.new(0, 10, 0, 65)
    categorySidebar.BackgroundTransparency = 1
    categorySidebar.Parent = mainFrame

    local categoryLayout = Instance.new("UIListLayout")
    categoryLayout.SortOrder = Enum.SortOrder.LayoutOrder
    categoryLayout.Padding = UDim.new(0, 8)
    categoryLayout.Parent = categorySidebar

    -- Item grid (scrolling)
    local itemContainer = Instance.new("ScrollingFrame")
    itemContainer.Size = UDim2.new(1, -145, 1, -80)
    itemContainer.Position = UDim2.new(0, 135, 0, 70)
    itemContainer.BackgroundTransparency = 1
    itemContainer.ScrollBarThickness = 6
    itemContainer.CanvasSize = UDim2.new(0, 0, 0, 0)
    itemContainer.AutomaticCanvasSize = Enum.AutomaticSize.Y
    itemContainer.Parent = mainFrame

    local gridLayout = Instance.new("UIGridLayout")
    gridLayout.CellSize = UDim2.new(0, 130, 0, 170)
    gridLayout.CellPadding = UDim2.new(0, 12, 0, 12)
    gridLayout.SortOrder = Enum.SortOrder.LayoutOrder
    gridLayout.Parent = itemContainer

    return screenGui, mainFrame, categorySidebar, itemContainer
end

-- Item card component
local function createItemCard(item, parent)
    local card = Instance.new("Frame")
    card.Size = UDim2.new(1, 0, 1, 0)  -- Controlled by grid
    card.BackgroundColor3 = Color3.fromRGB(40, 40, 60)
    card.Parent = parent

    Instance.new("UICorner", card).CornerRadius = UDim.new(0, 12)

    -- Item icon
    local icon = Instance.new("ImageLabel")
    icon.Size = UDim2.new(0, 80, 0, 80)
    icon.Position = UDim2.new(0.5, 0, 0, 15)
    icon.AnchorPoint = Vector2.new(0.5, 0)
    icon.BackgroundColor3 = Color3.fromRGB(30, 30, 45)
    icon.Image = item.icon
    icon.Parent = card
    Instance.new("UICorner", icon).CornerRadius = UDim.new(0, 8)

    -- Item name
    local nameLabel = Instance.new("TextLabel")
    nameLabel.Size = UDim2.new(0.9, 0, 0, 20)
    nameLabel.Position = UDim2.new(0.05, 0, 0, 100)
    nameLabel.BackgroundTransparency = 1
    nameLabel.Text = item.name
    nameLabel.TextColor3 = Color3.new(1, 1, 1)
    nameLabel.TextSize = 14
    nameLabel.Font = Enum.Font.GothamMedium
    nameLabel.TextTruncate = Enum.TextTruncate.AtEnd
    nameLabel.Parent = card

    -- Buy button with price
    local buyButton = Instance.new("TextButton")
    buyButton.Size = UDim2.new(0.85, 0, 0, 36)
    buyButton.Position = UDim2.new(0.5, 0, 1, -45)
    buyButton.AnchorPoint = Vector2.new(0.5, 0)
    buyButton.BackgroundColor3 = Color3.fromRGB(0, 180, 100)
    buyButton.Text = string.format("%d %s", item.price, item.currency == "coins" and "🪙" or "💎")
    buyButton.TextColor3 = Color3.new(1, 1, 1)
    buyButton.TextSize = 16
    buyButton.Font = Enum.Font.GothamBold
    buyButton.Parent = card
    Instance.new("UICorner", buyButton).CornerRadius = UDim.new(0, 8)

    -- Hover effect
    buyButton.MouseEnter:Connect(function()
        TweenService:Create(buyButton, TweenInfo.new(0.2), {
            BackgroundColor3 = Color3.fromRGB(0, 200, 120)
        }):Play()
    end)

    buyButton.MouseLeave:Connect(function()
        TweenService:Create(buyButton, TweenInfo.new(0.2), {
            BackgroundColor3 = Color3.fromRGB(0, 180, 100)
        }):Play()
    end)

    -- Purchase logic
    buyButton.MouseButton1Click:Connect(function()
        -- Check affordability and process purchase
        print("Attempting to purchase:", item.name)
        -- Fire purchase event to server
    end)

    return card
end
```

## Inventory UI System

### Complete Inventory with Rarity System

```lua
-- Rarity configuration
local RarityColors = {
    Common = Color3.fromRGB(150, 150, 150),
    Rare = Color3.fromRGB(0, 150, 255),
    Epic = Color3.fromRGB(180, 0, 255),
    Legendary = Color3.fromRGB(255, 180, 0),
}

local RarityGlows = {
    Common = 0,
    Rare = 0.3,
    Epic = 0.5,
    Legendary = 0.8,
}

local function createInventoryUI()
    local screenGui = Instance.new("ScreenGui")
    screenGui.Name = "InventoryUI"
    screenGui.ResetOnSpawn = false

    local mainFrame = Instance.new("Frame")
    mainFrame.Size = UDim2.new(0, 800, 0, 550)
    mainFrame.Position = UDim2.new(0.5, 0, 0.5, 0)
    mainFrame.AnchorPoint = Vector2.new(0.5, 0.5)
    mainFrame.BackgroundColor3 = Color3.fromRGB(25, 25, 40)
    mainFrame.Parent = screenGui

    Instance.new("UICorner", mainFrame).CornerRadius = UDim.new(0, 16)

    -- Left panel: Item grid
    local gridPanel = Instance.new("ScrollingFrame")
    gridPanel.Size = UDim2.new(0.6, -20, 1, -130)
    gridPanel.Position = UDim2.new(0, 15, 0, 110)
    gridPanel.BackgroundColor3 = Color3.fromRGB(30, 30, 45)
    gridPanel.ScrollBarThickness = 6
    gridPanel.CanvasSize = UDim2.new(0, 0, 0, 0)
    gridPanel.AutomaticCanvasSize = Enum.AutomaticSize.Y
    gridPanel.Parent = mainFrame
    Instance.new("UICorner", gridPanel).CornerRadius = UDim.new(0, 12)

    local gridLayout = Instance.new("UIGridLayout")
    gridLayout.CellSize = UDim2.new(0, 90, 0, 90)
    gridLayout.CellPadding = UDim2.new(0, 10, 0, 10)
    gridLayout.SortOrder = Enum.SortOrder.LayoutOrder
    gridLayout.Parent = gridPanel

    local gridPadding = Instance.new("UIPadding")
    gridPadding.PaddingAll = UDim.new(0, 10)
    gridPadding.Parent = gridPanel

    -- Right panel: Item details
    local detailsPanel = Instance.new("Frame")
    detailsPanel.Size = UDim2.new(0.4, -25, 1, -130)
    detailsPanel.Position = UDim2.new(0.6, 5, 0, 110)
    detailsPanel.BackgroundColor3 = Color3.fromRGB(30, 30, 45)
    detailsPanel.Parent = mainFrame
    Instance.new("UICorner", detailsPanel).CornerRadius = UDim.new(0, 12)

    -- Details content
    local detailIcon = Instance.new("ImageLabel")
    detailIcon.Size = UDim2.new(0, 120, 0, 120)
    detailIcon.Position = UDim2.new(0.5, 0, 0, 30)
    detailIcon.AnchorPoint = Vector2.new(0.5, 0)
    detailIcon.BackgroundColor3 = Color3.fromRGB(40, 40, 55)
    detailIcon.Parent = detailsPanel
    Instance.new("UICorner", detailIcon).CornerRadius = UDim.new(0, 12)

    local detailName = Instance.new("TextLabel")
    detailName.Size = UDim2.new(0.9, 0, 0, 30)
    detailName.Position = UDim2.new(0.05, 0, 0, 165)
    detailName.BackgroundTransparency = 1
    detailName.Text = "Select an Item"
    detailName.TextColor3 = Color3.new(1, 1, 1)
    detailName.TextSize = 22
    detailName.Font = Enum.Font.GothamBold
    detailName.Parent = detailsPanel

    local detailRarity = Instance.new("TextLabel")
    detailRarity.Size = UDim2.new(0.9, 0, 0, 20)
    detailRarity.Position = UDim2.new(0.05, 0, 0, 200)
    detailRarity.BackgroundTransparency = 1
    detailRarity.Text = ""
    detailRarity.TextSize = 16
    detailRarity.Font = Enum.Font.GothamMedium
    detailRarity.Parent = detailsPanel

    local detailDescription = Instance.new("TextLabel")
    detailDescription.Size = UDim2.new(0.9, 0, 0, 60)
    detailDescription.Position = UDim2.new(0.05, 0, 0, 230)
    detailDescription.BackgroundTransparency = 1
    detailDescription.Text = ""
    detailDescription.TextColor3 = Color3.fromRGB(180, 180, 200)
    detailDescription.TextSize = 14
    detailDescription.Font = Enum.Font.Gotham
    detailDescription.TextWrapped = true
    detailDescription.TextYAlignment = Enum.TextYAlignment.Top
    detailDescription.Parent = detailsPanel

    -- Equip/Unequip button
    local equipButton = Instance.new("TextButton")
    equipButton.Size = UDim2.new(0.8, 0, 0, 45)
    equipButton.Position = UDim2.new(0.5, 0, 1, -70)
    equipButton.AnchorPoint = Vector2.new(0.5, 0)
    equipButton.BackgroundColor3 = Color3.fromRGB(0, 150, 255)
    equipButton.Text = "EQUIP"
    equipButton.TextColor3 = Color3.new(1, 1, 1)
    equipButton.TextSize = 18
    equipButton.Font = Enum.Font.GothamBold
    equipButton.Visible = false
    equipButton.Parent = detailsPanel
    Instance.new("UICorner", equipButton).CornerRadius = UDim.new(0, 10)

    return screenGui, gridPanel, {
        icon = detailIcon,
        name = detailName,
        rarity = detailRarity,
        description = detailDescription,
        equipButton = equipButton,
    }
end

-- Inventory item slot with rarity glow
local function createInventorySlot(item, parent)
    local slot = Instance.new("TextButton")
    slot.Size = UDim2.new(1, 0, 1, 0)
    slot.BackgroundColor3 = Color3.fromRGB(45, 45, 60)
    slot.Text = ""
    slot.Parent = parent

    Instance.new("UICorner", slot).CornerRadius = UDim.new(0, 10)

    -- Rarity border glow
    local rarityColor = RarityColors[item.rarity] or RarityColors.Common
    local stroke = Instance.new("UIStroke")
    stroke.Color = rarityColor
    stroke.Thickness = 3
    stroke.Transparency = 1 - RarityGlows[item.rarity]
    stroke.Parent = slot

    -- Item icon
    local icon = Instance.new("ImageLabel")
    icon.Size = UDim2.new(0.8, 0, 0.8, 0)
    icon.Position = UDim2.new(0.5, 0, 0.5, 0)
    icon.AnchorPoint = Vector2.new(0.5, 0.5)
    icon.BackgroundTransparency = 1
    icon.Image = item.icon
    icon.Parent = slot

    -- Equipped indicator
    if item.equipped then
        local equippedBadge = Instance.new("Frame")
        equippedBadge.Size = UDim2.new(0, 24, 0, 24)
        equippedBadge.Position = UDim2.new(1, -5, 0, 5)
        equippedBadge.AnchorPoint = Vector2.new(1, 0)
        equippedBadge.BackgroundColor3 = Color3.fromRGB(0, 200, 100)
        equippedBadge.Parent = slot
        Instance.new("UICorner", equippedBadge).CornerRadius = UDim.new(1, 0)

        local checkmark = Instance.new("TextLabel")
        checkmark.Size = UDim2.new(1, 0, 1, 0)
        checkmark.BackgroundTransparency = 1
        checkmark.Text = "✓"
        checkmark.TextColor3 = Color3.new(1, 1, 1)
        checkmark.TextSize = 16
        checkmark.Font = Enum.Font.GothamBold
        checkmark.Parent = equippedBadge
    end

    return slot
end
```

## Settings UI System

### Toggle Switches and Sliders

```lua
local TweenService = game:GetService("TweenService")

-- Toggle switch component
local function createToggle(name, defaultValue, onChange)
    local container = Instance.new("Frame")
    container.Size = UDim2.new(1, 0, 0, 50)
    container.BackgroundTransparency = 1

    local label = Instance.new("TextLabel")
    label.Size = UDim2.new(0.6, 0, 1, 0)
    label.BackgroundTransparency = 1
    label.Text = name
    label.TextColor3 = Color3.new(1, 1, 1)
    label.TextSize = 16
    label.Font = Enum.Font.GothamMedium
    label.TextXAlignment = Enum.TextXAlignment.Left
    label.Parent = container

    -- Toggle track
    local track = Instance.new("Frame")
    track.Size = UDim2.new(0, 50, 0, 26)
    track.Position = UDim2.new(1, -60, 0.5, 0)
    track.AnchorPoint = Vector2.new(0, 0.5)
    track.BackgroundColor3 = defaultValue and Color3.fromRGB(0, 180, 100) or Color3.fromRGB(80, 80, 100)
    track.Parent = container
    Instance.new("UICorner", track).CornerRadius = UDim.new(1, 0)

    -- Toggle knob
    local knob = Instance.new("Frame")
    knob.Size = UDim2.new(0, 22, 0, 22)
    knob.Position = defaultValue and UDim2.new(1, -24, 0.5, 0) or UDim2.new(0, 2, 0.5, 0)
    knob.AnchorPoint = Vector2.new(0, 0.5)
    knob.BackgroundColor3 = Color3.new(1, 1, 1)
    knob.Parent = track
    Instance.new("UICorner", knob).CornerRadius = UDim.new(1, 0)

    local isOn = defaultValue

    -- Click handler
    local button = Instance.new("TextButton")
    button.Size = UDim2.new(1, 0, 1, 0)
    button.BackgroundTransparency = 1
    button.Text = ""
    button.Parent = track

    button.MouseButton1Click:Connect(function()
        isOn = not isOn

        local targetKnobPos = isOn and UDim2.new(1, -24, 0.5, 0) or UDim2.new(0, 2, 0.5, 0)
        local targetColor = isOn and Color3.fromRGB(0, 180, 100) or Color3.fromRGB(80, 80, 100)

        TweenService:Create(knob, TweenInfo.new(0.2, Enum.EasingStyle.Quart), {
            Position = targetKnobPos
        }):Play()

        TweenService:Create(track, TweenInfo.new(0.2), {
            BackgroundColor3 = targetColor
        }):Play()

        if onChange then onChange(isOn) end
    end)

    return container
end

-- Slider component
local function createSlider(name, minValue, maxValue, defaultValue, onChange)
    local container = Instance.new("Frame")
    container.Size = UDim2.new(1, 0, 0, 70)
    container.BackgroundTransparency = 1

    local label = Instance.new("TextLabel")
    label.Size = UDim2.new(0.7, 0, 0, 25)
    label.BackgroundTransparency = 1
    label.Text = name
    label.TextColor3 = Color3.new(1, 1, 1)
    label.TextSize = 16
    label.Font = Enum.Font.GothamMedium
    label.TextXAlignment = Enum.TextXAlignment.Left
    label.Parent = container

    local valueLabel = Instance.new("TextLabel")
    valueLabel.Size = UDim2.new(0.3, 0, 0, 25)
    valueLabel.Position = UDim2.new(0.7, 0, 0, 0)
    valueLabel.BackgroundTransparency = 1
    valueLabel.Text = tostring(math.floor(defaultValue))
    valueLabel.TextColor3 = Color3.fromRGB(0, 180, 255)
    valueLabel.TextSize = 16
    valueLabel.Font = Enum.Font.GothamBold
    valueLabel.TextXAlignment = Enum.TextXAlignment.Right
    valueLabel.Parent = container

    -- Slider track
    local track = Instance.new("Frame")
    track.Size = UDim2.new(1, 0, 0, 8)
    track.Position = UDim2.new(0, 0, 0, 40)
    track.BackgroundColor3 = Color3.fromRGB(60, 60, 80)
    track.Parent = container
    Instance.new("UICorner", track).CornerRadius = UDim.new(1, 0)

    -- Filled portion
    local fill = Instance.new("Frame")
    local initialRatio = (defaultValue - minValue) / (maxValue - minValue)
    fill.Size = UDim2.new(initialRatio, 0, 1, 0)
    fill.BackgroundColor3 = Color3.fromRGB(0, 180, 255)
    fill.Parent = track
    Instance.new("UICorner", fill).CornerRadius = UDim.new(1, 0)

    -- Knob
    local knob = Instance.new("Frame")
    knob.Size = UDim2.new(0, 20, 0, 20)
    knob.Position = UDim2.new(initialRatio, 0, 0.5, 0)
    knob.AnchorPoint = Vector2.new(0.5, 0.5)
    knob.BackgroundColor3 = Color3.new(1, 1, 1)
    knob.ZIndex = 2
    knob.Parent = track
    Instance.new("UICorner", knob).CornerRadius = UDim.new(1, 0)

    -- Add shadow to knob
    local knobStroke = Instance.new("UIStroke")
    knobStroke.Color = Color3.fromRGB(0, 120, 200)
    knobStroke.Thickness = 2
    knobStroke.Parent = knob

    -- Drag functionality
    local dragging = false
    local UserInputService = game:GetService("UserInputService")

    local dragButton = Instance.new("TextButton")
    dragButton.Size = UDim2.new(1, 20, 0, 30)
    dragButton.Position = UDim2.new(0, -10, 0.5, 0)
    dragButton.AnchorPoint = Vector2.new(0, 0.5)
    dragButton.BackgroundTransparency = 1
    dragButton.Text = ""
    dragButton.ZIndex = 3
    dragButton.Parent = track

    dragButton.InputBegan:Connect(function(input)
        if input.UserInputType == Enum.UserInputType.MouseButton1 or
           input.UserInputType == Enum.UserInputType.Touch then
            dragging = true
        end
    end)

    dragButton.InputEnded:Connect(function(input)
        if input.UserInputType == Enum.UserInputType.MouseButton1 or
           input.UserInputType == Enum.UserInputType.Touch then
            dragging = false
        end
    end)

    local function updateSlider(inputPos)
        local trackAbsPos = track.AbsolutePosition
        local trackAbsSize = track.AbsoluteSize

        local relativeX = math.clamp(inputPos.X - trackAbsPos.X, 0, trackAbsSize.X)
        local ratio = relativeX / trackAbsSize.X

        fill.Size = UDim2.new(ratio, 0, 1, 0)
        knob.Position = UDim2.new(ratio, 0, 0.5, 0)

        local value = minValue + (maxValue - minValue) * ratio
        valueLabel.Text = tostring(math.floor(value))

        if onChange then onChange(value) end
    end

    UserInputService.InputChanged:Connect(function(input)
        if dragging then
            if input.UserInputType == Enum.UserInputType.MouseMovement or
               input.UserInputType == Enum.UserInputType.Touch then
                updateSlider(input.Position)
            end
        end
    end)

    dragButton.MouseButton1Click:Connect(function()
        local mouse = game:GetService("Players").LocalPlayer:GetMouse()
        updateSlider(Vector2.new(mouse.X, mouse.Y))
    end)

    return container
end

-- Complete settings panel
local function createSettingsUI()
    local screenGui = Instance.new("ScreenGui")
    screenGui.Name = "SettingsUI"
    screenGui.ResetOnSpawn = false

    local mainFrame = Instance.new("Frame")
    mainFrame.Size = UDim2.new(0, 450, 0, 550)
    mainFrame.Position = UDim2.new(0.5, 0, 0.5, 0)
    mainFrame.AnchorPoint = Vector2.new(0.5, 0.5)
    mainFrame.BackgroundColor3 = Color3.fromRGB(25, 25, 40)
    mainFrame.Parent = screenGui

    Instance.new("UICorner", mainFrame).CornerRadius = UDim.new(0, 16)

    -- Settings scroll container
    local settingsContainer = Instance.new("ScrollingFrame")
    settingsContainer.Size = UDim2.new(1, -30, 1, -100)
    settingsContainer.Position = UDim2.new(0, 15, 0, 80)
    settingsContainer.BackgroundTransparency = 1
    settingsContainer.ScrollBarThickness = 4
    settingsContainer.CanvasSize = UDim2.new(0, 0, 0, 0)
    settingsContainer.AutomaticCanvasSize = Enum.AutomaticSize.Y
    settingsContainer.Parent = mainFrame

    local listLayout = Instance.new("UIListLayout")
    listLayout.SortOrder = Enum.SortOrder.LayoutOrder
    listLayout.Padding = UDim.new(0, 15)
    listLayout.Parent = settingsContainer

    -- Add settings sections
    local function createSection(title)
        local section = Instance.new("Frame")
        section.Size = UDim2.new(1, 0, 0, 30)
        section.BackgroundTransparency = 1

        local sectionTitle = Instance.new("TextLabel")
        sectionTitle.Size = UDim2.new(1, 0, 1, 0)
        sectionTitle.BackgroundTransparency = 1
        sectionTitle.Text = title
        sectionTitle.TextColor3 = Color3.fromRGB(0, 180, 255)
        sectionTitle.TextSize = 18
        sectionTitle.Font = Enum.Font.GothamBold
        sectionTitle.TextXAlignment = Enum.TextXAlignment.Left
        sectionTitle.Parent = section

        return section
    end

    -- Audio Section
    createSection("🔊 AUDIO").Parent = settingsContainer
    createSlider("Master Volume", 0, 100, 80, function(v) print("Master:", v) end).Parent = settingsContainer
    createSlider("Music Volume", 0, 100, 60, function(v) print("Music:", v) end).Parent = settingsContainer
    createSlider("SFX Volume", 0, 100, 100, function(v) print("SFX:", v) end).Parent = settingsContainer

    -- Graphics Section
    createSection("🎮 GRAPHICS").Parent = settingsContainer
    createToggle("Particles", true, function(v) print("Particles:", v) end).Parent = settingsContainer
    createToggle("Shadows", true, function(v) print("Shadows:", v) end).Parent = settingsContainer
    createSlider("Render Distance", 100, 1000, 500, function(v) print("Render:", v) end).Parent = settingsContainer

    -- Gameplay Section
    createSection("⚙️ GAMEPLAY").Parent = settingsContainer
    createToggle("Auto-Collect", true, function(v) print("Auto:", v) end).Parent = settingsContainer
    createToggle("Screen Shake", false, function(v) print("Shake:", v) end).Parent = settingsContainer

    return screenGui
end
```

## Daily Reward System

### Calendar-Style Daily Rewards

```lua
local TweenService = game:GetService("TweenService")

local REWARDS = {
    {day = 1, reward = 100, type = "coins", icon = "🪙"},
    {day = 2, reward = 200, type = "coins", icon = "🪙"},
    {day = 3, reward = 5, type = "gems", icon = "💎"},
    {day = 4, reward = 500, type = "coins", icon = "🪙"},
    {day = 5, reward = 10, type = "gems", icon = "💎"},
    {day = 6, reward = 1000, type = "coins", icon = "🪙"},
    {day = 7, reward = 50, type = "gems", icon = "💎"},  -- Big reward!
}

local function createDailyRewardUI()
    local screenGui = Instance.new("ScreenGui")
    screenGui.Name = "DailyRewardUI"
    screenGui.ResetOnSpawn = false

    local mainFrame = Instance.new("Frame")
    mainFrame.Size = UDim2.new(0, 500, 0, 400)
    mainFrame.Position = UDim2.new(0.5, 0, 0.5, 0)
    mainFrame.AnchorPoint = Vector2.new(0.5, 0.5)
    mainFrame.BackgroundColor3 = Color3.fromRGB(25, 25, 45)
    mainFrame.Parent = screenGui
    mainFrame.Visible = false

    Instance.new("UICorner", mainFrame).CornerRadius = UDim.new(0, 16)

    -- Title
    local title = Instance.new("TextLabel")
    title.Size = UDim2.new(1, 0, 0, 50)
    title.BackgroundTransparency = 1
    title.Text = "🎁 DAILY REWARDS"
    title.TextColor3 = Color3.fromRGB(255, 220, 100)
    title.TextSize = 28
    title.Font = Enum.Font.GothamBold
    title.Parent = mainFrame

    -- Reward calendar grid
    local calendarFrame = Instance.new("Frame")
    calendarFrame.Size = UDim2.new(0.95, 0, 0, 200)
    calendarFrame.Position = UDim2.new(0.5, 0, 0, 70)
    calendarFrame.AnchorPoint = Vector2.new(0.5, 0)
    calendarFrame.BackgroundTransparency = 1
    calendarFrame.Parent = mainFrame

    local gridLayout = Instance.new("UIGridLayout")
    gridLayout.CellSize = UDim2.new(0, 60, 0, 80)
    gridLayout.CellPadding = UDim2.new(0, 10, 0, 10)
    gridLayout.HorizontalAlignment = Enum.HorizontalAlignment.Center
    gridLayout.SortOrder = Enum.SortOrder.LayoutOrder
    gridLayout.Parent = calendarFrame

    -- Current day (would come from DataStore in real game)
    local currentDay = 3  -- Example: player is on day 3
    local canClaim = true  -- Example: player can claim today

    -- Create day cells
    for i, rewardData in ipairs(REWARDS) do
        local dayCell = Instance.new("Frame")
        dayCell.Size = UDim2.new(1, 0, 1, 0)
        dayCell.LayoutOrder = i
        dayCell.Parent = calendarFrame

        -- State-based styling
        local isClaimed = i < currentDay
        local isToday = i == currentDay
        local isFuture = i > currentDay

        local bgColor
        if isClaimed then
            bgColor = Color3.fromRGB(60, 60, 80)  -- Greyed out
        elseif isToday and canClaim then
            bgColor = Color3.fromRGB(0, 150, 100)  -- Claimable (green)
        elseif isToday then
            bgColor = Color3.fromRGB(100, 100, 50)  -- Today but claimed
        else
            bgColor = Color3.fromRGB(45, 45, 65)  -- Locked
        end

        dayCell.BackgroundColor3 = bgColor
        Instance.new("UICorner", dayCell).CornerRadius = UDim.new(0, 10)

        -- Day number
        local dayLabel = Instance.new("TextLabel")
        dayLabel.Size = UDim2.new(1, 0, 0, 20)
        dayLabel.BackgroundTransparency = 1
        dayLabel.Text = "Day " .. i
        dayLabel.TextColor3 = isClaimed and Color3.fromRGB(120, 120, 140) or Color3.new(1, 1, 1)
        dayLabel.TextSize = 12
        dayLabel.Font = Enum.Font.GothamMedium
        dayLabel.Parent = dayCell

        -- Reward icon
        local rewardIcon = Instance.new("TextLabel")
        rewardIcon.Size = UDim2.new(1, 0, 0, 30)
        rewardIcon.Position = UDim2.new(0, 0, 0, 22)
        rewardIcon.BackgroundTransparency = 1
        rewardIcon.Text = rewardData.icon
        rewardIcon.TextSize = 24
        rewardIcon.Parent = dayCell

        -- Reward amount
        local amountLabel = Instance.new("TextLabel")
        amountLabel.Size = UDim2.new(1, 0, 0, 20)
        amountLabel.Position = UDim2.new(0, 0, 1, -25)
        amountLabel.BackgroundTransparency = 1
        amountLabel.Text = "+" .. rewardData.reward
        amountLabel.TextColor3 = isClaimed and Color3.fromRGB(120, 120, 140) or Color3.fromRGB(255, 220, 100)
        amountLabel.TextSize = 14
        amountLabel.Font = Enum.Font.GothamBold
        amountLabel.Parent = dayCell

        -- Checkmark for claimed
        if isClaimed then
            local check = Instance.new("TextLabel")
            check.Size = UDim2.new(1, 0, 1, 0)
            check.BackgroundTransparency = 1
            check.Text = "✓"
            check.TextColor3 = Color3.fromRGB(0, 200, 100)
            check.TextSize = 32
            check.Font = Enum.Font.GothamBold
            check.Parent = dayCell
        end

        -- Glow effect for today
        if isToday and canClaim then
            local glow = Instance.new("UIStroke")
            glow.Color = Color3.fromRGB(0, 255, 150)
            glow.Thickness = 3
            glow.Parent = dayCell

            -- Pulsing animation
            task.spawn(function()
                while dayCell.Parent do
                    TweenService:Create(glow, TweenInfo.new(0.8, Enum.EasingStyle.Sine), {
                        Transparency = 0.7
                    }):Play()
                    task.wait(0.8)
                    TweenService:Create(glow, TweenInfo.new(0.8, Enum.EasingStyle.Sine), {
                        Transparency = 0
                    }):Play()
                    task.wait(0.8)
                end
            end)
        end
    end

    -- Claim button
    local claimButton = Instance.new("TextButton")
    claimButton.Size = UDim2.new(0.6, 0, 0, 55)
    claimButton.Position = UDim2.new(0.5, 0, 1, -80)
    claimButton.AnchorPoint = Vector2.new(0.5, 0)
    claimButton.BackgroundColor3 = canClaim and Color3.fromRGB(0, 200, 100) or Color3.fromRGB(80, 80, 100)
    claimButton.Text = canClaim and "CLAIM REWARD!" or "COME BACK TOMORROW"
    claimButton.TextColor3 = Color3.new(1, 1, 1)
    claimButton.TextSize = 20
    claimButton.Font = Enum.Font.GothamBold
    claimButton.Parent = mainFrame
    Instance.new("UICorner", claimButton).CornerRadius = UDim.new(0, 12)

    if canClaim then
        claimButton.MouseButton1Click:Connect(function()
            local reward = REWARDS[currentDay]
            print("Claimed:", reward.reward, reward.type)
            -- Fire claim event to server
            -- Server validates and grants reward
        end)
    end

    return screenGui, mainFrame
end

-- Pulsing notification button for daily reward
local function createDailyRewardButton(parent, onClick)
    local button = Instance.new("ImageButton")
    button.Size = UDim2.new(0, 70, 0, 70)
    button.Position = UDim2.new(0, 15, 0.5, 0)
    button.AnchorPoint = Vector2.new(0, 0.5)
    button.BackgroundColor3 = Color3.fromRGB(200, 50, 50)
    button.Image = "rbxassetid://..."  -- Gift icon
    button.Parent = parent

    Instance.new("UICorner", button).CornerRadius = UDim.new(0, 12)

    -- Pulsing animation
    task.spawn(function()
        while button.Parent do
            TweenService:Create(button, TweenInfo.new(0.6, Enum.EasingStyle.Sine), {
                Size = UDim2.new(0, 78, 0, 78)
            }):Play()
            task.wait(0.6)
            TweenService:Create(button, TweenInfo.new(0.6, Enum.EasingStyle.Sine), {
                Size = UDim2.new(0, 70, 0, 70)
            }):Play()
            task.wait(0.6)
        end
    end)

    -- Notification badge
    local badge = Instance.new("Frame")
    badge.Size = UDim2.new(0, 24, 0, 24)
    badge.Position = UDim2.new(1, -5, 0, -5)
    badge.AnchorPoint = Vector2.new(0.5, 0.5)
    badge.BackgroundColor3 = Color3.fromRGB(255, 80, 80)
    badge.Parent = button
    Instance.new("UICorner", badge).CornerRadius = UDim.new(1, 0)

    local badgeText = Instance.new("TextLabel")
    badgeText.Size = UDim2.new(1, 0, 1, 0)
    badgeText.BackgroundTransparency = 1
    badgeText.Text = "!"
    badgeText.TextColor3 = Color3.new(1, 1, 1)
    badgeText.TextSize = 16
    badgeText.Font = Enum.Font.GothamBold
    badgeText.Parent = badge

    button.MouseButton1Click:Connect(onClick)

    return button
end
```
