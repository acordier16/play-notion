from setuptools import setup, find_packages

setup(
    name="play-notion",
    version="1.0",
    packages=find_packages(),
    install_requires=["requests>=2.31.0",
                      "termcolor>=2.3.0"],
    entry_points={
        "console_scripts": [
            "play-notion = main:main",
        ],
    },
)
