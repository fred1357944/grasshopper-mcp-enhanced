# Grasshopper MCP Enhanced

🚀 **教學導向的 Grasshopper MCP 增強版**

基於 [grasshopper-mcp](https://github.com/alfredatnycu/grasshopper-mcp) 開發的增強版本，專為 **Grasshopper 教學與自動化評分** 設計。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Grasshopper](https://img.shields.io/badge/Grasshopper-Compatible-brightgreen.svg)](https://www.grasshopper3d.com/)

---

## 📋 目錄

- [專案簡介](#專案簡介)
- [致謝與參考](#致謝與參考)
- [新增功能](#新增功能)
- [快速開始](#快速開始)
- [使用範例](#使用範例)
- [文檔](#文檔)
- [專案結構](#專案結構)
- [開發計劃](#開發計劃)
- [貢獻](#貢獻)
- [授權](#授權)

---

## 專案簡介

**Grasshopper MCP Enhanced** 是一個增強版的 Grasshopper MCP 橋接服務器，在原有功能基礎上新增了 **10+ 個教學導向功能**，讓教師能夠：

✨ **自動創建練習題** - 批量生成標準化練習
📊 **自動評分系統** - 分析學生作業並評分
🎯 **參數動態控制** - 遠程調整 Slider、Panel 等組件
🔍 **詳細組件分析** - 獲取組件完整資訊
📦 **批量操作** - 一次性設置多個組件

---

## 致謝與參考

### 🙏 基於原專案

本專案基於 **Alfred Chen** 的優秀開源專案 [grasshopper-mcp](https://github.com/alfredatnycu/grasshopper-mcp) 開發。

**原專案特點**：
- MCP 協議橋接
- 基礎組件創建
- WebSocket 通訊
- 組件知識庫

**致謝**：
感謝 Alfred Chen 創建了這個優秀的基礎框架，使得我們能夠在此基礎上開發教學導向的增強功能。

**關係說明**：
```
grasshopper-mcp (原版)
    ↓
    └─ grasshopper-mcp-enhanced (本專案)
       新增 10+ 教學導向功能
```

---

## 新增功能

### ⭐ 核心增強功能（10 個）

| 功能 | API | 描述 |
|------|-----|------|
| 進階組件創建 | `add_component_advanced` | 支援 50+ 組件類型，可設置初始參數 |
| 組件詳細資訊 | `get_component_details` | 獲取組件完整資訊（位置、參數、連接） |
| Slider 控制 | `set_slider_value` | 動態設置 Number Slider 數值 |
| 批量 Slider | `batch_set_sliders` | 一次設置多個 Slider |
| 刪除組件 | `delete_component` | 移除指定組件 |
| 搜尋組件 | `find_components_by_type` | 按類型搜尋所有組件 |
| Panel 控制 | `set_panel_text` | 設置 Panel 文字內容 |
| Toggle 控制 | `set_toggle_state` | 控制 Boolean Toggle 狀態 |
| 讀取輸出 | `get_component_output_data` | 獲取組件輸出數據 |
| 連接關係 | `get_all_connections` | 獲取所有組件連接關係 |

### 📚 支援的組件類型（50+）

- **參數**: point, curve, surface, vector, number, geometry
- **UI**: slider, panel, toggle, button, value_list
- **數學**: addition, subtraction, multiplication, division, series, range
- **列表**: list_item, shift_list, relative_item, partition_list, merge, explode_tree
- **向量**: vector_2pt, amplitude, unit_x/y/z, cross_product, vector_display
- **曲線**: line, circle, rectangle, fit_line, end_points
- **表面**: surface_closest_point, evaluate_surface, map_to_surface
- **變換**: move, rotate, scale, extrude
- **分析**: area, length, deconstruct_point, deconstruct_brep

完整清單請查看 [API 文檔](docs/API_REFERENCE.md)

---

## 快速開始

### 前置需求

- Python 3.8+
- Rhino 7/8
- Grasshopper
- 原版 [grasshopper-mcp](https://github.com/alfredatnycu/grasshopper-mcp) 組件

### 安裝

#### 1. Python 端（立即可用）

```bash
# 克隆專案
git clone https://github.com/YOUR_USERNAME/grasshopper-mcp-enhanced.git
cd grasshopper-mcp-enhanced

# 創建虛擬環境
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安裝依賴
pip install grasshopper-mcp mcp aiohttp websockets

# 啟動服務器
python python_bridge/bridge_enhanced.py
```

#### 2. C# 端（可選，需要編譯）

詳細步驟請查看 [實作指南](docs/IMPLEMENTATION_GUIDE.md)

---

## 使用範例

### 範例 1: 自動創建練習題

```python
from bridge_enhanced import add_component_advanced, set_panel_text

# 創建帶初始值的 Slider
slider = add_component_advanced(
    "slider",
    x=100, y=100,
    initial_params={
        "min": 0,
        "max": 100,
        "value": 50,
        "name": "Radius"
    }
)

# 創建提示 Panel
panel = add_component_advanced(
    "panel",
    x=300, y=100,
    initial_params={
        "text": "調整 Slider 以改變圓的大小"
    }
)
```

### 範例 2: 自動評分系統

```python
from bridge_enhanced import get_document_info, find_components_by_type

# 獲取文檔資訊
doc = get_document_info()

# 搜尋所有 Slider
sliders = find_components_by_type("GH_NumberSlider")

# 評分邏輯
score = 0
if len(sliders) >= 2:
    score += 20  # 使用了足夠的 Slider

print(f"學生得分: {score}/100")
```

### 範例 3: 批量調整參數

```python
from bridge_enhanced import batch_set_sliders

# 根據難度等級調整
batch_set_sliders({
    "slider_1": 25,   # 簡單
    "slider_2": 50,   # 中等
    "slider_3": 75    # 困難
})
```

更多範例請查看 [examples/](examples/) 目錄。

---

## 文檔

### 📖 完整文檔

- **[API 參考手冊](docs/API_REFERENCE.md)** - 完整 API 說明與範例
- **[使用說明](docs/README_ENHANCED.md)** - 詳細功能介紹
- **[實作指南](docs/IMPLEMENTATION_GUIDE.md)** - C# 端編譯指南
- **[教學文件](docs/Grasshopper_教學文件.md)** - Grasshopper 教學應用

### 🎓 教學應用

本專案特別適合：

1. **Grasshopper 課程教學**
   - 自動創建標準化練習
   - 確保每個學生起點一致
   - 遠程調整參數展示效果

2. **作業自動評分**
   - 分析組件類型與數量
   - 檢查連接關係
   - 生成評分報告

3. **互動式教學**
   - 根據學生表現調整難度
   - 即時反饋與提示
   - 進度追蹤

---

## 專案結構

```
grasshopper-mcp-enhanced/
├── README.md                      # 本文件
├── LICENSE                        # MIT 授權
├── .gitignore                     # Git 忽略文件
│
├── python_bridge/                 # Python MCP 服務器
│   └── bridge_enhanced.py         # 增強版橋接服務器
│
├── csharp_source/                 # C# 源碼
│   ├── ComponentCommandHandler_Enhanced.cs
│   └── GrasshopperCommandRegistry_Enhanced.cs
│
├── examples/                      # 使用範例
│   ├── README.md                  # 範例說明
│   ├── create_circle_exercise.py  # 自動創建練習題
│   └── check_student_work.py      # 自動評分系統
│
├── tests/                         # 測試腳本
│   ├── test_basic.py              # 基礎功能測試
│   └── test_enhanced.py           # 增強功能測試
│
└── docs/                          # 文檔
    ├── API_REFERENCE.md           # API 手冊
    ├── README_ENHANCED.md         # 使用說明
    ├── IMPLEMENTATION_GUIDE.md    # 實作指南
    └── Grasshopper_教學文件.md    # 教學文件
```

---

## 開發計劃

### ✅ 已完成（v1.0）

- [x] Python 端增強功能（10 個 API）
- [x] C# 源碼開發
- [x] 基礎功能測試
- [x] 範例腳本（2 個）
- [x] 完整文檔

### 🚧 進行中（v1.1）

- [ ] C# 端編譯與測試
- [ ] 更多教學範例
- [ ] 視頻教學
- [ ] 中英文文檔

### 📅 未來計劃（v2.0）

- [ ] Web 界面（教師控制台）
- [ ] 學生進度儀表板
- [ ] AI 輔助評分
- [ ] 多人協作功能
- [ ] 練習題模板庫

---

## 貢獻

歡迎貢獻！請遵循以下步驟：

1. Fork 本專案
2. 創建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 開啟 Pull Request

### 貢獻指南

- 保持代碼風格一致
- 添加適當的註釋
- 更新相關文檔
- 添加測試用例

---

## 授權

本專案採用 MIT 授權 - 詳見 [LICENSE](LICENSE) 文件

### 原專案授權

原專案 [grasshopper-mcp](https://github.com/alfredatnycu/grasshopper-mcp) 同樣採用 MIT 授權。

---

## 聯繫方式

- **GitHub Issues**: [提交問題](https://github.com/YOUR_USERNAME/grasshopper-mcp-enhanced/issues)
- **原專案**: [grasshopper-mcp](https://github.com/alfredatnycu/grasshopper-mcp)

---

## 相關資源

- [Grasshopper 官網](https://www.grasshopper3d.com/)
- [Rhino 官網](https://www.rhino3d.com/)
- [MCP 協議](https://modelcontextprotocol.io/)
- [原專案 grasshopper-mcp](https://github.com/alfredatnycu/grasshopper-mcp)

---

**版本**: 1.0.0
**最後更新**: 2025-10-07
**作者**: Based on grasshopper-mcp by Alfred Chen
**授權**: MIT

---

⭐ 如果這個專案對你有幫助，請給我們一個 Star！
