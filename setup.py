from setuptools import setup


setup(
    name='dollar-ref',
    version='0.1.3',

    description='JSON Reference Resolution',
    long_description="Both a command line tool and a library for resolving JSON references,"
    "which let's you easily split your JSON or YAML files and then merge on demand.",

    url='https://github.com/bagrat/dollar-ref',

    author='Bagrat Aznauryan',
    author_email='contact@bagrat.io',

    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',

        'Environment :: Console',

        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',

        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',

        'Topic :: Utilities'
    ],

    keywords='json schema ref reference openapi yaml resolve',

    packages=['dollar_ref'],

    install_requires=[
        'PyYAML',
        'termcolor'
    ],

    entry_points={
        'console_scripts': [
            'dref=dollar_ref.console:main'
        ]
    }
)
