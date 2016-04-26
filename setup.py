from setuptools import setup

setup(
    name='django-wms',
    version='0.1.12',
    packages=['wms'],
    include_package_data=True,
    license='BSD',
    description='Mapscript based WMS framework for GeoDjango',
    url='https://github.com/geodesign/django-wms',
    author='Daniel Wiesmann',
    author_email='daniel@urbmet.com',
    install_requires=[
        'Django>=1.9',
    ],
    keywords=[
        'django', 'gis', 'mapserver', 'mapscript', 'wms',
        'tms', 'web map service', 'tile map service',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.9',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Scientific/Engineering :: GIS',
    ]
)
