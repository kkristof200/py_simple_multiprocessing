import setuptools, os

readme_path = os.path.join(os.getcwd(), "README.md")
if os.path.exists(readme_path):
    with open(readme_path, "r") as f:
        long_description = f.read()
else:
    long_description = 'simple_multiprocessing'

setuptools.setup(
    name="simple_multiprocessing",
    version="0.0.11",
    author="Kristof",
    description="execute multiple async tasks as simple as possible",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kkristof200/py_simple_multiprocessing",
    packages=setuptools.find_packages(),
    install_requires=[
        'noraise>=0.0.8',
        'stopit>=1.1.2'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)