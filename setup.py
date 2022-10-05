from setuptools import find_packages, setup

setup(
    name='cocktail_maker',
    version='0.0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask',
        'python-dotenv',
    ],
)
