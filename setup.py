from setuptools import setup
setup(
    name="recontool",
    version="1.0.0",
    packages=["src"],
    install_requires=open("requirements.txt").readlines(),
)
