# Grasshopper MCP 增強版實作指南

## 📦 已創建的文件

### C# 源碼（位於 grasshopper-mcp-source/）
1. **ComponentCommandHandler_Enhanced.cs** - 增強版命令處理器（10個新命令）
2. **GrasshopperCommandRegistry_Enhanced.cs** - 增強版命令註冊器

### Python 端（已完成）
3. **bridge_enhanced.py** - Python MCP 服務器（已實作完成）

---

## 🔧 實作步驟

### 方法 1: 編譯增強版組件（完整方案）

#### 步驟 1: 準備開發環境

**需求**：
- Visual Studio 2019 或更新版本
- Rhino 7 或 8
- Grasshopper SDK（隨 Rhino 安裝）

#### 步驟 2: 整合增強代碼到專案

```bash
cd /Users/laihongyi/Downloads/專案/程式專案/grasshopper-mcp-source/GH_MCP
```

**2.1 文件已創建在正確位置**：
- `GH_MCP/Commands/ComponentCommandHandler_Enhanced.cs` ✅
- `GH_MCP/Commands/GrasshopperCommandRegistry_Enhanced.cs` ✅

**2.2 修改 `GH_MCPComponent.cs`**：

打開文件：
```bash
open GH_MCP/GH_MCPComponent.cs
```

找到初始化部分（大約在組件構造函數或啟動方法中），將：
```csharp
// 原始代碼
GrasshopperCommandRegistry.Initialize();
```

改為：
```csharp
// 使用增強版
GH_MCP.Commands.GrasshopperCommandRegistry_Enhanced.Initialize();
```

**2.3 添加文件到專案**：

1. 用 Visual Studio 打開 `GH_MCP.sln`：
   ```bash
   open GH_MCP/GH_MCP.sln
   ```

2. 在 Solution Explorer 中：
   - 右鍵點擊 `Commands` 資料夾
   - Add > Existing Item
   - 選擇 `ComponentCommandHandler_Enhanced.cs`
   - 再次添加 `GrasshopperCommandRegistry_Enhanced.cs`

#### 步驟 3: 編譯專案

1. 在 Visual Studio 中：
   - Build > Build Solution（或按 Ctrl+Shift+B）

2. 等待編譯完成，檢查輸出：
   ```
   ========== Build: 1 succeeded, 0 failed ==========
   ```

3. 編譯後的 `.gha` 文件位於：
   ```
   GH_MCP/GH_MCP/bin/Debug/GH_MCP.gha
   或
   GH_MCP/GH_MCP/bin/Release/GH_MCP.gha
   ```

#### 步驟 4: 安裝增強版組件

1. 複製編譯後的 `.gha` 文件到 Grasshopper 組件資料夾：

   **macOS**:
   ```bash
   cp GH_MCP/GH_MCP/bin/Debug/GH_MCP.gha ~/Library/Application\ Support/McNeel/Rhinoceros/7.0/Plug-ins/Grasshopper/Components/GH_MCP_Enhanced.gha
   ```

   **Windows**:
   ```
   %APPDATA%\Grasshopper\Libraries\GH_MCP_Enhanced.gha
   ```

2. 重啟 Rhino 和 Grasshopper

3. 在 Grasshopper 中找到並放置 "Grasshopper MCP" 組件

4. 確認組件顯示 "Listening on port 8080"

#### 步驟 5: 測試增強功能

```bash
cd /Users/laihongyi/Downloads/專案/程式專案/grasshopper-mcp
source venv/bin/activate
python test_enhanced.py
```

**預期輸出**：
```
======================================================================
測試 3: 創建進階組件 (Number Slider)
======================================================================
✅ 成功創建 Number Slider！
   組件 ID: abc-123-def-456

======================================================================
測試 4: 獲取組件詳細資訊
======================================================================
✅ 成功！
   類型: GH_NumberSlider
   位置: {'x': 100, 'y': 100}
   參數: {'min': 0, 'max': 100, 'value': 50}
```

---

### 方法 2: 快速測試（不重新編譯）

如果暫時不想編譯，可以先用 Python 端的包裝器：

#### 創建 Python 包裝器

```python
# wrapper.py - 將增強功能映射到現有命令

def add_component_advanced_wrapper(type, x, y, initial_params=None, name=None):
    """
    使用現有的 add_component，然後用 set_component_value 設置參數
    """
    # 1. 創建組件
    result = add_component(type, x, y)
    component_id = result["data"]["componentId"]

    # 2. 設置參數
    if initial_params and type == "slider":
        if "value" in initial_params:
            set_component_value(component_id, str(initial_params["value"]))

    return result
```

