from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='index-check',
    version='1.0',
    description='GSI index checking tools',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    python_requires='>=3.6, <4',
    install_requires=requirements,
    scripts=[
        'bin/check_controls.py',
        'bin/fetch_index_counts.py'
    ]
)
