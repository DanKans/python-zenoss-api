# Copyright (C) 2011, Endre Karlson
# All rights reserved
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Code found on the web and modified - don't remember the url
"""

import imp
import os
import logging
import sys

from zope.interface import Interface


class PluginManager:
    definitions = {}

    def __init__(self, folder):
        """Load all available definitions stored in folder"""

        # Woop, loop through the paths and set the folder to path if folder
        # exists in one of the items in sys.path
        for path in sys.path:
            path = os.path.abspath(path + "/" + folder)
            if os.path.isdir(path):
                folder = path
                break

        # Is it there?
        if not os.path.isdir(folder):
            logging.error(
                "Unable to load plugins because '%s' is not a folder" % folder)
            return

        # Append the folder because we need straight access
        sys.path.append(folder)

        # Build list of folders in directory
        to_import = [
            os.path.join(folder, f) for f in os.listdir(folder) \
                if f.endswith(".py") and not f.startswith("__init__")]

        # Do the actual importing
        for mpath in sorted(to_import):
            self.__initialize_def(mpath)

    def __initialize_def(self, mpath):
        """Attempt to load the definition"""

        basename = os.path.basename(mpath)
        # Import works the same for py files and package modules so strip!
        if basename.endswith(".py"):
            name = basename[:-3]
        else:
            name = basename

        # Do the actual import
        imp.load_source(name, mpath)
        definition = sys.modules[name]

        # Add the definition only if the class is available
        if hasattr(definition, definition.info["class"]):
            self.definitions[definition.info["name"]] = definition
            logging.info("Loaded '%s'" % name)

    def loadSingle(self, name, *args, **kw):
        """
        Creates a new instance of a definition
        name - name of the definition to create

        any other parameters passed will be sent to the __init__ function
        of the definition, including those passed by keyword
        """
        logging.info("Loading definition '%s'" % name)
        definition = self.definitions[name]
        if "pathinfo" in kw:
            fp = (definition.__file__, os.path.dirname(definition.__file__))
            kw["path"] = fp
        try:
            instance = getattr(
                definition, definition.info["class"])(*args, **kw)
        except TypeError, e:
            logging.fatal(
                "Failed when loading definition '%s / %s' error - '%s'" %
                    (name, definition, e))
            return None
        except NotImplementedError, e:
            logging.info("Not loading '%s' - not implemented")
            return None

        return instance

    def loadAll(self, *args, **kw):
        """
        Creates an instance of each definition in definitions loaded when the
        manager is instantiated - should only be used if the definitions works
        the same ways.

        returns a dict of {"name": instance}
        params passed to *args and **kw will be passed to each definition
        """
        loaded = {}
        logging.info("Attempting to load up definitions - '%s'" %
            " ".join(self.definitions.keys()))
        for definition in self.definitions.keys():
            loaded[definition] = self.loadSingle(definition, *args, **kw)

        return loaded
