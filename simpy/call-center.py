"""Simulação da central de atendimento do projeto de simução de sistemas."""
import simpy
import random
import csv
import numpy as np


class CentralAtendimentos(object):
    """Ambiente de simulação."""

    def __init__(self, env, num_atendentes) -> None:
        """Inicialização do objeto Central de Atendimentos."""
        self.env = env
        self.atendente = simpy.Resource(env,
                                        num_atendentes)

    def atendimento(self, chamada) -> None:
        """Realiza timeout do tempo para atendimento."""
        # Tempo de atendimento
        yield self.env.timeout(np.random.exponential(299.1))


def chamados(env, chamada, central) -> None:
    """Realiza o seize do recurso 'atendente'."""
    # Instante de chegada da chamada cliente
    inst_chegada = env.now
    # Requisição de ligação
    with central.atendente.request() as request:
        # Fila
        yield request
        inst_atendimento = env.now
        # Seize do recurso e atendimento
        yield env.process(central.atendimento(chamada))
    inst_saida = env.now
    # Saída de dados
    r_type = random.random()
    call_type = None  # Tipo da ligação
    if r_type < 0.2481:
        call_type = 0
    elif r_type < 0.50:
        call_type = 2
    else:
        call_type = 1
    output.append([n_rep, inst_chegada, inst_atendimento,
                   inst_saida, call_type])


def run_simulacao(env, num_atendentes: int, arrival_interval: float) -> None:
    """Controla a simulação e gera novas chamadas."""
    central = CentralAtendimentos(env, num_atendentes)
    # O primeiro cliente chega sempre na abertura
    chamada = 1
    env.process(chamados(env, chamada, central))
    while True:
        # Tempo entre chegadas
        yield env.timeout(np.random.exponential(arrival_interval))
        chamada += 1
        env.process(chamados(env, chamada, central))


def main(arrival_interval) -> None:
    """Chama todas as funções da simulação."""
    # Setup
    num_atendentes = 4
    # Simulação
    env = simpy.Environment()
    env.process(run_simulacao(env, num_atendentes, arrival_interval))
    env.run(until=36000)


if __name__ == "__main__":
    # Intervalos entre chegadas variam ao longo do ano
    arrival_intervals = [248.624000, 231.885332, 226.209798, 214.172433,
                         206.973750, 195.431206, 180.276498, 171.872452,
                         156.499403, 149.751203, 139.963744, 131.373340]
    output = []
    for n_rep in range(1, 262):
        if n_rep <= 21:
            arrival_interval = arrival_intervals[0]
        elif n_rep <= 41:
            arrival_interval = arrival_intervals[1]
        elif n_rep <= 64:
            arrival_interval = arrival_intervals[2]
        elif n_rep <= 86:
            arrival_interval = arrival_intervals[3]
        elif n_rep <= 107:
            arrival_interval = arrival_intervals[4]
        elif n_rep <= 129:
            arrival_interval = arrival_intervals[5]
        elif n_rep <= 151:
            arrival_interval = arrival_intervals[6]
        elif n_rep <= 173:
            arrival_interval = arrival_intervals[7]
        elif n_rep <= 195:
            arrival_interval = arrival_intervals[8]
        elif n_rep <= 216:
            arrival_interval = arrival_intervals[9]
        elif n_rep <= 238:
            arrival_interval = arrival_intervals[10]
        else:
            arrival_interval = arrival_intervals[11]
        # Realiza a simulação
        main(arrival_interval)

    # Escrevendo output em csv
    header = ["replication", "call_started", "call_answered",
              "call_ended", "call_type"]
    with open("simpy/output-simpy.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for line in output:
            writer.writerow(line)
