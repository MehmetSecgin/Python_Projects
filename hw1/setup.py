import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="circle-mesecg", # Replace with your own username
    version="0.0.1",
    author="Mehmet Ali Secgin",
    author_email="mesecg@ttu.ee",
    description="A package for HW1",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Scentryum/Advanced_Python_Hw",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "circle"},
    packages=setuptools.find_packages(where="circle"),
    python_requires=">=3.6",
)