from setuptools import setup


setup(
    name='efidgy',
    version='0.11',
    packages=[
        'efidgy',
        'tests'
    ],
    install_requires=[
        'httpx==0.22',
    ],
)
