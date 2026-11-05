#!/usr/bin/env python3
"""A4 - versão 3: ordem trocada que pode causar deadlock.

A chamada padrão executa três tentativas de 20.000 amostras com N=5. Uma
barreira de demonstração libera o consumidor quando o produtor, já com o
buffer cheio, segura mutex e tenta adquirir vazio. Isso torna o deadlock
reproduzível sem alterar a ordem de aquisição que está sendo estudada.
"""

import argparse
import threading

N_BUFFER = 5
AMOSTRAS_PADRAO = 20_000
EXECUCOES_PADRAO = 3
TIMEOUT_CONSUMIDOR_S = 1.0


def executar(amostras, capacidade, timeout_s):
    """Executa uma tentativa com produtor adquirindo mutex antes de vazio.

    Args:
        amostras: Quantidade de IDs que o produtor tentará gerar.
        capacidade: Quantidade de posições do buffer circular.
        timeout_s: Segundos sem receber amostra antes de marcar travamento.

    Returns:
        Dicionário com geradas, consumidas, perdidas, duplicadas e travou.

    Funcionamento:
        O produtor inverte a ordem para mutex -> vazio. A barreira de teste
        revela a espera circular ao atingir a capacidade total do buffer.
    """
    buffer = [None] * capacidade
    vazio = threading.Semaphore(capacidade)
    cheio = threading.Semaphore(0)
    mutex = threading.Semaphore(1)
    indice_escrita = [0]
    indice_leitura = [0]
    geradas = []
    consumidas = []
    parar = threading.Event()
    produtor_finalizado = threading.Event()
    consumidor_liberado = threading.Event()
    travou = threading.Event()

    def marcar_travamento():
        """Registra o timeout e solicita que as duas threads encerrem."""
        travou.set()
        parar.set()

    def produtor():
        """Gera amostras tomando mutex antes de esperar por espaço vazio."""
        try:
            for identificador in range(amostras):
                if parar.is_set():
                    break
                if identificador == capacidade:
                    # O teste libera o consumidor só depois de o produtor
                    # segurar mutex com o buffer cheio: espera circular certa.
                    if not mutex.acquire(timeout=timeout_s):
                        marcar_travamento()
                        break
                    consumidor_liberado.set()
                    if not vazio.acquire(timeout=timeout_s):
                        marcar_travamento()
                        mutex.release()
                        break
                else:
                    if not mutex.acquire(timeout=timeout_s):
                        marcar_travamento()
                        break
                    if identificador == capacidade - 1 and identificador + 1 == amostras:
                        # Quando a execução termina junto com o buffer cheio, não há
                        # próxima inserção para travar; libera o consumidor.
                        consumidor_liberado.set()
                    if not vazio.acquire(timeout=timeout_s):
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
            consumidor_liberado.set()

    def consumidor():
        """Aguarda a barreira e retira itens até completar ou detectar timeout."""
        consumidor_liberado.wait()
        while len(consumidas) < amostras and not parar.is_set():
            if not cheio.acquire(timeout=timeout_s):
                if not produtor_finalizado.is_set() or len(consumidas) < len(geradas):
                    marcar_travamento()
                break
            if not mutex.acquire(timeout=timeout_s):
                cheio.release()
                marcar_travamento()
                break
            posicao = indice_leitura[0]
            identificador = buffer[posicao]
            buffer[posicao] = None
            indice_leitura[0] = (posicao + 1) % capacidade
            mutex.release()
            vazio.release()
            if identificador is not None:
                consumidas.append(identificador)

    thread_produtor = threading.Thread(target=produtor, name='produtor')
    thread_consumidor = threading.Thread(target=consumidor, name='consumidor')
    thread_consumidor.start()
    thread_produtor.start()
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
    print('A4 — Versão 3: produtor adquire mutex antes de vazio')
    print(f'N={N_BUFFER}; amostras por execução={args.samples}; execuções={args.runs}')
    print('Barreira de teste: libera o consumidor somente após o buffer encher.')
    for numero in range(1, args.runs + 1):
        resultado = executar(args.samples, N_BUFFER, TIMEOUT_CONSUMIDOR_S)
        imprimir_resultado(numero, resultado)


if __name__ == '__main__':
    main()
