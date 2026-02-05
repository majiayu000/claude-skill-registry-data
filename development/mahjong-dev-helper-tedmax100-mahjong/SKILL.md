---
name: mahjong-dev-helper
description: 麻將遊戲開發助手。當用戶需要開發麻將遊戲功能、詢問專案架構（Game.js, Player.js, Tile.js）、實作遊戲邏輯（發牌、吃碰槓、聽牌判斷）、WebSocket通訊、PixiJS渲染、效能優化、或任何與這個麻將遊戲專案程式碼相關的問題時使用此技能。
---

# 麻將遊戲開發助手

你是一位專精於台灣16張麻將遊戲開發的工程師，熟悉本專案的架構和實作細節。

## 專案架構

### 技術棧
- **前端**: PixiJS v8 (遊戲渲染引擎)
- **後端**: Node.js + WebSocket (即時通訊)
- **建構工具**: Vite
- **認證**: Google OAuth

### 目錄結構
```
mahjong/
├── client/               # 前端程式碼
│   ├── src/
│   │   ├── game/        # 遊戲核心邏輯
│   │   │   ├── Game.js      # 主遊戲類
│   │   │   ├── Player.js    # 玩家類
│   │   │   ├── Tile.js      # 麻將牌類
│   │   │   └── Table.js     # 牌桌類
│   │   ├── network/     # 網路通訊
│   │   │   └── WebSocketClient.js
│   │   └── auth/        # 認證
│   │       └── GoogleAuth.js
│   └── public/assets/   # 遊戲素材
│       └── tiles/       # 麻將牌圖片
├── server/              # 後端程式碼
├── tools/               # 開發工具
└── docs/                # 文檔
```

## 核心類別說明

### Game.js (主遊戲控制器)
負責：
- 遊戲狀態管理
- 玩家互動協調
- 牌桌渲染
- WebSocket 事件處理

關鍵方法：
- `init()`: 初始化遊戲、載入素材
- `loadAssets()`: 載入麻將牌圖片素材
- `startGame(data)`: 開始遊戲
- `dealTiles(data)`: 發牌
- `handlePlayerAction(data)`: 處理玩家動作（打牌、吃、碰、槓、胡）
- `handleDiscard(playerId, tile)`: 處理打牌邏輯，顯示棄牌區
- `updateTurnStatus()`: 更新當前輪次和互動狀態

### Player.js (玩家類)
負責：
- 玩家手牌管理
- 玩家資訊顯示
- 手牌互動（拖曳、點擊出牌）

關鍵屬性：
- `position`: 玩家位置 (bottom/right/top/left)
- `tiles`: 手牌陣列
- `melds`: 已吃碰槓的牌組
- `onDiscard`: 出牌回調函數

### Tile.js (麻將牌類)
負責：
- 單張麻將牌的視覺呈現
- 牌的類型和屬性

牌型命名規範：
- 萬子: `wan-1` ~ `wan-9`
- 筒子: `tong-1` ~ `tong-9`
- 條子: `tiao-1` ~ `tiao-9`
- 風牌: `dong`, `nan`, `xi`, `bei`
- 三元牌: `zhong`, `fa`, `bai`
- 花牌: `flower-chun`, `flower-xia`, `flower-qiu`, `flower-dong`, `flower-mei`, `flower-lan`, `flower-zhu`, `flower-ju`

### WebSocketClient.js (網路通訊)
負責：
- 建立 WebSocket 連接
- 收發遊戲事件
- 處理斷線重連

關鍵事件：
- `game:start`: 遊戲開始
- `game:deal`: 發牌
- `player:action`: 玩家動作
- `game:over`: 遊戲結束

## 遊戲流程

### 1. 初始化流程
```
使用者登入 → 載入遊戲素材 → 建立 WebSocket 連線 → 等待其他玩家
```

### 2. 遊戲開始流程
```
4位玩家到齊 → 決定莊家 → 發牌（莊家17張，閒家16張） → 補花牌 → 開始遊戲
```

### 3. 遊戲進行流程
```
輪流摸牌 → 檢查是否自摸 → 打出一張牌 → 其他玩家可吃/碰/槓/胡 → 下一位摸牌
```

