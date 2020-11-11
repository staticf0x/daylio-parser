import pathlib

from setuptools import find_packages, setup

here = pathlib.Path(__file__).parent.resolve()
long_description = (here/'README.md').read_text(encoding='utf-8')

setup(
    name='daylio-parser',
    version='0.0.1',
    description='',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/meesha7/daylio-parser',
    author='Meesha',
    license='MIT',
    classifiers=[
    ],
    keywords='',
    packages=find_packages(),
    python_requires='>=3.7, <4',
    install_requires=['numpy'],
    extras_require={
        'dev': ['pycodestyle', 'isort'],
        'test': ['green']
    }
)
