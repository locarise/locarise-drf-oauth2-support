from setuptools import setup, find_packages

setup(
    name='locarise-drf-oauth2-support',
    version=__import__('locarise_drf_oauth2_support').__version__,
    description=__import__('locarise_drf_oauth2_support').__doc__,
    long_description=open('README.md').read(),
    author='Charles Vallantin Dulac',
    author_email='charles.vallantin-dulac@locarise.com',
    url='https://github.com/locarise/locarise-drf-oauth2-support',
    license='BSD License',
    packages=find_packages(),
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
        'shortuuid>=0.4.3'
    ],
    include_package_data=True,
    zip_safe=True,
)
