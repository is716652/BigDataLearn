# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller 打包配置文件
用于生成大数据学习平台的独立可执行文件
"""

import os
from PyInstaller.utils.hooks import collect_data_files

# 获取项目根目录
project_root = os.path.dirname(os.path.abspath('.'))

# 数据文件配置
datas = [
    # 前端文件
    ('frontend', 'frontend'),
    # 数据库文件
    ('DB', 'DB'),
    ('bigdata_learning.db', '.'),
    # 模板文件
    ('templates', 'templates'),
    # SQL文件（可选）
    ('SQL', 'SQL'),
]

# 隐藏导入模块
hiddenimports = [
    'flask',
    'flask_cors',
    'sqlite3',
    'openpyxl',
    'openai',
    'werkzeug.security',
    'threading',
    'webbrowser',
]

# 排除的模块
excludes = [
    'tkinter',
    'matplotlib',
    'numpy',
    'pandas',
    'PIL',
    'cv2',
]

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=excludes,
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='BigDataLearn',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # 可以添加图标文件路径
)