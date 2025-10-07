# 測試與示範

## 📋 檔案說明

### test_basic.py
測試基礎 MCP 功能（6 個基本 API）

**功能測試**：
- ✅ 連接到 Grasshopper
- ✅ 獲取文檔資訊
- ✅ 創建組件（Slider, Panel）
- ✅ 連接組件
- ✅ 分析文檔結構

**運行方式**：
```bash
# 確保 Grasshopper 已開啟並運行 MCP 組件 (port 8080)
python3 tests/test_basic.py
```

**預期結果**：
```
✅ 所有測試通過
- 成功連接到 Grasshopper
- 創建了 Slider 和 Panel
- 連接成功
- 找到 6 個 Slider
```

---

### test_enhanced.py
測試增強功能（10 個進階 API）

**功能測試**：
- ⏳ add_component_advanced
- ⏳ get_component_details
- ⏳ set_slider_value
- ⏳ 等其他增強功能

**注意**：這些功能需要編譯 C# 組件才能使用

**運行方式**：
```bash
python3 tests/test_enhanced.py
```

**預期結果**（未編譯 C#）：
```
❌ No handler registered for command type 'add_component_advanced'
（這是正常的，需要編譯 C# 組件）
```

---

### ai_grading_demo.py ⭐
**AI 協作評分系統示範**

這是本專案的核心功能展示。

#### 🎯 功能

1. **提取 Grasshopper 作業資訊**
   - 文檔名稱
   - 組件總數
   - 組件類型分布

2. **AI 智慧評分**
   - 理解作業要求
   - 分析學生作業
   - 給出分數與等級

3. **詳細反饋**
   - ✅ 優點分析
   - ⚠️  需要改進的地方
   - 💡 具體建議
   - 📝 詳細評語

#### 🚀 運行方式

```bash
# 方式 1: 連接實際 Grasshopper
# 確保 Grasshopper 已開啟並運行 MCP 組件
python3 tests/ai_grading_demo.py

# 方式 2: 使用模擬資料（無需 Grasshopper）
# 腳本會自動檢測連接失敗並使用模擬資料
python3 tests/ai_grading_demo.py
```

#### 📊 輸出範例

```
======================================================================
AI 協作評分系統
======================================================================
📊 正在提取 Grasshopper 作業資訊...
✅ 成功連接 - 讀取到 33 個組件

🤖 AI 評分分析中...

======================================================================
📋 評分提示（會被 Claude AI 處理）:
======================================================================
你是一位 Grasshopper 教學專家，請評分這份學生作業。

## 作業要求
作業名稱：幕牆嵌板的展平和標注

要求：
1. 使用 Unroll 組件展平曲面
2. 使用 Dimension 組件標注尺寸
3. 使用 Slider 控制參數
4. 排列整齊，有清楚的註解
5. 邏輯清晰，避免不必要的組件

## 學生提交的作業資訊
- 文檔名稱: 幕墙嵌板的展平和标注*
- 組件總數: 33
- 組件類型分布:
  - GH_Markup: 10 個
  - GH_NumberSlider: 4 個
  - UnrollBrep: 1 個
  - Component_PolylineEdgeDimension: 1 個
  ...

======================================================================

📤 正在將評分結果傳回 Grasshopper...

╔══════════════════════════════════╗
║     AI 評分結果                   ║
╚══════════════════════════════════╝

📊 分數: 85/100
🎯 等級: B+

✅ 優點:
  • 正確使用了 Number Slider 控制參數
  • 文檔組織清晰，有適當的註解（10個 Markup）
  • 使用了 Unroll 展平曲面，達成基本要求

⚠️  需要改進:
  • 組件數量較多（33個），可能可以簡化邏輯
  • Markup 組件過多，可以整合

💡 建議:
  • 建議使用 Group 將相關組件組織起來
  • 可以考慮使用 Data Dam 優化運算效率
  • 將多個 Markup 整合為更少的文字說明

📝 詳細評語:
這份作業達成了基本要求，能夠正確展平曲面並標注尺寸。使用了
適當的組件類型，邏輯清晰。但組件數量偏多（33個），特別是
Markup 組件有10個，建議簡化。整體來說是一份合格的作業（85分，
B+），但仍有優化空間。

✅ 評分完成
```

#### 🔧 自定義評分標準

修改 `ai_grading_demo.py` 中的 `assignment_requirements`：

```python
assignment_requirements = """
作業名稱：你的作業名稱

要求：
1. 你的要求 1
2. 你的要求 2
3. ...

評分重點：
- 重點 1 (30%)
- 重點 2 (30%)
- ...
"""
```

#### 💡 實際使用場景

**場景 1: 課堂即時評分**
```bash
# 學生完成練習後
python3 tests/ai_grading_demo.py

# AI 立即給出反饋
# 老師可以投影顯示結果並講解
```

**場景 2: 批量評分作業**
```python
# 修改腳本，批量處理多個檔案
for student_file in ["張三.gh", "李四.gh", "王五.gh"]:
    result = grade_assignment(student_file)
    save_report(result)
```

**場景 3: 學生自評**
```bash
# 學生自己運行評分
python3 tests/ai_grading_demo.py

# 根據 AI 建議改進
# 重新評分看進步情況
```

---

## 🎓 教學應用

### 1. 基礎測試（test_basic.py）

**適合**：
- 確認 MCP 連接正常
- 測試基礎 API 功能
- 學習如何使用 MCP 工具

### 2. AI 評分系統（ai_grading_demo.py）⭐

**適合**：
- Grasshopper 課程作業評分
- 即時反饋與指導
- 學生自我評估
- 批量處理班級作業

**優勢**：
- ✅ 評分一致性高
- ✅ 給出具體建議
- ✅ 省時省力
- ✅ 學生能從反饋中學習

---

## 📚 進一步閱讀

- [AI 評分系統完整文檔](../docs/AI_GRADING_SYSTEM.md)
- [API 參考手冊](../docs/API_REFERENCE.md)
- [實作指南](../docs/IMPLEMENTATION_GUIDE.md)

---

## ❓ 常見問題

### Q1: 為什麼顯示「無法連接到 Grasshopper」？

**A**: 請確認：
1. Rhino/Grasshopper 已開啟
2. grasshopper-mcp 組件已放置在畫布上
3. MCP 組件顯示 "Server running on port 8080"

### Q2: test_enhanced.py 為什麼失敗？

**A**: 增強功能需要編譯 C# 組件，請參考 [實作指南](../docs/IMPLEMENTATION_GUIDE.md)

### Q3: 如何在 Claude Code 中使用？

**A**: 在 Claude Code 中直接呼叫：
```
@grasshopper-mcp 請評分這份學生作業
```

Claude 會自動：
1. 使用 MCP 工具讀取 Grasshopper 資訊
2. 分析作業品質
3. 給出評分與建議

---

**測試愉快！** 🚀
