using System;
using System.Collections.Generic;
using GrasshopperMCP.Models;
using Grasshopper.Kernel;
using Grasshopper.Kernel.Parameters;
using Grasshopper.Kernel.Special;
using Rhino;
using Grasshopper;
using System.Linq;
using System.Threading;

namespace GrasshopperMCP.Commands
{
    /// <summary>
    /// 增強版組件命令處理器 - 添加教學導向功能
    /// </summary>
    public static class ComponentCommandHandler_Enhanced
    {
        /// <summary>
        /// 進階添加組件 - 支援初始參數設置
        /// 命令: add_component_advanced
        /// </summary>
        public static object AddComponentAdvanced(Command command)
        {
            string type = command.GetParameter<string>("type");
            double x = command.GetParameter<double>("x");
            double y = command.GetParameter<double>("y");

            // 可選參數
            object initialParamsObj = null;
            command.Parameters.TryGetValue("initialParams", out initialParamsObj);
            var initialParams = initialParamsObj as Dictionary<string, object>;

            string customName = command.GetParameterOrDefault<string>("name", null);
            int? width = command.GetParameterOrDefault<int?>("width", null);
            int? height = command.GetParameterOrDefault<int?>("height", null);

            object result = null;
            Exception exception = null;

            RhinoApp.InvokeOnUiThread(new Action(() =>
            {
                try
                {
                    var doc = Grasshopper.Instances.ActiveCanvas?.Document;
                    if (doc == null)
                        throw new InvalidOperationException("No active Grasshopper document");

                    IGH_DocumentObject component = CreateComponentByType(type);

                    if (component != null)
                    {
                        // 確保有屬性
                        if (component.Attributes == null)
                            component.CreateAttributes();

                        // 設置位置
                        component.Attributes.Pivot = new System.Drawing.PointF((float)x, (float)y);

                        // 設置自訂名稱
                        if (!string.IsNullOrEmpty(customName))
                            component.NickName = customName;

                        // 設置初始參數
                        if (initialParams != null)
                        {
                            SetInitialParameters(component, initialParams);
                        }

                        // TODO: 設置寬高（需要特殊處理不同組件類型）

                        // 添加到文檔
                        doc.AddObject(component, false);
                        doc.NewSolution(false);

                        result = new
                        {
                            componentId = component.InstanceGuid.ToString(),
                            type = component.GetType().Name,
                            name = component.NickName,
                            position = new { x = component.Attributes.Pivot.X, y = component.Attributes.Pivot.Y }
                        };
                    }
                }
                catch (Exception ex)
                {
                    exception = ex;
                    RhinoApp.WriteLine($"Error in AddComponentAdvanced: {ex.Message}");
                }
            }));

            while (result == null && exception == null)
                Thread.Sleep(10);

            if (exception != null)
                throw exception;

            return result;
        }

        /// <summary>
        /// 獲取組件詳細資訊
        /// 命令: get_component_details
        /// </summary>
        public static object GetComponentDetails(Command command)
        {
            string componentId = command.GetParameter<string>("componentId");

            object result = null;
            Exception exception = null;

