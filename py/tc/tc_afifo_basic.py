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
# tc_afifo_basic
#
# The balanced crossing: both clocks at 10 ns and neither side throttled, so
# the FIFO neither fills nor starves.
#
# Eight bursts of sixteen counter beats must arrive complete and in order.
# This is the case that proves the crossing works at all; the two asymmetric
# tests are what stress the pointer synchronisation.
#
################################################################################

from __future__ import annotations

from afifo_base_test import afifo_base_test
from seq_lib.vip_axi4s_seq import vip_axi4s_seq
from vip_axi4s_types_pkg import Axi4sTdataType, Axi4sTstrbType


class tc_afifo_basic(afifo_base_test):

  def build_phase(self):
    super().build_phase()
    self.wp_cfg.zero_delays_enable = True
    self.rp_cfg.zero_delays_enable = True

  async def run_phase(self):
    self.raise_objection()
    await self.settle()

    seq = vip_axi4s_seq("afifo_seq0", self.cfg_t)
    seq.set_tdata_type(Axi4sTdataType.COUNTER)
    seq.set_burst_length(16)
    seq.set_nr_of_bursts(8)
    seq.set_tstrb_type(Axi4sTstrbType.ALL)
    await seq.start(self.wp_sequencer)

    assert await self.wait_for_compared(8), (
      f"Only {self.env.scoreboard0.number_of_compared} of 8 packets compared")
    assert self.env.scoreboard0.number_of_failed == 0
    self.drop_objection()
