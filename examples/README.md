# Grasshopper MCP 教學範例

## 📚 範例清單

### 1. create_circle_exercise.py
**自動創建圓形練習題**

**功能**：
- 自動創建 Slider、XY Plane、Circle 組件
- 設置初始參數
- 添加練習提示

**使用方法**：
```bash
cd /Users/laihongyi/Downloads/專案/程式專案/grasshopper-mcp
source venv/bin/activate
python examples/create_circle_exercise.py
```

**效果**：
在 Grasshopper 畫布上自動創建：
- Number Slider (x: 100, y: 100) - 初始值 10
- XY Plane (x: 100, y: 200)
- Circle (x: 400, y: 150)
- Panel (x: 650, y: 100) - 包含練習提示

**教學用途**：
- 快速創建標準練習題
- 確保每個學生有相同的起點
- 節省手動設置時間

---

### 2. check_student_work.py
**檢查學生作業並評分**

**功能**：
- 分析文檔中的組件類型和數量
- 自動評分（滿分 100）
- 提供改進建議

**使用方法**：
```bash
python examples/check_student_work.py
```

**評分項目**：
1. **Number Slider**（10分）- 是否使用參數控制
2. **幾何組件**（20分）- 是否創建幾何圖形
3. **組件數量**（20分）- 是否適中（10-50個）
4. **參數組件**（15分）- 是否使用 Param_Point 等
5. **組織性**（15分）- 是否使用 Panel/Group 組織
6. **基礎分**（20分）

**輸出範例**：
```
📊 總分: 85/100
🎯 等級: 良好 (B)

詳細評分：
   ✅ 使用了 Number Slider (4 個) +10分
   ✅ 包含幾何組件 +20分
   ✅ 組件數量適中 (30 個) +20分
   ❌ 缺少參數組件 0分
   ✅ 有組織（Panel/Group） +15分
   ✅ 基礎分 +20分

💡 改進建議：
   • 使用參數組件來提高可重用性
```

---

## 🎯 使用場景

### 場景 1: 課堂準備
**老師在課前**：
```bash
# 創建標準練習題
python examples/create_circle_exercise.py
```

然後保存為模板文件：
- File → Save As → `circle_exercise_template.gh`

**學生開始練習時**：
- 每個人載入相同的模板
- 確保起點一致

---

### 場景 2: 作業檢查
**學生提交 .gh 檔案後**：

```bash
# 1. 在 Grasshopper 中打開學生作業
# 2. 運行評分腳本
python examples/check_student_work.py
```

**優點**：
- 快速初步評分
- 識別常見問題
- 節省手動檢查時間

---

### 場景 3: 批量處理（需要額外腳本）

可以創建批量處理腳本：
```python
# batch_check.py (待創建)
import os

student_files = [
    "student_001.gh",
    "student_002.gh",
    # ...
]

for file in student_files:
    # 載入文檔
    load_document(file)
    # 評分
    score = check_student_work()
    # 記錄結果
    save_result(file, score)
```

---

## 🔧 自訂範例

### 創建你自己的練習題

```python
# my_exercise.py
import socket
import json

def send_command(command_type, params):
    # ... (複製 send_command 函數)
    pass

def create_my_exercise():
    # 1. 創建你需要的組件
    send_command("add_component", {
        "type": "slider",
        "x": 100,
        "y": 100
    })

    # 2. 設置參數
    # 3. 添加提示
    # ...

if __name__ == "__main__":
    create_my_exercise()
```

---

## 📝 基礎功能限制

### 可用功能
✅ add_component - 添加組件（基本類型）
✅ set_component_value - 設置 Slider/Panel 值
✅ get_document_info - 獲取文檔資訊
✅ connect_components - 連接組件

### 限制
❌ 無法設置 Slider 的 min/max 範圍（需要增強版）
❌ 無法按類型搜尋組件（需要手動從 document_info 篩選）
❌ 無法批量操作（需要用循環）
❌ 無法讀取組件詳細參數（需要增強版）

### 解決方法（臨時）
```python
# 搜尋 Slider（手動篩選）
doc = send_command("get_document_info")
sliders = [c for c in doc["data"]["components"]
           if "Slider" in c["type"]]

# 批量設置（循環）
for slider in sliders:
    send_command("set_component_value", {
        "id": slider["id"],
        "value": "50"
    })
```

---

## 🚀 進階：編譯增強版後

編譯增強版後，可以使用：

### 更強大的練習題創建
```python
slider = add_component_advanced(
    "slider", 100, 100,
    initial_params={
        "min": 0,
        "max": 100,
        "value": 50,
        "name": "Radius"
    }
)
```

### 更精確的評分
```python
# 獲取詳細參數
details = get_component_details(slider_id)
if 0 <= details["parameters"]["min"] <= 10:
    score += 5  # Slider 範圍設置合理
```

### 批量操作
```python
batch_set_sliders({
    "slider_1": 10,
    "slider_2": 20,
    "slider_3": 30
})
```

---

## 💡 更多範例創意

### 1. 自動生成練習變化版本
```python
# 為每個學生生成不同參數的相同練習
for i in range(1, 31):  # 30 個學生
    clear_document()
    create_circle_exercise(radius=10+i)
    save_document(f"student_{i:02d}_exercise.gh")
```

### 2. 進度追蹤
```python
# 記錄學生何時完成練習
log_completion(student_name, timestamp, score)
```

### 3. 互動式教學
```python
# 根據學生表現調整難度
if score < 60:
    create_easy_exercise()
elif score < 80:
    create_medium_exercise()
else:
    create_hard_exercise()
```

---

## 📞 需要幫助？

查看文檔：
- **API_REFERENCE.md** - 完整 API 說明
- **README_ENHANCED.md** - 功能介紹
- **IMPLEMENTATION_GUIDE.md** - 編譯增強版指南

---

**版本**: Basic Examples v1.0
**最後更新**: 2025-10-07
**適用於**: 基礎版 Grasshopper MCP
