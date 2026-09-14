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
# pyUVM scoreboard for the asynchronous FIFO testbench.
#
################################################################################

from __future__ import annotations

from pyuvm import uvm_component, uvm_subscriber


class _SbSub(uvm_subscriber):

  def __init__(self, name, parent, callback):
    super().__init__(name, parent)
    self._callback = callback

  def write(self, item):
    self._callback(item)


class afifo_scoreboard(uvm_component):

  def __init__(self, name, parent):
    super().__init__(name, parent)
    self.mst_items = []
    self.slv_items = []
    self.number_of_mst_items = 0
    self.number_of_slv_items = 0
    self.number_of_compared = 0
    self.number_of_passed = 0
    self.number_of_failed = 0
    self.mst_port = None
    self.slv_port = None

  def build_phase(self):
    self._mst_sub = _SbSub("mst_sub", self, self.write_mst_port)
    self._slv_sub = _SbSub("slv_sub", self, self.write_slv_port)
    self.mst_port = self._mst_sub.analysis_export
    self.slv_port = self._slv_sub.analysis_export

  def handle_reset(self):
    self.mst_items.clear()
    self.slv_items.clear()

  def write_mst_port(self, item):
    self.number_of_mst_items += 1
    self.mst_items.append(item.clone())
    self._compare_ready_items()

  def write_slv_port(self, item):
    self.number_of_slv_items += 1
    self.slv_items.append(item.clone())
    self._compare_ready_items()

  def _compare_ready_items(self):
    while self.mst_items and self.slv_items:
      mst = self.mst_items.pop(0)
      slv = self.slv_items.pop(0)
      self.number_of_compared += 1
      if _items_equal(mst, slv):
        self.number_of_passed += 1
      else:
        self.number_of_failed += 1
        self.logger.error(
          f"Packet {self.number_of_compared} mismatch: "
          f"mst={_item_tuple(mst)} slv={_item_tuple(slv)}")

  def check_phase(self):
    self._compare_ready_items()
    if self.mst_items or self.slv_items:
      self.number_of_failed += len(self.mst_items) + len(self.slv_items)
      self.logger.error(
        f"Unmatched packets: mst={len(self.mst_items)} "
        f"slv={len(self.slv_items)}")
    if self.number_of_failed:
      self.logger.error(
        f"Test failed! ({self.number_of_failed} mismatches)")
    else:
      self.logger.info(
        f"Test passed ({self.number_of_passed}/{self.number_of_compared}) "
        "finished transfers")


def _item_tuple(item):
  return (
    int(item.tid),
    int(item.tdest),
    [int(x) for x in item.tdata],
    [int(x) for x in item.tstrb],
    [int(x) for x in item.tkeep],
    [int(x) for x in item.tuser],
  )


def _items_equal(mst, slv):
  return _item_tuple(mst) == _item_tuple(slv)
