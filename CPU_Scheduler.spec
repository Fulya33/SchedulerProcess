# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['C:\\Users\\matas\\Desktop\\Cpu-Scheduler3\\main.py'],
    pathex=[],
    binaries=[],
    datas=[('C:\\Users\\matas\\Desktop\\Cpu-Scheduler3\\themes', 'themes'), ('C:\\Users\\matas\\Desktop\\Cpu-Scheduler3\\ui', 'ui'), ('C:\\Users\\matas\\Desktop\\Cpu-Scheduler3\\services', 'services'), ('C:\\Users\\matas\\Desktop\\Cpu-Scheduler3\\utils', 'utils'), ('C:\\Users\\matas\\Desktop\\Cpu-Scheduler3\\models', 'models'), ('C:\\Users\\matas\\Desktop\\Cpu-Scheduler3\\algorithms', 'algorithms')],
    hiddenimports=['PyQt6', 'PyQt6.QtCore', 'PyQt6.QtGui', 'PyQt6.QtWidgets', 'matplotlib', 'matplotlib.backends.backend_qtagg', 'numpy'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='CPU_Scheduler',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
