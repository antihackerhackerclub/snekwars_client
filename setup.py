import os
from distutils.sysconfig import get_python_lib
from shutil import copyfile
from setuptools import setup
copyfile('snekwars_client.py', os.path.join(get_python_lib(), 'snekwars_client.py'))
setup(
    name="snekwars_client", 
    version="1.0.0", 
    install_requires = ["requests >= 2.28.0", "tabulate >= 0.9.0"],
    license="All Rights Reserved. Do not distribute.",
    url="https://github.com/antihackerhackerclub/snekwars_client"
    )

