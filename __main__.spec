# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['C:\\Users\\alexg\\OneDrive - Technical University of Moldova\\Anul 4\\Semestrul 1\\PIG\\code_zone\\__main__.py'],
    pathex=[],
    binaries=[],
    datas=[('C:\\Users\\alexg\\OneDrive - Technical University of Moldova\\Anul 4\\Semestrul 1\\PIG\\code_zone\\pig_lab\\Lib\\site-packages/customtkinter', 'customtkinter/')],
    hiddenimports=[],
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
    [],
    exclude_binaries=True,
    name='__main__',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='__main__',
)
