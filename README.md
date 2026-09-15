# Asynchronous FIFO

![Verilator](https://img.shields.io/badge/Verilator-5.050-green)
![cocotb](https://img.shields.io/badge/cocotb-2.0.1-green)
![pyUVM](https://img.shields.io/badge/pyUVM-4.0.1-green)
![VCS](https://img.shields.io/badge/VCS-2025.06-green)
![FuseSoC](https://img.shields.io/badge/FuseSoC-2.4.6-blue)
A dual-clock FIFO: the write side runs on `clk_wp`, the read side on `clk_rp`,
and neither needs to know the other's frequency or phase.

Crossing a clock boundary safely is the whole problem, and it is solved with
**Gray-coded pointers**. A binary counter can change many bits at once, so a
reader sampling it mid-update can latch a value that was never written. A Gray
code changes exactly one bit per increment, so a sample taken during a
transition returns either the old value or the new one — never a third. Each
side's pointer is converted to Gray, synchronised into the other domain through
`cdc_bit_sync`, and converted back by `gray_to_bin`.

Based on Clifford Cummings, *Simulation and Synthesis Techniques for
Asynchronous FIFO Design*
([SNUG 2002](http://www.sunburst-design.com/papers/CummingsSNUG2002SJ_FIFO1.pdf)).

## Structure

| Module | Role |
|--------|------|
| `afifo` | top: the RAM-backed core plus a small output register stage |
| `afifo_core` | the pointer logic, the CDC synchronisers and the dual-clock RAM |
| `gray_to_bin` | Gray-to-binary conversion for a synchronised pointer |

The storage is `ram_sdp2c`, the two-clock simple-dual-port RAM — written on one
clock, read on the other, which is exactly what this needs.

## Cores

| VLNV | Contents |
|------|----------|
| `akerlund::afifo:1.0.0` | `afifo`, `afifo_core`, `gray_to_bin` |
| `akerlund::afifo_example_py:0` | the cocotb/pyUVM testbench |
| `akerlund::afifo_example:0` | the SystemVerilog/UVM testbench |

```sh
git clone --recurse-submodules git@github.com:akerlund/rtl_afifo.git
```

Submodules: [`rtl_fifo`](https://github.com/akerlund/rtl_fifo) for
`fifo_register`, which carries the read-side output stage and reaches
[`rtl_common`](https://github.com/akerlund/rtl_common) in turn; and
[`vip_axi4s_agent`](https://github.com/akerlund/vip_axi4s_agent), which both
testbenches drive the FIFO with.

## Running

```sh
cd py
./run_fusesoc.sh --target sim      # cocotb/Verilator: 3 test cases
./run_fusesoc.sh --target lint
fusesoc run --target rtl akerlund::afifo:1.0.0   # lint the RTL alone
```

The three cases cover a balanced crossing, a fast writer into a slow reader
(the FIFO fills and `ing_full` must hold), and a slow writer into a fast reader
(it drains and `egr_empty` must hold) — the two directions being where a
pointer-synchronisation bug shows up.

The SystemVerilog/UVM testbench under [`sv/`](sv/) needs a VCS licence and is
not runnable here.