            RhinoApp.InvokeOnUiThread(new Action(() =>
            {
                try
                {
                    var doc = Grasshopper.Instances.ActiveCanvas?.Document;
                    if (doc == null)
                        throw new InvalidOperationException("No active Grasshopper document");

                    Guid id;
                    if (!Guid.TryParse(componentId, out id))
                        throw new ArgumentException("Invalid component ID format");

                    IGH_DocumentObject component = doc.FindObject(id, true);
                    if (component == null)
                        throw new ArgumentException($"Component {componentId} not found");

                    var details = new Dictionary<string, object>
                    {
                        ["id"] = component.InstanceGuid.ToString(),
                        ["type"] = component.GetType().Name,
                        ["name"] = component.NickName,
                        ["description"] = component.Description,
                        ["position"] = new Dictionary<string, object>
                        {
                            ["x"] = component.Attributes.Pivot.X,
                            ["y"] = component.Attributes.Pivot.Y
                        },
                        ["size"] = new Dictionary<string, object>
                        {
                            ["width"] = component.Attributes.Bounds.Width,
                            ["height"] = component.Attributes.Bounds.Height
                        }
                    };

                    // Slider 特殊參數
                    if (component is GH_NumberSlider slider)
                    {
                        details["parameters"] = new Dictionary<string, object>
                        {
                            ["min"] = (double)slider.Slider.Minimum,
                            ["max"] = (double)slider.Slider.Maximum,
                            ["value"] = (double)slider.Slider.Value
                        };
                    }

                    // Panel 特殊參數
                    if (component is GH_Panel panel)
                    {
                        details["parameters"] = new Dictionary<string, object>
                        {
                            ["text"] = panel.UserText
                        };
                    }

                    // Toggle 特殊參數
                    if (component is GH_BooleanToggle toggle)
                    {
                        details["parameters"] = new Dictionary<string, object>
                        {
                            ["value"] = toggle.Value
                        };
                    }

                    // 輸入輸出參數
                    if (component is IGH_Component ghComponent)
                    {
                        var inputs = new List<Dictionary<string, object>>();
                        foreach (var param in ghComponent.Params.Input)
                        {
                            inputs.Add(new Dictionary<string, object>
                            {
                                ["name"] = param.Name,
                                ["nickname"] = param.NickName,
                                ["type"] = param.TypeName,
                                ["optional"] = param.Optional
                            });
                        }
                        details["inputs"] = inputs;

                        var outputs = new List<Dictionary<string, object>>();
                        foreach (var param in ghComponent.Params.Output)
                        {
                            outputs.Add(new Dictionary<string, object>
                            {
                                ["name"] = param.Name,
                                ["nickname"] = param.NickName,
                                ["type"] = param.TypeName
                            });
                        }
                        details["outputs"] = outputs;
                    }

                    // 連接資訊
                    var connections = new Dictionary<string, object>();
                    if (component is IGH_Param param)
                    {
                        var sources = new List<string>();
                        foreach (var source in param.Sources)
                        {
                            sources.Add(source.InstanceGuid.ToString());
                        }
                        connections["sources"] = sources;

                        var recipients = new List<string>();
                        foreach (var recipient in param.Recipients)
                        {
                            recipients.Add(recipient.InstanceGuid.ToString());
                        }
                        connections["recipients"] = recipients;
                    }
                    details["connections"] = connections;

                    result = details;
                }
                catch (Exception ex)
                {
                    exception = ex;
                    RhinoApp.WriteLine($"Error in GetComponentDetails: {ex.Message}");
                }
            }));

            while (result == null && exception == null)
                Thread.Sleep(10);

            if (exception != null)
                throw exception;

            return result;
        }

        /// <summary>
        /// 設置 Slider 數值
        /// 命令: set_slider_value
        /// </summary>
        public static object SetSliderValue(Command command)
        {
            string componentId = command.GetParameter<string>("componentId");
            double value = command.GetParameter<double>("value");

            object result = null;
            Exception exception = null;

            RhinoApp.InvokeOnUiThread(new Action(() =>
            {
                try
                {
                    var doc = Grasshopper.Instances.ActiveCanvas?.Document;
                    if (doc == null)
                        throw new InvalidOperationException("No active Grasshopper document");

                    Guid id;
                    if (!Guid.TryParse(componentId, out id))
                        throw new ArgumentException("Invalid component ID format");

                    IGH_DocumentObject component = doc.FindObject(id, true);
                    if (!(component is GH_NumberSlider slider))
                        throw new ArgumentException("Component is not a Number Slider");

                    slider.SetSliderValue((decimal)value);
                    slider.ExpireSolution(true);

                    result = new
                    {
                        componentId = component.InstanceGuid.ToString(),
                        value = (double)slider.Slider.Value
                    };
                }
                catch (Exception ex)
                {
                    exception = ex;
                    RhinoApp.WriteLine($"Error in SetSliderValue: {ex.Message}");
                }
            }));

            while (result == null && exception == null)
                Thread.Sleep(10);

            if (exception != null)
                throw exception;

            return result;
        }

        /// <summary>
        /// 刪除組件
        /// 命令: delete_component
        /// </summary>
        public static object DeleteComponent(Command command)
        {
            string componentId = command.GetParameter<string>("componentId");

