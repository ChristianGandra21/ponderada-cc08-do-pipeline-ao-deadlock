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

Os parâmetros podem ser ajustados com `--samples` e `--runs`; a versão 3 usa uma barreira de demonstração para tornar o deadlock reproduzível.
