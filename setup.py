from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
    long_description = long_description.replace("\r","")
except:
    print("Pypandoc not found. Long_description conversion failure.")
    with open(path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()

setup(
    name='lambdamanager',

    version='0.0.1',

    description='Tooling to manage functions in aws lambda',
    long_description=long_description,

    url='https://github.com/ant30/lambdamanager',

    author='Antonio Perez-Aranda Alcaide (ant30)',
    author_email='ant30tx_at_gmail_dot_com',

    # Choose your license
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    keywords='aws lambda serverless',

    packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    install_requires=[
        'boto3',
        'docopt',
        'GitPython',
        'PyYAML',
    ],

    # $ pip install -e .[dev,test]
    extras_require={
        'dev': ['check-manifest'],
        'test': ['coverage'],
        'build': ['pypandoc'],
    },

    entry_points={
        'console_scripts': [
            'lambdamanager=lambdamanager:main',
        ],
    },
)
