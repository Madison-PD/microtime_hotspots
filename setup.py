from setuptools import find_packages, setup

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='mths_package',
    version='0.1.0',
    description='A package for identifying Micro-Time Hot Spots (MTHS) using Shapely and other base Python libraries.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Daniel Haueter',
    author_email='dhaueter@cityofmadison.com',
    url='https://github.com/Madison-PD/microtime_hotspots',
    packages=find_packages(),
    install_requires=[
        'shapely',
        'numpy'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent"
    ]
)
