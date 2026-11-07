#!/usr/bin/env python3
"""A4 — versão 1: buffer circular com contador compartilhado sem mutex."""

import threading
import time

from common import TIMEOUT_CONSUMIDOR_S, executar_rodadas, resumir


def executar(amostras, capacidade):
    """Executa produtor e consumidor sem proteger o contador compartilhado.

    Args:
        amostras: Quantidade de IDs que o produtor tentará gerar.
        capacidade: Número de posições do buffer circular.

    Returns:
        Métricas calculadas a partir dos IDs consumidos e do estado final do buffer.

    Funcionamento:
        time.sleep(0) cede a execução depois de ler o contador e antes de
        atualizá-lo, abrindo uma janela para a corrida em cada operação válida.
    """
    buffer = [None] * capacidade
    ocupadas = [0]
    geradas = []
    consumidas = []
    leituras_vazias = [0]
    indice_escrita = [0]
    indice_leitura = [0]
    produtor_finalizado = threading.Event()
    parar = threading.Event()
    travou = threading.Event()

    def produtor():
        """Publica IDs e atualiza ocupadas sem exclusão mútua."""
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
                    # A cedência fica entre ler e gravar o contador ocupado.
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
                if parar.is_set():
                    break
        finally:
            produtor_finalizado.set()

    def consumidor():
        """Retira IDs por espera ocupada e registra leituras de posição vazia."""
        ultima_amostra = time.monotonic()
        tentativas_vazias = 0
        while not parar.is_set():
            observado = ocupadas[0]
            if observado > 0:
                # A cedência fica entre ler e gravar o contador ocupado.
                time.sleep(0)
                if parar.is_set():
                    break
                posicao = indice_leitura[0]
                identificador = buffer[posicao]
                buffer[posicao] = None
                indice_leitura[0] = (posicao + 1) % capacidade
                ocupadas[0] = observado - 1
                if identificador is None:
                    leituras_vazias[0] += 1
                else:
                    consumidas.append(identificador)
                    ultima_amostra = time.monotonic()
                continue

            if produtor_finalizado.is_set() and len(geradas) == amostras:
                if ocupadas[0] <= 0:
                    break
            if time.monotonic() - ultima_amostra >= TIMEOUT_CONSUMIDOR_S:
                travou.set()
                parar.set()
                break
            tentativas_vazias += 1
            if tentativas_vazias % 64 == 0:
                time.sleep(0)

    thread_produtor = threading.Thread(target=produtor, name='produtor')
    thread_consumidor = threading.Thread(target=consumidor, name='consumidor')
    thread_produtor.start()
    thread_consumidor.start()
    thread_produtor.join()
    thread_consumidor.join()

    return resumir(
        amostras, geradas, consumidas, buffer,
        leituras_vazias=leituras_vazias[0], travou=travou.is_set()
    )


def main():
    """Executa as rodadas configuradas da versão sem sincronização."""
    executar_rodadas(1, 'contador compartilhado sem sincronização', executar)


if __name__ == '__main__':
    main()
