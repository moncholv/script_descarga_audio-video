# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['script_descarga.py'],
    pathex=[],
    binaries=[
        ('binaries/yt-dlp.exe', 'binaries'),
        ('binaries/ffmpeg.exe', 'binaries'),
    ],
    datas=[
        ('binaries/yt-dlp.exe.version', 'binaries'),
    ],
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
    a.binaries,
    a.datas,
    [],
    name='Moncho_YT',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # True para mostrar ventana de consola
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/Moncho_YT.ico',
)
