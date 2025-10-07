# Grasshopper 參數化設計教學文件

**檔案：設計新.gh**

## 課程概述

本教學基於一個進階的 Grasshopper 參數化設計專案，涵蓋：
- 表面幾何處理與映射
- 數據樹結構操作
- 圖案生成與細分
- 向量運算與幾何變換

**總組件數：145 個**
**難度等級：中高級**

---

## 第一部分：核心概念

### 1.1 數據結構基礎

本專案大量使用**數據樹（Data Tree）**結構，是 Grasshopper 中處理複雜數據的關鍵：

```
{0} - 第一個分支
  [0] - 第一個項目
  [1] - 第二個項目
{1} - 第二個分支
  [0] - 第一個項目
  [1] - 第二個項目
```

#### 關鍵組件
- **Explode Tree** - 將樹狀結構拆解為分支
- **Shift Paths** - 偏移數據路徑索引
- **Relay** - 數據中繼，用於組織線路

---

## 第二部分：主要技術模組

### 2.1 點與曲線處理

#### 組件清單
| 組件 | 功能 | 用途 |
|------|------|------|
| `Deconstruct Point` | 拆解點坐標 | 提取 X, Y, Z 值 |
| `Create Set` | 創建集合 | 去除重複點 |
| `Member Index` | 查找索引 | 確定點在集合中的位置 |
| `Fit Line` | 擬合線條 | 通過點創建最佳擬合線 |
| `removeDuplicatePts` | 移除重複點 | 清理點集合 |

#### 工作流程示例
```
Points → Deconstruct → Create Set → Member Index → List Item → Fit Line
```

**學習重點**：

- 點的拆解與重組
- 集合運算去重
- 索引查找與列表操作

---

### 2.2 Delaunay 三角化與網格

#### 核心組件
- **Delaunay Edges** (`Component_Connectivity`) - 創建 Delaunay 三角網格
- **End Points** - 提取線段端點
- **Cull Pattern** - 按圖案篩選

#### 應用場景
Delaunay 三角化常用於：
- 創建不規則網格結構
- 點雲表面重建
- 參數化立面設計

#### 與向量結合
```
Delaunay Edges → Cross Product (Unit X/Y) → Gate And → Cull Pattern
```

**技巧**：使用 `Cross Product` 和 `Unit Vector` 可以篩選特定方向的邊緣。

---

### 2.3 表面操作與映射

#### 關鍵組件組
| 組件 | 功能 |
|------|------|
| `Surface Closest Point` | 找到表面最近點 |
| `Evaluate Surface` | 評估表面參數 |
| `Map to Surface` | 映射幾何到表面 |
| `Surface Morph` | 表面變形 |
| `Unroll Brep` | 展開曲面 |

#### 典型工作流
1. **創建基礎圖案**（Rectangle）
2. **映射到目標表面**（Map to Surface）
3. **評估表面法向量**（Evaluate Surface）
4. **應用變換**（Move, Extrude）

#### 案例：菱形面板
```
Rectangle → Area → Vector 2Pt → Amplitude → Move → Map to Surface
```

**教學要點**：
- UV 參數空間概念
- 平面到曲面的映射原理
- 法向量在設計中的應用

---

### 2.4 三角形細分系統

組件：**Subdivide Triangle** (`TriSub`)

#### 應用場景
- Diamond Panels（菱形面板）
- 多層次細分結構
- 漸變密度網格

#### 配合使用
```
Surface → Subdivide Triangle → Surface Closest Point → Evaluate Surface
```

---

### 2.5 數據列表操作（重點模組）

這是專案中的核心技術，用於創建交錯連接的線條網格。

#### 組件清單
| 組件 | 功能 | 參數 |
|------|------|------|
| `Partition List` | 分割列表 | 每組大小 |
| `Shift List` | 循環移位 | 偏移量 |
| `Shift Paths` | 路徑偏移 | 樹路徑偏移值 |
| `Relative Item` | 相對項目 | 相對索引 |
| `Merge` | 合併數據 | 多個輸入 |
| `Series` | 數列生成 | 起始值、步長、數量 |

#### 典型應用：交錯網格（如截圖所示）

