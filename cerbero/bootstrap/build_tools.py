# cerbero - a multi-platform build system for Open Source software
# Copyright (C) 2012 Andoni Morales Alastruey <ylatuya@gmail.com>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public
# License along with this library; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.

import os

from cerbero.config import Config, DEFAULT_HOME, Platform
from cerbero.bootstrap import BootstraperBase
from cerbero.build.oven import Oven
from cerbero.build.cookbook import CookBook


class BuildTools (BootstraperBase):

    BUILD_TOOLS = ['automake', 'autoconf', 'm4', 'libtool', 'pkg-config',
                   'orc-tool', 'gettext-m4']
    PLAT_BUILD_TOOLS = {
            Platform.DARWIN: ['intltool'],
            Platform.WINDOWS: ['intltool'],
            }

    def start(self):
        # Use a common prefix for the build tools for all the configurations
        # so that it can be reused
        config = Config()
        os.environ.clear()
        os.environ.update(self.config._pre_environ)
        config.load()
        config.prefix = config.build_tools_prefix
        config.sources = os.path.join(DEFAULT_HOME, 'sources', 'buid-tools')
        config.cache_file = 'build_tools'

        if not os.path.exists(config.prefix):
            os.makedirs(config.prefix)
        if not os.path.exists(config.sources):
            os.makedirs(config.sources)

        config.do_setup_env()
        cookbook = CookBook(config)
        recipes = self.BUILD_TOOLS
        recipes += self.PLAT_BUILD_TOOLS.get(self.config.platform, [])
        oven = Oven(recipes, cookbook)
        oven.start_cooking()
        self.config.do_setup_env()
