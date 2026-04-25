# 分发包说明

## 📦 获取安装包

本项目提供三种格式的安装包：

### 方法 1: 从 GitHub Releases 下载（推荐）

访问 [Releases 页面](https://github.com/TheShuiLan/IDA-PRO-MCP/releases) 下载最新版本的安装包：

- `ida_pro_mcp-1.5.0-py3-none-any.whl` - Wheel 格式（推荐）
- `ida_pro_mcp-1.5.0.tar.gz` - Tar.gz 源码包
- `ida_pro_mcp-1.5.0.zip` - Zip 源码包

### 方法 2: 从源码构建

```bash
# 克隆仓库
git clone https://github.com/TheShuiLan/IDA-PRO-MCP.git
cd IDA-PRO-MCP

# 安装构建工具
pip install build

# 构建分发包
python -m build

# 安装包将生成在 dist/ 目录
```

### 方法 3: 直接从 GitHub 安装

```bash
pip install git+https://github.com/TheShuiLan/IDA-PRO-MCP.git
```

## 🚀 安装

下载安装包后，使用以下命令安装：

```bash
# Wheel 包（推荐）
pip install ida_pro_mcp-1.5.0-py3-none-any.whl

# Tar.gz 包
pip install ida_pro_mcp-1.5.0.tar.gz

# Zip 包
pip install ida_pro_mcp-1.5.0.zip
```

## ⚙️ 配置

安装后运行自动配置：

```bash
ida-pro-mcp --install
```

详细安装说明请参考 [INSTALL.md](INSTALL.md)

## 📝 版本历史

### v1.5.0 (2026-04-26)

- 新增轻量级插件加载器
- 改进模块化架构
- 支持多种分发格式
- 完善文档和安装指南

## 🔗 相关链接

- [GitHub 仓库](https://github.com/TheShuiLan/IDA-PRO-MCP)
- [问题反馈](https://github.com/TheShuiLan/IDA-PRO-MCP/issues)
- [原始项目](https://github.com/namename333/idapromcp_333)
