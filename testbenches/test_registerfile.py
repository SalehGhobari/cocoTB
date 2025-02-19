import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, Timer
from cocotb.result import TestSuccess
import random

@cocotb.test()
async def test_register_file(dut):
    """Testbench for registerFile module with negative edge triggered writes."""

    # Start a clock
    clock = Clock(dut.clk, 10, units="ns")  # 10 ns clock period
    cocotb.start_soon(clock.start())

    # Helper function to reset the register file
    async def reset_register_file():
        dut.rst.value = 0  # Active low reset
        await FallingEdge(dut.clk)  # Wait for one clock cycle
        dut.rst.value = 1  # Deactivate reset
        await RisingEdge(dut.clk)

    # Initialize signals
    dut.we1.value = 0
    dut.we2.value = 0
    dut.readRegister1.value = 0
    dut.readRegister2.value = 0
    dut.readRegister3.value = 0
    dut.readRegister4.value = 0
    dut.writeRegister1.value = 0
    dut.writeRegister2.value = 0
    dut.writeData1.value = 0
    dut.writeData2.value = 0
    await reset_register_file()  # Reset the register file

    # Test 1: Check reset behavior
    assert dut.readData1.value == 0, f"Reset failed: readData1 expected 0, got {dut.readData1.value}"
    assert dut.readData2.value == 0, f"Reset failed: readData2 expected 0, got {dut.readData2.value}"
    assert dut.readData3.value == 0, f"Reset failed: readData3 expected 0, got {dut.readData3.value}"
    assert dut.readData4.value == 0, f"Reset failed: readData4 expected 0, got {dut.readData4.value}"

    # Test 2: Write to a single register and read back
    dut.we1.value = 1
    dut.writeRegister1.value = 5  # Write to register 5
    dut.writeData1.value = 0xDEADBEEF
    await FallingEdge(dut.clk)  # Wait for the falling edge to trigger the write
    dut.we1.value = 0
    dut.readRegister1.value = 5  # Read from register 5
    await Timer(1, units="ns")  # Wait for signals to propagate
    assert dut.readData1.value == 0xDEADBEEF, f"Write/Read failed: expected 0xDEADBEEF, got {dut.readData1.value}"

    # Test 3: Write to two different registers simultaneously
    dut.we1.value = 1
    dut.we2.value = 1
    dut.writeRegister1.value = 10  # Write to register 10
    dut.writeData1.value = 0xCAFEBABE
    dut.writeRegister2.value = 15  # Write to register 15
    dut.writeData2.value = 0x12345678
    await FallingEdge(dut.clk)  # Wait for the falling edge to trigger the writes
    dut.we1.value = 0
    dut.we2.value = 0
    dut.readRegister1.value = 10  # Read from register 10
    dut.readRegister2.value = 15  # Read from register 15
    await Timer(1, units="ns")  # Wait for signals to propagate
    assert dut.readData1.value == 0xCAFEBABE, f"Write/Read failed: expected 0xCAFEBABE, got {dut.readData1.value}"
    assert dut.readData2.value == 0x12345678, f"Write/Read failed: expected 0x12345678, got {dut.readData2.value}"

    # Test 4: Write to the same register simultaneously (priority test)
    dut.we1.value = 1
    dut.we2.value = 1
    dut.writeRegister1.value = 20  # Write to register 20
    dut.writeData1.value = 0x11111111
    dut.writeRegister2.value = 20  # Write to the same register 20
    dut.writeData2.value = 0x22222222
    await FallingEdge(dut.clk)  # Wait for the falling edge to trigger the writes
    dut.we1.value = 0
    dut.we2.value = 0
    dut.readRegister1.value = 20  # Read from register 20
    await Timer(1, units="ns")  # Wait for signals to propagate
    assert dut.readData1.value == 0x11111111, f"Write priority failed: expected 0x11111111, got {dut.readData1.value}"

    # Test 5: Write to register 0 (should not write)
    dut.we1.value = 1
    dut.writeRegister1.value = 0  # Attempt to write to register 0
    dut.writeData1.value = 0xDEADBEEF
    await FallingEdge(dut.clk)  # Wait for the falling edge to trigger the write
    dut.we1.value = 0
    dut.readRegister1.value = 0  # Read from register 0
    await Timer(1, units="ns")  # Wait for signals to propagate
    assert dut.readData1.value == 0, f"Write to register 0 failed: expected 0, got {dut.readData1.value}"

    # Test 6: Random read/write operations
    for _ in range(100000):  # Test 10 random cases
        reg1 = random.randint(1, 31)  # Random register (1 to 31)
        reg2 = random.randint(1, 31)  # Random register (1 to 31)
        data1 = random.randint(0, 2**32 - 1)  # Random 32-bit data
        data2 = random.randint(0, 2**32 - 1)  # Random 32-bit data

        # Write to two registers
        dut.we1.value = 1
        dut.we2.value = 1
        dut.writeRegister1.value = reg1
        dut.writeData1.value = data1
        dut.writeRegister2.value = reg2
        dut.writeData2.value = data2
        await FallingEdge(dut.clk)  # Wait for the falling edge to trigger the writes
        dut.we1.value = 0
        dut.we2.value = 0

        # Read back from the same registers
        dut.readRegister1.value = reg1
        dut.readRegister2.value = reg2
        await Timer(1, units="ns")  # Wait for signals to propagate
        assert dut.readData1.value == data1, f"Random write/read failed: expected {data1}, got {dut.readData1.value}"
        assert dut.readData2.value == data2, f"Random write/read failed: expected {data2}, got {dut.readData2.value}"

    # If all assertions pass, the test is successful
    raise TestSuccess("All registerFile test cases passed!")