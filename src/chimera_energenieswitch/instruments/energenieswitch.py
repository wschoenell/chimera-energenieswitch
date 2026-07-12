# SPDX-FileCopyrightText: 2015-present William Schoenell <wschoenell@gmail.com>
# SPDX-License-Identifier: GPL-2.0-or-later
"""Driver for EnerGenie EG-PMS-LAN / EG-PM2-LAN network power switches."""

import ast

import requests
from chimera.core.chimeraobject import ChimeraObject
from chimera.interfaces.switch import Switch


class EnergenieSwitch(ChimeraObject, Switch):
    __config__ = {
        "device": "127.0.0.1",
        "output": 1,  # which output to switch on/off
        "switch_timeout": None,  # max seconds to wait for a state change
        "password": "",
    }

    def __init__(self):
        super().__init__()
        self.states = None

    def _get_state(self):
        self.states = None
        r = requests.post(
            f"http://{self['device']}/login.html",
            data={"pw": self["password"]},
        )
        self.states = ast.literal_eval(r.text.split("sockstates = ")[1].split(";")[0])
        return True

    def _set_state(self, state):
        self.states = None
        r = requests.post(
            f"http://{self['device']}/",
            data={"pw": self["password"], f"cte{self['output']}": f"{int(state)}"},
        )
        self.states = ast.literal_eval(r.text.split("sockstates = ")[1].split(";")[0])
        return bool(self.states[self["output"] - 1]) == state

    def switch_on(self):
        if self.is_switched_on():
            return True
        if self._set_state(True):
            self.switched_on()
            return True
        return False

    def switch_off(self):
        if not self.is_switched_on():
            return True
        if self._set_state(False):
            self.switched_off()
            return True
        return False

    def is_switched_on(self):
        self._get_state()
        if self.states is not None:
            return bool(self.states[self["output"] - 1])
        return False
