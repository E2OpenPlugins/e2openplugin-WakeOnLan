from distutils.core import setup
import setup_translate

pkg = 'Extensions.WakeOnLan'
setup(name='enigma2-plugin-extensions-wakeonlan',
       version='0.1',
       description='Sends Wake-On-LAN packets when recording etc.',
       packages=[pkg],
       package_dir={pkg: 'plugin'},
       package_data={pkg: ['*.png', '*.xml', '*/*.png', 'locale/*/LC_MESSAGES/*.mo']},
       cmdclass=setup_translate.cmdclass, # for translation
      )
