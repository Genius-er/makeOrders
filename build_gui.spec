# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_all

block_cipher = None

charset_normalizer_datas, charset_normalizer_binaries, charset_normalizer_hiddenimports = collect_all('charset_normalizer')

a = Analysis(
    ['src\\gui_main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('templete.xlsx', '.'),
        ('店小秘导出订单表', '店小秘导出订单表'),
    ] + charset_normalizer_datas,
    hiddenimports=[
        'openpyxl',
        'openpyxl.cell._writer',
        'PIL',
        'PIL._tkinter_finder',
        'requests',
        'tkinterdnd2',
    ] + charset_normalizer_hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='店小秘做单工具',
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
    icon=None,
)
