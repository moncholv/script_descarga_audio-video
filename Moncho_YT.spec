# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['gui_moncholv.py'],
    pathex=[],
    binaries=[
        ('binaries/ffmpeg', 'binaries'),
    ],
    datas=[],
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
    name='Moncho_YT',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['assets/Moncho_YT.icns'],
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name='Moncho_YT',
)

app = BUNDLE(
    coll,
    name='Moncho_YT.app',
    icon='assets/Moncho_YT.icns',
    bundle_identifier='com.moncholv.moncho-yt-gui',
    version='1.1.1',
    info_plist={
        'NSHighResolutionCapable': True,
        'CFBundleVersion': '1.1.1',
        'CFBundleShortVersionString': '1.1.1',
    },
)
