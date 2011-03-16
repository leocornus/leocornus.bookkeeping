from setuptools import setup, find_packages
import os

version = open(os.path.join('leocornus/bookkeeping', 'version.txt')).read().split('\n')[0]

setup(name='leocornus.bookkeeping',
      version=version,
      description="A Plone way to book keeping",
      long_description=open(os.path.join('leocornus/bookkeeping', "README.txt")).read() + "\n" +
          open(os.path.join("leocornus/bookkeeping/docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Programming Language :: Python",
        "Programming Language :: Zope",
        "Topic :: Software Development :: Documentation",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='Python Plone Zope Project Management',
      author='Sean Chen',
      author_email='sean.chen@leocorn.com',
      url='http://plonexp.leocorn.com/xp/leocornus.bookkeeping',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['leocornus'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'Products.MasterSelectWidget',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
