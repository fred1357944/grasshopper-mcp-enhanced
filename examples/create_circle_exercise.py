#!/usr/bin/env python3
"""
範例：自動創建圓形練習題
使用基礎功能創建教學練習
"""

import socket
import json
import time

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

def create_circle_exercise():
    """創建圓形練習題"""
    print("\n" + "="*70)
    print("創建圓形練習題")
    print("="*70)

    # 1. 創建 Number Slider（半徑）
    print("\n1️⃣  創建 Radius Slider...")
    slider = send_command("add_component", {
        "type": "slider",
        "x": 100,
        "y": 100
    })

    if slider.get("success"):
        slider_id = slider["data"]["id"]
        print(f"   ✅ Slider ID: {slider_id[:8]}...")

        # 設置 Slider 數值為 10
        send_command("set_component_value", {
            "id": slider_id,
            "value": "10"
        })
        print(f"   ✅ 設置初始值: 10")

    time.sleep(0.2)

    # 2. 創建 XY Plane
    print("\n2️⃣  創建 XY Plane...")
    plane = send_command("add_component", {
        "type": "xy plane",
        "x": 100,
        "y": 200
    })

    if plane.get("success"):
        plane_id = plane["data"]["id"]
        print(f"   ✅ Plane ID: {plane_id[:8]}...")

    time.sleep(0.2)

    # 3. 創建 Circle
    print("\n3️⃣  創建 Circle...")
    circle = send_command("add_component", {
        "type": "circle",
        "x": 400,
        "y": 150
    })

    if circle.get("success"):
        circle_id = circle["data"]["id"]
        print(f"   ✅ Circle ID: {circle_id[:8]}...")

    time.sleep(0.2)

    # 4. 創建提示 Panel
    print("\n4️⃣  創建提示 Panel...")
    panel = send_command("add_component", {
        "type": "panel",
        "x": 650,
        "y": 100
    })

    if panel.get("success"):
        panel_id = panel["data"]["id"]
        print(f"   ✅ Panel ID: {panel_id[:8]}...")

        # 設置 Panel 文字
        send_command("set_component_value", {
            "id": panel_id,
            "value": "練習任務：\n1. 連接 XY Plane → Circle (Plane)\n2. 連接 Slider → Circle (Radius)\n3. 調整 Slider 觀察圓的變化"
        })
        print(f"   ✅ 設置提示文字")

    print("\n" + "="*70)
    print("✅ 練習題創建完成！")
    print("📝 請在 Grasshopper 畫布中查看")
    print("="*70)

if __name__ == "__main__":
    try:
        create_circle_exercise()
    except Exception as e:
        print(f"\n❌ 錯誤: {e}")
