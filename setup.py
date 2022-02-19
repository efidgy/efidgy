import os
from setuptools import setup
from setuptools import find_packages
import efidgy


def read(fname):
    return open(fname, encoding='utf8').read()


setup(
    name='efidgy',
    version=efidgy.__version__,
    author='Vasily Stepanov',
    author_email='vasily.stepanov@efidgy.com',
    license='GPL3',
    keywords='efidgy logistics optimization dispatcing vrp',
    url='https://github.com/efidgy/efidgy',
    description='Python bindings to efidgy services.',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: AsyncIO',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries',
    ],
    project_urls={
        'Documentation': 'https://efidgy.com/docs',
    },
    packages=find_packages(),
    install_requires=[
        'httpx>=0.22',
    ],
    python_requires='>=3.6',
)