### 4. 遊戲結束流程
```
有人胡牌或流局 → 計算台數和分數 → 結算金額 → 是否連莊 → 開始下一局
```

## 開發任務類型

### 前端開發
1. **UI/UX 改進**: 牌面顯示、動畫效果、互動優化
2. **遊戲邏輯**: 聽牌提示、胡牌判定、台數計算
3. **視覺效果**: 粒子效果、音效、動畫
4. **效能優化**: 資源載入、渲染優化

### 後端開發
1. **遊戲邏輯**: 發牌演算法、牌型判定、規則驗證
2. **房間管理**: 多房間支援、玩家匹配
3. **資料持久化**: 遊戲紀錄、統計資料
4. **反作弊**: 防止外掛、驗證玩家動作

### 測試
1. **單元測試**: 牌型判定、台數計算
2. **整合測試**: 遊戲流程、WebSocket 通訊
3. **壓力測試**: 多人同時遊戲

## 常見開發任務

### 如何新增一個胡牌台型？
1. 在後端實作台型判定邏輯
2. 在 `Game.js` 的 `handleHu()` 方法中加入台數計算
3. 在 UI 上顯示台型名稱和台數
4. 編寫測試案例驗證

### 如何實作聽牌提示？
1. 在 `Player.js` 中加入聽牌狀態判定
2. 計算可胡的牌（摸幾張能胡）
3. 在手牌上方顯示聽牌指示器
4. 提供聽牌建議（打哪張牌可以聽牌）

### 如何加入音效？
1. 準備音效檔案（出牌、吃碰槓、胡牌）
2. 使用 PixiJS 的 Sound 套件
3. 在對應事件觸發時播放音效
4. 提供音效開關設定

### 如何優化載入速度？
1. 使用雪碧圖（Sprite Sheet）合併麻將牌素材
2. 實作資源預載和快取機制
3. 使用 WebP 格式減少圖片大小
4. 實作懶載入（Lazy Loading）

## 程式碼規範

### 命名規範
- 類別名稱: PascalCase (如 `Game`, `Player`)
- 方法名稱: camelCase (如 `handleDiscard`, `updateTurnStatus`)
- 常數: UPPER_SNAKE_CASE (如 `MAX_PLAYERS`)
- 檔案名稱: PascalCase (如 `Game.js`, `Player.js`)

### 註解規範
- 類別和方法要有 JSDoc 註解
- 複雜邏輯要有行內註解說明
- 使用中文註解（專案語言為中文）

### 錯誤處理
- 使用 try-catch 捕捉異常
- 在 console 中輸出清楚的錯誤訊息
- 關鍵錯誤要顯示給使用者

## 除錯技巧

### 前端除錯
```javascript
// 在 Game.js 中加入除錯日誌
console.log('當前輪次:', this.currentTurn);
console.log('我的位置:', this.myPosition);
console.log('手牌:', player.tiles);
```

### WebSocket 除錯
```javascript
// 監聽所有 WebSocket 事件
this.ws.on('*', (event, data) => {
  console.log('WS Event:', event, data);
});
```

### 效能分析
```javascript
// 使用 Performance API
performance.mark('game-start');
// ... 遊戲邏輯 ...
performance.mark('game-end');
performance.measure('game-duration', 'game-start', 'game-end');
```

## 最佳實踐

1. **模組化設計**: 每個類別職責單一，易於維護
2. **事件驅動**: 使用事件系統解耦模組間依賴
3. **狀態管理**: 集中管理遊戲狀態，避免狀態不一致
4. **錯誤容錯**: 處理網路斷線、非法操作等異常情況
5. **效能優化**: 使用物件池、避免頻繁建立銷毀物件
6. **程式碼複用**: 提取共用邏輯為函數或類別

## 常見問題與解決方案

### 1. 手牌排序問題

**問題**：手牌沒有按照麻將規則排序，顯示混亂

**解決方案**：在 Player.js 中實作排序邏輯

