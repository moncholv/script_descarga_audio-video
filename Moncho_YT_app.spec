# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['script_descarga.py'],
    pathex=[],
    binaries=[
        ('binaries/yt-dlp', 'binaries'),
        ('binaries/ffmpeg', 'binaries'),
    ],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    cipher=block_cipher,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Moncho_YT',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # Cambiado a False para usar el wrapper
    disable_windowed_traceback=False,
    argv_emulation=True,  # Importante para macOS
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Moncho_YT',
)

app = BUNDLE(
    coll,
    name='Moncho_YT.app',
    icon='assets/Moncho_YT.icns',
    bundle_identifier='com.moncholv.moncho-yt',
    version='1.0.0',
    info_plist={
        'NSPrincipalClass': 'NSApplication',
        'NSHighResolutionCapable': True,
        'CFBundleName': 'Moncho YT Downloader',
        'CFBundleDisplayName': 'Moncho YT',
        'CFBundleGetInfoString': 'Descargador de videos y audio de YouTube',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'LSApplicationCategoryType': 'public.app-category.utilities',
        'LSBackgroundOnly': False,
        'LSMinimumSystemVersion': '10.13.0',
    },
)
