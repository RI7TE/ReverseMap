import setuptools


setuptools.setup(
    name="reversemap",
    version="0.1.0",
    author="Steven Kellum",
    author_email="sk@perfectatrifecta.com",
    description="ReverseMap is a specialized Python dictionary that enables bidirectional lookups - you can search using either keys or values with the in operator. It handles non-hashable objects by automatically converting them to hashable representations while maintaining the ability to revert back to the original objects.",
    download_url="https://github.com/RI7TE/ReverseMap.git",
    py_modules=["convert", "main", "rdict", "reverse", "test"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Proprietary License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
    python_requires=">=3.10",
    install_requires=["colorama==0.4.6"],
)
