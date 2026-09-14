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
# Base pyUVM test for the asynchronous FIFO.
#
################################################################################

from __future__ import annotations

from cocotb.triggers import Timer
from pyuvm import ConfigDB, uvm_test

from afifo_env import afifo_env
from vip_axi4s_config import vip_axi4s_config
from vip_axi4s_types_pkg import Axi4sAgentType


class afifo_base_test(uvm_test):

  def __init__(self, name, parent):
    super().__init__(name, parent)
    self.cfg_t = None
    self.env = None
    self.wp_cfg = None
    self.rp_cfg = None
    self.wp_vif = None
    self.rp_vif = None

  def build_phase(self):
    self.cfg_t = ConfigDB().get(self, "", "cfg_t")
    self.wp_vif = ConfigDB().get(self, "", "wp_vif")
    self.rp_vif = ConfigDB().get(self, "", "rp_vif")
    self.env = afifo_env("tb_env", self)

    self.wp_cfg = vip_axi4s_config("afifo_wp_cfg0")
    self.rp_cfg = vip_axi4s_config("afifo_rp_cfg0")
    self.rp_cfg.vip_axi4s_agent_type = Axi4sAgentType.SLAVE

    self.wp_cfg.min_tvalid_delay_period = 1
    self.wp_cfg.max_tvalid_delay_period = 4
    self.rp_cfg.min_tready_delay_period = 1
    self.rp_cfg.max_tready_delay_period = 4

    ConfigDB().set(self, "tb_env.wp_agent0", "cfg", self.wp_cfg)
    ConfigDB().set(self, "tb_env.rp_agent0", "cfg", self.rp_cfg)

  @property
  def wp_sequencer(self):
    return self.env.wp_agent0.sequencer

  @property
  def rp_sequencer(self):
    return self.env.rp_agent0.sequencer

  async def wait_for_compared(self, expected, timeout=20000):
    for _ in range(timeout):
      if self.env.scoreboard0.number_of_compared >= expected:
        return True
      await self.rp_vif.rising()
      await Timer(1, unit="step")
    return self.env.scoreboard0.number_of_compared >= expected

  async def settle(self, cycles=20):
    for _ in range(cycles):
      await self.wp_vif.rising()
      await self.rp_vif.rising()

  def report_phase(self):
    sb = self.env.scoreboard0
    self.logger.info(
      f"[{self.get_name()}] DONE -- compared={sb.number_of_compared} "
      f"passed={sb.number_of_passed} failed={sb.number_of_failed}")
