#!/usr/bin/env python3
"""A4 v3: ordem trocada que pode causar deadlock quando o buffer enche.

Execute da raiz: python3 ponderada/codigo/versao3.py [--samples N --runs R].
"""

import threading
import time

from common import ATRASO_MOTOR_S, TIMEOUT_CONSUMIDOR_S, executar_rodadas, resumir


def executar(amostras, capacidade):
    """Executa produtor-consumidor invertendo a ordem de aquisição.

    Args:
        amostras: Quantidade de IDs que o produtor tentará gerar.
        capacidade: Número de posições do buffer circular.

    Returns:
        Métricas que separam perdas, amostras retidas e amostras não geradas.

    Funcionamento:
        O produtor adquire mutex antes de esperar por vazio. O consumidor
        processa cada item por 0,1 ms, como na v2, e pode ficar bloqueado
        tentando obter mutex enquanto o produtor espera uma posição vazia.
        Não há barreira: o escalonador e a diferença de ritmo determinam a
        intercalação; timeouts limitam a duração da demonstração.
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
        """Marca que uma espera excedeu o limite da simulação."""
        travou.set()
        parar.set()

    def produtor():
        """Adquire mutex antes de vazio; ao encher, pode reter mutex e travar."""
        try:
            for identificador in range(amostras):
                if parar.is_set():
                    break
                if not mutex.acquire(timeout=TIMEOUT_CONSUMIDOR_S):
                    marcar_travamento()
                    break
                if not vazio.acquire(timeout=TIMEOUT_CONSUMIDOR_S):
                    # O timeout encerra a demonstração e libera o semáforo
                    # apenas para que as threads simuladas possam terminar.
                    marcar_travamento()
                    mutex.release()
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
        """Consome itens; se o produtor retiver mutex, expira e encerra."""
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
    # Iniciar produtor primeiro permite que ele avance naturalmente; não há
    # barreira nem espera condicionada ao buffer cheio.
    thread_produtor.start()
    thread_consumidor.start()
    thread_produtor.join()
    thread_consumidor.join()

    return resumir(
        amostras, geradas, consumidas, buffer,
        leituras_vazias=leituras_vazias[0], travou=travou.is_set()
    )


def main():
    """Executa as rodadas padrão da versão com ordem de aquisição trocada."""
    executar_rodadas(
        3, 'produtor adquire mutex antes de vazio', executar,
        atraso_motor_s=ATRASO_MOTOR_S
    )


if __name__ == '__main__':
    main()
