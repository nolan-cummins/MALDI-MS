from setuptools import setup, find_packages

setup(name="fluigent_sdk",
      version="23.0.0",
      description="SDK for Fluigent Instruments",
      url="http://www.fluigent.com",
      author="Fluigent",
      author_email="support@fluigent.com",
      license="Proprietary",
      packages=find_packages(exclude=("tests",)),
      package_data={"Fluigent.SDK": ["shared/windows/*/*.dll",
                                     "shared/linux/*/*.so",
                                     "shared/mac/*/*.dylib"]},
      zip_safe=False)
