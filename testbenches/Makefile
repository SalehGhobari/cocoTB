# Define the simulator (ModelSim for Windows)
SIM = modelsim  # Use ModelSim's 'vsim' for simulation

# Define the top-level language
TOPLEVEL_LANG = verilog

# Path to all Verilog source files (wildcard to include all .v files in the directory)
VERILOG_SOURCES += $(wildcard ../SuperScalar/*.v)

# Specify the top-level module (must match the testbench)
TOPLEVEL = signextender

# The Python file containing Cocotb testbenches
MODULE = test_signextender

# Enable waveform dump for debugging
export WAVES=1

# Simulation arguments
SIM_ARGS += -voptargs=+acc
SIM_ARGS += -L work
SIM_ARGS += -L lpm_ver
SIM_ARGS += -L altera_mf_ver

# Path to Quartus libraries (change version if needed)


# Include the default Cocotb makefile
include $(shell cocotb-config --makefiles)/Makefile.sim

