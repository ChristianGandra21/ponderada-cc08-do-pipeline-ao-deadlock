#!/usr/bin/env python3
"""A4 — versão 2: buffer circular protegido por vazio, cheio e mutex."""

import threading
import time

from common import ATRASO_MOTOR_S, TIMEOUT_CONSUMIDOR_S, executar_rodadas, resumir


def executar(amostras, capacidade):
    """Executa produtor-consumidor com semáforos na ordem segura.

    Args:
        amostras: Quantidade de IDs que o produtor tentará gerar.
        capacidade: Número de posições do buffer circular.

    Returns:
        Métricas incluindo integridade FIFO e estado final do buffer.

    Funcionamento:
        O produtor espera vazio antes de mutex. O consumidor espera cheio
        antes de mutex. O motor leva 0,1 ms por item no modelo da simulação.
    """
    buffer = [None] * capacidade
    vazio = threading.Semaphore(capacidade)
    cheio = threading.Semaphore(0)
    mutex = threading.Semaphore(1)
    indice_escrita = [0]
    indice_leitura = [0]
    geradas = []
    consumidas = []
    leituras_vazias = [0]
    parar = threading.Event()
    produtor_finalizado = threading.Event()
    travou = threading.Event()

    def marcar_travamento():
        """Registra timeout e solicita encerramento das threads."""
        travou.set()
        parar.set()

    def produtor():
        """Publica amostras usando vazio → mutex → inserir → cheio."""
        try:
            for identificador in range(amostras):
                if parar.is_set():
                    break
                if not vazio.acquire(timeout=TIMEOUT_CONSUMIDOR_S):
                    marcar_travamento()
                    break
                if not mutex.acquire(timeout=TIMEOUT_CONSUMIDOR_S):
                    vazio.release()
                    marcar_travamento()
                    break
                posicao = indice_escrita[0]
                buffer[posicao] = identificador
                indice_escrita[0] = (posicao + 1) % capacidade
                geradas.append(identificador)
                mutex.release()
                cheio.release()
        finally:
            produtor_finalizado.set()

    def consumidor():
        """Retira itens em FIFO e registra qualquer posição vazia observada."""
        while len(consumidas) < amostras and not parar.is_set():
            if not cheio.acquire(timeout=TIMEOUT_CONSUMIDOR_S):
                if not produtor_finalizado.is_set() or len(consumidas) < len(geradas):
                    marcar_travamento()
                break
            if not mutex.acquire(timeout=TIMEOUT_CONSUMIDOR_S):
                cheio.release()
                marcar_travamento()
                break
            posicao = indice_leitura[0]
            identificador = buffer[posicao]
            buffer[posicao] = None
            indice_leitura[0] = (posicao + 1) % capacidade
            mutex.release()
            vazio.release()
            if identificador is None:
                leituras_vazias[0] += 1
            else:
                consumidas.append(identificador)
                time.sleep(ATRASO_MOTOR_S)

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
    """Executa as rodadas padrão da versão com semáforos."""
    executar_rodadas(
        2, 'semáforos vazio, cheio e mutex', executar,
        atraso_motor_s=ATRASO_MOTOR_S
    )


if __name__ == '__main__':
    main()
