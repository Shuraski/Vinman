from setuptools import setup, find_packages

setup(
    name='vinman',
    version='0.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'vinman=main_prototype:cli',
        ],
    },
    install_requires=[
    ],
)