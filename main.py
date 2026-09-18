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

    def _indice_registrador(self, nome):

        if not isinstance(nome, str) or nome.upper() not in ("R0", "R1", "R2", "R3"):
            raise ValueError(f"Registrador inválido: {nome!r}")
        return int(nome[1])

    def _valor(self, operando):

        if isinstance(operando, str):
            return self.registradores[self._indice_registrador(operando)]
        if type(operando) is not int:
            raise ValueError(f"Operando inválido: {operando!r}")
        return operando

    def _endereco(self, operando):
        endereco = self._valor(operando)
        if not 0 <= endereco < len(self.memoria):
            raise ValueError(f"Endereço de memória inválido: {endereco}")
        return endereco

    def execute(self, instrucao):

        if not self.rodando:
            return
        if not isinstance(instrucao, (tuple, list)) or not instrucao:
            raise ValueError("Instrução deve ser uma tupla/lista não vazia")

        opcode, *args = instrucao
        if not isinstance(opcode, str):
            raise ValueError(f"Opcode inválido: {opcode!r}")
        opcode = opcode.upper()
        quantidade = {
            "LOAD": 2, "STORE": 2, "ADD": 2, "SUB": 2,
            "MOV": 2, "CMP": 2, "JMP": 1, "JZ": 1,
            "JNZ": 1, "HALT": 0,
        }
        if opcode not in quantidade:
            raise ValueError(f"Opcode desconhecido: {opcode}")
        if len(args) != quantidade[opcode]:
            raise ValueError(f"{opcode} espera {quantidade[opcode]} operando(s)")

        if opcode == "LOAD":
            destino = self._indice_registrador(args[0])
            self.registradores[destino] = self.memoria[self._endereco(args[1])]
        elif opcode == "STORE":
            origem = self._indice_registrador(args[0])
            self.memoria[self._endereco(args[1])] = self.registradores[origem]
        elif opcode == "ADD":
            destino = self._indice_registrador(args[0])
            self.registradores[destino] = (self.registradores[destino] + self._valor(args[1])) & 0xFF
        elif opcode == "SUB":
            destino = self._indice_registrador(args[0])
            self.registradores[destino] = (self.registradores[destino] - self._valor(args[1])) & 0xFF
        elif opcode == "MOV":
            destino = self._indice_registrador(args[0])
            self.registradores[destino] = self._valor(args[1])
        elif opcode == "CMP":
            self.zf = int(self._valor(args[0]) == self._valor(args[1]))
        elif opcode == "JMP":
            self.pc = self._valor(args[0])
        elif opcode == "JZ":
            if self.zf == 1:
                self.pc = self._valor(args[0])
        elif opcode == "JNZ":
            if self.zf == 0:
                self.pc = self._valor(args[0])
        elif opcode == "HALT":
            self.rodando = False
        
    def decode(self, opcode, operando1, operando2):
        if opcode == 0x01:
            return "LOAD", f"R{operando1}", operando2

        elif opcode == 0x02:
            return "STORE", f"R{operando1}", operando2

        elif opcode == 0x03:
            return "ADD", f"R{operando1}", f"R{operando2}"

        elif opcode == 0x04:
            return "SUB", f"R{operando1}", f"R{operando2}"

        elif opcode == 0x05:
            return "MOV", f"R{operando1}", operando2

        elif opcode == 0x06:
            return "CMP", f"R{operando1}", f"R{operando2}"

        elif opcode == 0x07:
            return "JMP", operando1

        elif opcode == 0x08:
            return "JZ", operando1

        elif opcode == 0x09:
            return "JNZ", operando1

        elif opcode == 0x0A:
            return "HALT",

        else:
            return "INVALIDA",
        
    def trace(self, instrucao):
        print(
            f"Ciclo {self.ciclo}: {instrucao} | "
            f"R0={self.registradores[0]} "
            f"R1={self.registradores[1]} "
            f"R2={self.registradores[2]} "
            f"R3={self.registradores[3]} | "
            f"PC={self.pc} ZF={self.zf}"
        )
        
    def carregar_programa(self):
        valores = [3, 7, 2, 5, 1, 8, 4, 6]

        for i in range(8):
            self.memoria[0x10 + i] = valores[i]

        programa = [
            0x05, 0x00, 0x00,

            0x01, 0x01, 0x10,
            0x03, 0x00, 0x01,

            0x01, 0x01, 0x11,
            0x03, 0x00, 0x01,

            0x01, 0x01, 0x12,
            0x03, 0x00, 0x01,

            0x01, 0x01, 0x13,
            0x03, 0x00, 0x01,

            0x01, 0x01, 0x14,
            0x03, 0x00, 0x01,

            0x01, 0x01, 0x15,
            0x03, 0x00, 0x01,

            0x01, 0x01, 0x16,
            0x03, 0x00, 0x01,

            0x01, 0x01, 0x17,
            0x03, 0x00, 0x01,

            0x02, 0x00, 0x20,
            0x0A, 0x00, 0x00
        ]

        inicio = 0x30

        for i in range(len(programa)):
            self.memoria[inicio + i] = programa[i]

        self.pc = inicio

    def fetch(self):
        opcode = self.memoria[self.pc]
        op1 = self.memoria[self.pc + 1]
        op2 = self.memoria[self.pc + 2]

        self.pc = self.pc + 3

        return opcode, op1, op2

    def run(self):
        while self.rodando and self.pc < 256:
            self.ciclo += 1

            opcode, op1, op2 = self.fetch()

            instrucao = self.decode(opcode, op1, op2)

            self.execute(instrucao)

            self.trace(instrucao)


if __name__ == "__main__":
    cpu = MiniCPU()

    cpu.carregar_programa()

    cpu.run()

    print("\nResultado final:", cpu.memoria[0x20])