**配置 A（原始連接）：**
```
Points → Partition → Relative Item(0) → Line Start
                  → Relative Item(+1) → Line End
```

**配置 B（偏移連接）：**
```
Points → Shift Paths(offset=1) → Relative Item → Line
```

**Number Slider 控制：**
- 分區大小（64）
- 偏移量（1）
- 步長

**Panel 顯示數據路徑：**
- `{+1} {+1}` - 路徑索引
- `{-1} {+1}` - 偏移後索引

---

### 2.6 向量運算與顯示

#### 向量組件套組
- **Vector 2Pt** - 兩點創建向量
- **Amplitude** - 設置向量長度
- **Unit Vector X/Y/Z** - 單位向量
- **Cross Product** - 向量叉乘
- **Vector Display** - 向量可視化
- **Plane Normal** - 平面法向量

#### 典型應用鏈
```
Plane → Deconstruct Plane → Normal Vector → Amplitude → Vector Display
```

**Number Slider 控制顯示長度**

#### 多組向量顯示系統
專案中有多個 Vector Display 組（用於分析不同方向）：
- X 方向分析
- Y 方向分析
- Z 方向分析（法向量）

---

### 2.7 幾何變換與擠出

#### 組件群組
| 組件 | 功能 | 常用參數 |
|------|------|----------|
| `Move` | 移動 | 向量 |
| `Extrude` | 擠出 | 方向、距離 |
| `Bounding Box` | 邊界框 | - |
| `Area Properties` | 面積屬性 | 中心點、面積 |
| `Deconstruct Brep` | 拆解 Brep | 面、邊、頂點 |

#### 典型工作流（重複出現 3 次）
```
Rectangle → Move → Area → Vector 2Pt → Deconstruct Brep
         → Amplitude(Negative) → List Item
```

**設計意圖**：創建具有深度的表面面板

---

## 第三部分：進階技術

### 3.1 Python 腳本整合

專案中使用了 **GhPython Script** 組件：
- 自定義運算邏輯
- 數據處理
- 條件判斷

配合：
- **Boolean Toggle** - 開關控制
- **Value List** - 選項列表

### 3.2 群組（Group）系統

專案中有多個命名群組：
- **"different"** - 偏移差異處理模組
- 多個未命名群組 - 功能模組化

**最佳實踐**：
- 為關鍵模組命名
- 使用顏色區分功能區
- Scribble 組件添加註釋

---

## 第四部分：實作練習

### 練習 1：基礎數據樹操作
**目標**：理解 Shift Paths 和 List Shift 的差異

1. 創建點陣列（20×20）
2. 使用 Partition List 分組（每組 20 個）
3. 應用 Shift List（偏移 1）
4. 應用 Shift Paths（偏移 1）
5. 使用 Panel 觀察數據路徑變化

### 練習 2：交錯線條網格
**目標**：重現截圖中的效果

**步驟**：
1. 創建矩形網格點（Number Slider 控制數量）
2. 使用 Partition List（Size = 64）
3. 配置兩組 Tree：
   - 原始組：Offset = 0, Wrap Items
   - 偏移組：Shift Paths(offset = 1), Wrap Items
4. 使用 Relative Item 提取相鄰點
5. 創建 Line 連接
6. 使用 Merge 合併兩組線條

### 練習 3：表面映射面板
**目標**：將平面圖案映射到曲面

**步驟**：
1. 創建目標表面（Loft, Sweep, 或導入）
2. 繪製平面矩形陣列
3. 找到矩形中心點（Area Properties）
4. 從中心向外創建向量
5. 移動矩形（模擬深度）
6. 使用 Map to Surface 映射到曲面
7. 添加 Extrude（沿法向量）

### 練習 4：Delaunay 網格設計
**目標**：創建不規則三角網格立面

**步驟**：
1. 在平面上隨機分布點（Random + Range）
2. 應用 Delaunay Edges
3. 使用 Cross Product 篩選特定方向邊緣
4. 提取端點（End Points）
5. 創建連接線
6. 映射到建築立面曲面

---

## 第五部分：關鍵概念總結

### 5.1 數據管理策略

