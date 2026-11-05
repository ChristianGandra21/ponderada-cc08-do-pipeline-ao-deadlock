Christian Vinícius Gandra dos Santos | D1 = 9 | D2 = 2 | N = 5

# Parte A — O problema técnico

## A1. Arquitetura e memória: qual processador vai na pulseira?

Para comparar as plataformas, primeiro calculo os parâmetros individuais de Christian Vinícius Gandra dos Santos. O primeiro nome tem 9 letras, então D1 = 9. O nome completo tem 32 letras, então D2 = 2.

```text
IC = 100.000 + 20.000 × D2
IC = 100.000 + 20.000 × 2 = 140.000 instruções por amostra

m = 3% + 0,5% × D1
m = 3% + 0,5% × 9 = 7,5% = 0,075
```

**Plataforma H.** Como cada instrução leva 1,5 ciclos e o processador opera a 48 MHz, calculo o tempo de uma amostra da seguinte forma:

```text
Ciclos por amostra = IC × CPI = 140.000 × 1,5 = 210.000 ciclos
Tempo = 210.000 ÷ 48.000.000 s = 0,004375 s = 4,375 ms
```

A Plataforma H processa a amostra em 4,375 ms. Portanto, ela atende ao limite de 5 ms, com uma margem de 0,625 ms.

**Plataforma V.** Em cada acesso, a cache acerta em 1 ciclo e uma falta acrescenta a penalidade de 120 ciclos. Assim, o tempo médio de acesso à memória (AMAT) é:

```text
AMAT = tempo de acerto + (taxa de falta × penalidade da falta)
AMAT = 1 + (0,075 × 120) = 10 ciclos por acesso, em média
```

Com 1,3 acessos à memória por instrução, o CPI efetivo fica:

```text
CPI efetivo = 1,0 + (acessos por instrução × m × penalidade)
CPI efetivo = 1,0 + (1,3 × 0,075 × 120) = 12,7 ciclos por instrução
```

Agora calculo o tempo de processamento usando o clock de 1,2 GHz:

```text
Ciclos por amostra = 140.000 × 12,7 = 1.778.000 ciclos
Tempo de processamento = 1.778.000 ÷ 1.200.000.000 s ≈ 1,482 ms
Pior caso pedido = 1,482 ms + 3 ms de atraso do Linux ≈ 4,482 ms
```

A Plataforma V também atende ao limite: o tempo estimado, somado ao atraso máximo informado para o sistema operacional, é de aproximadamente 4,482 ms. Esse cálculo usa o CPI baseado na taxa média de faltas indicada no enunciado e acrescenta o atraso máximo do Linux.

**Efeito do acelerador DSP na Plataforma H.** O filtro corresponde a 60% do tempo e fica 5 vezes mais rápido. Pela Lei de Amdahl, o speedup total é:

```text
Speedup = 1 ÷ [(1 − 0,60) + (0,60 ÷ 5)]
Speedup = 1 ÷ (0,40 + 0,12) = 1 ÷ 0,52 ≈ 1,923

Novo tempo = 4,375 ms ÷ 1,923 ≈ 2,275 ms
```

Com o DSP, a Plataforma H continua atendendo ao limite de 5 ms e reduz o tempo por amostra para aproximadamente 2,275 ms.

**Por que V precisa de cache e H funciona sem?** A Plataforma V usa DRAM externa, cujo acesso é muito mais lento que um ciclo do processador; a cache mantém instruções e dados usados recentemente perto do processador e reduz esse custo médio. A Plataforma H acessa SRAM interna em um ciclo e não precisa de cache para esconder uma diferença de velocidade semelhante. Em um sistema Von Neumann, instruções e dados compartilham o caminho de acesso à memória, o que pode criar o gargalo de Von Neumann.

**Evidência da máquina.** A imagem abaixo registra a saída do comando `lscpu` deste ambiente Linux. Ela identifica um Intel Core i5-1345U de 13ª geração e mostra caches L1 separadas: 352 KiB para dados (L1d) e 576 KiB para instruções (L1i), distribuídas em 10 instâncias. Portanto, a L1 é dividida entre instruções e dados. Assim, classifico o computador como Von Neumann com cache L1 Harvard modificada: a L1 é dividida, mas essa evidência, por si só, não mostra memórias principais separadas para instruções e dados.

![Saída do comando lscpu com os tamanhos das caches L1, L2 e L3.](img/cache-lscpu.png)

## A2. Pipeline

## A3. Processos e threads

## A4. Código com semáforos

## A5. Deadlock

# Parte B — A decisão do CTO
