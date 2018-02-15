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

from pydbus import SystemBus

_system_bus = SystemBus()
_name = 'org.freedesktop.login1'
_logind = _system_bus.get(".login1")


def request_reboot(interactive=True):
    _logind.Reboot(interactive)


def request_power_off(interactive=True):
    _logind.PowerOff(interactive)


class Session():

    def __init__(self, session_id, user_id, user_name, seat, object_path):
        self.id = session_id
        self.user_id = user_id
        self.user_name = user_name
        self.seat = seat
        self.object_path = object_path

        self._session_proxy = _system_bus.get(_name, self.object_path)

    def is_user_session(self):
        return self._session_proxy.Class == "user"

    def is_local(self):
        return not self._session_proxy.Remote

    def vt_nr(self):
        return self._session_proxy.VTNr

    def type(self):
        return self._session_proxy.Type


def sessions():
    for s_id, user_id, user_name, seat, object_path in _logind.ListSessions():
        yield Session(s_id, user_id, user_name, seat, object_path)


def _this_session():
    return _system_bus.get(_name, "/org/freedesktop/login1/session/self")


def current_session():
    this_session = _this_session()
    session_id = this_session.Id
    user_id = this_session.User[0]
    user_name = this_session.Name
    seat = this_session.Seat[0]
    object_path = "/org/freedesktop/login1/session/{}".format(session_id)
    return Session(session_id, user_id, user_name, seat, object_path)


def other_user_sessions(including_remote=False):
    this_session = _this_session()
    return [
        session for session in sessions() if
        session.is_user_session() and
        (including_remote or session.is_local()) and
        session.id != this_session.Id
    ]


def no_users(including_remote=False):
    return all(not session.is_user_session() or
               not (including_remote or session.is_local())
               for session in sessions())
