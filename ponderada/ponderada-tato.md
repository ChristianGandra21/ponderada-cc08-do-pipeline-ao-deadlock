Christian Vinícius Gandra dos Santos | D1 = 9 | D2 = 2 | N = 5

# Ponderada CC08

## Parâmetros individuais

| Parâmetro | Conta | Valor |
| --- | --- | ---: |
| D1 | Letras de “Christian” | 9 |
| D2 | 9 + 8 + 6 + 3 + 6 = 32; último dígito | 2 |
| IC | 100.000 + 20.000 × 2 | 140.000 instruções/amostra |
| m | 3% + 0,5% × 9 | 7,5% |
| N | 3 + (2 mod 5) | 5 |

# Parte A — O problema técnico

## A1. Arquitetura e memória: qual processador vai na pulseira?

### Premissas de cálculo

- A Plataforma H opera a 48 MHz, tem CPI de 1,5 e acessa SRAM interna em 1 ciclo.
- A Plataforma V opera a 1,2 GHz; o acerto na cache custa 1 ciclo, a penalidade de falta é 120 ciclos e há 1,3 acessos à memória por instrução.
- O atraso máximo do sistema operacional na V é 3 ms; o limite por amostra é 5 ms.
- Para o DSP, a fração acelerada é 60% e o speedup dessa fração é 5; tempos finais em ms são arredondados a 3 casas decimais.

### A1.1 Plataforma H: tempo por amostra

> Calcule o tempo para processar uma amostra na Plataforma H, usando o seu IC. Ela atende os 5 ms?

**Dados usados:** IC = 140.000 instruções/amostra; CPI_H = 1,5 ciclos/instrução; f_H = 48 MHz.

**Passo 1: calcular os ciclos por amostra**

```text
Fórmula geral: C_H = IC × CPI_H
Substituindo: C_H = 140.000 instruções × 1,5 ciclos/instrução
Conta: C_H = 210.000 ciclos
```

**Passo 2: converter ciclos em tempo**

```text
Fórmula geral: T_H = C_H ÷ f_H
Substituindo: T_H = 210.000 ciclos ÷ (48 × 10⁶ ciclos/s)
Conta: T_H = 0,004375 s = 4,375 ms
```

**Resposta:** **4,375 ms < 5 ms; a Plataforma H atende**, com folga de 0,625 ms (12,5%).

### A1.2 Plataforma V: AMAT, CPI efetivo e tempo por amostra

> Para a Plataforma V, calcule o tempo médio de acesso à memória (AMAT) e o CPI efetivo, usando a sua taxa de falta m. Considere CPI efetivo = 1,0 + (acessos por instrução × m × penalidade). Calcule o tempo por amostra e o pior caso, somando o atraso do sistema operacional. Ela atende os 5 ms?

**Dados usados:** m = 7,5% = 0,075; acerto = 1 ciclo; penalidade = 120 ciclos; 1,3 acessos/instrução; IC = 140.000; f_V = 1,2 GHz; atraso máximo do SO = 3 ms.

**Passo 1: calcular AMAT**

```text
Fórmula geral: AMAT = tempo de acerto + (m × penalidade da falta)
Substituindo: AMAT = 1 ciclo + (0,075 × 120 ciclos)
Conta: AMAT = 1 + 9 = 10 ciclos por acesso, em média
```

**Passo 2: calcular CPI efetivo**

```text
Fórmula geral: CPI_efetivo = CPI_base + (acessos/instrução × m × penalidade)
Substituindo: CPI_efetivo = 1,0 + (1,3 × 0,075 × 120)
Conta: CPI_efetivo = 1,0 + 11,7 = 12,7 ciclos/instrução
```

**Passo 3: calcular o tempo médio por amostra**

```text
Fórmula geral: T_V = (IC × CPI_efetivo) ÷ f_V
Substituindo: T_V = (140.000 instruções × 12,7 ciclos/instrução) ÷ (1,2 × 10⁹ ciclos/s)
Conta: T_V = 1.778.000 ciclos ÷ (1,2 × 10⁹ ciclos/s) ≈ 0,001482 s ≈ 1,482 ms
```

**Passo 4: somar o atraso máximo do sistema operacional**

