from setuptools import setup


with open("README.md") as fileobj:
    long_description = fileobj.read()


setup(
    name="dsc40graph",
    description="A simple graph library used in DSC 40B @ UCSD.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    version="0.2.0",
    author="Justin Eldridge",
    author_email="jeldridge@ucsd.edu",
    url="https://github.com/eldridgejm/dsc40graph",
    py_modules=["dsc40graph"],
    install_requires=[],
)