**限制**：
- 無法設置 Slider 的 min/max 範圍
- 無法一次性設置所有參數
- 功能有限

---

## 📝 編譯故障排除

### 問題 1: Visual Studio 找不到 Grasshopper 引用

**解決方案**：
1. 確認已安裝 Rhino
2. 檢查專案的引用路徑：
   ```xml
   <Reference Include="Grasshopper">
     <HintPath>C:\Program Files\Rhino 7\Plug-ins\Grasshopper\Grasshopper.dll</HintPath>
   </Reference>
   ```
3. 根據你的 Rhino 安裝路徑調整

### 問題 2: 編譯錯誤「找不到類型」

**解決方案**：
確保在 `ComponentCommandHandler_Enhanced.cs` 開頭有：
```csharp
using GrasshopperMCP.Models;
using Grasshopper.Kernel;
using Grasshopper.Kernel.Special;
```

### 問題 3: Runtime 錯誤「找不到方法」

**解決方案**：
確認已修改 `GH_MCPComponent.cs` 使用增強版註冊器。

---

## 🎯 驗證增強功能

### 測試清單

1. ✅ **基礎功能** (Python test_basic.py)
   - 連接 Grasshopper
   - 創建組件
   - 獲取文檔資訊

2. ✅ **增強功能** (Python test_enhanced.py)
   - add_component_advanced
   - get_component_details
   - set_slider_value
   - find_components_by_type
   - batch_set_sliders

3. ✅ **教學應用**
   - 自動創建練習題
   - 批量設置參數
   - 分析學生作業

---

## 📋 增強功能清單

| 功能 | 命令 | 狀態 |
|------|------|------|
| 進階組件創建 | add_component_advanced | ✅ 已實作 |
| 獲取組件詳情 | get_component_details | ✅ 已實作 |
| 設置 Slider | set_slider_value | ✅ 已實作 |
| 批量設置 Slider | batch_set_sliders | ✅ 已實作 |
| 刪除組件 | delete_component | ✅ 已實作 |
| 搜尋組件 | find_components_by_type | ✅ 已實作 |
| 設置 Panel | set_panel_text | ✅ 已實作 |
| 設置 Toggle | set_toggle_state | ✅ 已實作 |
| 獲取輸出數據 | get_component_output_data | ✅ 已實作 |
| 獲取所有連接 | get_all_connections | ✅ 已實作 |

---

## 🚀 下一步

### 如果編譯成功
1. 測試所有增強功能
2. 開始創建教學應用
3. 編寫學生練習題

### 如果遇到問題
1. 檢查錯誤訊息
2. 參考故障排除章節
3. 或者先使用方法 2（Python 包裝器）

---

## 💡 教學應用範例

編譯成功後，你可以：

### 1. 自動創建練習題

```python
from bridge_enhanced import *

# 創建帶提示的練習
slider = add_component_advanced(
    "slider", 100, 100,
    initial_params={"min": 1, "max": 50, "value": 10, "name": "Radius"}
)

hint_panel = add_component_advanced(
    "panel", 300, 100,
    initial_params={"text": "調整 Slider 控制圓的大小"}
)
```

### 2. 批量評分

```python
# 獲取所有 Slider
sliders = find_components_by_type("GH_NumberSlider")

# 檢查每個 Slider 的設置
for slider_id in sliders:
    details = get_component_details(slider_id)
    if details["parameters"]["min"] == 0 and details["parameters"]["max"] == 100:
        print("✅ Slider 設置正確")
```

### 3. 動態調整難度

```python
# 根據學生程度調整
if student_level == "beginner":
    batch_set_sliders({
        "slider_1": 10,
        "slider_2": 20
    })
else:
    batch_set_sliders({
        "slider_1": 50,
        "slider_2": 75
    })
```

---

## 📞 支援

- **GitHub**: https://github.com/alfredatnycu/grasshopper-mcp
- **問題反饋**: 在專案的 Issues 頁面提出
- **文檔**: 查看 README_ENHANCED.md 和 API_REFERENCE.md

---

**版本**: Enhanced v2.0
**最後更新**: 2025-10-07
**狀態**: ✅ Python 端完成，C# 端待編譯
