#!/usr/bin/env python3
"""
AI 協作評分系統 Demo
展示如何結合 MCP + Claude AI 進行智慧評分

注意：這是架構示範，實際使用時可以：
1. 使用 Claude Code 的 MCP 功能直接呼叫
2. 或使用 Anthropic API（需要 pip install anthropic）
"""

import socket
import json

GRASSHOPPER_HOST = "localhost"
GRASSHOPPER_PORT = 8080

def send_command(command_type, params=None):
    """發送命令到 Grasshopper"""
    command = {
        "type": command_type,
        "parameters": params or {}
    }

    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((GRASSHOPPER_HOST, GRASSHOPPER_PORT))

        command_json = json.dumps(command)
        client.sendall((command_json + "\n").encode("utf-8"))

        response_data = b""
        while True:
            chunk = client.recv(4096)
            if not chunk:
                break
            response_data += chunk
            if b"\n" in chunk:
                break

        client.close()

        response = json.loads(response_data.decode("utf-8"))
        return response

    except Exception as e:
        return {"success": False, "error": str(e)}

def extract_grasshopper_context():
    """從 Grasshopper 提取完整作業資訊"""

    print("📊 正在提取 Grasshopper 作業資訊...")

    try:
        # 1. 文檔基本資訊
        doc_info = send_command("get_document_info")

        if not doc_info.get("success"):
            print(f"⚠️  無法連接到 Grasshopper (port {GRASSHOPPER_PORT})")
            print("   請確認：")
            print("   1. Grasshopper 已開啟")
            print("   2. grasshopper-mcp 組件已放置在畫布上")
            print("   3. MCP 組件顯示 'Server running on port 8080'")
            print("\n   使用模擬資料示範...")

            # 使用示範資料
            return {
                "document_name": "幕墙嵌板的展平和标注*",
                "total_components": 33,
                "component_types": {
                    "GH_Markup": 10,
                    "GH_NumberSlider": 4,
                    "GH_BooleanToggle": 2,
                    "GH_ValueList": 2,
                    "Component_Circle": 2,
                    "GH_Panel": 2,
                    "Param_Surface": 1,
                    "UnrollBrep": 1,
                    "ArrangeInGrid": 1,
                    "Component_PolylineEdgeDimension": 1
                }
            }

        # 解析實際資料
        data = doc_info.get("data", {})
        context = {
            "document_name": data.get("name", "未命名"),
            "total_components": data.get("component_count", 0),
            "component_types": data.get("component_types", {}),
            # 未來加上：
            # "connections": connections,
            # "data_flow": analyze_data_flow(components_details),
            # "component_details": components_details
        }

        print(f"✅ 成功連接 - 讀取到 {context['total_components']} 個組件")
        return context

    except Exception as e:
        print(f"❌ 連接錯誤: {e}")
        print("   使用模擬資料示範...\n")

        # 使用示範資料
        return {
            "document_name": "幕墙嵌板的展平和标注*",
            "total_components": 33,
            "component_types": {
                "GH_Markup": 10,
                "GH_NumberSlider": 4,
                "GH_BooleanToggle": 2,
                "GH_ValueList": 2,
                "Component_Circle": 2,
                "GH_Panel": 2,
                "Param_Surface": 1,
                "UnrollBrep": 1,
                "ArrangeInGrid": 1,
                "Component_PolylineEdgeDimension": 1
            }
        }

def prepare_grading_prompt(context, assignment_requirements):
    """準備給 Claude 的評分提示"""

    prompt = f"""你是一位 Grasshopper 教學專家，請評分這份學生作業。

## 作業要求
{assignment_requirements}

## 學生提交的作業資訊
- 文檔名稱: {context['document_name']}
- 組件總數: {context['total_components']}

組件類型分布:
"""

    for comp_type, count in context['component_types'].items():
        prompt += f"- {comp_type}: {count} 個\n"

    prompt += """
## 請評分並給出詳細反饋

請以 JSON 格式回覆：
{
  "score": <0-100 的分數>,
  "grade": "<等級：A/B/C/D/F>",
  "strengths": ["優點1", "優點2", ...],
  "weaknesses": ["缺點1", "缺點2", ...],
  "suggestions": ["建議1", "建議2", ...],
  "detailed_feedback": "<詳細評語>"
}

評分標準：
1. 是否達成作業要求（40分）
2. 邏輯合理性與效率（30分）
3. 組件使用的適當性（20分）
4. 代碼組織與可讀性（10分）
"""

    return prompt