```text
Fórmula geral: T_pior = T_V + atraso máximo do SO
Substituindo: T_pior = 1,482 ms + 3 ms
Conta: T_pior = 4,482 ms
```

**Resposta:** **AMAT = 10 ciclos/acesso; CPI efetivo = 12,7; T_V = 1,482 ms; pior caso = 4,482 ms < 5 ms, atende**, com folga de 0,518 ms (10,4%). O tempo de processamento usa o CPI calculado pela taxa média de faltas; o atraso máximo do SO foi somado conforme pedido.

### A1.3 Plataforma H com DSP: Lei de Amdahl

> O time oferece um acelerador DSP para a Plataforma H que executa o filtro 5 vezes mais rápido. O filtro é 60% do tempo de processamento. Use a Lei de Amdahl para calcular o speedup global e o novo tempo por amostra. Agora atende?

**Dados usados:** fração acelerada p = 0,60; speedup dessa fração s = 5; tempo original T_H = 4,375 ms.

**Passo 1: calcular o speedup global**

```text
Fórmula geral: S = 1 ÷ [(1 − p) + (p ÷ s)]
Substituindo: S = 1 ÷ [(1 − 0,60) + (0,60 ÷ 5)]
Conta: S = 1 ÷ (0,40 + 0,12) = 1 ÷ 0,52 ≈ 1,923
```

**Passo 2: calcular o novo tempo**

```text
Fórmula geral: T_novo = T_original ÷ S
Substituindo: T_novo = 4,375 ms ÷ 1,923
Conta: T_novo ≈ 2,275 ms
```

**Resposta:** **Speedup global ≈ 1,923; novo tempo ≈ 2,275 ms < 5 ms; a Plataforma H com DSP atende**, com folga de 2,725 ms (54,5%).

### A1.4 Por que V precisa de cache e H funciona sem?

> Em até cinco linhas: por que a Plataforma V precisa de cache e a H funciona sem? Use a ideia de gargalo de Von Neumann.

- A V usa organização Von Neumann e faz 1,3 acessos à memória por instrução; sem cache, todos pagariam a latência de DRAM.
- Sem cache: CPI = 1,0 + (1,3 × 120) = 157; tempo = (140.000 × 157) ÷ 1,2 GHz ≈ 18,317 ms, acima de 5 ms.
- Com cache, CPI cai para 12,7 e o tempo médio estimado cai para 1,482 ms; o caminho compartilhado de instruções e dados continua sendo um gargalo.
- A H usa Harvard e SRAM interna de 1 ciclo, então não tem a grande diferença de latência da DRAM externa que a cache da V precisa compensar.

**Resposta:** a cache reduz o custo do caminho de memória compartilhado na V; a H usa caminhos Harvard e SRAM de 1 ciclo, por isso funciona sem cache.

### A1.5 Evidência das caches da máquina

> Cole o print das caches do seu computador (Linux: lscpu; macOS: sysctl -a | grep cachesize; Windows: aba Caches do CPU-Z). A sua L1 é dividida em instruções e dados? Então o seu computador é Von Neumann ou Harvard? Justifique.

![Registro da saída do comando lscpu com os tamanhos das caches L1, L2 e L3.](img/cache-lscpu.png)

**O que o print mostra:** o comando `lscpu` identifica um Intel Core i5-1345U de 13ª geração. A saída informa L1d = 352 KiB (10 instâncias), L1i = 576 KiB (10 instâncias), L2 = 6,5 MiB (4 instâncias) e L3 = 12 MiB (1 instância).

**A L1 é dividida?** Sim. Há caches L1 separadas para dados (L1d) e instruções (L1i).

**Von Neumann ou Harvard?** A organização da L1 é Harvard modificada, pois mantém caches separadas de instruções e dados. Classifico o computador como Harvard modificada; essa separação na L1 não implica que as memórias principais sejam separadas.

**Resposta:** a L1 é dividida em instruções e dados, e a máquina apresenta organização Harvard modificada.

### Resumo dos resultados da A1

