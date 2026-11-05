Christian Vinícius Gandra dos Santos | D1 = 9 | D2 = 2 | N = 5

# Parte A — O problema técnico

## A1. Arquitetura e memória: qual processador vai na pulseira?

**1. Calcule o tempo para processar uma amostra na Plataforma H, usando o seu IC. Ela atende os 5 ms?**

Para calcular o número de instruções por amostra (IC), uso a fórmula dada no enunciado:

```text
Fórmula geral: IC = 100.000 + 20.000 × D2
Substituindo D2 = 2: IC = 100.000 + 20.000 × 2
Conta: IC = 100.000 + 40.000 = 140.000 instruções por amostra
```

O tempo de processamento é o total de ciclos dividido pela frequência. O total de ciclos é o IC multiplicado pelo CPI:

```text
Fórmula geral: T_H = (IC × CPI_H) ÷ f_H
Substituindo: T_H = (140.000 × 1,5) ÷ 48.000.000
Conta: T_H = 210.000 ÷ 48.000.000 = 0,004375 s = 4,375 ms
```

A Plataforma H **atende** ao limite: 4,375 ms é menor que 5 ms. Sua margem é de 5 − 4,375 = 0,625 ms.

**2. Para a Plataforma V, calcule o tempo médio de acesso à memória (AMAT) e o CPI efetivo, usando a sua taxa de falta m. Considere CPI efetivo = 1,0 + (acessos por instrução × m × penalidade). Calcule o tempo por amostra e o pior caso, somando o atraso do sistema operacional. Ela atende os 5 ms?**

Primeiro calculo a taxa de falta da cache usando D1 = 9:

```text
Fórmula geral: m = 3% + 0,5% × D1
Substituindo: m = 3% + 0,5% × 9
Conta: m = 3% + 4,5% = 7,5% = 0,075
```

O AMAT soma o tempo de acerto ao custo médio das faltas. Considero os 120 ciclos como a penalidade de falta, conforme a fórmula de CPI efetivo do enunciado:

```text
Fórmula geral: AMAT = tempo de acerto + (m × penalidade de falta)
Substituindo: AMAT = 1 + (0,075 × 120)
Conta: AMAT = 1 + 9 = 10 ciclos por acesso, em média
```

Agora calculo o CPI efetivo, usando 1,3 acessos à memória por instrução:

```text
Fórmula geral: CPI_efetivo = 1,0 + (acessos por instrução × m × penalidade)
Substituindo: CPI_efetivo = 1,0 + (1,3 × 0,075 × 120)
Conta: CPI_efetivo = 1,0 + 11,7 = 12,7 ciclos por instrução
```

O tempo por amostra é o número total de ciclos dividido pela frequência de 1,2 GHz:

```text
Fórmula geral: T_V = (IC × CPI_efetivo) ÷ f_V
Substituindo: T_V = (140.000 × 12,7) ÷ 1.200.000.000
Conta: T_V = 1.778.000 ÷ 1.200.000.000 ≈ 0,0014817 s ≈ 1,482 ms
```

Para obter o pior caso solicitado, somo o atraso máximo do sistema operacional:

```text
Fórmula geral: T_pior = T_V + atraso máximo do sistema operacional
Substituindo: T_pior = 1,482 ms + 3 ms = 4,482 ms
```

A Plataforma V **atende** ao limite, pois a estimativa no pior caso é 4,482 ms, menor que 5 ms. A parcela de processamento usa o CPI calculado com a taxa média de faltas; os 3 ms representam o atraso máximo do Linux informado no enunciado.

**3. O time oferece um acelerador DSP para a Plataforma H que executa o filtro 5 vezes mais rápido. O filtro é 60% do tempo de processamento. Use a Lei de Amdahl para calcular o speedup global e o novo tempo por amostra. Agora atende?**

A Lei de Amdahl considera a fração do programa que melhora e o speedup aplicado a essa fração. Aqui, a fração acelerada é 60% e ela fica 5 vezes mais rápida:

```text
Fórmula geral: S = 1 ÷ [(1 − p) + (p ÷ s)]
Substituindo p = 0,60 e s = 5: S = 1 ÷ [(1 − 0,60) + (0,60 ÷ 5)]
Conta: S = 1 ÷ (0,40 + 0,12) = 1 ÷ 0,52 ≈ 1,923
```

O novo tempo é o tempo original dividido pelo speedup global:

```text
Fórmula geral: T_novo = T_original ÷ S
Substituindo: T_novo = 4,375 ms ÷ 1,923
Conta: T_novo ≈ 2,275 ms por amostra
```

Com o DSP, a Plataforma H **atende** ao limite de 5 ms, com tempo estimado de 2,275 ms por amostra.

**4. Em até cinco linhas: por que a Plataforma V precisa de cache e a H funciona sem? Use a ideia de gargalo de Von Neumann.**

- A Plataforma V usa DRAM externa, cujo acesso é mais lento que o processador; a cache mantém dados e instruções usados recentemente por perto.
- A Plataforma H acessa SRAM interna em um ciclo, então não precisa de cache para esconder uma diferença de velocidade semelhante.
- Na arquitetura Von Neumann, instruções e dados compartilham o caminho até a memória, criando o gargalo de Von Neumann.
- A cache reduz a espera média da Plataforma V, embora não elimine esse gargalo.

**5. Evidência da sua máquina. Cole o print das caches do seu computador (Linux: lscpu; macOS: sysctl -a | grep cachesize; Windows: aba Caches do CPU-Z). A sua L1 é dividida em instruções e dados? Então o seu computador é Von Neumann ou Harvard? Justifique.**

Usei `lscpu` no ambiente Linux desta atividade. A saída identifica um Intel Core i5-1345U de 13ª geração e informa 352 KiB de cache L1 de dados (L1d) e 576 KiB de cache L1 de instruções (L1i), em 10 instâncias. Portanto, a L1 é dividida entre instruções e dados. Isso é uma organização Harvard modificada na cache L1; classifico o computador como Von Neumann com cache L1 separada, pois a divisão da L1 não demonstra que as memórias principais de instruções e dados também sejam separadas.

![Registro da saída do comando lscpu com os tamanhos das caches L1, L2 e L3.](img/cache-lscpu.png)

## A2. Pipeline

## A3. Processos e threads

## A4. Código com semáforos

## A5. Deadlock

# Parte B — A decisão do CTO