def ai_grade_assignment(context, assignment_requirements):
    """使用 Claude AI 評分作業

    這個函數展示評分的流程架構。
    實際使用時，可以：
    1. 在 Claude Code 中直接使用這個工具讀取 Grasshopper 資訊
    2. Claude 會自動分析並給出智慧評分
    3. 結果可以傳回 Grasshopper 顯示
    """

    print("\n🤖 AI 評分分析中...")

    # 準備提示（這個提示會被 Claude 看到）
    prompt = prepare_grading_prompt(context, assignment_requirements)

    print("\n" + "="*70)
    print("📋 評分提示（會被 Claude AI 處理）:")
    print("="*70)
    print(prompt)
    print("="*70)

    # 模擬 AI 評分結果（實際使用時 Claude 會給出真實分析）
    print("\n⚠️  這是模擬結果 - 實際使用時 Claude 會根據作業內容給出真實評分")

    return {
        "score": 85,
        "grade": "B+",
        "strengths": [
            "正確使用了 Number Slider 控制參數",
            "文檔組織清晰，有適當的註解（10個 Markup）",
            "使用了 Unroll 展平曲面，達成基本要求"
        ],
        "weaknesses": [
            "組件數量較多（33個），可能可以簡化邏輯",
            "Markup 組件過多，可以整合"
        ],
        "suggestions": [
            "建議使用 Group 將相關組件組織起來",
            "可以考慮使用 Data Dam 優化運算效率",
            "將多個 Markup 整合為更少的文字說明"
        ],
        "detailed_feedback": "這份作業達成了基本要求，能夠正確展平曲面並標注尺寸。使用了適當的組件類型，邏輯清晰。但組件數量偏多（33個），特別是 Markup 組件有10個，建議簡化。整體來說是一份合格的作業（85分，B+），但仍有優化空間。"
    }

def display_result_in_grasshopper(grading_result):
    """將評分結果顯示在 Grasshopper 中"""

    print("\n📤 正在將評分結果傳回 Grasshopper...")

    # 格式化結果為易讀的文字
    result_text = f"""
╔══════════════════════════════════╗
║     AI 評分結果                   ║
╚══════════════════════════════════╝

📊 分數: {grading_result['score']}/100
🎯 等級: {grading_result['grade']}

✅ 優點:
"""

    for strength in grading_result.get('strengths', []):
        result_text += f"  • {strength}\n"

    result_text += "\n⚠️  需要改進:\n"
    for weakness in grading_result.get('weaknesses', []):
        result_text += f"  • {weakness}\n"

    result_text += "\n💡 建議:\n"
    for suggestion in grading_result.get('suggestions', []):
        result_text += f"  • {suggestion}\n"

    result_text += f"\n📝 詳細評語:\n{grading_result.get('detailed_feedback', '')}\n"

    # 創建一個 Panel 顯示結果（或更新現有的 Panel）
    # send_command("set_panel_text", {
    #     "component_id": "grading_result_panel",
    #     "text": result_text
    # })

    # 目前先印出來
    print(result_text)

    return result_text

def main():
    """主流程：提取資訊 → AI 評分 → 顯示結果"""

    print("=" * 70)
    print("AI 協作評分系統")
    print("=" * 70)

    # 1. 從 Grasshopper 提取作業資訊
    context = extract_grasshopper_context()

    # 2. 定義作業要求
    assignment_requirements = """
作業名稱：幕牆嵌板的展平和標注

要求：
1. 使用 Unroll 組件展平曲面
2. 使用 Dimension 組件標注尺寸
3. 使用 Slider 控制參數
4. 排列整齊，有清楚的註解
5. 邏輯清晰，避免不必要的組件
"""

    # 3. 使用 AI 評分
    grading_result = ai_grade_assignment(
        context,
        assignment_requirements
    )

    # 4. 顯示結果到 Grasshopper
    display_result_in_grasshopper(grading_result)

    print("\n✅ 評分完成")

if __name__ == "__main__":
    main()