            object result = null;
            Exception exception = null;

            RhinoApp.InvokeOnUiThread(new Action(() =>
            {
                try
                {
                    var doc = Grasshopper.Instances.ActiveCanvas?.Document;
                    if (doc == null)
                        throw new InvalidOperationException("No active Grasshopper document");

                    Guid id;
                    if (!Guid.TryParse(componentId, out id))
                        throw new ArgumentException("Invalid component ID format");

                    IGH_DocumentObject component = doc.FindObject(id, true);
                    if (component == null)
                        throw new ArgumentException("Component not found");

                    doc.RemoveObject(component, false);
                    doc.NewSolution(false);

                    result = new { success = true, componentId = componentId };
                }
                catch (Exception ex)
                {
                    exception = ex;
                    RhinoApp.WriteLine($"Error in DeleteComponent: {ex.Message}");
                }
            }));

            while (result == null && exception == null)
                Thread.Sleep(10);

            if (exception != null)
                throw exception;

            return result;
        }

        /// <summary>
        /// 按類型搜尋組件
        /// 命令: find_components_by_type
        /// </summary>
        public static object FindComponentsByType(Command command)
        {
            string componentType = command.GetParameter<string>("componentType");

            object result = null;
            Exception exception = null;

            RhinoApp.InvokeOnUiThread(new Action(() =>
            {
                try
                {
                    var doc = Grasshopper.Instances.ActiveCanvas?.Document;
                    if (doc == null)
                        throw new InvalidOperationException("No active Grasshopper document");

                    var componentIds = new List<string>();

                    foreach (var obj in doc.Objects)
                    {
                        if (obj.GetType().Name == componentType)
                        {
                            componentIds.Add(obj.InstanceGuid.ToString());
                        }
                    }

                    result = componentIds;
                }
                catch (Exception ex)
                {
                    exception = ex;
                    RhinoApp.WriteLine($"Error in FindComponentsByType: {ex.Message}");
                }
            }));

            while (result == null && exception == null)
                Thread.Sleep(10);

            if (exception != null)
                throw exception;

            return result;
        }

        /// <summary>
        /// 批量設置 Slider 數值
        /// 命令: batch_set_sliders
        /// </summary>
        public static object BatchSetSliders(Command command)
        {
            object sliderValuesObj = command.GetParameter<object>("sliderValues");
            var sliderValues = sliderValuesObj as Dictionary<string, object>;

            if (sliderValues == null)
                throw new ArgumentException("sliderValues must be a dictionary");

            object result = null;
            Exception exception = null;

            RhinoApp.InvokeOnUiThread(new Action(() =>
            {
                try
                {
                    var doc = Grasshopper.Instances.ActiveCanvas?.Document;
                    if (doc == null)
                        throw new InvalidOperationException("No active Grasshopper document");

                    var results = new List<Dictionary<string, object>>();

                    foreach (var kvp in sliderValues)
                    {
                        Guid id;
                        if (!Guid.TryParse(kvp.Key, out id))
                            continue;

                        IGH_DocumentObject component = doc.FindObject(id, true);
                        if (component is GH_NumberSlider slider)
                        {
                            double value = Convert.ToDouble(kvp.Value);
                            slider.SetSliderValue((decimal)value);

                            results.Add(new Dictionary<string, object>
                            {
                                ["componentId"] = kvp.Key,
                                ["value"] = value,
                                ["success"] = true
                            });
                        }
                    }

                    doc.NewSolution(false);
                    result = results;
                }
                catch (Exception ex)
                {
                    exception = ex;
                    RhinoApp.WriteLine($"Error in BatchSetSliders: {ex.Message}");
                }
            }));

            while (result == null && exception == null)
                Thread.Sleep(10);

            if (exception != null)
                throw exception;

            return result;
        }

        /// <summary>
        /// 設置 Panel 文字
        /// 命令: set_panel_text
        /// </summary>
        public static object SetPanelText(Command command)
        {
            string componentId = command.GetParameter<string>("componentId");
            string text = command.GetParameter<string>("text");

            object result = null;
            Exception exception = null;

