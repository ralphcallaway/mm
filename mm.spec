# -*- mode: python -*-
import os
import encodings

a = Analysis(['mm.py'],
             hiddenimports=[
              'encodings',
              'jinja2.ext',
              'gnomekeyring',
              'keyring',
              'keyring.backend',
              'keyring.cli',
              'keyring.core',
              'keyring.credentials',
              'keyring.errors',
              'keyring.getpassbackend',
              'keyring.http',
              'keyring.py27compat',
              'keyring.backends._win_crypto',
              'keyring.backends.file',
              'keyring.backends.Gnome',
              'keyring.backends.Google',
              'keyring.backends.keyczar',
              'keyring.backends.kwallet',
              'keyring.backends.multi',
              'keyring.backends.OS_X',
              'keyring.backends.pyfs',
              'keyring.backends.SecretService',
              'keyring.backends.Windows',
              'keyring.util.escape',
              'keyring.util.platform',
              'keyring.util.properties',
              'keyring.util.XDG',
              'keyring.util.platform_'
            ],
             hookspath=None,
             runtime_hooks=None)

pyz = PYZ(a.pure)

exes = Tree(os.path.join('mm','bin'), prefix='lib/bin', excludes=[])
ui = Tree(os.path.join('mm','ui'), prefix='lib/ui', excludes=[])
sforce = Tree(os.path.join('mm','sforce'), prefix='lib/sforce', excludes=[])
templates = Tree(os.path.join('mm','templates'), prefix='lib/templates', excludes=[])
wsdl = Tree(os.path.join('mm','wsdl'), prefix='lib/wsdl', excludes=[])
server = Tree(os.path.join('mm','server'), prefix='lib/server', excludes=[])

exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='mm',
          debug=False,
          strip=None,
          upx=True,
          console=True)

coll = COLLECT( exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               wsdl,
               sforce,
               templates,
               server,
               ui,
               exes,
               strip=None,
               upx=True,
               name=os.path.join('dist','mm'))

