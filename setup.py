from setuptools import setup

setup(name='PGConfig API',
      version='1.0',
      description='PGConfig.org API',
      author='Sebastian Webber',
      author_email='sebastian@swebber.me',
      url='http://api.pgconfig.org/',
      install_requires=['tornado', 'requests', 'beautifulsoup4'],
     )