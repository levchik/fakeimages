from setuptools import setup, find_packages

setup(
    name='fakeimages',
    version='0.2',
    author='Lev Rubel',
    author_email='rubel.lev@gmail.com',
    packages=find_packages(),
    url='http://pypi.python.org/pypi/fakeimages/',
    license='Apache 2.0',
    package_data={'': ['LICENSE'], 'fakeimages': ['*.pem']},
    package_dir={'fakeimages': 'fakeimages'},
    include_package_data=True,
    description='Placeholder images manipulating library.',
    install_requires=['Pillow==2.4.0', 'requests==2.2.1', 'six==1.6.1'],
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries',
    ]
)
