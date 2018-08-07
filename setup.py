from setuptools import setup

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='textmetrics',
    version='0.0.1',
    author='Maxwell Forbes',
    author_email='mbforbes@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='text-metrics text metrics nlp bleu rouge meteor ngrams vocabulary vocab',
    packages=['textmetrics'],
    url='https://github.com/mbforbes/textmetrics/',
    license='MIT',
    description='Automatic text metrics---BLEU, ROUGE, and METEOR, pllus extras like vocab and ngrams.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        "mypy-extensions >= 0.3.0",
        "numpy >= 1.15.0",
        "rouge >= 0.3.1",
        "six >= 1.11.0",
        "tabulate >= 0.8.2",
    ],
)
