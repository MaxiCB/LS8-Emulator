"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # This emaulates having 256 individual bits
        # Being utilized as RAM
        self.ram = [0] * 256
        # 8 general-purpose 8-bit numeric registers R0-R7.

        # * R5 is reserved as the interrupt mask (IM)
        # * R6 is reserved as the interrupt status (IS)
        # * R7 is reserved as the stack pointer (SP)
        self.reg = [0] * 8
        # Program Counter
        self.pc = 0

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def ram_read(self, address: int):
        print("Reading RAM")
        return self.ram[address]

    def ram_write(self, address: int, value):
        print("Writing RAM")
        self.ram[address] = value

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        self.trace()

if __name__ == "__main__":
    cpu = CPU()

    cpu.run()
