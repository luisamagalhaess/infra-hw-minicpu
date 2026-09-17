import unittest

from main import MiniCPU


class ExecuteTests(unittest.TestCase):
    def test_decode_e_execute_usam_indices_numericos(self):
        cpu = MiniCPU()
        cpu.execute(cpu.decode(0x05, 0, 12))  # MOV R0, 12
        cpu.execute(cpu.decode(0x05, 1, 3))   # MOV R1, 3
        cpu.execute(cpu.decode(0x04, 0, 1))   # SUB R0, R1
        self.assertEqual(cpu.registradores[0], 9)

        cpu.execute(cpu.decode(0x03, 0, 1))   # ADD R0, R1
        self.assertEqual(cpu.registradores[0], 12)
        cpu.execute(cpu.decode(0x02, 0, 0x20))  # STORE R0, 0x20
        cpu.execute(cpu.decode(0x01, 2, 0x20))  # LOAD R2, 0x20
        self.assertEqual(cpu.memoria[0x20], 12)
        self.assertEqual(cpu.registradores[2], 12)

        cpu.execute(cpu.decode(0x06, 0, 2))  # CMP igual
        self.assertEqual(cpu.zf, 1)
        cpu.pc = 30  # Fetch já teria avançado o PC
        cpu.execute(cpu.decode(0x09, 90, 0))  # JNZ não tomado
        self.assertEqual(cpu.pc, 30)
        cpu.execute(cpu.decode(0x08, 60, 0))  # JZ tomado
        self.assertEqual(cpu.pc, 60)

        cpu.execute(cpu.decode(0x06, 0, 1))  # CMP diferente
        self.assertEqual(cpu.zf, 0)
        cpu.execute(cpu.decode(0x08, 90, 0))  # JZ não tomado
        self.assertEqual(cpu.pc, 60)
        cpu.execute(cpu.decode(0x09, 63, 0))  # JNZ tomado
        self.assertEqual(cpu.pc, 63)
        cpu.execute(cpu.decode(0x07, 66, 0))  # JMP
        self.assertEqual(cpu.pc, 66)

        cpu.execute(cpu.decode(0x0A, 0, 0))  # HALT
        self.assertFalse(cpu.rodando)
        cpu.execute(cpu.decode(0x05, 0, 99))
        self.assertEqual(cpu.registradores[0], 12)

    def test_soma_e_subtracao_fazem_wrap_em_oito_bits(self):
        cpu = MiniCPU()
        cpu.execute(("MOV", 0, 255))
        cpu.execute(("MOV", 1, 1))
        cpu.execute(("ADD", 0, 1))
        self.assertEqual(cpu.registradores[0], 0)
        cpu.execute(("SUB", 0, 1))
        self.assertEqual(cpu.registradores[0], 255)

    def test_operandos_invalidos(self):
        cpu = MiniCPU()
        with self.assertRaises(ValueError):
            cpu.execute(("LOAD", 4, 0))
        with self.assertRaises(ValueError):
            cpu.execute(("LOAD", 0, 256))
        with self.assertRaises(ValueError):
            cpu.execute(("MOV", 0, 256))
        with self.assertRaises(ValueError):
            cpu.execute(("INVALIDA", 0, 0))


if __name__ == "__main__":
    unittest.main()
