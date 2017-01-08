from setuptools import setup, find_packages

setup(
    name = 'liveset',
    version = '0.7.1',
    author = 'Alessandro Filippo',
    author_email = 'alessandro.filippo@infinito.it',
    license = 'GPLv2+',

    packages = find_packages('src'),
    package_dir = {'':'src'},
    scripts = ['./src/scripts/liveset','./src/scripts/usbswitchd.py'],

    include_package_data = True,
    package_data = {'':['src/etc/*.rules'],'':['install_udev-rules.sh']},
 
)