            RhinoApp.InvokeOnUiThread(new Action(() =>
            {
                try
                {
                    var doc = Grasshopper.Instances.ActiveCanvas?.Document;
                    if (doc == null)
                        throw new InvalidOperationException("No active Grasshopper document");

                    Guid id;
                    if (!Guid.TryParse(componentId, out id))
                        throw new ArgumentException("Invalid component ID format");

                    IGH_DocumentObject component = doc.FindObject(id, true);
                    if (!(component is GH_Panel panel))
                        throw new ArgumentException("Component is not a Panel");

                    panel.UserText = text;
                    panel.ExpireSolution(true);

                    result = new { componentId = componentId, text = text };
                }
                catch (Exception ex)
                {
                    exception = ex;
                    RhinoApp.WriteLine($"Error in SetPanelText: {ex.Message}");
                }
            }));

            while (result == null && exception == null)
                Thread.Sleep(10);

            if (exception != null)
                throw exception;

            return result;
        }

        /// <summary>
        /// 設置 Toggle 狀態
        /// 命令: set_toggle_state
        /// </summary>
        public static object SetToggleState(Command command)
        {
            string componentId = command.GetParameter<string>("componentId");
            bool state = command.GetParameter<bool>("state");

            object result = null;
            Exception exception = null;

            RhinoApp.InvokeOnUiThread(new Action(() =>
            {
                try
                {
                    var doc = Grasshopper.Instances.ActiveCanvas?.Document;
                    if (doc == null)
                        throw new InvalidOperationException("No active Grasshopper document");

                    Guid id;
                    if (!Guid.TryParse(componentId, out id))
                        throw new ArgumentException("Invalid component ID format");

                    IGH_DocumentObject component = doc.FindObject(id, true);
                    if (!(component is GH_BooleanToggle toggle))
                        throw new ArgumentException("Component is not a Boolean Toggle");

                    toggle.Value = state;
                    toggle.ExpireSolution(true);

                    result = new { componentId = componentId, state = state };
                }
                catch (Exception ex)
                {
                    exception = ex;
                    RhinoApp.WriteLine($"Error in SetToggleState: {ex.Message}");
                }
            }));

            while (result == null && exception == null)
                Thread.Sleep(10);

            if (exception != null)
                throw exception;

            return result;
        }

        /// <summary>
        /// 獲取組件輸出數據
        /// 命令: get_component_output_data
        /// </summary>
        public static object GetComponentOutputData(Command command)
        {
            string componentId = command.GetParameter<string>("componentId");
            int outputIndex = command.GetParameterOrDefault<int>("outputIndex", 0);

            object result = null;
            Exception exception = null;

            RhinoApp.InvokeOnUiThread(new Action(() =>
            {
                try
                {
                    var doc = Grasshopper.Instances.ActiveCanvas?.Document;
                    if (doc == null)
                        throw new InvalidOperationException("No active Grasshopper document");

                    Guid id;
                    if (!Guid.TryParse(componentId, out id))
                        throw new ArgumentException("Invalid component ID format");

                    IGH_DocumentObject component = doc.FindObject(id, true);
                    if (component == null)
                        throw new ArgumentException("Component not found");

                    // 特殊處理 Slider
                    if (component is GH_NumberSlider slider)
                    {
                        result = new
                        {
                            outputName = "Number",
                            outputType = "double",
                            data = new object[] { (double)slider.CurrentValue }
                        };
                        return;
                    }

                    // 處理一般組件
                    if (component is IGH_Component ghComponent)
                    {
                        if (outputIndex < 0 || outputIndex >= ghComponent.Params.Output.Count)
                            throw new ArgumentException("Invalid output index");

                        var outputParam = ghComponent.Params.Output[outputIndex];
                        var dataList = new List<object>();

                        foreach (var item in outputParam.VolatileData.AllData(true))
                        {
                            dataList.Add(item.ToString());
                        }

                        result = new
                        {
                            outputName = outputParam.Name,
                            outputType = outputParam.TypeName,
                            data = dataList
                        };
                    }
                    else
                    {
                        throw new ArgumentException("Component does not have outputs");
                    }
                }
                catch (Exception ex)
                {
                    exception = ex;
                    RhinoApp.WriteLine($"Error in GetComponentOutputData: {ex.Message}");
                }
            }));

