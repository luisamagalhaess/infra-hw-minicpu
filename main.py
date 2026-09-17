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

    def _indice_registrador(self, indice):
        """Na ISA, R0..R3 são representados pelos inteiros 0..3."""
        if type(indice) is not int or not 0 <= indice < len(self.registradores):
            raise ValueError(f"Registrador inválido: {indice!r}")
        return indice

    def _byte(self, valor):
        if type(valor) is not int or not 0 <= valor <= 0xFF:
            raise ValueError(f"Valor fora do intervalo 0..255: {valor!r}")
        return valor

    def execute(self, instrucao):
        """Executa (mnemônico, operando1, operando2) retornado pelo Decode.

        Cada instrução ocupa três bytes; operandos não usados valem zero.
        O Fetch avança o PC em 3 antes desta chamada. Só os saltos tomados
        alteram o PC aqui.
        """
        if not self.rodando:
            return
        if not isinstance(instrucao, (tuple, list)) or len(instrucao) != 3:
            raise ValueError("Instrução deve conter mnemônico e dois operandos")

        opcode, a, b = instrucao

        if opcode == "LOAD":
            self.registradores[self._indice_registrador(a)] = self.memoria[self._byte(b)]
        elif opcode == "STORE":
            self.memoria[self._byte(b)] = self.registradores[self._indice_registrador(a)]
        elif opcode == "ADD":
            destino = self._indice_registrador(a)
            origem = self._indice_registrador(b)
            self.registradores[destino] = (
                self.registradores[destino] + self.registradores[origem]
            ) & 0xFF
        elif opcode == "SUB":
            destino = self._indice_registrador(a)
            origem = self._indice_registrador(b)
            self.registradores[destino] = (
                self.registradores[destino] - self.registradores[origem]
            ) & 0xFF
        elif opcode == "MOV":
            self.registradores[self._indice_registrador(a)] = self._byte(b)
        elif opcode == "CMP":
            self.zf = int(
                self.registradores[self._indice_registrador(a)]
                == self.registradores[self._indice_registrador(b)]
            )
        elif opcode == "JMP":
            self.pc = self._byte(a)
        elif opcode == "JZ":
            destino = self._byte(a)
            if self.zf == 1:
                self.pc = destino
        elif opcode == "JNZ":
            destino = self._byte(a)
            if self.zf == 0:
                self.pc = destino
        elif opcode == "HALT":
            self.rodando = False
        else:
            raise ValueError(f"Instrução desconhecida: {opcode!r}")
        
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
