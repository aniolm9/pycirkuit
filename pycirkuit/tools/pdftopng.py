# -*- coding: utf-8 -*-
"""
Module implementing a class to handle the pdftoppm external tool
"""
# Copyright (C) 2018 Orestes Mas
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


# Third-party imports
from PyQt5.QtCore import QCoreApplication

# Local application imports
from pycirkuit.tools.tool_base import ExternalTool

# Translation function
_translate = QCoreApplication.translate

class ToolPdfToPng(ExternalTool):
    def __init__(self):
        super().__init__("pdftoppm", _translate("ExternalTool", "PDF to PNG image converter", "Tool Long Name"))
        
    def execute(self, baseName):
        # Calculate src and dst names
        src = baseName + '.pdf'
        dst = baseName + '.png'
        # Instantiate a settings object to load config values. At this point the config have valid entries, so don't test much
        command = [self.executableName, "-png", "{source}".format(source=src), ">", "{destination}".format(destination=dst)]
        errMsg = _translate("ExternalTool", "PDFTOPPM: Error converting PDF -> PNG", "Error message")
        super().execute(command, errMsg)
