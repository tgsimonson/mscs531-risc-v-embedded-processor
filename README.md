# MSCS 531 — Low-Power RISC-V Microprocessor: gem5 Implementation

**Course:** MSCS 531: Computer Architecture and Design  
**Author:** Todd Simonson  
**Institution:** University of the Cumberlands  
**Project:** Residency Project — Designing and Implementing a Microprocessor Using gem5

## Overview

This repository contains the gem5 simulation implementation for a low-power RISC-V microprocessor targeting real-time embedded control applications. The processor is designed around the RISC-V RV32I + M + Zicsr ISA with a five-stage in-order pipeline and a two-level cache hierarchy. Three DVFS operating points are simulated to quantify the energy-performance trade-off across workload conditions.

## Processor Architecture Summary

| Parameter | Specification |
|---|---|
| ISA | RISC-V RV32I + M + Zicsr |
| Pipeline | 5-stage in-order |
| L1 I-Cache | 8kB, direct-mapped, 32B lines |
| L1 D-Cache | 8kB, 2-way, 32B lines |
| L2 Unified | 128kB, 4-way, 8-cycle latency |
| DVFS Point 1 | 200 MHz / 1.0V (high performance) |
| DVFS Point 2 | 100 MHz / 0.9V (balanced) |
| DVFS Point 3 | 50 MHz / 0.8V (low power) |
| Target application | Real-time embedded control (PLC, automotive) |

## Repository Structure

```
mscs531-risc-v-embedded-processor/
├── benchmarks/
│   ├── control_loop.c      # PID control loop benchmark source
│   └── control_loop        # Compiled binary (x86)
├── configs/
│   ├── high_perf.py        # 200MHz / 1.0V DVFS operating point
│   ├── balanced.py         # 100MHz / 0.9V DVFS operating point
│   └── low_power.py        # 50MHz / 0.8V DVFS operating point
├── results/
│   ├── high_perf/stats.txt
│   ├── balanced/stats.txt
│   └── low_power/stats.txt
├── .gitignore
└── README.md
```

## Requirements

- gem5 version 25.1.0.0 built for X86
- GCC (for compiling the benchmark)
- Python 3

## Setup

**1. Build gem5 for X86** (if not already built):
```bash
cd ~/gem5
scons build/X86/gem5.opt -j4
```

**2. Clone this repository:**
```bash
git clone https://github.com/tgsimonson/mscs531-risc-v-embedded-processor.git
cd mscs531-risc-v-embedded-processor
```

**3. Compile the benchmark:**
```bash
gcc -O0 benchmarks/control_loop.c -o benchmarks/control_loop
```

**4. Verify native execution:**
```bash
./benchmarks/control_loop
# Expected: Control loop complete. Final actuator output: 401
```

## Running Simulations

```bash
~/gem5/build/X86/gem5.opt --outdir=results/high_perf configs/high_perf.py
~/gem5/build/X86/gem5.opt --outdir=results/balanced configs/balanced.py
~/gem5/build/X86/gem5.opt --outdir=results/low_power configs/low_power.py
```

## Results Summary

| Configuration | Clock | Voltage | Sim Ticks | IPC | Relative Time |
|---|---|---|---|---|---|
| High Performance | 200 MHz | 1.0V | 1,830,760,000 | 0.3867 | 1.0x |
| Balanced | 100 MHz | 0.9V | 3,540,900,000 | 0.3999 | 1.93x |
| Low Power | 50 MHz | 0.8V | 6,951,680,000 | 0.3999 | 3.80x |

Reducing from 200 MHz / 1.0V to 50 MHz / 0.8V reduces dynamic power by approximately 84% at the cost of 3.80x longer execution time.

## Extracting Statistics

```bash
grep -E "simInsts|simTicks|ipc|cpi" results/high_perf/stats.txt | head -6
```

## Troubleshooting Notes

- **MinorCPU not available:** The MinorCPU model is not compiled into the X86 gem5 binary by default. TimingSimpleCPU is used as a functionally equivalent in-order substitute.
- **DRAM capacity warning:** Expected in SE mode. Does not affect results.
- **Cache size warnings:** gem5 casts base-10 sizes to base-2 equivalents. 8kB becomes 8KiB, 128kB becomes 128KiB. No impact on simulation accuracy.
