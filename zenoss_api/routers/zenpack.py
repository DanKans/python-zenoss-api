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
Zenpacks router for the Zenoss JSON API
"""

from zope.interface import implements

from zenoss_api.interfaces import IZenpack
from zenoss_api.router import RouterBase
from zenoss_api.utils import myArgs

info = {"name": "zenpack",
    "author": "Endre Karlson endre.karlson@gmail.com",
    "version": "0.1",
    "class": "Zenpack"}


class Zenpack(RouterBase):
    implements(IZenpack)

    # Location + action
    location = 'zenpack_router'
    action = 'ZenpackRouter'

    def getEligiblePacks(self, **kw):
        args = myArgs()[0]
        return self._request(args, **kw)

    def addToZenPack(self, topack, zenpack, **kw):
        args = myArgs()[0]
        return self._request(args, **kw)
