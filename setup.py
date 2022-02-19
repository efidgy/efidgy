import os
from setuptools import setup
import efidgy


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='efidgy',
    version=efidgy.__version__,
    author='Vasily Stepanov',
    author_email='vasily.stepanov@efidgy.com',
    license='MIT',  # FIXME
    keywords='',  # FIXME
    url='https://github.com/efidgy/efidgy',
    long_description=read('README.md'),
    sifiers=[  # FIXME
        'Development Status :: 3 - Alpha',
        'Topic :: Software Development :: Code Generators',
        'License :: OSI Approved :: MIT License',
    ],
    packages=[
        'efidgy',
        'tests'
    ],
    install_requires=[
        'httpx>=0.22',
    ],
    # entry_points = {
    #     'console_scripts' : [
    #         'efidgy = efidgy:main'
    #     ],
    # },
)
