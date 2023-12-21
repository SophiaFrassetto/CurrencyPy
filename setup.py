import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="CurrencyPy",
    version="0.1.1",
    author="Sophia de Angelo Frassetto",
    author_email="sophiafrassetto@gmail.com",
    description="Some tools for currency values, such as conversion sanitization and validation",
    keywords="currency tools converter",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SophiaFrassetto/CurrencyPy",
    project_urls={
        "Documentation": "",
        "Source Code": "https://github.com/SophiaFrassetto/CurrencyPy",
    },
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Natural Language :: Portuguese (Brazilian)"
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development",
        "Topic :: Utilities",
    ],
    package_dir={"": "currencypy"},
    packages=setuptools.find_packages(where="currencypy"),
    include_package_data=True,
    zip_safe=True,
    test_requires=[],
    install_requires=[],
    extras_require={
        'coverage'
    },
    python_requires=">=3.6",
)
