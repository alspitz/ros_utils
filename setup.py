from setuptools import find_packages, setup

setup(
    name="ros_utils",
    packages=find_packages(),
    author="Alex Spitzer",
    author_email="aes368@cornell.edu",
    license=open("LICENSE", mode="r").read(),
    install_requires=[
      'scipy>=1.2.0',
    ],
)
