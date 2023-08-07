from setuptools import setup, find_packages

setup(
    name="play-notion",
    version="0.1",
    packages=find_packages(),
    install_requires=["requests>=2.31.0"],
    entry_points={
        "console_scripts": [
            "play-notion = main:main",
        ],
    },
)
