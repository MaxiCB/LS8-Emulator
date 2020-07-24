"""CPU functionality."""
import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # This emulates having 256 individual bytes
        # Being utilized as RAM
        self.ram = [0] * 256
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
        # Flag Register
        self.fl = [0, 0, 0, 0, 0, 0, 0, 0]
        # Instruction Iteration Pointer
        self.iter = 0
        # Stack Pointer
        self.sp = 255
        # CALL Instruction Pointer
        self.call_cache = 0

    def load(self, load_file: str = "print8"):
        """Load a program into memory."""

        parsed = []
        f = open('examples/' + load_file + '.ls8', 'r')
        f1 = f.readlines()
        for f in f1:
            if f[0] != "#" and not f.isspace():
                test = f.split(' ', 1)[0]
                parsed.append(int(test, 2))

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

        for instruction in parsed:
            self.ram[address] = instruction
            # print(f"ADD: %02X | DATA: %02X | " % (address, instruction), end='')
            # print("BIN: ", bin(instruction))
            address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        # AND
        # OR
        # XOR
        # NOT
        # SHL
        # SHR
        # MOD

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        if op == "AND":
            self.reg[reg_a] = self.reg[reg_a] & self.reg[reg_b]
        if op == "OR":
            self.reg[reg_a] = self.reg[reg_a] | self.reg[reg_b]
        if op == "XOR":
            self.reg[reg_a] = self.reg[reg_a] ^ self.reg[reg_b]
        if op == "NOT":
            self.reg[reg_a] = ~self.reg[reg_a]
        if op == "SHL":
            self.reg[reg_a] = self.reg[reg_a] << self.reg[reg_b]
        if op == "SHR":
            self.reg[reg_a] = ~self.reg[reg_a] >> self.reg[reg_b]
        if op == "MOD":
            self.reg[reg_a] = self.reg[reg_a] % self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def ram_read(self, address: int):
        self.mar = address
        self.mdr = self.ram[address]
        # print(f"MAR: %02X | MDR: %02X" % (self.mar, self.mdr), end='')
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
        # LDI requires next 2 address's
        op_a = self.ram[self.ir + 1]
        op_b = self.ram[self.ir + 2]
        self.reg[op_a] = op_b
        self.iter = 3
        return f"LDI | ADDRESS: %02X | INST: %02X |" % (op_a, op_b)

    def prn(self):
        # PRN requires next address
        self.iter = 2
        op_a = self.ram[self.ir + 1]
        print(self.reg[op_a])
        return f"PRN | ADDRESS: %02X | INST: %02X |" % (op_a, self.reg[op_a])

    def mul(self):
        # MUL requires next 2 address's
        self.iter = 3
        op_a = self.reg[self.ram[self.ir + 1]]
        op_b = self.reg[self.ram[self.ir + 2]]
        self.reg[self.ram[self.ir + 1]] = op_a * op_b
        return f"MUL | ADDRESS: %02X | INST: %02X |" % (self.ram[self.ir + 1], self.reg[self.ram[self.ir + 1]])

    def add(self):
        # ADD requires the next 2 address's
        self.iter = 3
        op_a = self.reg[self.ram[self.ir + 1]]
        op_b = self.reg[self.ram[self.ir + 2]]
        self.reg[self.ram[self.ir + 1]] = op_a + op_b
        return f"ADD | ADDRESS: %02X | INST: %02X |" % (self.ram[self.ir + 1], op_a + op_b)

    def histo(self):
        out = "*"
        for star in range(0, 6):
            print(out)
            out = out * 2

    def push(self):
        # PUSH requires next address
        self.iter = 2
        op_a = self.reg[self.ram[self.ir + 1]]
        self.ram[self.sp] = op_a
        self.sp -= 1
        return f"PUSH | ADDRESS: %02X | INST: %02X |" % (self.sp, op_a)

    def pop(self):
        # POP requires next address
        self.iter = 2
        self.reg[self.ram[self.ir + 1]] = self.ram[self.sp + 1]
        self.sp += 1
        return f"POP | ADDRESS: %02X | INST: %02X |" % (self.sp, self.ram[self.sp])

    def call(self):
        self.iter = 2
        self.call_cache = self.ir + 1
        op_a = self.reg[self.ram[self.ir + 1]]
        self.ir = op_a - 1
        return f"CALL | ADDRESS: %02X | INST: %02X |" % (self.ram[self.ir + 1], self.ram[0])

    def ret(self):
        self.ir = self.call_cache
        return f"RET | ADDRESS: %02X | INST: %02X |" % (self.ram[self.ir + 1], self.ir)

    def cmp(self):
        # Compare the values on two registers
        # Uses the next two address's
        self.iter = 3
        eq, les, grt = 0, 0, 0
        op_a = self.reg[self.ram[self.ir + 1]]
        op_b = self.reg[self.ram[self.ir + 2]]
        if op_a == op_b:
            eq = 1
        if op_a < op_b:
            les = 1
        if op_a > op_b:
            grt = 1
        self.fl = [0, 0, 0, 0, 0, les, grt, eq]
        return f"CMP | OP_A: %02X | OP_B: %02X |" % (self.reg[self.ram[self.ir + 1]], self.reg[self.ram[self.ir + 2]])

    def jmp(self):
        self.iter = 2
        op_a = self.reg[self.ram[self.ir + 1]]
        self.ir = op_a - 1
        return f"JMP | ADDRESS: %02X | " % (self.reg[self.ram[self.ir + 1]])

    def jeq(self):
        op_a = self.reg[self.ram[self.ir + 1]]
        if self.fl == [0, 0, 0, 0, 0, 0, 0, 1]:
            self.ir = op_a - 1
        return f"JEQ | ADDRESS: %02X | " % op_a

    def jne(self):
        op_a = self.reg[self.ram[self.ir + 1]]
        if self.fl == [0, 0, 0, 0, 0, 1, 0, 0]:
            self.ir = op_a - 1
        return f"JNE | ADDRESS: %02X | " % op_a

    def st(self):
        self.iter = 2
        op_a = self.reg[self.ram[self.ir + 1]]
        op_b = self.reg[self.ram[self.ir + 2]]
        self.reg[op_a] = op_b
        return f"ST | ADDRESS: %02X | INST: %02X |" % (op_a, op_b)

    def op_switch(self, code: str):
        switcher = {
            "0b10000010": self.ldi,
            "0b1000111": self.prn,
            "0b10100010": self.mul,
            "0b10100000": self.add,
            "0b1000101": self.push,
            "0b1000110": self.pop,
            "0b1010000": self.call,
            "0b10001": self.ret,
            "0b10100111": self.cmp,
            "0b1010100": self.jmp,
            "0b1010101": self.jeq,
            "0b1010110": self.jne,
            "0b10000100": self.st,
            "0b11111111": self.histo,
        }
        func = switcher.get(code, lambda: "")
        func()
        # print(func())

    def run(self):
        """Run the CPU."""
        print("---RUNNING---")
        while self.ir < len(self.ram):
            ir = self.ram[self.ir]
            if bin(ir) == "0b1" and self.iter <= 0:
                print("PROGRAM TERMINATING")
                break
            else:
                self.op_switch(bin(ir))
                self.iter -= 1
            self.ir += 1


if __name__ == "__main__":
    file = input('File name: ')
    cpu = CPU()
    cpu.load(file)
    cpu.run()
