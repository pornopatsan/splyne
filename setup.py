try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

def get_requirements(fname):
    with open(fname, 'r') as f:
        return [line.rstrip('\n') for line in f.readlines()]

setup(
    name="splyne",
    version="0.0.1",
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')
)
