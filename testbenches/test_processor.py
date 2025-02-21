import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer


def to_int(array):
    return [int(x) for x in array]

def decode_instruction(instruction):
    opcode = (instruction >> 26) & 0x3F
    rs = (instruction >> 21) & 0x1F
    rt = (instruction >> 16) & 0x1F
    rd = (instruction >> 11) & 0x1F
    shamt = (instruction >> 6) & 0x1F
    funct = instruction & 0x3F
    imm = instruction & 0xFFFF
    address = instruction & 0x3FFFFFF

    opcodes = {
        0x08: "addi", 0x23: "lw", 0x2B: "sw", 0x04: "beq", 0x05: "bne",
        0x03: "jal", 0x0D: "ori", 0x16: "xori", 0x0C: "andi", 0x0A: "slti",
        0x02: "j"
    }

    functs = {
        0x20: "add", 0x22: "sub", 0x24: "and", 0x25: "or", 0x2A: "slt",
        0x14: "sgt", 0x00: "sll", 0x02: "srl", 0x27: "nor", 0x15: "xor",
        0x08: "jr"
    }

    if opcode == 0:  # R-Type instruction
        if funct in functs:
            if funct in {0x00, 0x02}:  # Shift instructions
                return f"{functs[funct]} ${rd}, ${rt}, {shamt}"
            elif funct == 0x08:  # JR instruction
                return f"{functs[funct]} ${rs}"
            else:
                return f"{functs[funct]} ${rd}, ${rs}, ${rt}"
        else:
            return "Unknown R-Type instruction"
    elif opcode in opcodes:
        if opcode in {0x04, 0x05}:  # Branch instructions
            return f"{opcodes[opcode]} ${rs}, ${rt}, {imm}"
        elif opcode in {0x02, 0x03}:  # Jump instructions
            return f"{opcodes[opcode]} {hex(address)}"
        elif opcode in {0x23, 0x2B}:  # Load/store instructions
            return f"{opcodes[opcode]} ${rt}, {imm}(${rs})"
        else:  # Immediate-type instructions
            return f"{opcodes[opcode]} ${rt}, ${rs}, {imm}"
    else:
        return "Unknown instruction"

@cocotb.test()
async def processor_test(dut):
    """Testbench for the processor module."""
    
    # Create a clock with a period of 10 ns (100 MHz)
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())

    dut.enable.value = 1
    # Apply reset
    dut.rst.value = 0
    await Timer(1, units="ns")  # Hold reset for a few ns
    cocotb.log.info(f"rst asserted, PCin Value = {int(dut.pc.PCin.value)}")
    cocotb.log.info(f"rst asserted, PCout Value = {int(dut.pc.PCout.value)}")
    await Timer(3, units="ns")  # Hold reset for a few ns

    dut.rst.value = 1
    
    # Run simulation for 1000 ns
    await RisingEdge(dut.clk)
    await Timer(1, units="ns")

    for cycle in range(200):
        await RisingEdge(dut.clk)
        await Timer(1, units="ns")
        cocotb.log.info(f"Cycle {cycle}: PC = {int(dut.PC.value)}")
        instr1 = dut.instMem.q_a.value.integer
        instr2 = dut.instMem.q_b.value.integer
        cocotb.log.info(f"Instruction 1 = {hex(instr1)} ({decode_instruction(instr1)})")
        cocotb.log.info(f"Instruction 2 = {hex(instr2)} ({decode_instruction(instr2)})")

        # Print registers in a single line
        registers = to_int(dut.RegFile.registers.value)
        register_values = " | ".join(f"R{i}: {reg}" for i, reg in enumerate(registers))
        cocotb.log.info(f"Register File: {register_values}")

        # Print first 20 memory values
        dm_values = to_int(dut.DM.altsyncram_component.m_default.altsyncram_inst.mem_data.value[0:20])
        cocotb.log.info(f"DM: {dm_values}\n")
