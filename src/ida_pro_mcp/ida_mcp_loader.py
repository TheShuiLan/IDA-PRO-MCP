"""IDA Pro MCP Plugin Loader

这是一个轻量级的插件加载器，用于在 IDA Pro 中注册插件。
实际的服务器实现在 ida_mcp_plugin 模块中。
"""

import sys
import idaapi


class MCP(idaapi.plugin_t):
    """IDA Pro MCP 插件加载器"""
    
    flags = idaapi.PLUGIN_KEEP
    comment = "IDA Pro MCP Test"
    help = "IDA Pro MCP Plugin"
    wanted_name = "IDA Pro MCP Test"
    wanted_hotkey = "Ctrl-Alt-T"
    
    def init(self):
        """插件初始化"""
        hotkey = MCP.wanted_hotkey.replace("-", "+")
        if sys.platform == "darwin":
            hotkey = hotkey.replace("Alt", "Option")
        
        print(f"[MCP] Plugin loaded, use Edit -> Plugins -> {MCP.wanted_name} ({hotkey}) to start the server")
        
        # 延迟导入，避免在初始化时加载大量代码
        self.server_module = None
        self.server_instance = None
        
        return idaapi.PLUGIN_KEEP
    
    def run(self, arg):
        """运行插件（启动/停止服务器）"""
        try:
            # 延迟导入服务器模块
            if self.server_module is None:
                print("[MCP] Loading server module...")
                import ida_mcp_plugin
                self.server_module = ida_mcp_plugin
            
            # 如果服务器已经在运行，停止它
            if self.server_instance is not None:
                print("[MCP] Stopping existing server...")
                try:
                    self.server_instance.stop()
                except Exception as e:
                    print(f"[MCP] Warning: Failed to stop server: {e}")
                self.server_instance = None
            
            # 创建并启动新的服务器实例
            print("[MCP] Starting server...")
            self.server_instance = self.server_module.create_server()
            self.server_instance.start()
            
        except Exception as e:
            print(f"[MCP] Error: {e}")
            import traceback
            traceback.print_exc()
    
    def term(self):
        """插件终止"""
        if self.server_instance is not None:
            try:
                print("[MCP] Shutting down server...")
                self.server_instance.stop()
            except Exception as e:
                print(f"[MCP] Warning: Failed to stop server during termination: {e}")
            self.server_instance = None


def PLUGIN_ENTRY():
    """IDA Pro 插件入口点"""
    return MCP()
