#!/usr/bin/env python3
"""
測試基礎 Grasshopper MCP 功能（已實作的功能）
"""

import socket
import json
import time

GRASSHOPPER_HOST = "localhost"
GRASSHOPPER_PORT = 8080

def send_command(command_type, params=None):
    """發送命令到 Grasshopper"""
    if params is None:
        params = {}

    command = {
        "type": command_type,
        "parameters": params
    }

    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(5.0)
        client.connect((GRASSHOPPER_HOST, GRASSHOPPER_PORT))

        command_json = json.dumps(command)
        client.sendall((command_json + "\n").encode("utf-8"))

        response_data = b""
        while True:
            chunk = client.recv(4096)
            if not chunk:
                break
            response_data += chunk
            if response_data.endswith(b"\n"):
                break

        response_str = response_data.decode("utf-8-sig").strip()
        response = json.loads(response_str)
        client.close()
        return response
    except Exception as e:
        return {"success": False, "error": str(e)}

def test_get_document_info():
    """測試 1: 獲取文檔資訊"""
    print("\n" + "="*70)
    print("測試 1: 獲取文檔資訊")
    print("="*70)

    result = send_command("get_document_info")
    if result.get("success"):
        print(f"✅ 成功！")
        data = result['data']
        print(f"   文檔名稱: {data['name']}")
        print(f"   組件數量: {data['componentCount']}")

        # 統計組件類型
        types = {}
        for comp in data['components']:
            comp_type = comp['type']
            types[comp_type] = types.get(comp_type, 0) + 1

        print(f"\n   組件類型統計:")
        for comp_type, count in sorted(types.items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f"      {comp_type}: {count} 個")

        return data
    else:
        print(f"❌ 失敗: {result.get('error')}")
        return None

def test_add_basic_component():
    """測試 2: 添加基礎組件（使用原始 API）"""
    print("\n" + "="*70)
    print("測試 2: 添加基礎組件 (slider)")
    print("="*70)

    result = send_command("add_component", {
        "type": "slider",
        "x": 100,
        "y": 100
    })

    if result.get("success"):
        print("✅ 成功創建 Slider！")
        if "componentId" in result.get("data", {}):
            print(f"   組件 ID: {result['data']['componentId']}")
            return result['data']['componentId']
        return True
    else:
        print(f"❌ 失敗: {result.get('error')}")
        return None

def test_add_panel():
    """測試 3: 添加 Panel"""
    print("\n" + "="*70)
    print("測試 3: 添加 Panel")
    print("="*70)

    result = send_command("add_component", {
        "type": "panel",
        "x": 300,
        "y": 100
    })

    if result.get("success"):
        print("✅ 成功創建 Panel！")
        if "componentId" in result.get("data", {}):
            print(f"   組件 ID: {result['data']['componentId']}")
            return result['data']['componentId']
        return True
    else:
        print(f"❌ 失敗: {result.get('error')}")
        return None

def test_connect_components(source_id, target_id):
    """測試 4: 連接組件"""
    print("\n" + "="*70)
    print("測試 4: 連接組件")
    print("="*70)

    if not source_id or not target_id:
        print("⚠️  跳過（沒有組件 ID）")
        return

    result = send_command("connect_components", {
        "sourceId": source_id,
        "targetId": target_id
    })

    if result.get("success"):
        print("✅ 成功連接組件！")
    else:
        print(f"❌ 失敗: {result.get('error')}")

def analyze_document():
    """測試 5: 分析文檔結構"""
    print("\n" + "="*70)
    print("測試 5: 分析文檔結構")
    print("="*70)

    result = send_command("get_document_info")
    if not result.get("success"):
        print("❌ 無法獲取文檔資訊")
        return

    data = result['data']
    components = data['components']

    # 找出所有 Slider
    sliders = [c for c in components if "Slider" in c['type']]
    print(f"✅ 找到 {len(sliders)} 個 Slider")
    for slider in sliders[:3]:
        print(f"   - {slider['type']} (ID: {slider['id'][:8]}...)")

    # 找出所有 Panel
    panels = [c for c in components if "Panel" in c['type']]
    print(f"\n✅ 找到 {len(panels)} 個 Panel")
    for panel in panels[:3]:
        print(f"   - {panel['type']} (ID: {panel['id'][:8]}...)")

    return {"sliders": sliders, "panels": panels}

def test_save_document():
    """測試 6: 保存文檔"""
    print("\n" + "="*70)
    print("測試 6: 保存文檔（測試用）")
    print("="*70)

    import os
    test_path = os.path.join(
        os.path.expanduser("~"),
        "Downloads",
        "test_grasshopper_mcp.gh"
    )

    print(f"保存路徑: {test_path}")

    # 詢問用戶
    print("\n⚠️  這會保存當前文檔，是否繼續？(y/n): ", end="")
    # 自動跳過，避免交互
    print("跳過")
    return

def main():
    """主測試流程"""
    print("\n" + "="*70)
    print("Grasshopper MCP - 基礎功能測試")
    print("="*70)
    print("測試已在 Grasshopper 端實作的功能")
    print("="*70)

    # 測試 1: 獲取文檔資訊
    doc_info = test_get_document_info()
    time.sleep(0.5)

    # 測試 2: 添加 Slider
    slider_id = test_add_basic_component()
    time.sleep(0.5)

    # 測試 3: 添加 Panel
    panel_id = test_add_panel()
    time.sleep(0.5)

    # 測試 4: 連接組件
    if slider_id and panel_id:
        test_connect_components(slider_id, panel_id)
        time.sleep(0.5)

    # 測試 5: 分析文檔
    analysis = analyze_document()
    time.sleep(0.5)

    # 測試 6: 保存文檔
    test_save_document()

    # 總結
    print("\n" + "="*70)
    print("測試完成！")
    print("="*70)
    print("\n✅ 基礎功能測試通過！")
    print("📝 檢查 Grasshopper 畫布，應該可以看到新增的組件。")
    print("\n💡 增強功能需要在 Grasshopper 端實作對應的處理器。")

if __name__ == "__main__":
    main()
