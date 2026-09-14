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
// HDL shell for the asynchronous FIFO pyUVM/cocotb testbench.
//
////////////////////////////////////////////////////////////////////////////////

`default_nettype none

module afifo_hdl_top #(
    parameter int DATA_WIDTH = 32,
    parameter int ADDR_WIDTH = 6
  )(
    input wire clk_wp,
    input wire rst_wp_n,
    input wire clk_rp,
    input wire rst_rp_n
  );

  logic                         wp_tvalid;
  logic                         wp_tready;
  logic                         wp_ready_q;
  logic                         wp_valid_q;
  logic [DATA_WIDTH : 0]        wp_data_q;
  logic [DATA_WIDTH-1 : 0]      wp_tdata;
  logic [DATA_WIDTH/8-1 : 0]    wp_tstrb;
  logic [DATA_WIDTH/8-1 : 0]    wp_tkeep;
  logic                         wp_tlast;
  logic                         wp_tid;
  logic                         wp_tdest;
  logic                         wp_tuser;

  logic                         rp_tvalid;
  logic                         rp_tready;
  logic [DATA_WIDTH-1 : 0]      rp_tdata;
  logic [DATA_WIDTH/8-1 : 0]    rp_tstrb;
  logic [DATA_WIDTH/8-1 : 0]    rp_tkeep;
  logic                         rp_tlast;
  logic                         rp_tid;
  logic                         rp_tdest;
  logic                         rp_tuser;

  logic [DATA_WIDTH : 0]        ing_data;
  logic [DATA_WIDTH : 0]        egr_data;
  logic                         fifo_full;
  logic                         fifo_empty;
  logic                         fifo_write_ready;
  logic [ADDR_WIDTH : 0]        unused_wp_fill_level;
  logic [ADDR_WIDTH : 0]        unused_wp_max_fill_level;
  logic [ADDR_WIDTH : 0]        unused_rp_fill_level;

  assign wp_tready = wp_ready_q && wp_valid_q;
  assign rp_tvalid = !fifo_empty;
  assign ing_data = wp_data_q;
  assign {rp_tlast, rp_tdata} = egr_data;

  // Hold READY stable across the write edge. This prevents the cocotb master
  // from observing a post-edge full-flag transition and advancing its item
  // before the DUT has sampled the corresponding handshake.
  always @(negedge clk_wp or negedge rst_wp_n) begin
    if (!rst_wp_n) begin
      wp_ready_q <= 1'b0;
      wp_valid_q <= 1'b0;
      wp_data_q  <= '0;
    end else begin
      wp_ready_q <= fifo_write_ready;
      wp_valid_q <= wp_tvalid;
      wp_data_q  <= {wp_tlast, wp_tdata};
    end
  end

  assign rp_tstrb = '1;
  assign rp_tkeep = '1;
  assign rp_tid = '0;
  assign rp_tdest = '0;
  assign rp_tuser = '0;

  afifo #(
    .DATA_WIDTH_P ( DATA_WIDTH + 1 ),
    .ADDR_WIDTH_P ( ADDR_WIDTH       )
  ) afifo_i0 (
    .clk_wp               ( clk_wp                 ),
    .rst_wp_n             ( rst_wp_n               ),
    .clk_rp               ( clk_rp                 ),
    .rst_rp_n             ( rst_rp_n               ),
    .wp_write_en          ( wp_valid_q && wp_ready_q ),
    .wp_data_in           ( ing_data                ),
    .wp_fifo_full         ( fifo_full               ),
    .rp_read_en           ( rp_tvalid && rp_tready ),
    .rp_data_out          ( egr_data                ),
    .rp_fifo_empty        ( fifo_empty              ),
    .sr_wp_fill_level     ( unused_wp_fill_level    ),
    .sr_wp_max_fill_level ( unused_wp_max_fill_level),
    .sr_rp_fill_level     ( unused_rp_fill_level    )
  );

  // The public AFIFO full flag clears before the internal write pointer is
  // released by the cross-domain reset synchronizer. Do not expose a ready
  // handshake during that interval.
  assign fifo_write_ready = !fifo_full &&
                            afifo_i0.afifo_core_i0.wclk_rclk_rst_n;

endmodule

`default_nettype wire
