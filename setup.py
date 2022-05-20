from setuptools import find_packages, setup

with open("README.md") as readme_file:
    readme = readme_file.read()

requirements = [
    "attrs>=19.3",
    "requests>=2.24.0",
    "sqlparse==0.4.2",
    "oddrn>=0.0.7",
    "pydantic>=1.8.2",
]

extras_require = {}

setup(
    name="odd_ge",
    version="0.0.1",
    description="ODD adapter to Great Expectations",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Provectus ODD team",
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    extras_require=extras_require,
    python_requires=">=3.6",
    zip_safe=False,
    keywords="odd-ge-adapter",
)
