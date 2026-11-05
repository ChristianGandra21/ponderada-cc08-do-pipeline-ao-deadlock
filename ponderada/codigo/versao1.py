#!/usr/bin/env python3
"""A4 - versão 1: buffer circular com contador compartilhado sem sincronização.

A chamada padrão executa três tentativas de 20.000 amostras com N=5.
"""

import argparse
import threading
import time

N_BUFFER = 5
AMOSTRAS_PADRAO = 20_000
EXECUCOES_PADRAO = 3
TIMEOUT_CONSUMIDOR_S = 1.0


def executar(amostras, capacidade, timeout_s):
    """Executa uma tentativa da versão sem sincronização.

    Args:
        amostras: Quantidade de identificadores que o produtor tentará gerar.
        capacidade: Quantidade de posições do buffer circular.
        timeout_s: Segundos sem consumo válido antes de marcar travamento.

    Returns:
        Dicionário com geradas, consumidas, perdidas, duplicadas e travou.

    Funcionamento:
        Produtor e consumidor alteram o contador compartilhado sem mutex.
        time.sleep(0) força uma oportunidade de troca entre leitura e escrita.
    """
    buffer = [None] * capacidade
    ocupadas = [0]
    geradas = []
    consumidas = []
    indice_escrita = [0]
    indice_leitura = [0]
    produtor_finalizado = threading.Event()
    parar = threading.Event()
    travou = threading.Event()

    def produtor():
        """Publica IDs no buffer e atualiza o contador sem exclusão mútua."""
        try:
            tentativas_cheias = 0
            for identificador in range(amostras):
                while not parar.is_set():
                    observado = ocupadas[0]
                    if observado >= capacidade:
                        tentativas_cheias += 1
                        if tentativas_cheias % 64 == 0:
                            time.sleep(0)
                        continue
                    if identificador % 256 == 0:
                        time.sleep(0)
                    if parar.is_set():
                        break
                    posicao = indice_escrita[0]
                    buffer[posicao] = identificador
                    indice_escrita[0] = (posicao + 1) % capacidade
                    geradas.append(identificador)
                    ocupadas[0] = observado + 1
                    break
                else:
                    break
        finally:
            produtor_finalizado.set()

    def consumidor():
        """Retira IDs por espera ocupada e encerra após um segundo sem dado."""
        ultima_amostra = time.monotonic()
        retiradas = 0
        tentativas_vazias = 0
        while not parar.is_set():
            observado = ocupadas[0]
            if observado > 0:
                if retiradas % 256 == 0:
                    time.sleep(0)
                retiradas += 1
                if parar.is_set():
                    break
                posicao = indice_leitura[0]
                identificador = buffer[posicao]
                buffer[posicao] = None
                indice_leitura[0] = (posicao + 1) % capacidade
                ocupadas[0] = observado - 1
                if identificador is not None:
                    consumidas.append(identificador)
                    ultima_amostra = time.monotonic()
                continue
            tentativas_vazias += 1
            if tentativas_vazias % 64 == 0:
                time.sleep(0)
            if produtor_finalizado.is_set() and len(geradas) == amostras:
                if ocupadas[0] <= 0:
                    break
            if time.monotonic() - ultima_amostra >= timeout_s:
                travou.set()
                parar.set()
                break

    thread_produtor = threading.Thread(target=produtor, name='produtor')
    thread_consumidor = threading.Thread(target=consumidor, name='consumidor')
    thread_produtor.start()
    thread_consumidor.start()
    thread_produtor.join()
    thread_consumidor.join()

    unicas = set(consumidas)
    geradas_unicas = set(geradas)
    return {
        'geradas': len(geradas_unicas),
        'consumidas': len(consumidas),
        'perdidas': len(geradas_unicas - unicas),
        'duplicadas': max(0, len(consumidas) - len(unicas)),
        'travou': travou.is_set(),
    }


def imprimir_resultado(numero, resultado):
    """Imprime os contadores da tentativa em uma linha legível."""
    estado = 'SIM' if resultado['travou'] else 'NÃO'
    print(
        f"Execução {numero}: geradas={resultado['geradas']}; "
        f"consumidas={resultado['consumidas']}; perdidas={resultado['perdidas']}; "
        f"duplicadas={resultado['duplicadas']}; travou={estado}"
    )


def main():
    """Lê opções CLI e executa a quantidade configurada de tentativas."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--samples', type=int, default=AMOSTRAS_PADRAO,
                        help='amostras que o produtor tentará gerar (padrão: 20000)')
    parser.add_argument('--runs', type=int, default=EXECUCOES_PADRAO,
                        help='quantidade de execuções (padrão: 3)')
    args = parser.parse_args()
    if args.samples < 1 or args.runs < 1:
        parser.error('--samples e --runs precisam ser positivos')
    print('A4 — Versão 1: contador compartilhado sem sincronização')
    print(f'N={N_BUFFER}; amostras por execução={args.samples}; execuções={args.runs}')
    for numero in range(1, args.runs + 1):
        resultado = executar(args.samples, N_BUFFER, TIMEOUT_CONSUMIDOR_S)
        imprimir_resultado(numero, resultado)


if __name__ == '__main__':
    main()