| Cenário | Tempo por amostra | Folga até 5 ms | Atende? |
| --- | ---: | ---: | :---: |
| H | 4,375 ms | 0,625 ms (12,5%) | Sim |
| H + DSP | 2,275 ms | 2,725 ms (54,5%) | Sim |
| V, média | 1,482 ms | 3,518 ms (70,4%) | Sim |
| V, pior caso com atraso do SO | 4,482 ms | 0,518 ms (10,4%) | Sim |

## A2. Pipeline: o loop do filtro

### A2.1 Dependências de dados RAW

> Liste as dependências de dados (RAW) do trecho: qual instrução depende de qual, por qual registrador.

Uma dependência RAW (Read After Write) ocorre quando uma instrução precisa ler um registrador escrito por uma instrução anterior. No trecho, as dependências são:

| Instrução que escreve | Instrução que lê | Registrador | Valor transmitido |
| --- | --- | --- | --- |
| 1. `lw x5, 0(x10)` | 2. `add x6, x6, x5` | `x5` | Amostra nova lida do sensor |
| 2. `add x6, x6, x5` | 4. `sub x6, x6, x7` | `x6` | Soma atualizada com a amostra nova |
| 3. `lw x7, 0(x11)` | 4. `sub x6, x6, x7` | `x7` | Amostra mais antiga do buffer |
| 4. `sub x6, x6, x7` | 5. `sw x6, 0(x12)` | `x6` | Soma final a ser gravada |

As instruções 6 e 7 atualizam os ponteiros `x10` e `x11` depois dos loads. Não criam dependência RAW com instrução posterior no trecho; ao reordená-las, mantenho cada incremento depois do load que usa aquele ponteiro.

### A2.2 Pipeline sem forwarding

> Sem forwarding: desenhe o diagrama do pipeline ciclo a ciclo e diga quantos ciclos o trecho leva do primeiro IF ao último WB.

**Premissas:** o pipeline tem os estágios IF, ID, EX, MEM e WB. Sem forwarding, a instrução consumidora só pode ler o valor no banco de registradores em ID depois que a produtora o escreveu em WB. Como a escrita ocorre na primeira metade do ciclo e a leitura na segunda, a consumidora pode fazer ID no mesmo ciclo de WB. `ID (espera)` marca uma instrução parada no decodificador; `IF (mantida)` marca a próxima instrução esperando para avançar; `Bolha` é um estágio EX vazio.

| Ciclo | IF | ID | EX | MEM | WB |
| ---: | --- | --- | --- | --- | --- |
| 1 | I1 | — | — | — | — |
| 2 | I2 | I1 | — | — | — |
| 3 | I3 | I2 (espera x5) | I1 | — | — |
| 4 | I3 (mantida) | I2 (espera x5) | Bolha | I1 | — |
| 5 | I3 (mantida) | I2 | Bolha | — | I1 |
| 6 | I4 | I3 | I2 | — | — |
| 7 | I5 | I4 (espera x6 e x7) | I3 | I2 | — |
| 8 | I5 (mantida) | I4 (espera x6 e x7) | Bolha | I3 | I2 |
| 9 | I5 (mantida) | I4 | Bolha | — | I3 |
| 10 | I6 | I5 (espera x6) | I4 | — | — |
| 11 | I6 (mantida) | I5 (espera x6) | Bolha | I4 | — |
| 12 | I6 (mantida) | I5 | Bolha | — | I4 |
| 13 | I7 | I6 | I5 | — | — |
| 14 | — | I7 | I6 | I5 | — |
| 15 | — | — | I7 | I6 | I5 |
| 16 | — | — | — | I7 | I6 |
| 17 | — | — | — | — | I7 |

O pipeline ideal de 7 instruções teria `7 + (5 − 1) = 11` ciclos. Sem forwarding, as dependências acrescentam 6 ciclos de espera: 2 para `I1 → I2`, 2 para `I2/I3 → I4` e 2 para `I4 → I5`.

**Resposta:** **11 + 6 = 17 ciclos**, do primeiro IF de I1 ao último WB de I7.

### A2.3 Pipeline com forwarding

> Com forwarding: mesmo diagrama e total. Qual dependência continua causando bolha mesmo com forwarding, e por quê?

