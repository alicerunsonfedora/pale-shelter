# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

data_files = [
    ("assets", "assets")
]

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
          name='Lifelight',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
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
             icon=None,
             bundle_identifier="net.marquiskurt.pale-shelter")
