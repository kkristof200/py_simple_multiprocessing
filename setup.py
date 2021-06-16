import setuptools, os

readme_path = 'README.md'

if os.path.exists(readme_path):
    with open(readme_path, 'r') as f:
        long_description = f.read()
else:
    long_description = 'simple_multiprocessing'

setuptools.setup(
    name='simple_multiprocessing',
    version="0.0.15",
    author='Kristóf-Attila Kovács',
    description='simple_multiprocessing',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/kkristof200/py_simple_multiprocessing',
    packages=setuptools.find_packages(),
    install_requires=[
        'noraise>=0.0.16',
        'stopit>=1.1.2'
    ],
    classifiers=[
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.4',
)