| 策略 | 何時使用 |
|------|----------|
| **List** 操作 | 單一分支，線性數據 |
| **Tree** 操作 | 多層次，網格狀數據 |
| **Shift List** | 循環偏移項目 |
| **Shift Paths** | 改變樹狀結構索引 |
| **Relative Item** | 訪問相鄰項目 |
| **Partition** | 將長列表分組 |

### 5.2 表面設計工作流

```
平面設計 → UV 映射 → 表面評估 → 法向量 → 幾何變換 → 最終幾何
```

### 5.3 參數化設計原則

1. **模組化** - 將複雜系統分解為獨立群組
2. **可控性** - 使用 Number Slider 控制關鍵參數
3. **可視化** - Panel、Point List、Vector Display 輔助理解
4. **數據清理** - 去重、篩選、驗證

---

## 第六部分：故障排除

### 常見問題

**Q1：線條連接錯誤**
- 檢查 Relative Item 的索引設置
- 確認 Wrap 模式是否啟用
- 使用 Panel 檢查數據路徑

**Q2：表面映射失敗**
- 確認 UV 參數在 0-1 範圍
- 檢查表面是否已修剪（Trimmed）
- 使用 Surface Closest Point 替代直接映射

**Q3：數據樹不匹配**
- 使用 Graft/Flatten 調整樹結構
- 檢查 Path Mapper 是否需要
- Simplify Tree 簡化過度複雜的結構

**Q4：組件顯示橙色警告**
- 檢查輸入數據類型
- 確認數據數量匹配
- 查看組件提示信息

---

## 第七部分：延伸學習

### 推薦主題
1. **Anemone** - 循環迭代插件
2. **Kangaroo** - 物理模擬
3. **Pufferfish** - 進階幾何工具
4. **Lunchbox** - 面板與結構工具

### 實際應用案例
- 建築立面參數化設計
- 結構圖案優化
- 數位製造準備
- 互動裝置設計

---

## 附錄：組件速查表

### A. 點與曲線 (15 組件)
- Point, Curve
- Deconstruct Point
- End Points
- Fit Line
- removeDuplicatePts

### B. 表面操作 (12 組件)
- Surface, Geometry
- Surface Closest Point
- Evaluate Surface
- Map to Surface
- Surface Morph
- Unroll Brep

### C. 變換 (8 組件)
- Move, Extrude
- Bounding Box
- Area Properties
- Deconstruct Brep

### D. 向量 (13 組件)
- Vector 2Pt
- Amplitude
- Unit X/Y/Z
- Cross Product
- Vector Display
- Plane Normal

### E. 列表/樹 (12 組件)
- List Item
- Shift List
- Shift Paths
- Relative Item
- Partition List
- Explode Tree
- Merge

### F. 數學/邏輯 (8 組件)
- Number Slider
- Series
- Negative
- Gate And

### G. 顯示 (7 組件)
- Panel
- Point List
- Vector Display
- Scribble

### H. 幾何生成 (10 組件)
- Rectangle
- Circle
- Line
- Construct Plane
- Deconstruct Plane

### I. 特殊組件 (8 組件)
- GhPython Script
- Boolean Toggle
- Value List
- Relay
- Diamond Panels
- Subdivide Triangle
- Grasshopper MCP

---

## 學習路徑建議

### 初學者（第 1-2 週）
- 理解數據列表基礎
- 練習基本幾何生成
- 學習 Number Slider 控制

### 中級（第 3-4 週）
- 數據樹結構操作
- 表面 UV 映射
- 向量運算應用

### 進階（第 5-6 週）
- 複雜數據流設計
- 多模組整合
- Python 腳本整合

### 專家（第 7-8 週）
- 完整專案重現
- 自定義優化
- 創新應用開發

---

**文件版本：1.0**
**最後更新：2025-10-07**
**專案文件：設計新.gh (145 組件)**

---

## 教師備註

本教學文件基於實際專案分析生成，建議：
1. 分階段教學，避免一次性教授所有內容
2. 每個模組配合實機演示
3. 鼓勵學生自行探索參數變化
4. 使用 Panel 和 Point List 幫助理解數據流
5. 強調模組化和可讀性的重要性

**關鍵學習成果**：
- 掌握數據樹操作
- 理解表面映射原理
- 能夠設計交錯網格系統
- 具備參數化設計思維
