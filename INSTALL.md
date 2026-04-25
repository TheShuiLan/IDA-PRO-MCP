# IDA Pro MCP 安装指南

## 📦 可用的安装包

在 `dist/` 目录下有三种格式的安装包：

1. **ida_pro_mcp-1.5.0-py3-none-any.whl** (推荐) - Wheel 格式，安装最快
2. **ida_pro_mcp-1.5.0.tar.gz** - 源代码压缩包（tar.gz 格式）
3. **ida_pro_mcp-1.5.0.zip** - 源代码压缩包（zip 格式）

## 🚀 安装方法

### 方法 1: 使用 Wheel 包安装（推荐）

```bash
pip install dist/ida_pro_mcp-1.5.0-py3-none-any.whl
```

### 方法 2: 使用 tar.gz 包安装

```bash
pip install dist/ida_pro_mcp-1.5.0.tar.gz
```

### 方法 3: 使用 zip 包安装

```bash
pip install dist/ida_pro_mcp-1.5.0.zip
```

### 方法 4: 从 GitHub 直接安装

```bash
pip install https://github.com/namename333/idapromcp_333/archive/refs/heads/main.zip
```

### 方法 5: 开发模式安装（用于开发和调试）

```bash
pip install -e .
```

## 📋 安装后配置

### 1. 自动安装（推荐）

运行以下命令自动配置 MCP 客户端和 IDA Pro 插件：

```bash
ida-pro-mcp --install
```

这将：
- 配置 Kiro/Cline/Claude Desktop 等 MCP 客户端
- 安装 IDA Pro 插件到用户插件目录
- 复制必要的工具模块

### 2. 手动安装 IDA Pro 插件

如果自动安装失败，可以手动复制插件文件：

**Windows:**
```bash
# 复制到用户插件目录
copy src\ida_pro_mcp\ida_mcp_loader.py "%APPDATA%\Hex-Rays\IDA Pro\plugins\"
copy src\ida_pro_mcp\ida_mcp_plugin.py "%APPDATA%\Hex-Rays\IDA Pro\plugins\"
copy src\ida_pro_mcp\script_utils.py "%APPDATA%\Hex-Rays\IDA Pro\plugins\"

# 或复制到 IDA Pro 安装目录
copy src\ida_pro_mcp\ida_mcp_loader.py "C:\Program Files\IDAProfessional\plugins\"
copy src\ida_pro_mcp\ida_mcp_plugin.py "C:\Program Files\IDAProfessional\plugins\"
copy src\ida_pro_mcp\script_utils.py "C:\Program Files\IDAProfessional\plugins\"
```

**macOS/Linux:**
```bash
# 复制到用户插件目录
cp src/ida_pro_mcp/ida_mcp_loader.py ~/.idapro/plugins/
cp src/ida_pro_mcp/ida_mcp_plugin.py ~/.idapro/plugins/
cp src/ida_pro_mcp/script_utils.py ~/.idapro/plugins/
```

### 3. 配置 Kiro MCP

编辑 `~/.kiro/settings/mcp.json`（或 `C:\Users\<用户名>\.kiro\settings\mcp.json`）：

```json
{
  "mcpServers": {
    "ida-pro-mcp": {
      "command": "python",
      "args": ["-m", "ida_pro_mcp.server"],
      "env": {},
      "disabled": false,
      "timeout": 1800,
      "autoApprove": [
        "check_connection",
        "get_metadata",
        "get_methods",
        "decompile_function",
        "disassemble_function",
        "get_function_by_name",
        "get_function_by_address"
      ]
    }
  }
}
```

## 🎯 使用方法

### 1. 启动 IDA Pro 插件

1. 在 IDA Pro 中打开一个二进制文件
2. 按 `Ctrl+Alt+T`（macOS: `Ctrl+Option+T`）
3. 或通过菜单：`Edit → Plugins → IDA Pro MCP Test`

插件启动后会在 `http://127.0.0.1:13339` 监听 JSON-RPC 请求。

### 2. 在 Kiro 中使用

重启 Kiro 或重新加载 MCP 服务器后，您可以通过自然语言与 IDA Pro 交互：

- "反编译函数 sub_401000"
- "列出所有导入的函数"
- "分析当前函数的调用图"
- "获取地址 0x401000 的交叉引用"

### 3. 验证连接

在 Kiro 中询问：
```
测试 IDA Pro MCP 连接
```

如果连接成功，会返回 IDA Pro 的元数据信息。

## 🔧 故障排除

### 插件未出现在 IDA Pro 菜单中

1. **检查插件文件是否存在**：
   ```bash
   # Windows
   dir "%APPDATA%\Hex-Rays\IDA Pro\plugins\ida_mcp_loader.py"
   
   # macOS/Linux
   ls ~/.idapro/plugins/ida_mcp_loader.py
   ```

2. **手动加载插件**：
   在 IDA Pro Python 控制台（Alt+F7）运行：
   ```python
   import ida_mcp_loader
   plugin = ida_mcp_loader.PLUGIN_ENTRY()
   plugin.init()
   plugin.run(0)
   ```

### 连接失败

1. **确认插件已启动**：
   检查 IDA Pro 控制台是否显示：
   ```
   [MCP] Server started at http://127.0.0.1:13339
   ```

2. **检查端口占用**：
   ```bash
   # Windows
   netstat -ano | findstr :13339
   
   # macOS/Linux
   lsof -i :13339
   ```

3. **修改端口**：
   编辑 `src/ida_pro_mcp/mcp_config.json` 修改端口号。

## 📚 更多信息

- GitHub: https://github.com/namename333/idapromcp_333
- 原项目: https://github.com/mrexodia/ida-pro-mcp
- 问题反馈: https://github.com/namename333/idapromcp_333/issues

## 📄 许可证

MIT License - 详见 LICENSE 文件
