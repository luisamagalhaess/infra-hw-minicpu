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
        """Converte R0..R3 em índices e rejeita registradores inexistentes."""
        if not isinstance(nome, str) or nome.upper() not in ("R0", "R1", "R2", "R3"):
            raise ValueError(f"Registrador inválido: {nome!r}")
        return int(nome[1])

    def _valor(self, operando):
        """Lê um registrador (R0..R3) ou um valor imediato inteiro."""
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
        """Executa uma instrução decodificada como (opcode, operando, ...).

        O Fetch é responsável por avançar o PC nas instruções comuns. Apenas
        JMP, JZ e JNZ alteram o PC aqui.
        """
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
            self.registradores[destino] += self._valor(args[1])
        elif opcode == "SUB":
            destino = self._indice_registrador(args[0])
            self.registradores[destino] -= self._valor(args[1])
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
