"""CPU functionality."""


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # This emulates having 256 individual bytes
        # Being utilized as RAM
        self.ram = [0, 0, 0, 0, 0, 0, 0, 0] * 256
        # 8 general-purpose 8-bit numeric registers R0-R7.
        # * R5 is reserved as the interrupt mask (IM)
        # * R6 is reserved as the interrupt status (IS)
        # * R7 is reserved as the stack pointer (SP)
        self.reg = [0] * 8
        # Memory Address Register
        # Current address being read or written to
        self.mar = None
        # Memory Data Register
        # Data from current read or write register
        self.mdr = None
        # Program Counter
        self.pc = 0
        self.ir = 0

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010,  # LDI R0,8
            0b00000000,  # REGISTER ADDRESS
            0b00001000,  # VALUE
            0b01000111,  # PRN R0
            0b00000000,  # REGISTER ADDRESS
            0b00000001,  # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            # print(f"ADD: %02X | DATA: %02X | " % (address, instruction), end='')
            # print("BIN: ", bin(instruction))
            # print()
            address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def ram_read(self, address: int):
        self.mar = address
        self.mdr = self.ram[address]
        # print(f"MAR: %02X | MDR: %02X" % (self.mar, self.mdr), end='')
        # print()
        return self.ram[address]

    def ram_write(self, address: int, value):
        self.mar = address
        self.mdr = value
        self.ram[address] = value

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def ldi(self):
        op_a = self.ram[self.pc + 1]
        op_b = self.ram[self.pc + 2]
        self.reg[op_a] = op_b
        return f"LDI | ADDRESS: %02X | INST : %02X |" % (op_a, op_b)

    def prn(self):
        op_a = self.ram[self.ir + 1]
        print(f"PRN | ADDRESS: %02X | INST : %02X |" % (op_a, self.reg[op_a]))
        return self.reg[op_a]

    def op_switch(self, code: str):
        switcher = {
            "0b10000010": self.ldi,
            "0b1000111": self.prn,
        }
        func = switcher.get(code, lambda: "")
        print(func())

    def run(self):
        """Run the CPU."""
        print("---RUNNING---")
        self.ir = 0
        # Temporarily checking for ir+3 to avoid iob errors
        while self.ir + 3 < len(self.ram):
            ir = self.ram[self.ir]
            if bin(ir) == "0b1":
                print("PROGRAM TERMINATING")
                break
            else:
                self.op_switch(bin(ir))
            self.ir += 1


if __name__ == "__main__":
    cpu = CPU()

    cpu.load()
    # cpu.trace()
    cpu.run()
