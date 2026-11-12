# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['script_descarga.py'],
    pathex=[],
    binaries=[
        ('binaries/yt-dlp', 'binaries'),
        ('binaries/ffmpeg', 'binaries'),
    ],
    datas=[
        ('binaries/yt-dlp.version', 'binaries'),
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
    [],
    exclude_binaries=True,
    name='Moncho_YT',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,  # La app abre Terminal por sí misma
    disable_windowed_traceback=False,
    argv_emulation=True,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
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
    bundle_identifier='com.moncholv.moncho-yt',
    version='1.1.1',
    info_plist={
        'NSPrincipalClass': 'NSApplication',
        'NSHighResolutionCapable': True,
        'CFBundleName': 'Moncho YT Downloader',
        'CFBundleDisplayName': 'Moncho YT',
        'CFBundleGetInfoString': 'Descargador de videos y audio de YouTube',
        'CFBundleVersion': '1.1.1',
        'CFBundleShortVersionString': '1.1.1',
        'LSApplicationCategoryType': 'public.app-category.utilities',
        'LSBackgroundOnly': False,
        'LSMinimumSystemVersion': '10.13.0',
        'NSAppleEventsUsageDescription': 'Moncho YT abre la app Terminal para mostrar el menú de descargas.',
    },
)
