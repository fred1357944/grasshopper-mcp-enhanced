using System;
using System.Collections.Generic;
using GH_MCP.Commands;
using GrasshopperMCP.Models;
using GrasshopperMCP.Commands;
using Grasshopper.Kernel;
using Rhino;
using System.Linq;

namespace GH_MCP.Commands
{
    /// <summary>
    /// 增強版 Grasshopper 命令註冊表
    /// 在原有基礎上添加教學導向的增強功能
    /// </summary>
    public static class GrasshopperCommandRegistry_Enhanced
    {
        private static readonly Dictionary<string, Func<Command, object>> CommandHandlers = new Dictionary<string, Func<Command, object>>();

        /// <summary>
        /// 初始化命令註冊表（增強版）
        /// </summary>
        public static void Initialize()
        {
            // === 原有命令 ===
            RegisterGeometryCommands();
            RegisterComponentCommands();
            RegisterDocumentCommands();
            RegisterIntentCommands();

            // === 新增：增強命令 ===
            RegisterEnhancedComponentCommands();

            RhinoApp.WriteLine("GH_MCP Enhanced: Command registry initialized with enhanced features.");
        }

        /// <summary>
        /// 註冊幾何命令
        /// </summary>
        private static void RegisterGeometryCommands()
        {
            RegisterCommand("create_point", GeometryCommandHandler.CreatePoint);
            RegisterCommand("create_curve", GeometryCommandHandler.CreateCurve);
            RegisterCommand("create_circle", GeometryCommandHandler.CreateCircle);
        }

        /// <summary>
        /// 註冊組件命令（原版）
        /// </summary>
        private static void RegisterComponentCommands()
        {
            RegisterCommand("add_component", ComponentCommandHandler.AddComponent);
            RegisterCommand("connect_components", ConnectionCommandHandler.ConnectComponents);
            RegisterCommand("set_component_value", ComponentCommandHandler.SetComponentValue);
            RegisterCommand("get_component_info", ComponentCommandHandler.GetComponentInfo);
        }

        /// <summary>
        /// 註冊增強組件命令（新版）
        /// </summary>
        private static void RegisterEnhancedComponentCommands()
        {
            // 1. 進階組件創建
            RegisterCommand("add_component_advanced", ComponentCommandHandler_Enhanced.AddComponentAdvanced);

            // 2. 獲取組件詳細資訊
            RegisterCommand("get_component_details", ComponentCommandHandler_Enhanced.GetComponentDetails);

            // 3. Slider 控制
            RegisterCommand("set_slider_value", ComponentCommandHandler_Enhanced.SetSliderValue);
            RegisterCommand("batch_set_sliders", ComponentCommandHandler_Enhanced.BatchSetSliders);

            // 4. 組件管理
            RegisterCommand("delete_component", ComponentCommandHandler_Enhanced.DeleteComponent);
            RegisterCommand("find_components_by_type", ComponentCommandHandler_Enhanced.FindComponentsByType);

            // 5. UI 組件控制
            RegisterCommand("set_panel_text", ComponentCommandHandler_Enhanced.SetPanelText);
            RegisterCommand("set_toggle_state", ComponentCommandHandler_Enhanced.SetToggleState);

            // 6. 數據讀取
            RegisterCommand("get_component_output_data", ComponentCommandHandler_Enhanced.GetComponentOutputData);
            RegisterCommand("get_all_connections", ComponentCommandHandler_Enhanced.GetAllConnections);

            RhinoApp.WriteLine("GH_MCP Enhanced: Registered 10 enhanced component commands.");
        }

        /// <summary>
        /// 註冊文檔命令
        /// </summary>
        private static void RegisterDocumentCommands()
        {
            RegisterCommand("get_document_info", DocumentCommandHandler.GetDocumentInfo);
            RegisterCommand("clear_document", DocumentCommandHandler.ClearDocument);
            RegisterCommand("save_document", DocumentCommandHandler.SaveDocument);
            RegisterCommand("load_document", DocumentCommandHandler.LoadDocument);
        }

        /// <summary>
        /// 註冊意圖命令
        /// </summary>
        private static void RegisterIntentCommands()
        {
            RegisterCommand("create_pattern", IntentCommandHandler.CreatePattern);
            RegisterCommand("get_available_patterns", IntentCommandHandler.GetAvailablePatterns);
        }

        /// <summary>
        /// 註冊命令處理器
        /// </summary>
        public static void RegisterCommand(string commandType, Func<Command, object> handler)
        {
            if (string.IsNullOrEmpty(commandType))
                throw new ArgumentNullException(nameof(commandType));

            if (handler == null)
                throw new ArgumentNullException(nameof(handler));

            CommandHandlers[commandType] = handler;
            RhinoApp.WriteLine($"GH_MCP Enhanced: Registered command handler for '{commandType}'");
        }

        /// <summary>
        /// 執行命令
        /// </summary>
        public static Response ExecuteCommand(Command command)
        {
            if (command == null)
                return Response.CreateError("Command is null");

            if (string.IsNullOrEmpty(command.Type))
                return Response.CreateError("Command type is null or empty");

            if (CommandHandlers.TryGetValue(command.Type, out var handler))
            {
                try
                {
                    var result = handler(command);
                    return Response.Ok(result);
                }
                catch (Exception ex)
                {
                    RhinoApp.WriteLine($"GH_MCP Enhanced: Error executing command '{command.Type}': {ex.Message}");
                    return Response.CreateError($"Error executing command '{command.Type}': {ex.Message}");
                }
            }

            return Response.CreateError($"No handler registered for command type '{command.Type}'");
        }

        /// <summary>
        /// 獲取所有已註冊的命令類型
        /// </summary>
        public static List<string> GetRegisteredCommandTypes()
        {
            return CommandHandlers.Keys.ToList();
        }
    }
}
