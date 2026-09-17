# infra-hw-minicpu

## Execute (Luiz)

`MiniCPU.execute(instrucao)` recebe uma tupla ou lista produzida pelo Decode:
`(opcode, operando1, operando2)`. O opcode pode ser `LOAD`, `STORE`, `ADD`,
`SUB`, `MOV`, `CMP`, `JMP`, `JZ`, `JNZ` ou `HALT`.

Registradores são escritos como `"R0"` a `"R3"`. Um inteiro é um valor
imediato; em `LOAD` e `STORE`, ele representa um endereço direto de memória.
Um registrador usado como endereço fornece acesso indireto, útil para percorrer
um array. Exemplos:

```python
cpu.execute(("MOV", "R1", 100))   # R1 = 100
cpu.execute(("LOAD", "R2", "R1")) # R2 = memoria[100]
cpu.execute(("ADD", "R0", "R2"))  # R0 += R2
cpu.execute(("STORE", "R0", 200)) # memoria[200] = R0
```

`CMP` coloca `ZF = 1` quando os valores são iguais e `ZF = 0` caso contrário.
As outras operações preservam `ZF`. `JZ` e `JNZ` alteram o PC somente quando
a condição é verdadeira. `HALT` define `rodando = False`.

O Fetch deve avançar o PC antes de chamar `execute`. O Execute só muda o PC
em desvios tomados. Quando `rodando` é falso, `execute` não faz mais nada.
