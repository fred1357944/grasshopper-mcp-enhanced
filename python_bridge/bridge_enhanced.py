import socket
import json
import os
import sys
import traceback
from typing import Dict, Any, Optional, List, Union

# 使用 MCP 服務器
from mcp.server.fastmcp import FastMCP

# 設置 Grasshopper MCP 連接參數
GRASSHOPPER_HOST = "localhost"
GRASSHOPPER_PORT = 8080  # 默認端口，可以根據需要修改

# 創建 MCP 服務器
server = FastMCP("Grasshopper Bridge Enhanced")

# ============================================================================
# 常用組件類型映射表
# ============================================================================
COMPONENT_TYPES = {
    # 參數組件
    "point": "Param_Point",
    "curve": "Param_Curve",
    "surface": "Param_Surface",
    "vector": "Param_Vector",
    "number": "Param_Number",
    "geometry": "Param_Geometry",

    # UI 組件
    "slider": "GH_NumberSlider",
    "panel": "GH_Panel",
    "toggle": "GH_BooleanToggle",
    "button": "GH_ButtonObject",
    "value_list": "GH_ValueList",

    # 數學組件
    "addition": "OperatorAdd",
    "subtraction": "OperatorSubtract",
    "multiplication": "OperatorMultiply",
    "division": "OperatorDivide",
    "negative": "OperatorSign",
    "series": "Component_Series",
    "range": "Component_Range",

    # 列表組件
    "list_item": "Component_ListItemVariable",
    "shift_list": "Component_ShiftList",
    "relative_item": "Component_RelativeItem",
    "partition_list": "Component_PartitionList",
    "merge": "Component_MergeVariable",
    "explode_tree": "GH_ExplodeTreeComponent",
    "shift_paths": "GH_ShiftDataPathComponent",
    "flatten": "Component_Flatten",
    "graft": "Component_Graft",

    # 向量組件
    "vector_2pt": "Component_Vector2Pt",
    "amplitude": "Component_VectorAmplitude",
    "unit_x": "Component_UnitVectorX",
    "unit_y": "Component_UnitVectorY",
    "unit_z": "Component_UnitVectorZ",
    "cross_product": "Component_VectorCrossProduct",
    "vector_display": "Component_VectorDisplay",
    "plane_normal": "Component_PlaneNormal",

    # 曲線組件
    "line": "Component_Line",
    "circle": "Component_Circle",
    "rectangle": "Component_Rectangle",
    "fit_line": "Component_LineFitPoints",
    "end_points": "Component_EndPoints",

    # 表面組件
    "surface_closest_point": "Component_SurfaceClosestPoint",
    "evaluate_surface": "Component_EvaluateSurface",
    "map_to_surface": "Component_MapOntoSurface",
    "surface_morph": "Component_MorphToSurfaceSpace",

    # 變換組件
    "move": "Component_Move",
    "rotate": "Component_Rotate",
    "scale": "Component_Scale",
    "extrude": "Component_Extrude",

    # 分析組件
    "area": "Component_AreaProperties",
    "length": "Component_Length",
    "deconstruct_point": "Component_DeconstructPoint",
    "deconstruct_brep": "Component_DeconstructBrep",
    "deconstruct_plane": "Component_DeconstructPlane",

    # 集合組件
    "create_set": "Component_CreateSet",
    "member_index": "Component_SetMemberIndex",

    # 其他常用組件
    "bounding_box": "Component_BoundingBox",
    "construct_plane": "Component_ConstructPlane",
    "relay": "GH_Relay",
}

