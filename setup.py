from setuptools import setup

setup(
    name='pysteam',
    version='0.1',
    description='Python library to work with Steam',
    url='http://github.com/scottrice/pysteam',
    author='Scott Rice',
    author_email='',
    license='MIT',
    packages=['pysteam'],
    install_requires=[
        'steamapi',
    ],
    data_files=[
    ],
    dependency_links=[
        'https://github.com/smiley/steamapi/archive/master.tar.gz#egg=steamapi-0.1',
    ],
    zip_safe=False,
    test_suite='nose.collector',
    tests_require=[
        'nose',
        'mock',
    ],
)
