import requests
import ast
from chimera.core.chimeraobject import ChimeraObject
from chimera.interfaces.switch import Switch


class EnergenieSwitch(ChimeraObject, Switch):
    __config__ = {"device": "127.0.0.1",
                  "output": 1,  # Which output to switch on/off
                  "switch_timeout": None,  # Maximum number of seconds to wait for state change
                  "password": ""
                  }

    def __init__(self):
        super(EngieSwitch, self).__init__()
        self.states = None

    def _getstate(self):
        self.states = None
        r = requests.post('http://%s/login.html' % self["device"], data=dict(pw=self["password"]))
        self.states = ast.literal_eval(r.text.split("sockstates = ")[1].split(";")[0])
        return True

    def _setstate(self, state):
        self.states = None
        r = requests.post('http://%s/' % self["device"], data={"pw": self["password"],
                                                                "cte%i" % self["output"]: "%i" % state})
        self.states = ast.literal_eval(r.text.split("sockstates = ")[1].split(";")[0])
        return bool(self.states[self["output"] - 1]) == state

    def switchOn(self):
        if not self.isSwitchedOn():
            if self._setstate(True):
                self.switchedOn()
                return True
            else:
                return False
        else:
            return True

    def switchOff(self):
        if self.isSwitchedOn():
            if self._setstate(False):
                self.switchedOff()
                return True
            else:
                return False
        else:
            return True

    def isSwitchedOn(self):
        self._getstate()
        if self.states is not None:
            return bool(self.states[self["output"] - 1])
