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
        
    def decode(self, opcode, operando1, operando2):
        if opcode == 0x01:
            instrucao = "LOAD"

        elif opcode == 0x02:
            instrucao = "STORE"

        elif opcode == 0x03:
            instrucao = "ADD"

        elif opcode == 0x04:
            instrucao = "SUB"

        elif opcode == 0x05:
            instrucao = "MOV"

        elif opcode == 0x06:
            instrucao = "CMP"

        elif opcode == 0x07:
            instrucao = "JMP"

        elif opcode == 0x08:
            instrucao = "JZ"

        elif opcode == 0x09:
            instrucao = "JNZ"

        elif opcode == 0x0A:
            instrucao = "HALT"

        else:
            instrucao = "INVALIDA"

        return instrucao, operando1, operando2