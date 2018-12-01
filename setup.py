"""
Copyright (c) 2018 Orestes Mas

This file is part of PyCirkuit.

PyCirkuit is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

PyCirkuit is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with PyCirkuit.  If not, see <https://www.gnu.org/licenses/>.
"""

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
        long_description = fh.read()

setup(name='pycirkuit',
      version='0.1',
      description='A front-end for Circuit Macros',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://gitlab.upc.edu/CSL/Programari/pycirkuit.git',
      author='Orestes Mas',
      author_email='orestes@tsc.upc.edu',
      license='GPLv3',
      packages=find_packages(),
      classifiers=[
          "Programming Language :: Python ::3",
          "Operating System :: OS Independent",
      ],
      zip_safe=False)
