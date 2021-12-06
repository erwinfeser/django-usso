import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))


def read(f):
    return open(f, 'r', encoding='utf-8').read()


setup(
    name='django-usso',
    version='0.2',
    packages=['usso'],
    description='(ugly) single sign-on for django projects',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    author='Erwin Feser',
    author_email='feser.erwin@gmail.com',
    url='https://github.com/erwinfeser/django-usso/',
    license='MIT',
    install_requires=[
        'Django>=3.2,<4',
    ]
)
