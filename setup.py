import os

from setuptools import setup


def get_packages(package):
    """
    Return root package and all sub-packages.
    """
    return [dirpath
            for dirpath, dirnames, filenames in os.walk(package)
            if os.path.exists(os.path.join(dirpath, '__init__.py'))]


def get_package_data(package):
    """
    Return all files under the root package, that are not in a
    package themselves.
    """
    walk = [(dirpath.replace(package + os.sep, '', 1), filenames)
            for dirpath, dirnames, filenames in os.walk(package)
            if not os.path.exists(os.path.join(dirpath, '__init__.py'))]

    filepaths = []
    for base, filenames in walk:
        filepaths.extend([os.path.join(base, filename)
                          for filename in filenames])
    return {package: filepaths}


setup(
    name='locarise-drf-oauth2-support',
    version=__import__('locarise_drf_oauth2_support').__version__,
    description=__import__('locarise_drf_oauth2_support').__doc__,
    long_description=open('README.md').read(),
    author='Charles Vallantin Dulac',
    author_email='charles.vallantin-dulac@locarise.com',
    url='https://github.com/locarise/locarise-drf-oauth2-support',
    license='BSD License',
    packages=get_packages('locarise_drf_oauth2_support'),
    package_data=get_package_data('locarise_drf_oauth2_support'),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    install_requires=[
        'djangorestframework>=3.0.1',
        'django-oauth-toolkit>=0.9.0',
        'python-social-auth>=0.2.2',
        'shortuuid>=0.4.3',
        'django-shortuuidfield>=0.1.3',
        'django-extensions>=1.6.1',
        # 'factory-boy>=2.5.1'
    ],
    include_package_data=True,
    zip_safe=True,
)
