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

import gettext

# general
application = "lisslo"
version = "0.4"

gettext.bindtextdomain(application)
gettext.textdomain(application)
_ = gettext.gettext

description = _('LiMux Schedule Shutdown with Logind')

# CLI strings
help_schedule_file = _("action will be stored here")
help_include_remote = _('consider not only local but also remote sessions')
help_action = _('schedule a shutdown with "reboot" or "poweroff" or abort a '
                'scheduled shutdown with "cancel"')
help_message = _("reason for shutdown")
help_no_login = _("prevent logins")
help_no_login_flag = _("flag file for preventing login")
help_interactive = _("get interactive confirmation from user")
help_request_file = _('filename in "/run/user/$UID/" which stores users '
                      'shutdown request')
help_timeout = _("automatically shutdown after this timeout")

error_request_evaluation = _("Can not evaluate shutdown request!")

status_cancel = _("Cancel any scheduled shutdown.")
status_shutdown = _("There are no users sessions running. Hence we shutdown.")
status_schedule = _("There are users sessions running. Hence we schedule "
                    "shutdown.")

# GUI strings
accept = _("Ok")
cancel = _("Cancel")
remote = _("via remote")
vt = _("on virtual terminal ")
confirmation_title = _("Shutdown")
confirmation_message = _("There are other user logged in. Their sessions "
                         "will be terminated inevitably. Do you really want "
                         "to shutdown?")
timeout_message = _("The system will automatically shutdown in {}s.")
