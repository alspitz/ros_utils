from setuptools import find_packages, setup

setup(
    name="ros_utils",
    version="0.1.1",
    packages=find_packages(),
    author="Alex Spitzer",
    author_email="aes368@cornell.edu",
    maintainer="Alex Spitzer",
    url="https://github.com/alspitz/ros_utils",
    license=open("LICENSE", mode="r").read(),
    install_requires=[
      'scipy>=1.2.0',
    ],
)
