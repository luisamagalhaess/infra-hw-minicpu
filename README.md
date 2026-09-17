# infra-hw-minicpu

## Execute (Luiz)

`MiniCPU.execute(instrucao)` recebe a tupla produzida por `decode(opcode, a, b)`:
`(mnemônico, a, b)`. Cada instrução ocupa três posições na memória. Operandos
não usados são preenchidos com zero.

Os registradores R0–R3 são representados pelos índices inteiros 0–3. `LOAD` e
`STORE` usam endereço direto em `b`; `ADD`, `SUB` e `CMP` usam dois índices de
registradores; `MOV` usa o valor imediato em `b`. Os saltos usam `a` como
endereço de destino. Exemplos:

```python
cpu.execute(cpu.decode(0x05, 0, 0))     # MOV R0, 0
cpu.execute(cpu.decode(0x01, 1, 0x10))  # LOAD R1, memoria[0x10]
cpu.execute(cpu.decode(0x03, 0, 1))     # ADD R0, R1
cpu.execute(cpu.decode(0x02, 0, 0x20))  # STORE R0, memoria[0x20]
```

`ADD` e `SUB` mantêm o resultado em 8 bits (0–255). `CMP` coloca `ZF = 1`
quando os registradores são iguais e `ZF = 0` caso contrário. As outras
operações preservam `ZF`. `JZ` e `JNZ` alteram o PC somente quando a condição
é verdadeira. `HALT` define `rodando = False`.

O Fetch deve avançar o PC em 3 antes de chamar `execute`. O Execute só muda o PC
em desvios tomados. Quando `rodando` é falso, `execute` não faz mais nada.