Com forwarding, o resultado pode seguir diretamente da saída de uma etapa para a entrada de outra sem esperar pela escrita e leitura no banco de registradores. Ainda há uma bolha de load-use quando a instrução seguinte precisa imediatamente do dado carregado: o valor de `lw` só fica disponível ao fim de MEM. Isso ocorre em `I1 → I2` (`x5`) e `I3 → I4` (`x7`). Considero forwarding completo, inclusive do dado usado por `sw`.

| Ciclo | IF | ID | EX | MEM | WB |
| ---: | --- | --- | --- | --- | --- |
| 1 | I1 | — | — | — | — |
| 2 | I2 | I1 | — | — | — |
| 3 | I3 | I2 (detecta load-use x5) | I1 | — | — |
| 4 | I3 (mantida) | I2 (1 bolha) | Bolha | I1 | — |
| 5 | I4 | I3 | I2 | — | I1 |
| 6 | I5 | I4 (detecta load-use x7) | I3 | I2 | — |
| 7 | I5 (mantida) | I4 (1 bolha) | Bolha | I3 | I2 |
| 8 | I6 | I5 | I4 | — | I3 |
| 9 | I7 | I6 | I5 | I4 | — |
| 10 | — | I7 | I6 | I5 | I4 |
| 11 | — | — | I7 | I6 | I5 |
| 12 | — | — | — | I7 | I6 |
| 13 | — | — | — | — | I7 |

O pipeline ideal leva 11 ciclos. As duas dependências load-use acrescentam uma bolha cada, então o total é `11 + 2 = 13` ciclos.

**Resposta:** **13 ciclos.** As dependências `lw x5 → add` e `lw x7 → sub` ainda geram uma bolha cada, pois o load só disponibiliza o dado ao fim de MEM; as demais dependências são atendidas pelo forwarding.

### A2.4 Reordenação sem bolhas com forwarding

> Reordene as instruções, sem mudar o resultado, para eliminar todas as bolhas com forwarding. Mostre a nova ordem e o novo total de ciclos.

Aproveito as instruções independentes de atualização dos ponteiros para separar cada `lw` de sua instrução consumidora. Mantenho cada atualização de ponteiro depois do load correspondente e a soma antes da subtração e da gravação:

| Nova ordem | Instrução original | Instrução |
| ---: | ---: | --- |
| 1 | 1 | `lw x5, 0(x10)` |
| 2 | 3 | `lw x7, 0(x11)` |
| 3 | 6 | `addi x10, x10, 4` |
| 4 | 7 | `addi x11, x11, 4` |
| 5 | 2 | `add x6, x6, x5` |
| 6 | 4 | `sub x6, x6, x7` |
| 7 | 5 | `sw x6, 0(x12)` |

Assim, há instruções independentes entre cada load e seu uso. A dependência entre `add` e `sub` é resolvida pelo forwarding; a dependência entre `sub` e `sw` também é resolvida pelo forwarding completo considerado acima. Não há bolhas:

| Ciclo | IF | ID | EX | MEM | WB |
| ---: | --- | --- | --- | --- | --- |
| 1 | R1 | — | — | — | — |
| 2 | R2 | R1 | — | — | — |
| 3 | R3 | R2 | R1 | — | — |
| 4 | R4 | R3 | R2 | R1 | — |
| 5 | R5 | R4 | R3 | R2 | R1 |
| 6 | R6 | R5 | R4 | R3 | R2 |
| 7 | R7 | R6 | R5 | R4 | R3 |
| 8 | — | R7 | R6 | R5 | R4 |
| 9 | — | — | R7 | R6 | R5 |
| 10 | — | — | — | R7 | R6 |
| 11 | — | — | — | — | R7 |

**Resposta:** a nova ordem preserva o resultado e elimina as bolhas com forwarding. O total é `7 + (5 − 1) =` **11 ciclos**.

### Resumo dos ciclos da A2

| Cenário | Bolhas | Total |
| --- | ---: | ---: |
| Sem forwarding | 6 | 17 ciclos |
| Com forwarding | 2 | 13 ciclos |
| Reordenado com forwarding | 0 | 11 ciclos |

## A3. Processos e threads

## A4. Código com semáforos

## A5. Deadlock

# Parte B — A decisão do CTO
