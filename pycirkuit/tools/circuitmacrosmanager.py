# -*- coding: utf-8 -*-
"""
Module implementing a CircuitMacros Manager class.
"""
# Copyright (C) 2018-2019 Orestes Mas
# This file is part of PyCirkuit.
#
# PyCirkuit is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PyCirkuit is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PyCirkuit.  If not, see <https://www.gnu.org/licenses/>.
#

# Standard library imports
import os
import shutil
import tarfile
import urllib.request as Net
import urllib.error as NetError

# Third-party imports
from PyQt5 import QtCore
from PyQt5.QtCore import QStandardPaths

# Local application imports
from pycirkuit.exceptions import *

# Translation function
_translate = QtCore.QCoreApplication.translate


class CircuitMacrosManager(QtCore.QObject):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor

        @param parent reference to the parent widget
        @type QWidget
        """
        pass

    def check_installed(self):
        #TODO: Should:
        #  1) Test several places, starting with the one set up in config, but then test also standard locations
        #  2) Two possibilities can arise:
        #     a) There's only one place where CM are
        #     b) They are found in two or more places
        #  3) We can do many things: Ask user which ones to use, use the newest ones, pick up the first found...
        #  4) Finally, as a SIDE EFFECT we can update config automatically or not.
        settings = QtCore.QSettings()
        cmPath = settings.value("General/cmPath",  "")
        return os.path.exists(os.path.join(cmPath , "libcct.m4"))

    def default_CMPath(self):
        return os.path.normpath(os.path.join(QtCore.QStandardPaths.writableLocation(QtCore.QStandardPaths.AppDataLocation), "circuit_macros"))
        
    def download_latest(self, percent):
        origin = "http://www.ece.uwaterloo.ca/~aplevich/Circuit_macros/Circuit_macros.tar.gz"
        destination = os.path.dirname(self.default_CMPath())
        if destination == "":
            raise PyCirkuitError(_translate("ExternalTool", "Cannot determine the standard writable location for PyCirkuit",  "Error message"))
        if not os.path.exists(destination):
            os.makedirs(destination)
        destination = os.path.join(destination,"Circuit_macros.tar.gz")
        try:
            with Net.urlopen(origin) as source,  open(destination, 'wb') as dest:
                length = source.getheader('content-length')
                if length:
                    length = int(length)
                    percent.setRange(0, length)
                    percent.setValue(0)
                    blocksize = max(4096, length//100)
                else:
                    blocksize = 1000000 # just made something up
                size = 0
                while True:
                    buf1 = source.read(blocksize)
                    if not buf1:
                        break
                    dest.write(buf1)
                    size += len(buf1)
                    percent.setValue(size)
        except NetError.URLError as e:
            #FIXME: Convert to MessageBox by reraising as PyCktCMFetchError
            print(_translate("ExternalTool", "Network error: ",  "Error message"), e)

    def getManUrl(self):
        # Get standard locations for documentation in a platform-independent way
        dirList = QStandardPaths.standardLocations(QStandardPaths.GenericDataLocation)
        # Append specific location
        dirList = [os.path.join(dir, "doc", "circuit_macros") for dir in dirList]
        # Add the config-stored Circuit Macros Location to this list
        settings = QtCore.QSettings()
        dirList.append(os.path.normpath(settings.value("General/cmPath",  "")))
        # Add the default Circuit Macros location to this list (can be the same as above)
        dirList.append(self.default_CMPath())
        import glob
        import magic
        mime = magic.Magic(mime=True)
        for testPath in dirList:
            testPath = os.path.join(testPath, "doc", "Circuit_macros")
            candidates = glob.glob(testPath + ".[pP][dD][fF]")
            for candidate in candidates:
                if (mime.from_file(candidate) == "application/pdf"):
                    return(candidate)
        else:
            raise PyCktCMManNotFoundError(os.path.normpath(settings.value("General/cmPath",  "")))

    def unpack_circuit_macros(self):
        try:
            dataPath = QtCore.QStandardPaths.writableLocation(QtCore.QStandardPaths.AppDataLocation)
            tarName = os.path.abspath(os.path.join(dataPath,  'Circuit_macros.tar.gz'))
            with tarfile.open(tarName, 'r:gz') as tarFile:
                # Circuit Macros is distributed in a tree structure.
                # We want the top dir of this structure to be 'circuit_macros', whichever it is now
                # The following algorithm assumes that all circuit macros's files are in a subdir.
                entry = tarFile.next()
                storedDir, foo, bar = entry.name.partition('/')  # Got stored top dir name in 'storedDir'
                # Now iterate and replace top directory name in all entries
                for entry in tarFile.getmembers():
                    filename = entry.name
                    entry.name = filename.replace(storedDir, 'circuit_macros', 1)
                tarFile.extractall(path=dataPath)
            os.remove(tarName)
            settings = QtCore.QSettings()
            settings.setValue("General/cmPath", os.path.join(dataPath , 'circuit_macros'))
            settings.sync()
        except tarfile.TarError as e:
            if os.path.exists(dataPath):
                shutil.rmtree(os.path.join(dataPath , "/."))
            #FIXME: Convert to MessageBox by reraising as PyCktCMFetchError
            print(_translate("ExternalTool", "Error uncompressing the Circuit Macros: ",  "Error message"), e)