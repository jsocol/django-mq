from setuptools import setup, find_packages

from djmq import __version__


try:
    with open('README.rst') as fp:
        LONGDESC = fp.read()
except:
    LONGDESC = ''


setup(
    name='djmq',
    version=__version__,
    description='Convert a MongoDB-style query into a Django query.',
    long_description=LONGDESC,
    author='James Socol',
    author_email='james@mozilla.com',
    url='https://github.com/jsocol/django-mq',
    license='BSD',
    packages=find_packages(),
    include_package_data=True,
    package_data={'': ['README.rst']},
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Environment :: Web Environment :: Mozilla',
        'Intended Audience :: Developers',
        'Framework :: Django',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