            while (result == null && exception == null)
                Thread.Sleep(10);

            if (exception != null)
                throw exception;

            return result;
        }

        /// <summary>
        /// 獲取所有連接
        /// 命令: get_all_connections
        /// </summary>
        public static object GetAllConnections(Command command)
        {
            object result = null;
            Exception exception = null;

            RhinoApp.InvokeOnUiThread(new Action(() =>
            {
                try
                {
                    var doc = Grasshopper.Instances.ActiveCanvas?.Document;
                    if (doc == null)
                        throw new InvalidOperationException("No active Grasshopper document");

                    var connections = new List<Dictionary<string, object>>();

                    foreach (var obj in doc.Objects)
                    {
                        if (obj is IGH_Component component)
                        {
                            foreach (var inputParam in component.Params.Input)
                            {
                                foreach (var source in inputParam.Sources)
                                {
                                    connections.Add(new Dictionary<string, object>
                                    {
                                        ["sourceId"] = source.Attributes.GetTopLevel.DocObject.InstanceGuid.ToString(),
                                        ["sourceParam"] = source.Name,
                                        ["targetId"] = obj.InstanceGuid.ToString(),
                                        ["targetParam"] = inputParam.Name
                                    });
                                }
                            }
                        }
                    }

                    result = connections;
                }
                catch (Exception ex)
                {
                    exception = ex;
                    RhinoApp.WriteLine($"Error in GetAllConnections: {ex.Message}");
                }
            }));

            while (result == null && exception == null)
                Thread.Sleep(10);

            if (exception != null)
                throw exception;

            return result;
        }

        // ======== 輔助方法 ========

        private static IGH_DocumentObject CreateComponentByType(string type)
        {
            // 嘗試從 ComponentServer 創建
            var proxy = Grasshopper.Instances.ComponentServer.ObjectProxies
                .FirstOrDefault(p => p.Desc.Name.Equals(type, StringComparison.OrdinalIgnoreCase));

            if (proxy != null)
                return proxy.CreateInstance();

            // 特殊處理常用組件
            switch (type.ToLowerInvariant())
            {
                case "gh_numberslider":
                case "numberslider":
                case "slider":
                    var slider = new GH_NumberSlider();
                    slider.SetInitCode("0.0 < 0.5 < 1.0");
                    return slider;

                case "gh_panel":
                case "panel":
                    return new GH_Panel();

                case "gh_booleantoggle":
                case "booleantoggle":
                case "toggle":
                    return new GH_BooleanToggle();

                case "param_point":
                case "point":
                    return new Param_Point();

                case "param_curve":
                case "curve":
                    return new Param_Curve();

                case "param_number":
                case "number":
                    return new Param_Number();

                default:
                    throw new ArgumentException($"Unknown component type: {type}");
            }
        }

        private static void SetInitialParameters(IGH_DocumentObject component, Dictionary<string, object> parameters)
        {
            if (component is GH_NumberSlider slider)
            {
                if (parameters.ContainsKey("min") && parameters.ContainsKey("max") && parameters.ContainsKey("value"))
                {
                    double min = Convert.ToDouble(parameters["min"]);
                    double max = Convert.ToDouble(parameters["max"]);
                    double value = Convert.ToDouble(parameters["value"]);

                    slider.SetInitCode($"{min} < {value} < {max}");
                }

                if (parameters.ContainsKey("name"))
                {
                    slider.NickName = parameters["name"].ToString();
                }
            }
            else if (component is GH_Panel panel)
            {
                if (parameters.ContainsKey("text"))
                {
                    panel.UserText = parameters["text"].ToString();
                }
            }
            else if (component is GH_BooleanToggle toggle)
            {
                if (parameters.ContainsKey("value"))
                {
                    toggle.Value = Convert.ToBoolean(parameters["value"]);
                }
            }
        }
    }

    /// <summary>
    /// 擴展方法，用於安全獲取參數
    /// </summary>
    public static class CommandExtensions
    {
        public static T GetParameterOrDefault<T>(this Command command, string key, T defaultValue)
        {
            if (command.Parameters.ContainsKey(key))
            {
                return command.GetParameter<T>(key);
            }
            return defaultValue;
        }
    }
}
