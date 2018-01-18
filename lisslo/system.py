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
import re


def prevent_login(message, path):
    with open(path, "w") as handle:
        handle.write(message)


def allow_login(path):
    if os.path.exists(path):
        os.remove(path)


def shutdown_is_scheduled(path):
    return os.path.exists(path)


def schedule_shutdown(action, path):
    tmp_file = path + str(os.getpid())
    with open(tmp_file, "w") as handle:
        handle.write(action)
    os.rename(tmp_file, path)


def unschedule_shutdown(path):
    if os.path.exists(path):
        os.remove(path)


def request_file_path(uid, file_name):
    return "/run/user/{}/{}".format(uid, file_name)


def user_requested_shutdown(uid, file_name):
    return os.path.exists(request_file_path(uid, file_name))


def read_shutdown_type(path):
    pattern = re.compile("\s*(?:poweroff)|(?:reboot)\s*")
    with open(path) as handle:
        content = handle.read()
        return content if pattern.match(content) else ""
