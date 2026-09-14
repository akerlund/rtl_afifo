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
// gray_to_bin
//
// Converts a Gray-coded value back to binary: bin[i] is the XOR of every gray
// bit from the top down to i.
//
// Needed because pointers cross the clock boundary Gray-coded -- only one bit
// changes per increment, so a sample taken mid-transition yields the old value
// or the new one and never a third -- but fill-level arithmetic needs them
// back in binary. Purely combinational, so it adds no latency to the crossing.
//
////////////////////////////////////////////////////////////////////////////////

`default_nettype none

module gray_to_bin #(
    parameter WIDTH_P = -1
  )(
    input  wire  [WIDTH_P-1 : 0] gray,
    output logic [WIDTH_P-1 : 0] bin
  );

  genvar i;

  generate
    for (i = 0; i < WIDTH_P; i++) begin
      assign bin[i] = ^gray[WIDTH_P-1 : i];
    end
  endgenerate

endmodule

`default_nettype wire
