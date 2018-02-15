# setup.py
#
# Copyright (C) 2018 Max Harmathy <max.harmathy@web.de>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import os
from distutils.command.build import build
from distutils.command.install import install
from distutils.core import setup
from subprocess import run, PIPE

from lisslo import strings

translations = ["de"]


def locale_target(lang, prefix):
    return "{0}/share/locale/{1}/LC_MESSAGES".format(prefix, lang)


def compile_translation(lang, name, prefix):
    po_path = "po/{0}.po".format(lang)
    mo_path = "{0}/{1}.mo".format(locale_target(lang, prefix), name)
    run(["msgfmt", po_path, "-o", mo_path],
        check=True, stdout=PIPE, stderr=PIPE)


def compile_translations(prefix):
    for lang in translations:
        os.makedirs(locale_target(lang, prefix), exist_ok=True)
        compile_translation(lang, strings.application, prefix)


class CustomBuild(build):
    def run(self):
        super().run()
        compile_translations(self.build_base)


class CustomInstall(install):
    def run(self):
        super().run()
        self.copy_tree(self.build_base + "/share", self.install_data + "/share")


setup(
    name=strings.application,
    version=strings.version,
    description=strings.description,
    license="GPL3",
    packages=["lisslo"],
    scripts=["bin/lisslo-system-event", "bin/lisslo-user-session"],
    requires=['pydbus', 'PyQt5'],
    cmdclass=dict(build=CustomBuild, install=CustomInstall),
)
