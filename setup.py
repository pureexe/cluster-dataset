import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cluster-dataset",
    version="0.1.4",
    author="Pakkapon Phongthawee",
    author_email="pakkapon.p_s19@vistec.ac.th",
    description="annoy to copy data from your computer to a lot of computing engines when you are doing data science? try cluster-dataset",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pureexe/cluster-dataset",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)