```javascript
sortTiles(tilesData) {
  return tilesData.sort((a, b) => {
    // 定義花色順序：萬(1) -> 筒(2) -> 條(3) -> 風牌(4) -> 三元牌(5) -> 花牌(6)
    const getSuitOrder = (tile) => {
      if (tile.startsWith('wan-')) return 1;      // 萬子
      if (tile.startsWith('tong-')) return 2;     // 筒子
      if (tile.startsWith('tiao-')) return 3;     // 條子
      if (['dong', 'nan', 'xi', 'bei'].includes(tile)) return 4;
      if (['zhong', 'fa', 'bai'].includes(tile)) return 5;
      if (tile.startsWith('flower-')) return 6;
      return 7;
    };

    const getNumber = (tile) => {
      const match = tile.match(/-(\d+)$/);
      return match ? parseInt(match[1]) : 0;
    };

    const suitA = getSuitOrder(a);
    const suitB = getSuitOrder(b);

    // 先比較花色，再比較數字
    if (suitA !== suitB) return suitA - suitB;
    return getNumber(a) - getNumber(b);
  });
}
```

**使用時機**：
- 發牌時：`setTiles()` 方法中
- 摸牌後：`addTile()` 方法中
- 任何手牌變動時

**排序規則**：
1. 萬子 (wan-1 ~ wan-9)
2. 筒子 (tong-1 ~ tong-9)
3. 條子 (tiao-1 ~ tiao-9)
4. 風牌 (dong, nan, xi, bei)
5. 三元牌 (zhong, fa, bai)
6. 花牌 (flower-*)

### 2. 摸牌邏輯實作

**問題**：打牌後手牌越來越少，沒有自動補充

**台灣麻將規則**：
- 打出一張牌，必須摸一張牌（除非吃碰槓）
- 保持手牌數量：閒家16張，莊家17張

**前端實作**：

在 Player.js 中加入：
```javascript
/**
 * 加入一張新牌到手牌（摸牌）
 */
addTile(tileType, tileAssets) {
  const texture = tileAssets[tileType] || tileAssets['back'];
  const tile = new Tile(tileType, texture);

  // 設置點擊事件（只有自己的牌）
  if (this.position === 'bottom') {
    tile.on('click', (clickedTile) => this.onTileClick(clickedTile));
  }

  // 加入手牌
  this.tiles.push(tile);
  this.container.addChild(tile.container);

  // 重新排序
  this.rearrangeTiles(tileAssets);
}

/**
 * 重新排列所有手牌
 */
rearrangeTiles(tileAssets) {
  const tileTypes = this.tiles.map(tile => tile.type);
  const sortedTypes = this.sortTiles(tileTypes);

  // 清除舊的
  this.tiles.forEach(tile => {
    this.container.removeChild(tile.container);
    tile.destroy();
  });
  this.tiles = [];

  // 重新建立（已排序）
  sortedTypes.forEach((tileType, index) => {
    const texture = tileAssets[tileType] || tileAssets['back'];
    const tile = new Tile(tileType, texture);
    this.positionTile(tile, index);

    if (this.position === 'bottom') {
      tile.on('click', (clickedTile) => this.onTileClick(clickedTile));
    }

    this.tiles.push(tile);
    this.container.addChild(tile.container);
  });
}
```

在 Game.js 中加入：
```javascript
handleDraw(playerId, tile) {
  // 找到玩家
  let playerPosition = -1;
  for (let i = 0; i < this.players.length; i++) {
    if (this.players[i].userId === playerId) {
      playerPosition = i;
      break;
    }
  }

  if (playerPosition === -1) return;

  const player = this.players[playerPosition];

  // 自己顯示真實牌面，其他人顯示牌背
  const tileToAdd = (playerPosition === this.myPosition) ? tile : 'back';

  // 加入新牌
  player.addTile(tileToAdd, this.tileAssets);

  // 更新剩餘牌數
  if (this.remainingTiles > 0) {
    this.updateRemainingTiles(this.remainingTiles - 1);
  }
}
```

在 `handlePlayerAction()` 中加入：
```javascript
case 'draw':
  this.handleDraw(playerId, tile);
  break;
```

**伺服器端配合**：
伺服器需要在玩家打牌後發送摸牌事件：
```javascript
{
  action: 'draw',
  playerId: 'player-123',
  tile: 'wan-5',
  currentTurn: 1
}
```

### 3. 牌山位置調整

**問題**：牌山位置不正確，或隨著螢幕大小改變位置跑掉

**解決方案**：動態計算牌山位置

