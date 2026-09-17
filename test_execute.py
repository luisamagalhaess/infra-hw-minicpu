import unittest

from main import MiniCPU


class ExecuteTests(unittest.TestCase):
    def test_operacoes_e_desvios(self):
        cpu = MiniCPU()
        cpu.execute(("MOV", "R0", 12))
        cpu.execute(("MOV", "R1", 3))
        cpu.execute(("SUB", "R0", "R1"))
        self.assertEqual(cpu.registradores[0], 9)
        cpu.execute(("ADD", "R0", 1))
        self.assertEqual(cpu.registradores[0], 10)

        cpu.execute(("STORE", "R0", 20))
        cpu.execute(("LOAD", "R2", 20))
        self.assertEqual(cpu.registradores[2], 10)

        cpu.execute(("CMP", "R0", "R2"))
        self.assertEqual(cpu.zf, 1)
        cpu.execute(("JNZ", 50))
        self.assertEqual(cpu.pc, 0)
        cpu.execute(("JZ", 5))
        self.assertEqual(cpu.pc, 5)

        cpu.execute(("CMP", "R0", "R1"))
        self.assertEqual(cpu.zf, 0)
        cpu.execute(("JZ", 50))
        self.assertEqual(cpu.pc, 5)
        cpu.execute(("JNZ", 6))
        self.assertEqual(cpu.pc, 6)
        cpu.execute(("JMP", 7))
        self.assertEqual(cpu.pc, 7)

        cpu.execute(("HALT",))
        self.assertFalse(cpu.rodando)
        cpu.execute(("MOV", "R0", 99))
        self.assertEqual(cpu.registradores[0], 10)

    def test_somatorio_de_array(self):
        cpu = MiniCPU()
        cpu.memoria[100:104] = [2, 3, 5, 7]
        programa = [
            ("MOV", "R0", 0),
            ("MOV", "R1", 100),
            ("MOV", "R2", 104),
            ("CMP", "R1", "R2"),
            ("JZ", 9),
            ("LOAD", "R3", "R1"),
            ("ADD", "R0", "R3"),
            ("ADD", "R1", 1),
            ("JMP", 3),
            ("HALT",),
        ]

        for _ in range(100):
            if not cpu.rodando:
                break
            instrucao = programa[cpu.pc]
            cpu.pc += 1  # responsabilidade do Fetch
            cpu.execute(instrucao)

        self.assertFalse(cpu.rodando)
        self.assertEqual(cpu.registradores[0], 17)

    def test_endereco_invalido(self):
        cpu = MiniCPU()
        with self.assertRaises(ValueError):
            cpu.execute(("LOAD", "R0", 256))


if __name__ == "__main__":
    unittest.main()
