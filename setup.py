from setuptools import setup


setup(
    name='dollar-ref',
    version='0.1',

    description='JSON Reference Magic',
    long_description="""
    """,

    url='http://dref.bagrat.io',

    author='Bagrat Aznauryan',
    author_email='contact@bagrat.io',

    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',

        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],

    keywords='json schema ref reference',

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
