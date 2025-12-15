# 电子科技大学成都学院自习室预约系统

一个现代化的校园自习室预约管理系统，为学生提供便捷的座位预约服务，为管理员提供高效的管理工具。

## 🌟 系统特色

### 📊 数据库设计
- **7个核心数据表**，满足复杂业务需求
- **管理员和学生完全分离**的权限体系
- 完整的预约流程管理
- 信用积分和违规记录系统

### 🏗️ 技术架构
- **后端**: Python Flask + SQLAlchemy
- **前端**: Bootstrap 5 + 原生JavaScript
- **数据库**: SQLite
- **认证**: Flask-Login + 密码加密
- **样式**: 现代化响应式设计

### 🎨 界面设计
- **学校元素**深度融入
- **现代化**的卡片式布局
- **响应式**设计，支持多设备访问
- **优雅**的动画和交互效果

## 📋 功能模块

### 🎓 学生端
- **用户登录**: 学号密码登录
- **个人中心**: 个人信息管理、信用积分查看
- **座位预约**: 实时查看座位状态，在线预约
- **预约记录**: 查看和管理个人预约历史
- **自习室浏览**: 查看各自习室详情和设施

### 👨‍💼 管理员端
- **用户管理**: 学生账户管理、权限控制
- **自习室管理**: 房间和座位的增删改查
- **预约管理**: 审核预约、处理违规
- **统计报表**: 使用率统计、数据分析
- **系统公告**: 发布和管理系统公告

## 🚀 快速开始

### 环境要求
- Python 3.11+
- uv 包管理器（推荐）

### 安装步骤

1. **克隆项目**
```bash
git clone <repository-url>
cd study_room_booking_system
```

2. **初始化虚拟环境并安装依赖**
```bash
# 初始化虚拟环境并安装依赖
uv venv
uv add flask flask-sqlalchemy flask-login flask-wtf wtforms python-dotenv flask-migrate
uv add --dev ruff
```

3. **初始化数据库并添加示例数据**
```bash
uv run python init_data.py
```

4. **启动应用**
```bash
# 方法一：使用uv运行（推荐）
uv run python main.py

# 方法二：使用flask命令
uv run flask run

# 方法三：使用集成启动文件
python start_app.py
```

访问 http://localhost:5000 开始使用！

### 默认账户信息

**管理员账户:**
- 用户名: `admin`
- 密码: `admin123`

**学生账户:**
- 学号: `2024001`
- 密码: `student123`

## 📁 项目结构

```
study_room_booking_system/
├── app/                    # 应用主目录
│   ├── __init__.py        # 应用工厂
│   ├── models/            # 数据模型
│   │   ├── admin.py       # 管理员模型
│   │   ├── student.py     # 学生模型
│   │   ├── study_room.py  # 自习室和座位模型
│   │   ├── booking.py     # 预约和公告模型
│   │   └── __init__.py    # 模型导入
│   ├── views/             # 视图控制器
│   │   ├── auth.py        # 认证相关
│   │   ├── admin.py       # 管理员功能
│   │   ├── student.py     # 学生功能
│   │   ├── main.py        # 主要页面
│   │   └── __init__.py
│   ├── forms/             # 表单处理
│   │   ├── auth.py        # 认证表单
│   │   └── booking.py     # 预约表单
│   ├── templates/         # HTML模板
│   │   ├── common/        # 公共模板
│   │   ├── auth/          # 认证页面
│   │   ├── admin/         # 管理员页面
│   │   ├── student/       # 学生页面
│   │   └── index.html     # 首页
│   └── static/            # 静态资源
│       ├── css/           # 样式文件
│       ├── js/            # JavaScript文件
│       └── images/        # 图片资源
├── instance/              # 实例配置（数据库文件等）
├── pyproject.toml         # 项目配置和依赖
├── requirements.txt       # 旧版依赖包列表（可选）
├── main.py                # 应用入口
├── start_app.py           # 集成启动脚本
├── init_data.py           # 数据库初始化和示例数据
├── config.py              # 应用配置
├── uv.lock               # uv依赖锁定文件
├── ruff.toml              # 代码格式化配置
└── README.md             # 项目说明
```

## 🗄️ 数据库设计

### 核心数据表

1. **admins** - 管理员表
   - 用户名、密码、邮箱、角色等

2. **students** - 学生表
   - 学号、姓名、专业、信用积分等

3. **study_rooms** - 自习室表
   - 房间信息、容量、设施等

4. **seats** - 座位表
   - 座位编号、类型、状态等

5. **bookings** - 预约记录表
   - 预约时间、状态、签到记录等

6. **time_slots** - 时间段表
   - 预约时段配置

7. **announcements** - 系统公告表
   - 公告内容、发布信息等

## 🔧 配置说明

### 环境变量
```bash
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///study_room.db
MAIL_SERVER=smtp.example.com
MAIL_PORT=587
MAIL_USERNAME=your-email@example.com
MAIL_PASSWORD=your-password
```

### 数据库配置
- **开发环境**: SQLite (默认)
- **生产环境**: SQLite 或可扩展至 MySQL/PostgreSQL

## 🎯 使用指南

### 学生使用流程
1. 使用学号密码登录系统
2. 浏览自习室和座位信息
3. 选择合适的时间段进行预约
4. 按时签到使用座位
5. 使用完毕后签退

### 管理员操作流程
1. 使用管理员账号登录
2. 管理自习室和座位信息
3. 监控预约情况
4. 处理违规记录
5. 发布系统公告

## 🛠️ 开发指南

### 添加新功能
1. 在 `app/models/` 中定义数据模型
2. 在 `app/views/` 中实现业务逻辑
3. 在 `app/templates/` 中创建页面模板
4. 更新路由配置

### 数据库迁移
```bash
# 生成迁移文件
flask db migrate -m "描述信息"

# 应用迁移
flask db upgrade
```

### 代码质量检查
```bash
# 代码检查
uv run ruff check .

# 自动修复代码格式问题
uv run ruff check . --fix

# 代码格式化
uv run ruff format .
```

### 数据库操作
```bash
# 重新初始化数据库
uv run python init_data.py

# 访问Flask shell
uv run flask shell
```

## 🐛 常见问题

### Q: 如何修改默认端口？
A: 修改 `run.py` 或 `app.py` 中的 `port` 参数

### Q: 如何更换数据库？
A: 修改 `config.py` 中的 `SQLALCHEMY_DATABASE_URI`

### Q: 如何重置管理员密码？
A: 运行 `init_data.py` 重新初始化数据库

## 📞 技术支持

如有问题或建议，请联系：
- 邮箱: support@cduestc.edu.cn
- 项目地址: https://github.com/your-repo

## 📄 许可证

本项目采用 MIT 许可证，详见 [LICENSE](LICENSE) 文件

## 🏆 致谢

感谢电子科技大学成都学院对项目开发的支持！