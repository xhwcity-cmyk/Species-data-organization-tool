# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['../plant_matrix_gui.py'],
    pathex=[],
    binaries=[],
    datas=[('/Users/runk/PyCharmMiscProject/.venv/lib/python3.13/site-packages/openpyxl', 'openpyxl')],
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
    name='SpeciesProcessor',
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
app = BUNDLE(
    exe,
    name='SpeciesProcessor.app',
    icon=None,
    bundle_identifier=None,
)
