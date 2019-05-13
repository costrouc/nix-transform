from setuptools import setup

setup(
    name="nix-transform",
    description="Tools for formatting and transforming nix source code",
    version="0.1.0",
    packages=["nix_transform"],
    license="MIT",
    long_description=open("README.md").read(),
    author="Christopher Ostrouchov",
    author_email="chris.ostrouchov@gmail.com",
    url="https://github.com/costrouc/nix-transform/",
    install_requires=["sly"],
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            "nix-format = nix_transform.__main__:main"
        ]
    },
    classifiers=[
        "Natural Language :: English",
        "Intended Audience :: Developers",
        "Operating System :: POSIX :: Linux",
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Software Development :: Code Generators",
        "Topic :: System :: Software Distribution",
    ],
)
