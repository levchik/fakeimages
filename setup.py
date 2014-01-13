from setuptools import setup, find_packages

setup(
    name='fakeimages',
    version='0.1.1',
    author='Lev Rubel',
    author_email='rubel.lev@gmail.com',
    packages=find_packages(),
    url='http://pypi.python.org/pypi/fakeimages/',
    license='Apache 2.0',
    package_data={'': ['LICENSE'], 'fakeimages': ['*.pem']},
    package_dir={'fakeimages': 'fakeimages'},
    include_package_data=True,
    description='Placeholder images manipulating library.',
    install_requires=['Pillow==2.2.2', 'requests==1.2.3'],
    zip_safe=False,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries',
    ]
)
