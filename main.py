#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
大数据学习平台 - 主启动程序
整合前后端服务，提供一键启动功能
"""

import os
import sys
import time
import threading
import webbrowser
from flask import Flask, send_from_directory
from flask_cors import CORS

# 添加backend目录到Python路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(BASE_DIR, 'backend')
sys.path.insert(0, BACKEND_DIR)

# 导入后端应用
backend_app = None
try:
    # 方法1: 尝试直接导入（开发环境）
    from app import app as backend_app
    print("✅ 使用直接导入方式加载后端模块")
except ImportError:
    try:
        # 方法2: 尝试从backend目录导入
        from backend.app import app as backend_app
        print("✅ 使用backend.app导入方式加载后端模块")
    except ImportError:
        try:
            # 方法3: 使用importlib动态导入
            import importlib.util
            app_path = os.path.join(BACKEND_DIR, 'app.py')
            if os.path.exists(app_path):
                spec = importlib.util.spec_from_file_location("backend_app", app_path)
                app_module = importlib.util.module_from_spec(spec)
                sys.modules['backend_app'] = app_module
                spec.loader.exec_module(app_module)
                backend_app = app_module.app
                print("✅ 使用动态导入方式加载后端模块")
            else:
                print(f"❌ 无法找到后端应用文件: {app_path}")
                sys.exit(1)
        except Exception as e:
            print(f"❌ 导入后端模块失败: {e}")
            print(f"当前工作目录: {os.getcwd()}")
            print(f"BASE_DIR: {BASE_DIR}")
            print(f"BACKEND_DIR: {BACKEND_DIR}")
            print(f"Python路径: {sys.path[:3]}")
            sys.exit(1)

if backend_app is None:
    print("❌ 无法加载后端应用模块")
    sys.exit(1)

# 前端服务配置
FRONTEND_DIR = os.path.join(BASE_DIR, 'frontend')
frontend_app = Flask(__name__, static_folder=os.path.join(FRONTEND_DIR, 'assets'))
CORS(frontend_app)

@frontend_app.route('/')
def index():
    return send_from_directory(FRONTEND_DIR, 'index.html')

@frontend_app.route('/assets/<path:path>')
def assets(path):
    return send_from_directory(frontend_app.static_folder, path)

def start_backend():
    """启动后端API服务"""
    print("🚀 启动后端API服务 (端口: 90)...")
    backend_app.run(host='0.0.0.0', port=90, debug=False, use_reloader=False)

def start_frontend():
    """启动前端Web服务"""
    print("🌐 启动前端Web服务 (端口: 8082)...")
    frontend_app.run(host='0.0.0.0', port=8082, debug=False, use_reloader=False)

def open_browser():
    """延迟打开浏览器"""
    time.sleep(3)  # 等待服务启动
    url = 'http://localhost:8082'
    print(f"🔗 正在打开浏览器: {url}")
    webbrowser.open(url)

def main():
    """主函数 - 启动所有服务"""
    print("="*50)
    print("🎓 大数据学习平台 - Hadoop学习系统")
    print("="*50)
    
    try:
        # 启动后端服务线程
        backend_thread = threading.Thread(target=start_backend, daemon=True)
        backend_thread.start()
        
        # 启动前端服务线程
        frontend_thread = threading.Thread(target=start_frontend, daemon=True)
        frontend_thread.start()
        
        # 启动浏览器线程
        browser_thread = threading.Thread(target=open_browser, daemon=True)
        browser_thread.start()
        
        print("\n✅ 所有服务已启动!")
        print("📱 前端地址: http://localhost:8082")
        print("🔧 后端API: http://localhost:90")
        print("\n💡 提示: 关闭此窗口将停止所有服务")
        print("\n按 Ctrl+C 退出程序")
        
        # 保持主线程运行
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n👋 正在关闭服务...")
        print("✅ 程序已退出")
        sys.exit(0)
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()