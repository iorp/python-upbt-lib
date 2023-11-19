
from setuptools import setup, find_packages

setup(
    description="Universal Package Building Tool",
    name='upbt',
    version='1.0.0',
    author='Iorp', 
    packages=find_packages(),
    install_requires=[
        'cython',
        'setuptools',
        'pyinstaller',
        'wheel'
    ],
    entry_points={}

)