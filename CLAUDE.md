# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

这是一个基于Flask的校园自习室座位预约系统，为大学校园提供服务。系统允许用户注册、浏览可用自习室、预约座位，并通过签到/签退功能管理预约。

## 开发环境搭建

```bash
# 初始化虚拟环境并安装依赖
cd study_room_system
uv venv
uv add flask flask-sqlalchemy flask-login flask-wtf wtforms python-dotenv flask-migrate
uv add --dev ruff

# 初始化数据库并添加示例数据
uv run python init_data.py

# 运行开发服务器
uv run python main.py
# 或者
uv run flask run
```

## 常用开发命令

```bash
# 代码质量检查
uv run ruff check .
uv run ruff check . --fix
uv run ruff format .

# 数据库操作
uv run python init_data.py  # 重新初始化数据库
uv run flask shell          # 访问Flask shell，已加载模型
```

## 架构概述

### 应用程序结构

系统使用Flask应用工厂模式，采用模块化蓝图架构：

- **app/__init__.py**: 应用工厂函数 `create_app()`，负责配置扩展和注册蓝图
- **main.py**: 应用程序入口点，创建数据库表并运行开发服务器
- **config.py**: 配置类，包含预约规则和会话设置

### 核心数据模型

1. **User**: 学生账户，包含认证、密码哈希和预约权限
2. **StudyRoom**: 物理自习室，包含容量、营业时间和位置信息
3. **Seat**: 自习室内的单个座位，具有网格位置（行/列）和类型（标准/靠窗/电源）
4. **Booking**: 预约记录，具有全面的状态跟踪和时间管理

### 关键业务逻辑

- **预约状态流转**: `pending`（待确认）→ `confirmed`（已确认）→ `checked_in`（已签到）→ `completed`（已完成）或 `cancelled`（已取消）/`no_show`（未签到）
- **时间限制**: 最长4小时预约，提前7天预约，15分钟签到窗口
- **用户限制**: 每个用户同时只能有一个有效预约
- **座位可用性**: 跨预约时间范围的实时冲突检测

### 蓝图架构

- **auth_bp** (`/auth`): 用户注册、登录/注销、个人资料管理
- **main_bp**: 首页、自习室列表、通用信息页面
- **booking_bp** (`/booking`): 座位选择、预约创建/取消、签到/签退
- **admin_bp** (`/admin`): 管理员界面（占位符）
- **errors_bp**: 404/500/403的全局错误处理器

### 数据库初始化

`init_data.py` 脚本创建：
- 三个自习室，具有不同的容量和营业时间
- 座位网格（5x8布局），按座位类型分类
- 管理员用户（admin/admin123）用于系统管理

### 表单处理

`app/forms/` 中的WTForms类处理：
- 用户注册/登录验证
- 预约时间选择和验证
- 带动态选择的自习室选择

### 前端架构

Bootstrap 5响应式设计，包含：
- 带导航和消息提示的基础模板
- 每个蓝图的模块化模板结构
- 用户认证感知的导航
- 预约的实时状态指示器

## 开发指南

- 所有命令执行使用 `uv run` 以确保正确的虚拟环境使用
- 提交更改前运行 `uv run ruff check . --fix`
- 数据库模型包含全面的关系定义和业务逻辑方法
- 除公共页面外，所有面向用户的路由都需要 `@login_required` 装饰器
- 配置值根据环境特定（开发/生产）
- 会话持久性设置为2小时，带自动清理