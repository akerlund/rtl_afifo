////////////////////////////////////////////////////////////////////////////////
//
// Copyright (C) 2026 Fredrik Åkerlund
// https://github.com/akerlund/rtl_afifo
//
// Permission is hereby granted, free of charge, to any person obtaining a copy
// of this software and associated documentation files (the "Software"), to deal
// in the Software without restriction, including without limitation the rights
// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
// copies of the Software, and to permit persons to whom the Software is
// furnished to do so, subject to the following conditions:
//
// The above copyright notice and this permission notice shall be included in
// all copies or substantial portions of the Software.
//
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
// SOFTWARE.
//
// Description:
// fi_tb_pkg
//
// Compilation unit for the testbench side of the UVM environment. Imports the
// UVM and AXI4-Stream agent packages, then includes the environment, the
// scoreboard and the virtual sequencer.
//
// Split from fi_tc_pkg so the reusable environment compiles independently of
// the test cases built on it.
//
////////////////////////////////////////////////////////////////////////////////

`ifndef SYFI_TB_PKG
`define SYFI_TB_PKG

package fi_tb_pkg;

  import uvm_pkg::*;
  `include "uvm_macros.svh"

  import clk_rst_types_pkg::*;
  import clk_rst_pkg::*;
  import vip_axi4s_types_pkg::*;
  import vip_axi4s_agent_pkg::*;

  localparam int VIP_AXI4S_TDATA_WIDTH_C = 32;
  localparam int VIP_AXI4S_TSTRB_WIDTH_C = VIP_AXI4S_TDATA_WIDTH_C/8;
  localparam int VIP_AXI4S_TKEEP_WIDTH_C = 0;
  localparam int VIP_AXI4S_TID_WIDTH_C   = 11;
  localparam int VIP_AXI4S_TDEST_WIDTH_C = 0;
  localparam int VIP_AXI4S_TUSER_WIDTH_C = 0;

  // Configuration of the VIP (Data)
  localparam vip_axi4s_cfg_t VIP_AXI4S_CFG_C = '{
    VIP_AXI4S_TDATA_WIDTH_P : VIP_AXI4S_TDATA_WIDTH_C,
    VIP_AXI4S_TSTRB_WIDTH_P : VIP_AXI4S_TSTRB_WIDTH_C,
    VIP_AXI4S_TKEEP_WIDTH_P : 0,
    VIP_AXI4S_TID_WIDTH_P   : 0,
    VIP_AXI4S_TDEST_WIDTH_P : 0,
    VIP_AXI4S_TUSER_WIDTH_P : 0
  };

  localparam int FIFO_ADDR_WIDTH_C = 6; // Minimum width is (1)
  localparam int FIFO_DATA_WIDTH_C = VIP_AXI4S_TDATA_WIDTH_C + 1;

  `include "fi_scoreboard.sv"
  `include "fi_virtual_sequencer.sv"
  `include "fi_env.sv"
  `include "vip_axi4s_seq_lib.sv"

endpackage

`endif
