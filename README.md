# Ponderada CC08

Christian Vinicius Gandra dos Santos

Aplicação de arquitetura de computadores, sistemas operacionais e decisão de negócio à pulseira sensorial Tato.

## Executar as versões da A4

Cada comando executa três rodadas de 20.000 amostras com o buffer individual `N = 5`. Execute a partir da raiz do repositório:

```bash
python3 ponderada/codigo/versao1.py
python3 ponderada/codigo/versao2.py
python3 ponderada/codigo/versao3.py
```

Os parâmetros podem ser ajustados com `--samples` e `--runs`. As versões 2 e 3 simulam 0,1 ms de processamento do motor por item, para dar tempo ao produtor e ao consumidor de avançarem em ritmos diferentes. A v1 usa `time.sleep(0)` entre ler e atualizar o contador em cada operação válida. A v3 não usa barreira; como cada espera tem timeout de 1 s, três execuções podem levar alguns segundos.

Os resultados variam com o escalonador do sistema operacional, a carga da máquina e a versão do Python. Os resultados registrados no Markdown foram obtidos em Python 3.12.3, Ubuntu 24.04, Linux x86_64, Intel Core i5-1345U. `ponderada/codigo/common.py` concentra a impressão dos resultados e o cálculo de perdas, amostras retidas, duplicatas e integridade FIFO; cada versão continua executável pelo comando acima.

As saídas integrais em texto estão em `ponderada/img/a4-versao1-stdout.txt`, `ponderada/img/a4-versao2-stdout.txt` e `ponderada/img/a4-versao3-stdout.txt`; o `lscpu` sem filtro está em `ponderada/img/lscpu-completo.txt`. Esses arquivos preservam a saída real dos comandos, mas não substituem as capturas de tela de terminal exigidas na entrega.
