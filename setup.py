import os

from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-wms',
    version='0.1.11',
    packages=['wms'],
    include_package_data=True,
    license='BSD',
    description='Mapscript based WMS framework for GeoDjango',
    long_description=README,
    url='https://github.com/geodesign/django-raster',
    download_url='https://github.com/geodesign/django-wms/tarball/v0.1.11',
    author='Daniel Wiesmann',
    author_email='daniel@urbmet.com',
    keywords=['django', 'gis', 'mapserver', 'mapscript', 'wms',
              'tms', 'web map service', 'tile map service'],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
