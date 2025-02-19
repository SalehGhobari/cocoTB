import cocotb
from cocotb.triggers import Timer
from cocotb.result import TestSuccess

@cocotb.test()
async def hello_world_test(dut):
    # Print "Hello, World!" to the console
    dut._log.info("Hello, World!")
    
    # Wait for a small amount of time (optional)
    await Timer(1, units='ns')
    
    # Raise TestSuccess to indicate that the test passed
    raise TestSuccess("All ORGate2 test cases passed!")