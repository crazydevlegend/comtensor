from setuptools import setup, find_packages

setup(
    name="comtensor",
    version="0.1.0",
    author="crazydevlegend, gitphantom",
    author_email="crazydevlegend@gmail.com, gitphantom@gmail.com",
    description="Bridging Commune and Bittensor",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Comtensor/comtensor",
    packages=find_packages(),
    install_requires=[open("requirements.txt").read().splitlines()],
    classifiers=[
        # Choose your license as you wish
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
