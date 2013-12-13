from setuptools import setup, find_packages
import os

version = '1.0.3dev'

setup(name='silva.pageactions.mailpdf',
      version=version,
      description="Send the current content by mail as a PDF in Silva CMS",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      classifiers=[
        "Framework :: Zope2",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='silva pageactions mail pdf',
      author='Infrae',
      author_email='info@infrae.com',
      url='https://github.com/silvacms/silva.pageactions.mailpdf',
      license='BSD',
      package_dir={'': 'src'},
      packages=find_packages('src'),
      namespace_packages=['silva', 'silva.pageactions'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        'five.grok',
        'grokcore.chameleon',
        'setuptools',
        'silva.captcha',
        'silva.core.conf',
        'silva.core.interfaces',
        'silva.core.layout',
        'silva.core.views',
        'silva.pageactions.base',
        'silva.pageactions.pdf',
        'zeam.form.silva',
        'zope.component',
        'zope.interface',
        'zope.schema',
        'zope.traversing',
        ],
      )
