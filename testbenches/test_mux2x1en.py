import cocotb
from cocotb.triggers import Timer
import random

@cocotb.test()
async def test_mux2x1En(dut):
    """Test the 2x1 multiplexer with enable."""
    
    # Test with multiple random values
    prev_out = 0  # Store previous output value
    for _ in range(10):
        in1 = random.randint(0, 2**32 - 1)  # Random 32-bit value
        in2 = random.randint(0, 2**32 - 1)  # Random 32-bit value
        s = random.randint(0, 1)  # Random selection bit
        en = random.randint(0, 1)  # Enable signal
        
        # Apply inputs to DUT
        dut.in1.value = in1
        dut.in2.value = in2
        dut.s.value = s
        dut.en.value = en
        
        await Timer(2, units="ns")  # Wait for a short time for propagation
        
        # Check output
        if en:
            expected_out = in2 if s else in1
        else:
            expected_out = prev_out  # Output should hold its previous value if en is 0
        
        assert dut.out.value == expected_out, f"Mismatch: s={s}, en={en}, in1={in1}, in2={in2}, expected={expected_out}, got={dut.out.value}"
        prev_out = dut.out.value  # Update previous output
    
    cocotb.log.info("MUX 2x1 with Enable test completed successfully.")
