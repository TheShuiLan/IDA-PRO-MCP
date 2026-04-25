# -*- coding: utf-8 -*-
"""
IDA Pro MCP Plugin Manual Loader

Usage:
1. Open a binary file in IDA Pro
2. Press Alt+F7 to open Python console
3. Run: exec(open(r'D:\WorkShip\AutoZHUC\新建文件夹\idapromcp_333\load_mcp_plugin.py', encoding='utf-8').read())
"""

import sys
import os

# Add plugin path to sys.path
plugin_dir = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "Hex-Rays", "IDA Pro", "plugins")
if plugin_dir not in sys.path:
    sys.path.insert(0, plugin_dir)

print("[MCP] Plugin directory: {}".format(plugin_dir))

# Import plugin module
try:
    # Unload if already loaded
    if 'mcp_plugin' in sys.modules:
        del sys.modules['mcp_plugin']
    
    # Import with dash in filename
    import importlib.util
    spec = importlib.util.spec_from_file_location("mcp_plugin", os.path.join(plugin_dir, "mcp-plugin.py"))
    mcp_plugin = importlib.util.module_from_spec(spec)
    sys.modules['mcp_plugin'] = mcp_plugin
    spec.loader.exec_module(mcp_plugin)
    
    print("[MCP] Plugin module loaded")
    
    # Call plugin entry point
    plugin_instance = mcp_plugin.PLUGIN_ENTRY()
    
    if plugin_instance:
        # Initialize plugin
        result = plugin_instance.init()
        if result == -1:
            print("[MCP] Plugin initialization failed")
        else:
            print("[MCP] Plugin initialized successfully: {}".format(result))
            
            # Run plugin
            plugin_instance.run(0)
            print("[MCP] Plugin started")
    else:
        print("[MCP] Cannot create plugin instance")
        
except Exception as e:
    import traceback
    print("[MCP] Failed to load plugin: {}".format(e))
    traceback.print_exc()
