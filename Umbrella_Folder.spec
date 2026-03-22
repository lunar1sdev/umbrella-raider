# -*- mode: python ; coding: utf-8 -*-
import os

# Get venv tls_client path
venv_path = os.path.abspath(os.path.join('..', 'venv', 'Lib', 'site-packages'))
tls_client_path = os.path.join(venv_path, 'tls_client')
tls_deps_path = os.path.join(tls_client_path, 'dependencies')

block_cipher = None

a = Analysis(
    ['Cwelium_GUI.py'],
    pathex=[],
    binaries=[
        (os.path.join(tls_deps_path, 'tls-client-64.dll'), 'tls_client/dependencies'),
        (os.path.join(tls_deps_path, 'tls-client-32.dll'), 'tls_client/dependencies'),
    ],
    datas=[
        ('config.json', '.'),
        (tls_client_path, 'tls_client'),
    ],
    hiddenimports=[
        'customtkinter',
        'PIL._tkinter_finder',
        'tls_client',
        'tls_client.sessions',
        'tls_client.cffi',
        'websocket',
        'colorama',
        'colorist',
    ],
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
    [],
    exclude_binaries=True,
    name='Umbrella',
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
    icon='umbrella.ico',
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Umbrella',
)
