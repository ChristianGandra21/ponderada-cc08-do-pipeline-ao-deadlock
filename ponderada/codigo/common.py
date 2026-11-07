#!/usr/bin/env python3
"""Funções compartilhadas para as três simulações da questão A4."""

import argparse

N_BUFFER = 5
AMOSTRAS_PADRAO = 20_000
EXECUCOES_PADRAO = 3
TIMEOUT_CONSUMIDOR_S = 1.0
ATRASO_MOTOR_S = 0.0001


def resumir(amostras, geradas, consumidas, buffer, leituras_vazias=0, travou=False):
    """Calcula perdas, retenções, duplicatas e integridade a partir dos IDs.

    Args:
        amostras: Total de IDs que o produtor deveria tentar publicar.
        geradas: IDs efetivamente escritos no buffer pelo produtor.
        consumidas: IDs válidos efetivamente retirados pelo consumidor.
        buffer: Estado final das posições do buffer circular.
        leituras_vazias: Quantas retiradas encontraram uma posição vazia.
        travou: Indica se a execução detectou timeout/travamento.

    Returns:
        Dicionário de métricas. IDs ainda no buffer são retidos, não perdidos.
    """
    conjunto_geradas = set(geradas)
    conjunto_consumidas = set(consumidas)
    ids_retidos = [identificador for identificador in buffer if identificador is not None]
    conjunto_retidos = set(ids_retidos)
    return {
        'geradas': len(conjunto_geradas),
        'consumidas': len(consumidas),
        'perdidas': len(conjunto_geradas - conjunto_consumidas - conjunto_retidos),
        'retidas': len(ids_retidos),
        'nao_geradas': max(0, amostras - len(conjunto_geradas)),
        'duplicadas': max(0, len(consumidas) - len(conjunto_consumidas)),
        'leituras_vazias': leituras_vazias,
        'travou': travou,
        'fifo_ok': consumidas == list(range(amostras)) and not travou and leituras_vazias == 0,
    }


def imprimir_resultado(numero, resultado):
    """Imprime as métricas de uma execução em uma linha."""
    estado = 'SIM' if resultado['travou'] else 'NÃO'
    fifo = 'OK' if resultado['fifo_ok'] else 'NÃO'
    print(
        f"Execução {numero}: geradas={resultado['geradas']}; "
        f"consumidas={resultado['consumidas']}; perdidas={resultado['perdidas']}; "
        f"retidas={resultado['retidas']}; não_geradas={resultado['nao_geradas']}; "
        f"duplicadas={resultado['duplicadas']}; leituras_vazias={resultado['leituras_vazias']}; "
        f"FIFO={fifo}; travou={estado}"
    )


def executar_rodadas(versao, descricao, executar, atraso_motor_s=0.0):
    """Configura a CLI e executa as rodadas de uma versão da A4.

    Args:
        versao: Número da versão, para compor a mensagem inicial.
        descricao: Descrição curta do mecanismo usado.
        executar: Função de execução recebendo amostras e capacidade.
        atraso_motor_s: Tempo simulado de processamento pelo consumidor.
    """
    parser = argparse.ArgumentParser(description=descricao)
    parser.add_argument('--samples', type=int, default=AMOSTRAS_PADRAO,
                        help='amostras que o produtor tentará gerar (padrão: 20000)')
    parser.add_argument('--runs', type=int, default=EXECUCOES_PADRAO,
                        help='quantidade de execuções (padrão: 3)')
    args = parser.parse_args()
    if args.samples < 1 or args.runs < 1:
        parser.error('--samples e --runs precisam ser positivos')
    print(f'A4 — Versão {versao}: {descricao}')
    configuracao = (
        f'N={N_BUFFER}; amostras por execução={args.samples}; execuções={args.runs}; '
        f'timeout={TIMEOUT_CONSUMIDOR_S:g} s'
    )
    if atraso_motor_s:
        configuracao += f'; atraso simulado do motor={atraso_motor_s * 1000:g} ms'
    print(configuracao)
    for numero in range(1, args.runs + 1):
        imprimir_resultado(numero, executar(args.samples, N_BUFFER))
