#!/usr/bin/env python3
"""
測試增強版 Grasshopper MCP 功能
確保 Grasshopper 已在 port 8080 啟動
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

def test_connection():
    """測試 1: 連接測試"""
    print("\n" + "="*70)
    print("測試 1: 連接測試")
    print("="*70)

    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(2.0)
        client.connect((GRASSHOPPER_HOST, GRASSHOPPER_PORT))
        client.close()
        print("✅ 連接成功！")
        return True
    except Exception as e:
        print(f"❌ 連接失敗: {e}")
        print("\n請確認：")
        print("1. Grasshopper 已開啟")
        print("2. MCP 組件已放置在畫布上")
        print("3. Port 設置為 8080")
        return False

def test_get_document_info():
    """測試 2: 獲取文檔資訊"""
    print("\n" + "="*70)
    print("測試 2: 獲取文檔資訊")
    print("="*70)

    result = send_command("get_document_info")
    if result.get("success"):
        print(f"✅ 成功！")
        print(f"   文檔名稱: {result['data']['name']}")
        print(f"   組件數量: {result['data']['componentCount']}")
        print(f"   前 5 個組件:")
        for i, comp in enumerate(result['data']['components'][:5]):
            print(f"      {i+1}. {comp['type']} (ID: {comp['id'][:8]}...)")
        return result
    else:
        print(f"❌ 失敗: {result.get('error')}")
        return None

def test_add_component_advanced():
    """測試 3: 創建進階組件"""
    print("\n" + "="*70)
    print("測試 3: 創建進階組件 (Number Slider)")
    print("="*70)

    params = {
        "type": "GH_NumberSlider",
        "x": 100,
        "y": 100,
        "initialParams": {
            "min": 0,
            "max": 100,
            "value": 50,
            "name": "Test Slider"
        }
    }

    result = send_command("add_component_advanced", params)
    if result.get("success"):
        print("✅ 成功創建 Number Slider！")
        if "componentId" in result.get("data", {}):
            component_id = result["data"]["componentId"]
            print(f"   組件 ID: {component_id}")
            return component_id
        return True
    else:
        print(f"❌ 失敗: {result.get('error')}")
        return None

def test_get_component_details(component_id):
    """測試 4: 獲取組件詳細資訊"""
    print("\n" + "="*70)
    print("測試 4: 獲取組件詳細資訊")
    print("="*70)

    if not component_id:
        print("⚠️  跳過（沒有組件 ID）")
        return

    params = {"componentId": component_id}
    result = send_command("get_component_details", params)

    if result.get("success"):
        print("✅ 成功！")
        data = result.get("data", {})
        print(f"   類型: {data.get('type')}")
        print(f"   名稱: {data.get('name')}")
        print(f"   位置: {data.get('position')}")
        print(f"   參數: {data.get('parameters')}")
    else:
        print(f"❌ 失敗: {result.get('error')}")

def test_set_slider_value(component_id):
    """測試 5: 設置 Slider 數值"""
    print("\n" + "="*70)
    print("測試 5: 設置 Slider 數值")
    print("="*70)

    if not component_id:
        print("⚠️  跳過（沒有 Slider ID）")
        return

    params = {
        "componentId": component_id,
        "value": 75.5
    }

    result = send_command("set_slider_value", params)
    if result.get("success"):
        print("✅ 成功將 Slider 設置為 75.5！")
    else:
        print(f"❌ 失敗: {result.get('error')}")

def test_find_components_by_type():
    """測試 6: 搜尋組件"""
    print("\n" + "="*70)
    print("測試 6: 搜尋所有 Number Slider")
    print("="*70)

    params = {"componentType": "GH_NumberSlider"}
    result = send_command("find_components_by_type", params)

    if result.get("success"):
        components = result.get("data", [])
        print(f"✅ 找到 {len(components)} 個 Number Slider")
        for i, comp_id in enumerate(components[:3]):
            print(f"   {i+1}. {comp_id[:8]}...")
        return components
    else:
        print(f"❌ 失敗: {result.get('error')}")
        return []

def test_batch_set_sliders(slider_ids):
    """測試 7: 批量設置 Slider"""
    print("\n" + "="*70)
    print("測試 7: 批量設置多個 Slider")
    print("="*70)

    if not slider_ids:
        print("⚠️  跳過（沒有 Slider）")
        return

    # 為每個 slider 設置不同的值
    slider_values = {}
    for i, slider_id in enumerate(slider_ids[:3]):
        slider_values[slider_id] = 10 + (i * 20)

    params = {"sliderValues": slider_values}
    result = send_command("batch_set_sliders", params)

    if result.get("success"):
        print(f"✅ 成功批量設置 {len(slider_values)} 個 Slider！")
        for slider_id, value in slider_values.items():
            print(f"   {slider_id[:8]}... → {value}")
    else:
        print(f"❌ 失敗: {result.get('error')}")

def main():
    """主測試流程"""
    print("\n" + "="*70)
    print("Grasshopper MCP Enhanced - 功能測試")
    print("="*70)

    # 測試 1: 連接
    if not test_connection():
        print("\n❌ 連接失敗，終止測試")
        return

    time.sleep(0.5)

    # 測試 2: 獲取文檔資訊
    doc_info = test_get_document_info()
    time.sleep(0.5)

    # 測試 3: 創建組件
    slider_id = test_add_component_advanced()
    time.sleep(0.5)

    # 測試 4: 獲取組件詳情
    if slider_id:
        test_get_component_details(slider_id)
        time.sleep(0.5)

    # 測試 5: 設置 Slider 值
    if slider_id:
        test_set_slider_value(slider_id)
        time.sleep(0.5)

    # 測試 6: 搜尋組件
    slider_ids = test_find_components_by_type()
    time.sleep(0.5)

    # 測試 7: 批量設置
    if slider_ids:
        test_batch_set_sliders(slider_ids)

    # 總結
    print("\n" + "="*70)
    print("測試完成！")
    print("="*70)
    print("\n如果所有測試都顯示 ✅，表示增強版功能正常運作！")
    print("檢查 Grasshopper 畫布，應該可以看到新創建的 Number Slider。")

if __name__ == "__main__":
    main()
