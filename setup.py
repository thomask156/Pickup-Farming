from distutils.core import setup

setup(
    name='Pickup Farming',
    version='0.8dev',
    packages=[],
    install_requires=['pynput', 'pyscreenshot', 'pywin32', 'PyQt5', 'pillow'],
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description=open('README.md').read(),
)