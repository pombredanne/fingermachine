from setuptools import setup, find_packages


install_requires = ['cv2', 'numpy']

with open('README.rst') as f:
    README = f.read()


classifiers = ["Programming Language :: Python",
               "License :: OSI Approved :: Apache Software License",
               "Development Status :: 1 - Planning"]


setup(name='fingermachine',
      version='0.1',
      url='https://github.com/tarekziade/fingermachine',
      packages=find_packages(),
      long_description=README,
      description=("Simple HTTP Load tester"),
      author="Tarek Ziade",
      author_email="tarek@ziade.org",
      include_package_data=True,
      zip_safe=False,
      classifiers=classifiers,
      install_requires=install_requires)
