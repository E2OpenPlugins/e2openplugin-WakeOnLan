from distutils.core import setup

pkg = 'Extensions.WakeOnLan'
setup (name = 'enigma2-plugin-extensions-wakeonlan',
       version = '0.1',
       description = 'Sends Wake-On-LAN packets when recording etc.',
       package_dir = {pkg: 'plugin'},
       packages = [pkg],
      )
