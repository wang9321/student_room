#!/usr/bin/env python3
"""
Flask自习室预约系统启动文件
集成环境初始化、数据库创建和系统启动
"""

import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def main():
    """主函数：初始化并启动Flask应用"""
    print("=" * 60)
    print("正在启动Flask自习室预约系统...")
    print("=" * 60)

    try:
        # 1. 导入应用工厂和扩展
        from app import create_app, db
        from app.models import Admin, Booking, Seat, Student, StudyRoom, User
        from app.utils.init_complete_data import init_complete_data

        print("[OK] 成功导入应用模块")

        # 2. 创建应用实例
        app = create_app()
        print("[OK] 成功创建应用实例")

        # 3. 在应用上下文中初始化数据库
        with app.app_context():
            try:
                # 创建数据库表（如果不存在）
                print("正在检查数据库结构...")
                db.create_all()
                print("[OK] 数据库表检查完成")

                # 4. 初始化完整数据（如果需要）
                print("正在检查数据完整性...")
                init_complete_data()
                print("[OK] 数据初始化检查完成")

            except Exception as e:
                print(f"[ERROR] 数据库初始化失败: {e}")
                return False

        # 5. 设置Flask shell上下文
        @app.shell_context_processor
        def make_shell_context():
            """为Flask shell提供上下文"""
            return {
                'db': db,
                'Student': Student,
                'Admin': Admin,
                'User': User,
                'StudyRoom': StudyRoom,
                'Seat': Seat,
                'Booking': Booking
            }

        print("=" * 60)
        print("系统启动成功！")
        print("访问地址:")
        print("   - 本地访问: http://127.0.0.1:5000")
        print("   - 网络访问: http://0.0.0.0:5000")
        print("=" * 60)
        print("提示:")
        print("   - 按 Ctrl+C 停止服务器")
        print("   - 默认管理员账户: admin / admin123")
        print("   - 调试模式已开启")
        print("=" * 60)

        # 6. 启动Flask开发服务器
        app.run(
            debug=True,
            host='0.0.0.0',
            port=5000,
            use_reloader=True
        )

    except ImportError as e:
        print(f"[ERROR] 模块导入失败: {e}")
        print("请确保已安装所有依赖包:")
        print("   pip install flask flask-sqlalchemy flask-login flask-wtf wtforms python-dotenv")
        return False

    except Exception as e:
        print(f"[ERROR] 系统启动失败: {e}")
        return False

if __name__ == '__main__':
    success = main()
    if not success:
        sys.exit(1)
