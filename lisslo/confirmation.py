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

from PyQt5 import QtGui, QtWidgets, QtCore
from lisslo import strings


class ConfirmationDialog(QtWidgets.QDialog):

    def __init__(self, sessions, timeout):
        self.shutdown = False
        self.timeout = timeout
        super().__init__()
        self.setWindowTitle(strings.confirmation_title)
        self.setWindowIcon(QtGui.QIcon.fromTheme("system-users"))

        self.main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.main_layout)

        self.message_widget = QtWidgets.QWidget(parent=self)
        self.main_layout.addWidget(self.message_widget)
        self.message_layout = QtWidgets.QHBoxLayout()
        self.message_widget.setLayout(self.message_layout)
        self.message_icon = QtWidgets.QLabel(
            parent=self.message_widget,
            pixmap=QtGui.QIcon.fromTheme("important").pixmap(48, 48),
        )
        self.message_layout.addWidget(self.message_icon)
        self.message_label = QtWidgets.QLabel(
            text=strings.confirmation_message, parent=self.message_widget)
        self.message_label.setWordWrap(True)
        self.message_layout.addWidget(self.message_label)

        self.session_display = QtWidgets.QListWidget(parent=self)
        self.session_display.setAlternatingRowColors(True)
        self.session_icon_graphical = QtGui.QIcon.fromTheme(
            "user", QtGui.QIcon.fromTheme("face-plain"))
        self.session_icon_terminal = QtGui.QIcon.fromTheme("network-wired")

        def icon_for(session_type):
            if session_type == "tty":
                return self.session_icon_terminal
            return self.session_icon_graphical

        def label_for(session):
            attached_to = strings.vt + str(
                session.vt_nr()) if session.is_local() else strings.remote
            return "{}\n({})".format(session.user_name, attached_to)

        self.session_entries = [
            QtWidgets.QListWidgetItem(
                icon_for(session.type()),
                label_for(session),
                parent=self.session_display,
            ) for session in sessions if session.is_user_session()
        ]
        self.main_layout.addWidget(self.session_display)

        self.timeout_message = QtWidgets.QLabel(
            strings.timeout_message.format(self.timeout)
        )
        self.main_layout.addWidget(self.timeout_message,
                                   alignment=QtCore.Qt.AlignHCenter)
        self.shutdown_timer = QtCore.QTimer(self)
        self.shutdown_timer.timeout.connect(self.on_timer)
        self.shutdown_timer.start(1000)

        self.button_widget = QtWidgets.QWidget(parent=self)
        self.button_layout = QtWidgets.QHBoxLayout()
        self.button_widget.setLayout(self.button_layout)
        self.main_layout.addWidget(self.button_widget)
        self.cancel_button = QtWidgets.QPushButton(
            text=strings.cancel, parent=self.button_widget)
        self.cancel_button.pressed.connect(self.on_cancel)
        self.button_layout.addWidget(self.cancel_button)
        self.button_layout.addStretch()
        self.accept_button = QtWidgets.QPushButton(
            text=strings.accept, parent=self.button_widget)
        self.accept_button.pressed.connect(self.on_accept)

        pal = self.accept_button.palette()
        pal.setColor(QtGui.QPalette.Button, QtGui.QColor(QtCore.Qt.red))
        self.accept_button.setAutoFillBackground(True)
        self.accept_button.setPalette(pal)
        self.accept_button.update()

        self.button_layout.addWidget(self.accept_button)

    def on_timer(self):
        if self.timeout <= 0:
            self.on_accept()
            return
        self.timeout -= 1
        self.timeout_message.setText(
            strings.timeout_message.format(self.timeout)
        )
        self.shutdown_timer.start(1000)

    def on_cancel(self):
        self.shutdown = False
        QtWidgets.QApplication.quit()

    def on_accept(self):
        self.shutdown = True
        QtWidgets.QApplication.quit()


def dialog(other_sessions, timeout):
    app = QtWidgets.QApplication([strings.application])
    if QtGui.QIcon.themeName() == "hicolor":
        QtGui.QIcon.setThemeName("breeze")
    confirm_dialog = ConfirmationDialog(other_sessions, timeout)
    confirm_dialog.show()
    app.exec()
    return confirm_dialog.shutdown

