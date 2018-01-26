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

from argparse import ArgumentParser

from lisslo import system
from lisslo import session

_arg_parser = ArgumentParser(
    description='LiMux Schedule Shutdown with Logind'
)


def _add_global_arguments():
    _arg_parser.add_argument(
        "-s", "--schedule-file", default="/run/scheduled_shutdown",
        help="action will be stored here"
    )


def request_shutdown(shutdown_type):
    if shutdown_type == "poweroff":
        session.request_power_off()
    elif shutdown_type == "reboot":
        session.request_reboot()
    else:
        print("Can not evaluate shutdown request!")
        return 1


def system_event_interface():
    _add_global_arguments()
    _arg_parser.add_argument(
        "action", choices=["reboot", "poweroff", "cancel"],
        help='schedule a shutdown with "reboot" or "poweroff" or abort a '
             'scheduled shutdown with "cancel"'
    )
    _arg_parser.add_argument(
        '-m', '--message', default="",
        help="reason for shutdown"
    )
    _arg_parser.add_argument(
        '-p', '--no-login', action="store_true", default=False,
        help="prevent logins"
    )
    _arg_parser.add_argument(
        '-f', '--no-login-flag', default="/run/nologin",
        help="flag file for preventing login"
    )
    args = _arg_parser.parse_args()

    if args.action == "cancel":
        print("Cancel any scheduled shutdown.")
        system.allow_login(args.no_login_flag)
        system.unschedule_shutdown(args.schedule_file)
        return

    if session.no_users():
        print("There are no users sessions running. Hence we shutdown.")
        if args.action == "request_reboot":
            session.request_reboot()
        if args.action == "poweroff":
            session.request_power_off()
    else:
        print("There are users sessions running. Hence we schedule shutdown.")
        system.schedule_shutdown(args.action, args.schedule_file)
        if args.no_login:
            system.prevent_login(args.message, args.no_login_flag)


def user_session_interface():
    _add_global_arguments()
    _arg_parser.add_argument(
        "-i", "--interactive", action="store_true", default=False,
        help="get interactive confirmation from user"
    )
    _arg_parser.add_argument(
        "-f", "--request-file", default="shutdown_request",
        help='filename in "/run/user/$UID/" which stores users shutdown request'
    )
    _arg_parser.add_argument(
        "-r", "--include-remote", action="store_true", default=False,
        help='consider remote sessions'
    )
    args = _arg_parser.parse_args()

    my_session = session.current_session()
    other_sessions = session.other_user_sessions(args.include_remote)
    if system.user_requested_shutdown(my_session.user_id, args.request_file):
        if len(other_sessions) > 0:
            # todo
            # ask user:
            # should other sessions get killed?
            # for now assume "No!"
            return
        path = system.request_file_path(my_session.user_id, args.request_file)
        shut_down = system.read_shutdown_type(path)
        request_shutdown(shut_down)
        return

    if system.shutdown_is_scheduled(args.schedule_file) and \
            not len(other_sessions) > 0:
        shutdown_type = system.read_shutdown_type(args.schedule_file)
        request_shutdown(shutdown_type)
