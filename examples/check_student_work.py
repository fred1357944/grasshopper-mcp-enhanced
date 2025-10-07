#!/usr/bin/env python3
"""
範例：檢查學生作業
分析文檔中的組件並給出評分建議
"""

import socket
import json

def send_command(command_type, params=None):
    """發送命令到 Grasshopper"""
    if params is None:
        params = {}

    command = {
        "type": command_type,
        "parameters": params
    }

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("localhost", 8080))
    client.sendall((json.dumps(command) + "\n").encode("utf-8"))

    response = b""
    while True:
        chunk = client.recv(4096)
        if not chunk:
            break
        response += chunk
        if response.endswith(b"\n"):
            break

    result = json.loads(response.decode("utf-8-sig").strip())
    client.close()
    return result

def check_student_work():
    """檢查學生作業並評分"""
    print("\n" + "="*70)
    print("學生作業檢查系統")
    print("="*70)

    # 獲取文檔資訊
    doc = send_command("get_document_info")

    if not doc.get("success"):
        print("❌ 無法獲取文檔資訊")
        return

    data = doc["data"]
    components = data["components"]

    print(f"\n📄 文檔名稱: {data['name']}")
    print(f"📊 組件總數: {data['componentCount']}")

    # 統計組件類型
    type_counts = {}
    for comp in components:
        comp_type = comp["type"]
        type_counts[comp_type] = type_counts.get(comp_type, 0) + 1

    print("\n📋 組件類型統計:")
    for comp_type, count in sorted(type_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"   • {comp_type}: {count} 個")

    # === 評分系統 ===
    print("\n" + "="*70)
    print("📝 評分結果")
    print("="*70)

    score = 0
    max_score = 100
    feedback = []

    # 1. 檢查是否有 Slider（10分）
    slider_count = type_counts.get("GH_NumberSlider", 0)
    if slider_count > 0:
        score += 10
        feedback.append(f"✅ 使用了 Number Slider ({slider_count} 個) +10分")
    else:
        feedback.append(f"❌ 缺少 Number Slider 0分")

    # 2. 檢查是否有幾何組件（20分）
    geometry_types = ["Component_Circle", "Component_Rectangle", "Component_Line"]
    has_geometry = any(t in type_counts for t in geometry_types)
    if has_geometry:
        score += 20
        feedback.append(f"✅ 包含幾何組件 +20分")
    else:
        feedback.append(f"⚠️  缺少幾何組件 0分")

    # 3. 組件數量適中（20分）
    if 10 <= data['componentCount'] <= 50:
        score += 20
        feedback.append(f"✅ 組件數量適中 ({data['componentCount']} 個) +20分")
    elif data['componentCount'] < 10:
        score += 10
        feedback.append(f"⚠️  組件數量較少 ({data['componentCount']} 個) +10分")
    else:
        score += 15
        feedback.append(f"⚠️  組件數量較多 ({data['componentCount']} 個) +15分")

    # 4. 使用了參數組件（15分）
    param_types = ["Param_Point", "Param_Curve", "Param_Surface", "Param_Number"]
    param_count = sum(type_counts.get(t, 0) for t in param_types)
    if param_count > 0:
        score += 15
        feedback.append(f"✅ 使用了參數組件 ({param_count} 個) +15分")
    else:
        feedback.append(f"❌ 缺少參數組件 0分")

    # 5. 組織性（使用 Group 或 Panel）（15分）
    has_organization = type_counts.get("GH_Panel", 0) > 0 or type_counts.get("GH_Group", 0) > 0
    if has_organization:
        score += 15
        feedback.append(f"✅ 有組織（Panel/Group） +15分")
    else:
        feedback.append(f"⚠️  缺少組織工具 0分")

    # 6. 基礎分（20分）
    score += 20
    feedback.append(f"✅ 基礎分 +20分")

    # 顯示結果
    print(f"\n📊 總分: {score}/{max_score}")
    print(f"🎯 等級: {get_grade(score)}")

    print("\n詳細評分：")
    for item in feedback:
        print(f"   {item}")

    # 建議
    print("\n💡 改進建議：")
    if slider_count == 0:
        print("   • 添加 Number Slider 以控制參數")
    if not has_geometry:
        print("   • 添加幾何組件（Circle, Rectangle, Line 等）")
    if not has_organization:
        print("   • 使用 Panel 或 Group 來組織和註釋你的工作")
    if param_count == 0:
        print("   • 使用參數組件來提高可重用性")

    print("\n" + "="*70)

def get_grade(score):
    """根據分數返回等級"""
    if score >= 90:
        return "優秀 (A)"
    elif score >= 80:
        return "良好 (B)"
    elif score >= 70:
        return "中等 (C)"
    elif score >= 60:
        return "及格 (D)"
    else:
        return "不及格 (F)"

if __name__ == "__main__":
    try:
        check_student_work()
    except Exception as e:
        print(f"\n❌ 錯誤: {e}")
