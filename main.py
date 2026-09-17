class MiniCPU:
    def __init__(self):

        self.memoria = []

        for i in range(256):
            self.memoria.append(0)

        self.registradores = [0, 0, 0, 0]

        self.pc = 0
        self.zf = 0

        self.rodando = True
        self.ciclo = 0

    def fetch(self):
        opcode = self.memoria[self.pc]
        op1 = self.memoria[self.pc + 1]
        op2 = self.memoria[self.pc + 2]

        self.pc = self.pc + 3

        return opcode, op1, op2