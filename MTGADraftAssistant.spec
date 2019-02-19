# -*- mode: python -*-

block_cipher = None


a = Analysis(['MTGADraftAssistant.py'],
             pathex=['C:\\Users\\xaos\\AppData\\Local\\Programs\\Python\\Python37\\MTGADraftAssistant'],
             binaries=[],
             datas=[('cards-parsed.json', '.'), ('uncommonData', 'uncommonData'), ('numbers', 'numbers')],
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
          name='MTGADraftAssistant',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='MTGADraftAssistant')
