import m5
from m5.objects import *

# High Performance Mode: 200MHz / 1.0V
# DVFS Operating Point 1 from Deliverable 1
# TimingSimpleCPU models in-order single-issue execution

system = System()
system.clk_domain = SrcClockDomain()
system.clk_domain.clock = "200MHz"
system.clk_domain.voltage_domain = VoltageDomain(voltage="1.0V")
system.mem_mode = "timing"
system.mem_ranges = [AddrRange("512MB")]

system.cpu = TimingSimpleCPU()
system.membus = SystemXBar()

# L1 Instruction Cache: 8kB direct-mapped, 32B lines (Deliverable 1 spec)
system.cpu.icache = Cache(
    size="8kB",
    assoc=1,
    tag_latency=1,
    data_latency=1,
    response_latency=1,
    mshrs=4,
    tgts_per_mshr=20
)

# L1 Data Cache: 8kB 2-way, 32B lines (Deliverable 1 spec)
system.cpu.dcache = Cache(
    size="8kB",
    assoc=2,
    tag_latency=1,
    data_latency=1,
    response_latency=1,
    mshrs=4,
    tgts_per_mshr=20
)

# L2 Unified Cache: 128kB 4-way, 8-cycle latency (Deliverable 1 spec)
system.l2cache = Cache(
    size="128kB",
    assoc=4,
    tag_latency=8,
    data_latency=8,
    response_latency=8,
    mshrs=16,
    tgts_per_mshr=20
)

system.l2bus = L2XBar()
system.cpu.icache.cpu_side = system.cpu.icache_port
system.cpu.dcache.cpu_side = system.cpu.dcache_port
system.cpu.icache.mem_side = system.l2bus.cpu_side_ports
system.cpu.dcache.mem_side = system.l2bus.cpu_side_ports
system.l2cache.cpu_side = system.l2bus.mem_side_ports
system.l2cache.mem_side = system.membus.cpu_side_ports

system.cpu.createInterruptController()
system.cpu.interrupts[0].pio = system.membus.mem_side_ports
system.cpu.interrupts[0].int_requestor = system.membus.cpu_side_ports
system.cpu.interrupts[0].int_responder = system.membus.mem_side_ports

system.mem_ctrl = MemCtrl()
system.mem_ctrl.dram = DDR3_1600_8x8()
system.mem_ctrl.dram.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.mem_side_ports

system.workload = SEWorkload.init_compatible("benchmarks/control_loop")
process = Process()
process.cmd = ["benchmarks/control_loop"]
system.cpu.workload = process
system.cpu.createThreads()

root = Root(full_system=False, system=system)
m5.instantiate()

print("Beginning simulation: High Performance Mode (200MHz / 1.0V)")
exit_event = m5.simulate()
print("Exiting @ tick {} because {}".format(m5.curTick(), exit_event.getCause()))