# ============================================================================
# 核心通訊函數
# ============================================================================
def send_to_grasshopper(command_type: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """向 Grasshopper MCP 發送命令"""
    if params is None:
        params = {}

    # 創建命令
    command = {
        "type": command_type,
        "parameters": params
    }

    try:
        print(f"Sending command to Grasshopper: {command_type} with params: {params}", file=sys.stderr)

        # 連接到 Grasshopper MCP
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(10.0)  # 設置超時
        client.connect((GRASSHOPPER_HOST, GRASSHOPPER_PORT))

        # 發送命令
        command_json = json.dumps(command)
        client.sendall((command_json + "\n").encode("utf-8"))
        print(f"Command sent: {command_json}", file=sys.stderr)

        # 接收響應
        response_data = b""
        while True:
            chunk = client.recv(4096)
            if not chunk:
                break
            response_data += chunk
            if response_data.endswith(b"\n"):
                break

        # 處理可能的 BOM
        response_str = response_data.decode("utf-8-sig").strip()
        print(f"Response received: {response_str}", file=sys.stderr)

        # 解析 JSON 響應
        response = json.loads(response_str)
        client.close()
        return response
    except Exception as e:
        print(f"Error communicating with Grasshopper: {str(e)}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        return {
            "success": False,
            "error": f"Error communicating with Grasshopper: {str(e)}"
        }

# ============================================================================
# 基礎功能（保留原有）
# ============================================================================
@server.tool("add_component")
def add_component(component_type: str, x: float, y: float):
    """
    Add a component to the Grasshopper canvas (basic version)

    Args:
        component_type: Component type (point, curve, circle, line, panel, slider)
        x: X coordinate on the canvas
        y: Y coordinate on the canvas

    Returns:
        Result of adding the component
    """
    params = {
        "type": component_type,
        "x": x,
        "y": y
    }

    return send_to_grasshopper("add_component", params)

@server.tool("clear_document")
def clear_document():
    """Clear the Grasshopper document"""
    return send_to_grasshopper("clear_document")

@server.tool("save_document")
def save_document(path: str):
    """
    Save the Grasshopper document

    Args:
        path: Save path

    Returns:
        Result of the save operation
    """
    params = {
        "path": path
    }

    return send_to_grasshopper("save_document", params)

@server.tool("load_document")
def load_document(path: str):
    """
    Load a Grasshopper document

    Args:
        path: Document path

    Returns:
        Result of the load operation
    """
    params = {
        "path": path
    }

    return send_to_grasshopper("load_document", params)

@server.tool("get_document_info")
def get_document_info():
    """Get information about the Grasshopper document"""
    return send_to_grasshopper("get_document_info")

@server.tool("connect_components")
def connect_components(source_id: str, target_id: str, source_param: str = None, target_param: str = None, source_param_index: int = None, target_param_index: int = None):
    """
    Connect two components in the Grasshopper canvas

    Args:
        source_id: ID of the source component (output)
        target_id: ID of the target component (input)
        source_param: Name of the source parameter (optional)
        target_param: Name of the target parameter (optional)
        source_param_index: Index of the source parameter (optional, used if source_param is not provided)
        target_param_index: Index of the target parameter (optional, used if target_param is not provided)

    Returns:
        Result of connecting the components
    """
    params = {
        "sourceId": source_id,
        "targetId": target_id
    }

    if source_param is not None:
        params["sourceParam"] = source_param
    elif source_param_index is not None:
        params["sourceParamIndex"] = source_param_index

    if target_param is not None:
        params["targetParam"] = target_param
    elif target_param_index is not None:
        params["targetParamIndex"] = target_param_index

    return send_to_grasshopper("connect_components", params)

@server.tool("create_pattern")
def create_pattern(description: str):
    """
    Create a pattern of components based on a high-level description

    Args:
        description: High-level description of what to create (e.g., '3D voronoi cube')

    Returns:
        Result of creating the pattern
    """
    params = {
        "description": description
    }

    return send_to_grasshopper("create_pattern", params)

@server.tool("get_available_patterns")
def get_available_patterns(query: str):
    """
    Get a list of available patterns that match a query

    Args:
        query: Query to search for patterns

    Returns:
        List of available patterns
    """
    params = {
        "query": query
    }

    return send_to_grasshopper("get_available_patterns", params)

# ============================================================================
# 新增：增強功能 (Step 1)
# ============================================================================

@server.tool("add_component_advanced")
def add_component_advanced(
    component_type: str,
    x: float,
    y: float,
    initial_params: Optional[Dict[str, Any]] = None,
    name: Optional[str] = None,
    width: Optional[int] = None,
    height: Optional[int] = None
):
    """
    Add a component with advanced options (ENHANCED VERSION)

    Args:
        component_type: Component type from COMPONENT_TYPES (e.g., 'slider', 'panel', 'list_item')
        x: X coordinate on the canvas
        y: Y coordinate on the canvas
        initial_params: Initial parameters for the component (e.g., for slider: {"min": 0, "max": 100, "value": 50})
        name: Custom name for the component (optional)
        width: Component width in pixels (optional)
        height: Component height in pixels (optional)

    Returns:
        Result including component ID

    Example:
        add_component_advanced("slider", 100, 100, {"min": 0, "max": 100, "value": 50, "name": "Radius"})
        add_component_advanced("panel", 200, 200, {"text": "Hello World"})
    """
    # 映射組件類型
    mapped_type = COMPONENT_TYPES.get(component_type, component_type)

    params = {
        "type": mapped_type,
        "x": x,
        "y": y
    }

    if initial_params:
        params["initialParams"] = initial_params
    if name:
        params["name"] = name
    if width:
        params["width"] = width
    if height:
        params["height"] = height

    return send_to_grasshopper("add_component_advanced", params)

@server.tool("get_component_details")
def get_component_details(component_id: str):
    """
    Get detailed information about a specific component (ENHANCED VERSION)

    Args:
        component_id: The unique ID of the component

    Returns:
        Detailed component information including:
        - id: Component ID
        - type: Component type
        - name: Component name
        - position: {x, y} coordinates
        - size: {width, height}
        - parameters: Component parameters (e.g., slider value, panel text)
        - inputs: List of input parameters
        - outputs: List of output parameters with data
        - connections: Connected components

    Example:
        get_component_details("abc-123-def-456")
    """
    params = {
        "componentId": component_id
    }

    return send_to_grasshopper("get_component_details", params)

@server.tool("set_slider_value")
def set_slider_value(component_id: str, value: float):
    """
    Set the value of a Number Slider component (ENHANCED VERSION)

    Args:
        component_id: The ID of the slider component
        value: The new value to set

    Returns:
        Result of the operation

    Example:
        set_slider_value("slider_123", 75.5)
    """
    params = {
        "componentId": component_id,
        "value": value
    }

    return send_to_grasshopper("set_slider_value", params)

# ============================================================================
# 新增：實用工具功能
# ============================================================================

@server.tool("delete_component")
def delete_component(component_id: str):
    """
    Delete a component from the canvas

    Args:
        component_id: The ID of the component to delete

    Returns:
        Result of the operation
    """
    params = {
        "componentId": component_id
    }

    return send_to_grasshopper("delete_component", params)

@server.tool("get_all_connections")
def get_all_connections():
    """
    Get all component connections in the document

    Returns:
        List of all connections with source and target information
    """
    return send_to_grasshopper("get_all_connections")

@server.tool("find_components_by_type")
def find_components_by_type(component_type: str):
    """
    Find all components of a specific type

    Args:
        component_type: The type to search for (e.g., 'slider', 'panel', 'GH_NumberSlider')

    Returns:
        List of component IDs matching the type

    Example:
        find_components_by_type("slider")  # Find all sliders
        find_components_by_type("GH_NumberSlider")  # Same as above
    """
    # 映射組件類型
    mapped_type = COMPONENT_TYPES.get(component_type, component_type)

    params = {
        "componentType": mapped_type
    }

    return send_to_grasshopper("find_components_by_type", params)

@server.tool("batch_set_sliders")
def batch_set_sliders(slider_values: Dict[str, float]):
    """
    Set multiple slider values at once

    Args:
        slider_values: Dictionary mapping component IDs to values

    Example:
        batch_set_sliders({
            "slider_1": 50.0,
            "slider_2": 75.5,
            "slider_3": 100.0
        })
    """
    params = {
        "sliderValues": slider_values
    }

    return send_to_grasshopper("batch_set_sliders", params)

@server.tool("set_panel_text")
def set_panel_text(component_id: str, text: str):
    """
    Set the text content of a Panel component

    Args:
        component_id: The ID of the panel component
        text: The text to set

    Returns:
        Result of the operation
    """
    params = {
        "componentId": component_id,
        "text": text
    }

    return send_to_grasshopper("set_panel_text", params)

@server.tool("set_toggle_state")
def set_toggle_state(component_id: str, state: bool):
    """
    Set the state of a Boolean Toggle component

    Args:
        component_id: The ID of the toggle component
        state: True or False

    Returns:
        Result of the operation
    """
    params = {
        "componentId": component_id,
        "state": state
    }

    return send_to_grasshopper("set_toggle_state", params)

@server.tool("get_component_output_data")
def get_component_output_data(component_id: str, output_index: int = 0):
    """
    Get the output data from a component

    Args:
        component_id: The ID of the component
        output_index: The index of the output parameter (default: 0)

    Returns:
        The output data from the component

    Example:
        get_component_output_data("slider_123")  # Get slider value
        get_component_output_data("point_456", 0)  # Get point coordinates
    """
    params = {
        "componentId": component_id,
        "outputIndex": output_index
    }

    return send_to_grasshopper("get_component_output_data", params)

# ============================================================================
# 資源 (Resources)
# ============================================================================
@server.resource("grasshopper://status")
def get_grasshopper_status():
    """Get Grasshopper connection status"""
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(2.0)
        client.connect((GRASSHOPPER_HOST, GRASSHOPPER_PORT))
        client.close()
        return {"status": "connected", "host": GRASSHOPPER_HOST, "port": GRASSHOPPER_PORT}
    except:
        return {"status": "disconnected", "host": GRASSHOPPER_HOST, "port": GRASSHOPPER_PORT}

@server.resource("grasshopper://component_types")
def get_component_types():
    """Get list of supported component types"""
    return {
        "title": "Supported Component Types",
        "description": "List of component types that can be used with add_component_advanced",
        "types": COMPONENT_TYPES,
        "categories": {
            "Parameters": ["point", "curve", "surface", "vector", "number", "geometry"],
            "UI": ["slider", "panel", "toggle", "button", "value_list"],
            "Math": ["addition", "subtraction", "multiplication", "division", "negative", "series", "range"],
            "Lists": ["list_item", "shift_list", "relative_item", "partition_list", "merge", "explode_tree", "shift_paths", "flatten", "graft"],
            "Vectors": ["vector_2pt", "amplitude", "unit_x", "unit_y", "unit_z", "cross_product", "vector_display", "plane_normal"],
            "Curves": ["line", "circle", "rectangle", "fit_line", "end_points"],
            "Surfaces": ["surface_closest_point", "evaluate_surface", "map_to_surface", "surface_morph"],
            "Transform": ["move", "rotate", "scale", "extrude"],
            "Analysis": ["area", "length", "deconstruct_point", "deconstruct_brep", "deconstruct_plane"],
            "Sets": ["create_set", "member_index"],
            "Other": ["bounding_box", "construct_plane", "relay"]
        }
    }

@server.resource("grasshopper://component_guide")
def get_component_guide():
    """Get guide for Grasshopper components and connections"""
    return {
        "title": "Grasshopper Component Guide - Enhanced",
        "description": "Comprehensive guide for creating and connecting Grasshopper components",
        "version": "2.0 - Enhanced Edition",
        "new_features": [
            "50+ supported component types",
            "Advanced component creation with initial parameters",
            "Component detail inspection",
            "Slider value control",
            "Batch operations",
            "Panel text control",
            "Toggle state control",
            "Component deletion",
            "Type-based search"
        ],
        "components": [
            {
                "name": "Number Slider",
                "type": "slider",
                "category": "UI",
                "description": "Interactive number slider",
                "initial_params": {
                    "min": "Minimum value",
                    "max": "Maximum value",
                    "value": "Initial value",
                    "name": "Slider name"
                },
                "example": "add_component_advanced('slider', 100, 100, {'min': 0, 'max': 100, 'value': 50})"
            },
            {
                "name": "Panel",
                "type": "panel",
                "category": "UI",
                "description": "Text display panel",
                "initial_params": {
                    "text": "Panel content"
                },
                "example": "add_component_advanced('panel', 200, 200, {'text': 'Hello World'})"
            },
            {
                "name": "List Item",
                "type": "list_item",
                "category": "Lists",
                "description": "Extract item from list by index",
                "example": "add_component_advanced('list_item', 300, 300)"
            }
        ],
        "tips": [
            "Use add_component_advanced for more control over component creation",
            "Use get_component_details to inspect component state",
            "Use set_slider_value to control sliders programmatically",
            "Use find_components_by_type to locate specific component types",
            "Use batch_set_sliders to update multiple sliders efficiently"
        ]
    }

# ============================================================================
# 主程式入口
# ============================================================================
def main():
    """Main entry point for the Enhanced Grasshopper MCP Bridge Server"""
    try:
        print("=" * 70, file=sys.stderr)
        print("Starting Grasshopper MCP Bridge Server (ENHANCED VERSION)", file=sys.stderr)
        print("=" * 70, file=sys.stderr)
        print(f"Version: 2.0", file=sys.stderr)
        print(f"Host: {GRASSHOPPER_HOST}", file=sys.stderr)
        print(f"Port: {GRASSHOPPER_PORT}", file=sys.stderr)
        print(f"Supported Components: {len(COMPONENT_TYPES)} types", file=sys.stderr)
        print("=" * 70, file=sys.stderr)
        print("Please add this MCP server to Claude Desktop", file=sys.stderr)
        print("=" * 70, file=sys.stderr)
        server.run()
    except Exception as e:
        print(f"Error starting MCP server: {str(e)}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
