#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
大数据学习平台 - 自动打包脚本
使用PyInstaller将项目打包为独立可执行文件
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def check_requirements():
    """检查打包环境"""
    print("🔍 检查打包环境...")
    
    try:
        import PyInstaller
        print(f"✅ PyInstaller 版本: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller 未安装")
        print("请运行: pip install pyinstaller")
        return False
    
    # 检查必要文件
    required_files = [
        'main.py',
        'backend/app.py',
        'frontend/index.html',
        'requirements.txt'
    ]
    
    for file in required_files:
        if not os.path.exists(file):
            print(f"❌ 缺少必要文件: {file}")
            return False
        print(f"✅ 找到文件: {file}")
    
    return True

def install_dependencies():
    """安装依赖"""
    print("\n📦 安装项目依赖...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                      check=True, capture_output=True)
        print("✅ 依赖安装完成")
    except subprocess.CalledProcessError as e:
        print(f"❌ 依赖安装失败: {e}")
        return False
    return True

def clean_build():
    """清理构建目录"""
    print("\n🧹 清理构建目录...")
    
    dirs_to_clean = ['build', 'dist', '__pycache__']
    files_to_clean = ['*.spec']
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"✅ 清理目录: {dir_name}")
    
    # 清理spec文件
    for spec_file in Path('.').glob('*.spec'):
        if spec_file.name != 'build_spec.py':
            spec_file.unlink()
            print(f"✅ 清理文件: {spec_file}")

def build_executable():
    """构建可执行文件"""
    print("\n🔨 开始构建可执行文件...")
    
    # PyInstaller 命令参数
    cmd = [
        'pyinstaller',
        '--onefile',                    # 打包成单个文件
        '--windowed',                   # Windows下隐藏控制台（可选）
        '--name=BigDataLearn',          # 可执行文件名称
        '--add-data=frontend;frontend', # 添加前端文件
        '--add-data=DB;DB',             # 添加数据库目录
        '--add-data=templates;templates', # 添加模板文件
        '--hidden-import=flask',
        '--hidden-import=flask_cors',
        '--hidden-import=sqlite3',
        '--hidden-import=openpyxl',
        '--hidden-import=openai',
        '--hidden-import=werkzeug.security',
        '--exclude-module=tkinter',
        '--exclude-module=matplotlib',
        '--exclude-module=numpy',
        '--exclude-module=pandas',
        'main.py'
    ]
    
    try:
        print("执行命令:", ' '.join(cmd))
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ 构建成功!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 构建失败: {e}")
        print(f"错误输出: {e.stderr}")
        return False

def create_portable_package():
    """创建便携式包"""
    print("\n📦 创建便携式包...")
    
    dist_dir = Path('dist')
    if not dist_dir.exists():
        print("❌ dist目录不存在")
        return False
    
    exe_file = dist_dir / 'BigDataLearn.exe'
    if not exe_file.exists():
        print("❌ 可执行文件不存在")
        return False
    
    # 创建发布包目录
    release_dir = Path('release')
    if release_dir.exists():
        shutil.rmtree(release_dir)
    release_dir.mkdir()
    
    # 复制可执行文件
    shutil.copy2(exe_file, release_dir / 'BigDataLearn.exe')
    
    # 创建说明文件
    readme_content = """# 大数据学习平台 - Hadoop学习系统

## 使用说明

1. 双击 `BigDataLearn.exe` 启动程序
2. 程序会自动启动后端服务和前端界面
3. 浏览器会自动打开学习平台页面
4. 关闭命令行窗口即可退出程序

## 功能特性

- 📚 6个完整的大数据学习模块
- 🎯 交互式知识点学习
- 📝 在线练习和测试
- 👥 学生信息管理
- 🔧 完整的后台管理功能

## 技术支持

如有问题，请联系技术支持。

---
版本: 1.0.0
构建时间: {}
""".format(subprocess.run(['date', '/t'], capture_output=True, text=True, shell=True).stdout.strip())
    
    with open(release_dir / 'README.txt', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print(f"✅ 便携式包已创建: {release_dir.absolute()}")
    print(f"📁 可执行文件: {(release_dir / 'BigDataLearn.exe').absolute()}")
    
    return True

def main():
    """主函数"""
    print("="*60)
    print("🎓 大数据学习平台 - PyInstaller 自动打包工具")
    print("="*60)
    
    # 检查环境
    if not check_requirements():
        print("\n❌ 环境检查失败，请解决上述问题后重试")
        return False
    
    # 安装依赖
    if not install_dependencies():
        print("\n❌ 依赖安装失败")
        return False
    
    # 清理构建目录
    clean_build()
    
    # 构建可执行文件
    if not build_executable():
        print("\n❌ 构建失败")
        return False
    
    # 创建便携式包
    if not create_portable_package():
        print("\n❌ 便携式包创建失败")
        return False
    
    print("\n🎉 打包完成!")
    print("\n📋 使用说明:")
    print("1. 进入 release 目录")
    print("2. 双击 BigDataLearn.exe 启动程序")
    print("3. 程序会自动打开浏览器访问学习平台")
    
    return True

if __name__ == '__main__':
    success = main()
    if not success:
        sys.exit(1)
    
    input("\n按回车键退出...")