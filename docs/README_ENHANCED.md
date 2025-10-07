# Grasshopper MCP - Enhanced Version

## 版本資訊
- **版本**: 2.0 Enhanced Edition
- **日期**: 2025-10-07
- **支援組件**: 50+ 種常用組件

## 🎯 新增功能

### Step 1 核心增強功能
1. ✅ **add_component_advanced** - 支援 50+ 組件類型，可設置初始參數
2. ✅ **get_component_details** - 獲取組件完整資訊
3. ✅ **set_slider_value** - 控制 Number Slider 數值

### 額外實用功能
4. ✅ **delete_component** - 刪除組件
5. ✅ **get_all_connections** - 獲取所有連接關係
6. ✅ **find_components_by_type** - 按類型搜尋組件
7. ✅ **batch_set_sliders** - 批量設置多個 Slider
8. ✅ **set_panel_text** - 設置 Panel 文字
9. ✅ **set_toggle_state** - 控制 Toggle 狀態
10. ✅ **get_component_output_data** - 讀取組件輸出數據

---

## 🚀 使用方法

### 方法 1: 直接運行增強版（推薦）

```bash
# 啟動增強版 MCP 服務器
source venv/bin/activate
python bridge_enhanced.py
```

### 方法 2: 替換原有版本

```bash
# 備份原有版本
cp venv/lib/python3.13/site-packages/grasshopper_mcp/bridge.py venv/lib/python3.13/site-packages/grasshopper_mcp/bridge_backup.py

# 複製增強版
cp bridge_enhanced.py venv/lib/python3.13/site-packages/grasshopper_mcp/bridge.py

# 重新啟動 MCP
source venv/bin/activate
grasshopper-mcp
```

---

## 📚 API 使用範例

### 1. add_component_advanced - 進階組件創建

```python
# 創建帶初始值的 Number Slider
add_component_advanced(
    component_type="slider",
    x=100,
    y=100,
    initial_params={
        "min": 0,
        "max": 100,
        "value": 50,
        "name": "Radius"
    }
)

# 創建帶文字的 Panel
add_component_advanced(
    component_type="panel",
    x=200,
    y=200,
    initial_params={"text": "Hello World"},
    width=200,
    height=100
)

# 創建 List Item 組件
add_component_advanced(
    component_type="list_item",
    x=300,
    y=300,
    name="Extract Item"
)
```

**支援的組件類型**：
- **參數**: point, curve, surface, vector, number, geometry
- **UI**: slider, panel, toggle, button, value_list
- **數學**: addition, subtraction, multiplication, division, negative, series, range
- **列表**: list_item, shift_list, relative_item, partition_list, merge, explode_tree, shift_paths, flatten, graft
- **向量**: vector_2pt, amplitude, unit_x, unit_y, unit_z, cross_product, vector_display, plane_normal
- **曲線**: line, circle, rectangle, fit_line, end_points
- **表面**: surface_closest_point, evaluate_surface, map_to_surface, surface_morph
- **變換**: move, rotate, scale, extrude
- **分析**: area, length, deconstruct_point, deconstruct_brep, deconstruct_plane
- **集合**: create_set, member_index
- **其他**: bounding_box, construct_plane, relay

### 2. get_component_details - 檢查組件狀態

```python
# 獲取組件完整資訊
details = get_component_details("component_id_123")

# 返回結構：
{
    "id": "component_id_123",
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
```

### 3. set_slider_value - 控制 Slider

```python
# 設置單個 Slider
set_slider_value("slider_123", 75.5)

# 批量設置多個 Slider
batch_set_sliders({
    "slider_1": 50.0,
    "slider_2": 75.5,
    "slider_3": 100.0
})
```

### 4. 其他實用功能

```python
# 刪除組件
delete_component("component_id_123")

# 獲取所有連接關係
connections = get_all_connections()

# 搜尋所有 Slider
sliders = find_components_by_type("slider")

# 設置 Panel 文字
set_panel_text("panel_123", "新的文字內容")

# 設置 Toggle 狀態
set_toggle_state("toggle_123", True)

# 讀取組件輸出數據
data = get_component_output_data("slider_123")
```

