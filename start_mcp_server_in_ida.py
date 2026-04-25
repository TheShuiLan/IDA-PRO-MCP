# -*- coding: utf-8 -*-
"""
IDA Pro MCP Server Starter
Directly start the MCP JSON-RPC server in IDA Pro without loading the full plugin

Usage in IDA Pro Python console:
exec(open(r'D:\WorkShip\AutoZHUC\新建文件夹\idapromcp_333\start_mcp_server_in_ida.py', encoding='utf-8').read())
"""

import sys
import os
import json
import threading
import http.server
from urllib.parse import urlparse

print("[MCP] Starting MCP server initialization...")

# Add plugin directory to path
plugin_dir = r"C:\Program Files\IDAProfessional\plugins"
if plugin_dir not in sys.path:
    sys.path.insert(0, plugin_dir)

# Import required IDA modules
try:
    import idaapi
    import idautils
    import idc
    import ida_funcs
    import ida_bytes
    import ida_nalt
    import ida_hexrays
    print("[MCP] IDA modules imported successfully")
except ImportError as e:
    print(f"[MCP] Failed to import IDA modules: {e}")
    raise

# Simple JSON-RPC server
class SimpleJSONRPCHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # Suppress HTTP logs
    
    def do_POST(self):
        if self.path not in ["/jsonrpc", "/mcp"]:
            self.send_error(404)
            return
        
        content_length = int(self.headers.get("Content-Length", 0))
        if content_length == 0:
            self.send_error(400, "Empty request")
            return
        
        request_body = self.rfile.read(content_length)
        try:
            request = json.loads(request_body)
        except json.JSONDecodeError:
            self.send_error(400, "Invalid JSON")
            return
        
        response = {"jsonrpc": "2.0", "id": request.get("id")}
        
        try:
            method = request.get("method")
            params = request.get("params", [])
            
            # Handle basic methods
            if method == "check_connection":
                response["result"] = {
                    "status": "ok",
                    "protocol": "MCP",
                    "version": "1.6.0",
                    "server": "IDA Pro MCP (Simple Mode)"
                }
            elif method == "get_metadata":
                response["result"] = {
                    "path": idaapi.get_input_file_path(),
                    "module": idaapi.get_root_filename(),
                    "base": hex(idaapi.get_imagebase())
                }
            elif method == "get_methods":
                response["result"] = [
                    {"name": "check_connection", "description": "Check server connection"},
                    {"name": "get_metadata", "description": "Get IDB metadata"},
                    {"name": "get_methods", "description": "List available methods"}
                ]
            else:
                response["error"] = {
                    "code": -32601,
                    "message": f"Method not found: {method}"
                }
        except Exception as e:
            response["error"] = {
                "code": -32603,
                "message": f"Internal error: {str(e)}"
            }
        
        response_body = json.dumps(response).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", len(response_body))
        self.end_headers()
        self.wfile.write(response_body)

# Server thread
class MCPServer:
    def __init__(self, host="127.0.0.1", port=13339):
        self.host = host
        self.port = port
        self.server = None
        self.thread = None
        self.running = False
    
    def start(self):
        if self.running:
            print("[MCP] Server already running")
            return
        
        def run_server():
            try:
                self.server = http.server.HTTPServer((self.host, self.port), SimpleJSONRPCHandler)
                self.server.allow_reuse_address = True
                print(f"[MCP] Server started at http://{self.host}:{self.port}")
                self.running = True
                self.server.serve_forever()
            except Exception as e:
                print(f"[MCP] Server error: {e}")
                self.running = False
        
        self.thread = threading.Thread(target=run_server, daemon=True)
        self.thread.start()
        print("[MCP] Server thread started")
    
    def stop(self):
        if not self.running:
            print("[MCP] Server not running")
            return
        
        if self.server:
            self.server.shutdown()
            self.server.server_close()
        self.running = False
        print("[MCP] Server stopped")

# Create and start server
if 'mcp_server' not in globals():
    mcp_server = MCPServer()

mcp_server.start()
print("[MCP] Server initialization complete!")
print("[MCP] You can now connect from Kiro")
print("[MCP] To stop: mcp_server.stop()")
