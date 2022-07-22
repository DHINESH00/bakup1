from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in my_bid/__init__.py
from my_bid import __version__ as version

setup(
	name="my_bid",
	version=version,
	description="bid",
	author="dhinesh",
	author_email="dhinesh200014@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