---

## 🎓 教學應用範例

### 範例 1: 自動創建練習題

```python
# 創建一個簡單的練習：點 → 圓
def create_circle_exercise():
    # 創建 XY Plane
    plane = add_component_advanced("construct_plane", 100, 100)

    # 創建 Number Slider (半徑)
    radius = add_component_advanced(
        "slider", 100, 200,
        initial_params={"min": 1, "max": 50, "value": 10, "name": "Radius"}
    )

    # 創建 Circle (留給學生連接)
    circle = add_component_advanced("circle", 300, 150)

    # 創建提示 Panel
    hint = add_component_advanced(
        "panel", 500, 100,
        initial_params={"text": "請將 Plane 和 Radius 連接到 Circle"}
    )

    return {
        "plane_id": plane["data"]["componentId"],
        "radius_id": radius["data"]["componentId"],
        "circle_id": circle["data"]["componentId"]
    }
```

### 範例 2: 批量評分

```python
# 檢查學生是否正確完成作業
def check_assignment(required_components):
    # 獲取文檔資訊
    doc = get_document_info()

    # 檢查組件數量
    has_slider = any(c["type"] == "GH_NumberSlider" for c in doc["data"]["components"])
    has_circle = any(c["type"] == "Component_Circle" for c in doc["data"]["components"])

    # 檢查連接
    connections = get_all_connections()

    score = 0
    if has_slider:
        score += 30
    if has_circle:
        score += 30
    if len(connections["data"]) >= 2:
        score += 40

    return {
        "score": score,
        "has_slider": has_slider,
        "has_circle": has_circle,
        "connection_count": len(connections["data"])
    }
```

### 範例 3: 動態參數調整

```python
# 根據學生進度調整難度
def adjust_difficulty(student_level):
    # 找到所有 Slider
    sliders = find_components_by_type("slider")

    if student_level == "beginner":
        # 簡單範圍
        for slider_id in sliders["data"]:
            set_slider_value(slider_id, 10)
    elif student_level == "advanced":
        # 複雜範圍
        for slider_id in sliders["data"]:
            set_slider_value(slider_id, 50)
```

---

## 🔧 故障排除

### 問題 1: 連接失敗
```
Error: Connection refused
```
**解決方案**: 確認 Grasshopper 已在 port 8080 啟動

### 問題 2: 組件類型不支援
```
Error: Unknown component type
```
**解決方案**: 使用 `grasshopper://component_types` 查看支援的類型清單

### 問題 3: 參數設置失敗
```
Error: Invalid parameter
```
**解決方案**: 使用 `get_component_details` 檢查組件當前狀態

---

## 📖 資源 (Resources)

### 查看連接狀態
```
grasshopper://status
```

### 查看支援的組件類型
```
grasshopper://component_types
```

### 查看組件指南
```
grasshopper://component_guide
```

---

## 🎯 下一步計劃

### Step 2: 批量操作增強
- [ ] batch_add_components - 批量創建組件
- [ ] batch_connect - 批量連接
- [ ] batch_delete - 批量刪除

### Step 3: 群組操作
- [ ] create_group - 創建群組
- [ ] get_all_groups - 獲取所有群組
- [ ] ungroup - 解散群組

### Step 4: 進階分析
- [ ] analyze_workflow - 分析數據流
- [ ] detect_errors - 偵測常見錯誤
- [ ] suggest_improvements - 優化建議

---

## 📝 版本歷史

### v2.0 (2025-10-07)
- ✅ 新增 add_component_advanced
- ✅ 新增 get_component_details
- ✅ 新增 set_slider_value
- ✅ 新增 10 個實用工具函數
- ✅ 支援 50+ 組件類型

### v1.0 (原版)
- 基礎 6 個功能
- 支援 6 種組件類型

---

## 🤝 貢獻

如有問題或建議，歡迎提出！

**作者**: Claude Code
**專案**: Grasshopper MCP Enhanced
**授權**: MIT
