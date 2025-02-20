import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer

@cocotb.test()
async def processor_test(dut):
    """Testbench for the processor module."""
    
    # Create a clock with a period of 10 ns (100 MHz)
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())


    dut.enable.value = 1
    # Apply reset
    dut.rst.value = 0
    await cocotb.triggers.Timer(1, units="ns")  # Hold reset for a few ns
    cocotb.log.info(f"rst asserted, PCin Value = {int(dut.pc.PCin.value)}")
    cocotb.log.info(f"rst asserted, PCout Value = {int(dut.pc.PCout.value)}")
    await cocotb.triggers.Timer(3, units="ns")  # Hold reset for a few ns

    dut.rst.value = 1
    
    # Run simulation for 1000 ns
    await RisingEdge(dut.clk)
    await Timer(1, units="ns")

    for cycle in range(100):
        await RisingEdge(dut.clk)
        await Timer(1, units="ns")
        cocotb.log.info(f"Cycle {cycle}: PC = {int(dut.PC.value)}")
        cocotb.log.info(f"Instruction 1 = {hex(dut.instMem.q_a.value)} \n")
        cocotb.log.info(f"Instruction 2 = {hex(dut.instMem.q_b.value)} \n") 