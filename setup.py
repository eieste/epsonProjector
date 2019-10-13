import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="epsonprojector",
    version="0.0.1",
    license='MIT',
    author="Stefan Eiermann",
    author_email="python-org@ultraapp.de",
    description="This library helps to control Epson projectors using the RS232 interface.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/eieste/epsonProjector",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    include_package_data=True,
    install_requires=[
        'jsonschema',
        'pyaml'
    ],
)
