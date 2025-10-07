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

**Grasshopper MCP Enhanced** 是一個增強版的 Grasshopper MCP 橋接服務器，讓 **Claude AI 能夠理解和分析 Grasshopper 檔案**。

### 🎯 核心價值

這不只是 API 工具，而是 **AI 輔助的 Grasshopper 教學系統**：

🧠 **理解 Grasshopper** - AI 能讀取組件、連接、資料結構
💬 **自然語言互動** - 學生用人話提問，AI 給出專業建議
🎓 **智慧評分系統** - AI 協作評分，給出具體改進建議
📊 **深度分析** - 解釋 Data Tree、連接邏輯、設計模式

**關鍵差異**：
- ❌ 傳統方式：數組件數量 → 機械式評分
- ✅ AI 協作：理解設計邏輯 → 智慧分析 → 具體建議

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

## 核心能力

本專案的核心目標是建立 **AI 輔助的 Grasshopper 教學助手**，能夠：

### 🧠 理解與解釋
- **分析 Grasshopper 組件**：解釋每個組件的功能、參數、用途
- **解析資料結構**：說明 Data Tree、List、Branch 的結構與關係
- **追蹤連結邏輯**：解釋組件之間的連接關係與資料流向

### 💬 自然語言互動
- **理解學生提問**：用自然語言描述需求（例如：「我想做一個圓形陣列」）
- **給出建議方案**：推薦適合的組件組合與連接方式
- **解釋設計邏輯**：說明為什麼這樣連接、參數如何影響結果

### 🎓 教學輔助
- **即時答疑**：學生遇到問題時提供解釋
- **最佳實踐建議**：指導更好的 Grasshopper 工作流程
- **錯誤診斷**：分析為什麼運算結果不如預期

---

## 文檔

### 📖 完整文檔

- **[AI 評分系統](docs/AI_GRADING_SYSTEM.md)** - ⭐ 核心功能說明
- **[API 參考手冊](docs/API_REFERENCE.md)** - 完整 API 說明與範例
- **[使用說明](docs/README_ENHANCED.md)** - 詳細功能介紹
- **[實作指南](docs/IMPLEMENTATION_GUIDE.md)** - C# 端編譯指南
- **[教學文件](docs/Grasshopper_教學文件.md)** - Grasshopper 教學應用

### 🎓 教學應用場景

本專案特別適合：

1. **即時答疑與解釋**
   - 學生：「這個 Shift List 是做什麼的？」
   - AI：分析組件功能、參數、連接關係，給出清楚解釋

2. **需求理解與建議**
   - 學生：「我想做一個螺旋樓梯」
   - AI：理解需求，推薦組件組合（Helix、Extrude、Array）與連接方式

3. **資料結構診斷**
   - 學生：「為什麼我的 List 數量不對？」
   - AI：分析 Data Tree 結構，解釋 Branch、Path 的邏輯，找出問題

4. **最佳實踐指導**
   - 分析學生的 Grasshopper 檔案
   - 提出改進建議（簡化邏輯、優化效能）
   - 教導正確的 Grasshopper 思維方式

---

## 專案結構

```
grasshopper-mcp-enhanced/
├── README.md                      # 本文件
├── LICENSE                        # MIT 授權
├── .gitignore                     # Git 忽略文件
│
├── python_bridge/                 # Python MCP 服務器
│   └── bridge_enhanced.py         # 增強版橋接服務器（分析與解釋核心）
│
├── csharp_source/                 # C# 源碼
│   ├── ComponentCommandHandler_Enhanced.cs
│   └── GrasshopperCommandRegistry_Enhanced.cs
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
