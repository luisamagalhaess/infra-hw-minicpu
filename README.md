# infra-hw-minicpu
## Integrantes: 

Luísa Magalhães, Laura Vitória, Luiz Vieira, Bruno Meneses

## Fetch (Laura)

`MiniCPU.fetch()` realiza a etapa de busca da instrução na memória.

Cada instrução ocupa três posições consecutivas: `opcode`, `operando1` e `operando2`. O Fetch utiliza o `PC` para acessar esses valores e, após a leitura, incrementa o `PC` em 3 para apontar para a próxima instrução.

Exemplo:

```python
opcode, op1, op2 = cpu.fetch()
```

O método `run()` controla a execução da CPU, repetindo o ciclo:

`FETCH → DECODE → EXECUTE → TRACE`

A execução continua até que a instrução `HALT` altere `rodando` para `False`.

## Decode (Luísa)

`MiniCPU.decode(opcode, operando1, operando2)` recebe o opcode e os operandos produzidos pelo Fetch e identifica qual instrução deve ser executada.

Os opcodes reconhecidos são `LOAD`, `STORE`, `ADD`, `SUB`, `MOV`, `CMP`, `JMP`, `JZ`, `JNZ` e `HALT`.

O Decode também adapta os operandos para o formato esperado pelo Execute. Índices de registradores são convertidos para `"R0"` a `"R3"`.

Exemplo:

```python
cpu.decode(0x03, 0, 1)

cpu.decode(0x05, 2, 10)

cpu.decode(0x0A, 0, 0)
```

Após a decodificação, a instrução retornada pode ser enviada diretamente para `execute()`:

```python
instrucao = cpu.decode(0x03, 0, 1)
cpu.execute(instrucao)
```

Caso o opcode não seja reconhecido, o Decode retorna `("INVALIDA",)`.

## Execute (Luiz)

`MiniCPU.execute(instrucao)` recebe uma tupla ou lista produzida pelo Decode:
`(opcode, operando1, operando2)`. O opcode pode ser `LOAD`, `STORE`, `ADD`,
`SUB`, `MOV`, `CMP`, `JMP`, `JZ`, `JNZ` ou `HALT`.

Registradores são escritos como `"R0"` a `"R3"`. Um inteiro é um valor
imediato; em `LOAD` e `STORE`, ele representa um endereço direto de memória.
Um registrador usado como endereço fornece acesso indireto, útil para percorrer
um array. Exemplos:

```python
cpu.execute(("MOV", "R1", 100))
cpu.execute(("LOAD", "R2", "R1"))
cpu.execute(("ADD", "R0", "R2"))
cpu.execute(("STORE", "R0", 200))
```

`CMP` coloca `ZF = 1` quando os valores são iguais e `ZF = 0` caso contrário.
As outras operações preservam `ZF`. `JZ` e `JNZ` alteram o PC somente quando
a condição é verdadeira. `HALT` define `rodando = False`.

O Fetch deve avançar o PC antes de chamar `execute`. O Execute só muda o PC
em desvios tomados. Quando `rodando` é falso, `execute` não faz mais nada.
