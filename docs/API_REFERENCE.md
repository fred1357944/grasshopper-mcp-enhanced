# Grasshopper MCP Enhanced - API 參考手冊

## 快速索引

### 基礎功能（原版）
1. [add_component](#1-add_component) - 添加基礎組件
2. [connect_components](#2-connect_components) - 連接組件
3. [get_document_info](#3-get_document_info) - 獲取文檔資訊
4. [save_document](#4-save_document) - 保存文檔
5. [load_document](#5-load_document) - 載入文檔
6. [clear_document](#6-clear_document) - 清空文檔

### 增強功能（新版）
7. [add_component_advanced](#7-add_component_advanced) ⭐ - 進階組件創建
8. [get_component_details](#8-get_component_details) ⭐ - 獲取組件詳情
9. [set_slider_value](#9-set_slider_value) ⭐ - 設置 Slider 值
10. [delete_component](#10-delete_component) - 刪除組件
11. [get_all_connections](#11-get_all_connections) - 獲取所有連接
12. [find_components_by_type](#12-find_components_by_type) - 搜尋組件
13. [batch_set_sliders](#13-batch_set_sliders) - 批量設置 Slider
14. [set_panel_text](#14-set_panel_text) - 設置 Panel 文字
15. [set_toggle_state](#15-set_toggle_state) - 設置 Toggle 狀態
16. [get_component_output_data](#16-get_component_output_data) - 讀取組件輸出

---

## 詳細 API

### 1. add_component
**基礎版本** - 添加組件

```python
add_component(
    component_type: str,  # 組件類型
    x: float,             # X 座標
    y: float              # Y 座標
)
```

**範例**:
```python
add_component("slider", 100, 100)
```

---

### 2. connect_components
連接兩個組件

```python
connect_components(
    source_id: str,              # 來源組件 ID
    target_id: str,              # 目標組件 ID
    source_param: str = None,    # 來源參數名稱（可選）
    target_param: str = None,    # 目標參數名稱（可選）
    source_param_index: int = None,  # 來源參數索引（可選）
    target_param_index: int = None   # 目標參數索引（可選）
)
```

**範例**:
```python
connect_components(
    source_id="slider_123",
    target_id="circle_456",
    target_param="Radius"
)
```

---

### 3. get_document_info
獲取當前文檔資訊

```python
get_document_info()
```

**返回**:
```json
{
    "success": true,
    "data": {
        "name": "設計新.gh",
        "path": "/path/to/file.gh",
        "componentCount": 145,
        "components": [
            {"id": "...", "type": "...", "name": "..."},
            ...
        ]
    }
}
```

---

### 4. save_document
保存文檔

```python
save_document(path: str)
```

**範例**:
```python
save_document("/Users/username/my_design.gh")
```

---

### 5. load_document
載入文檔

```python
load_document(path: str)
```

**範例**:
```python
load_document("/Users/username/existing_design.gh")
```

---

### 6. clear_document
清空整個文檔

```python
clear_document()
```

⚠️ **警告**: 會刪除所有組件，無法復原！

---

### 7. add_component_advanced
⭐ **進階版** - 支援 50+ 組件類型，可設置初始參數

```python
add_component_advanced(
    component_type: str,                    # 組件類型（支援簡寫）
    x: float,                               # X 座標
    y: float,                               # Y 座標
    initial_params: dict = None,            # 初始參數
    name: str = None,                       # 自訂名稱
    width: int = None,                      # 寬度
    height: int = None                      # 高度
)
```

**支援的組件類型** (50+ 種):

| 類別 | 類型 |
|------|------|
| **參數** | point, curve, surface, vector, number, geometry |
| **UI** | slider, panel, toggle, button, value_list |
| **數學** | addition, subtraction, multiplication, division, negative, series, range |
| **列表** | list_item, shift_list, relative_item, partition_list, merge, explode_tree, shift_paths, flatten, graft |
| **向量** | vector_2pt, amplitude, unit_x, unit_y, unit_z, cross_product, vector_display, plane_normal |
| **曲線** | line, circle, rectangle, fit_line, end_points |
| **表面** | surface_closest_point, evaluate_surface, map_to_surface, surface_morph |
| **變換** | move, rotate, scale, extrude |
| **分析** | area, length, deconstruct_point, deconstruct_brep, deconstruct_plane |
| **集合** | create_set, member_index |
| **其他** | bounding_box, construct_plane, relay |

**範例**:

```python
# 創建 Number Slider
add_component_advanced(
    "slider",
    x=100, y=100,
    initial_params={
        "min": 0,
        "max": 100,
        "value": 50,
        "name": "Radius"
    }
)

# 創建 Panel
add_component_advanced(
    "panel",
    x=200, y=200,
    initial_params={"text": "Hello World"},
    width=200,
    height=100
)

# 創建 List Item
add_component_advanced(
    "list_item",
    x=300, y=300,
    name="Extract First Item"
)
```

**返回**:
```json
{
    "success": true,
    "data": {
        "componentId": "abc-123-def-456"
    }
}
```

---

### 8. get_component_details
⭐ 獲取組件的完整詳細資訊

```python
get_component_details(component_id: str)
```

**範例**:
```python
get_component_details("abc-123-def-456")
```

**返回**:
```json
{
    "success": true,
    "data": {
        "id": "abc-123-def-456",
        "type": "GH_NumberSlider",
        "name": "Number Slider",
        "position": {"x": 100, "y": 200},
        "size": {"width": 200, "height": 20},
        "parameters": {
            "min": 0,
            "max": 100,
            "value": 64
        },
        "inputs": [],
        "outputs": [
            {
                "name": "Number",
                "type": "double",
                "data": [64.0]
            }
        ],
        "connections": {
            "outputs_to": ["component_abc", "component_def"]
        }
    }
}
```

---

### 9. set_slider_value
⭐ 設置 Number Slider 的數值

```python
set_slider_value(
    component_id: str,  # Slider 組件 ID
    value: float        # 新數值
)
```

**範例**:
```python
set_slider_value("slider_123", 75.5)
```

---

### 10. delete_component
刪除組件

```python
delete_component(component_id: str)
```

**範例**:
```python
delete_component("component_123")
```

---

### 11. get_all_connections
獲取文檔中所有連接關係

```python
get_all_connections()
```

**返回**:
```json
{
    "success": true,
    "data": [
        {
            "sourceId": "slider_123",
            "targetId": "circle_456",
            "sourceParam": "Number",
            "targetParam": "Radius"
        },
        ...
    ]
}
```

---

### 12. find_components_by_type
搜尋特定類型的所有組件

```python
find_components_by_type(component_type: str)
```

**範例**:
```python
# 使用簡寫
find_components_by_type("slider")

# 或使用完整類型名稱
find_components_by_type("GH_NumberSlider")
```

**返回**:
```json
{
    "success": true,
    "data": [
        "slider_123",
        "slider_456",
        "slider_789"
    ]
}
```

---

### 13. batch_set_sliders
批量設置多個 Slider 的數值

```python
batch_set_sliders(slider_values: dict)
```

**範例**:
```python
batch_set_sliders({
    "slider_1": 50.0,
    "slider_2": 75.5,
    "slider_3": 100.0
})
```

---

### 14. set_panel_text
設置 Panel 組件的文字內容

```python
set_panel_text(
    component_id: str,  # Panel 組件 ID
    text: str           # 文字內容
)
```

**範例**:
```python
set_panel_text("panel_123", "新的文字內容")
```

---

### 15. set_toggle_state
設置 Boolean Toggle 的狀態

```python
set_toggle_state(
    component_id: str,  # Toggle 組件 ID
    state: bool         # True 或 False
)
```

**範例**:
```python
set_toggle_state("toggle_123", True)
```

---

### 16. get_component_output_data
讀取組件的輸出數據

```python
get_component_output_data(
    component_id: str,      # 組件 ID
    output_index: int = 0   # 輸出索引（預設 0）
)
```

**範例**:
```python
# 讀取 Slider 的數值
get_component_output_data("slider_123")

# 讀取組件的第二個輸出
get_component_output_data("component_456", 1)
```

**返回**:
```json
{
    "success": true,
    "data": {
        "outputName": "Number",
        "outputType": "double",
        "data": [64.0]
    }
}
```

---

## 資源 (Resources)

### grasshopper://status
檢查 Grasshopper 連接狀態

```json
{
    "status": "connected",
    "host": "localhost",
    "port": 8080
}
```

### grasshopper://component_types
獲取所有支援的組件類型清單

### grasshopper://component_guide
獲取組件使用指南

---

## 錯誤處理

所有 API 都會返回統一的格式：

**成功**:
```json
{
    "success": true,
    "data": { ... }
}
```

**失敗**:
```json
{
    "success": false,
    "error": "錯誤訊息"
}
```

---

## 常見使用模式

### 模式 1: 自動創建練習題

```python
# 1. 創建組件
slider = add_component_advanced(
    "slider", 100, 100,
    {"min": 1, "max": 50, "value": 10}
)

circle = add_component_advanced("circle", 300, 100)

# 2. 連接組件
connect_components(
    slider["data"]["componentId"],
    circle["data"]["componentId"],
    target_param="Radius"
)

# 3. 添加提示
hint = add_component_advanced(
    "panel", 500, 100,
    {"text": "調整 Slider 以改變圓的大小"}
)
```

### 模式 2: 批量評分

```python
# 1. 獲取文檔資訊
doc = get_document_info()

# 2. 檢查組件數量
component_count = doc["data"]["componentCount"]

# 3. 檢查連接
connections = get_all_connections()
connection_count = len(connections["data"])

# 4. 計算分數
score = min(100, component_count * 10 + connection_count * 20)
```

### 模式 3: 參數動畫

```python
import time

# 找到所有 Slider
sliders = find_components_by_type("slider")

# 動畫循環
for value in range(0, 101, 5):
    for slider_id in sliders["data"]:
        set_slider_value(slider_id, value)
    time.sleep(0.1)
```

---

## 版本資訊

- **版本**: 2.0 Enhanced
- **日期**: 2025-10-07
- **更新內容**:
  - 新增 10 個增強功能
  - 支援 50+ 組件類型
  - 完整的組件控制能力
  - 批量操作支援

---

**文檔版本**: 1.0
**最後更新**: 2025-10-07
