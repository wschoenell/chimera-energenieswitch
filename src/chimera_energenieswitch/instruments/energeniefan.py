# SPDX-FileCopyrightText: 2015-present William Schoenell <wschoenell@gmail.com>
# SPDX-License-Identifier: GPL-2.0-or-later
"""Expose an EnerGenie switched output as a fan (start/stop via the switch)."""

from chimera.interfaces.fan import FanControl

from chimera_energenieswitch.instruments.energenieswitch import EnergenieSwitch


class EnergenieFan(EnergenieSwitch, FanControl):
    """A fan driven through an EnerGenie power switch output.

    FanControl inherits the Switch on/off contract, so the switch
    implementation doubles as the fan start/stop control.
    """
