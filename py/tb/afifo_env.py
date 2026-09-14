################################################################################
#
# Copyright (C) 2026 Fredrik Åkerlund
# https://github.com/akerlund/rtl_afifo
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# Description:
# pyUVM environment for the asynchronous FIFO testbench.
#
################################################################################

from __future__ import annotations

from pyuvm import ConfigDB, uvm_env

from afifo_scoreboard import afifo_scoreboard
from vip_axi4s_agent import vip_axi4s_agent


class afifo_env(uvm_env):

  def __init__(self, name, parent):
    super().__init__(name, parent)
    self.wp_agent0 = None
    self.rp_agent0 = None
    self.scoreboard0 = None

  def build_phase(self):
    self.wp_agent0 = vip_axi4s_agent("wp_agent0", self)
    self.rp_agent0 = vip_axi4s_agent("rp_agent0", self)
    self.scoreboard0 = afifo_scoreboard("scoreboard0", self)

    ConfigDB().set(self, "wp_agent0", "vif", ConfigDB().get(self, "", "wp_vif"))
    ConfigDB().set(self, "rp_agent0", "vif", ConfigDB().get(self, "", "rp_vif"))
    ConfigDB().set(self, "wp_agent0", "cfg_t", ConfigDB().get(self, "", "cfg_t"))
    ConfigDB().set(self, "rp_agent0", "cfg_t", ConfigDB().get(self, "", "cfg_t"))

  def connect_phase(self):
    self.wp_agent0.monitor.tdata_port.connect(self.scoreboard0.mst_port)
    self.rp_agent0.monitor.tdata_port.connect(self.scoreboard0.slv_port)

  def handle_reset(self):
    self.scoreboard0.handle_reset()
