# -*- mode: python ; coding: utf-8 -*-
block_cipher = None

data_files = [
    ("assets", "assets"),
    ("data", "data"),
    ("LICENSE", "."),
    ("READFIRST.txt", "."),
    ("src", "src")
]

PLIST = {
    'NSPrincipalClass': 'NSApplication',
    'CFBundleExecutable': 'NoLove',
    'CFBundleShortVersionString': '1.0.1',
    'CFBundleVersion': '1.0.3',
    'LSMinimumSystemVersion': '10.15',
    'NSHumanReadableCopyright': 'Copyright © 2021 Marquis Kurt. All rights reserved.',
    'ITSAppUsesNonExemptEncryption': False,
    'LSApplicationCategoryType': "public.app-category.arcade-games",
}

a = Analysis(['NoLove.py'],
             pathex=['/Users/marquiskurt/Developer/pale_shelter'],
             binaries=[],
             datas=data_files,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='NoLove',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          icon='icon.ico',
          console=False )
coll = COLLECT(exe,
                a.binaries,
                a.zipfiles,
                a.datas,
                strip=False,
                upx=True,
                upx_exclude=[],
                name='No Love')
app = BUNDLE(coll,
            name='No Love.app',
            icon="icon.icns",
            bundle_identifier="net.marquiskurt.pale-shelter",
            info_plist=PLIST
            )