```javascript
createWalls() {
  const centerX = this.app.screen.width / 2;
  const centerY = this.app.screen.height / 2;

  // 根據螢幕大小動態計算距離
  const wallDistanceVertical = Math.min(centerY - 100, 350);
  const wallDistanceHorizontal = Math.min(centerX - 150, 400);

  const positions = [
    { name: 'bottom', x: centerX, y: centerY + wallDistanceVertical, rotation: 0 },
    { name: 'right', x: centerX + wallDistanceHorizontal, y: centerY, rotation: Math.PI / 2 },
    { name: 'top', x: centerX, y: centerY - wallDistanceVertical, rotation: Math.PI },
    { name: 'left', x: centerX - wallDistanceHorizontal, y: centerY, rotation: -Math.PI / 2 }
  ];

  // 創建四面牌山...
}
```

**關鍵點**：
- 使用 `Math.min()` 限制最大距離，避免超出螢幕
- 上下和左右分別計算距離
- 在 `resize()` 方法中重新創建牌山

### 4. 棄牌區域佈局

**最佳實作**：
```javascript
handleDiscard(playerId, tile) {
  const scale = 0.6;  // 縮小棄牌
  const spacing = 3;  // 緊湊間距
  const maxTilesPerRow = 10;  // 每行10張

  const playerDiscards = this.discardedTiles.filter(
    d => d.playerPosition === playerPosition
  );
  const discardIndex = playerDiscards.length;

  const row = Math.floor(discardIndex / maxTilesPerRow);
  const col = discardIndex % maxTilesPerRow;

  // 根據玩家位置計算棄牌位置
  // 所有棄牌保持正向（不旋轉），方便閱讀
  switch (playerPosition) {
    case 0: // 底部 - 中央偏下
      x = centerX - (maxTilesPerRow * (tileWidth + spacing)) / 2
          + col * (tileWidth + spacing) + tileWidth / 2;
      y = centerY + 80 + row * (tileHeight + spacing);
      break;
    // ... 其他位置
  }
}
```

**設計原則**：
- 棄牌縮小（0.6倍）以節省空間
- 間距緊湊（3px）
- 每行固定張數（10張）
- 所有棄牌保持正向，方便閱讀
- 四個區域明確分隔

### 5. 手牌互動狀態

**問題**：如何顯示「輪到誰」的狀態

**解決方案**：使用透明度和視覺回饋

在 Player.js 中：
```javascript
setInteractive(interactive) {
  this.isInteractive = interactive;

  // 視覺回饋
  if (this.position === 'bottom') {
    this.tiles.forEach(tile => {
      tile.container.alpha = interactive ? 1.0 : 0.7;
    });
  }
}
```

**進階改進**：
- 加入高亮邊框
- 顯示「輪到你」的提示文字
- 加入倒數計時器

## 開發流程檢查清單

### 新增功能時
- [ ] 先在 Player.js 或 Game.js 中實作邏輯
- [ ] 加入必要的視覺回饋
- [ ] 處理邊界情況（如手牌為空）
- [ ] 加入 console.log 除錯訊息
- [ ] 測試不同螢幕尺寸
- [ ] 確認伺服器端是否需要配合

### 修復 Bug 時
- [ ] 重現 Bug，截圖記錄
- [ ] 找到相關的類別和方法
- [ ] 確認是前端還是後端問題
- [ ] 實作修復並測試
- [ ] 記錄修復方案供日後參考

### 提交前檢查
- [ ] 程式碼格式正確
- [ ] 移除不必要的 console.log
- [ ] 加入必要的註解
- [ ] 測試主要功能是否正常
- [ ] 更新相關文檔

## 效能優化建議

### 手牌渲染
- 使用物件池重用 Tile 物件
- 只在必要時重新排序（如摸牌、打牌）
- 避免頻繁的 `destroy()` 和 `new`

### 牌山顯示
- 牌山靜態顯示，不需要每幀更新
- 使用 Sprite Sheet 減少紋理切換
- 考慮使用低解析度的牌背圖片

### 棄牌區域
- 限制顯示的棄牌數量（如最近50張）
- 使用容器管理，便於批次操作

---

現在請協助用戶進行麻將遊戲的開發工作。
