import numpy as np 
import random 
import sys 
sys.path.append('chrome_trex.zip')

from chrome_trex import DinoGame

CHANCE_MUT = .2
CHANCE_CO = .25
NUM_MELHORES = 3
NUM_INDIVIDUOS = 20

def ordenar_lista(lista,ordenacao, decrescente = True):
    return [x for _, x in sorted(zip(ordenacao, lista), key=lambda p: p[0], reverse=decrescente)]

def populacao_aleatoria(n):
    populacao = []
    for i in range(n):
        individuo = np.random.uniform(-10,10,(3,10))
        populacao.append(individuo)
    return populacao


def valor_das_acoes(individuo, estado):
    return individuo @ estado


def melhor_jogada(individuo, estado):
    melhor = valor_das_acoes(individuo, estado)
    return np.argmax(melhor)


def mutacao(individuo):
    for i in range(3):
        for j in range(10):
            prob = random.uniform(0,1)
            if prob < CHANCE_MUT:
                individuo[i][j] = np.random.uniform(-10,10)
    

def crossover(individuo1, individuo2):
    filho = individuo1.copy()
    for i in range(3):
        for j in range(10):
            prob = np.random.uniform(0,1)
            if prob < CHANCE_CO:
                filho[i][j] = individuo2[i][j]
    return filho


def prox_ger(populacao, fitness):
    ordenados = ordenar_lista(populacao, fitness)
    prox_ger = ordenados[:NUM_MELHORES]
    while len(prox_ger) < NUM_INDIVIDUOS:
        ind1, ind2 = random.choices(populacao, k = 2)
        filho = crossover(ind1, ind2)
        mutacao(filho)
        prox_ger.append(filho)
    return prox_ger
    


def calcular_fitness(jogo, individuo):
    jogo.reset()
    while not jogo.game_over:
        estado = jogo.get_state()
        acao = melhor_jogada(individuo, estado)
        jogo.step(acao)
    return jogo.get_score()

num_geracoes = 100
jogo = DinoGame(fps = 50_000)

populacao = populacao_aleatoria(NUM_INDIVIDUOS)

print('ger | fitness \n ---+', '-'*5*NUM_INDIVIDUOS)

for ger in range(num_geracoes):
    fitness = []
    for ind in populacao:
        fitness.append(calcular_fitness(jogo, ind))

    populacao = prox_ger(populacao, fitness)
    
    print('{:3} |'.format(ger),
          ' '.join('{:4d}'.format(s) for s in sorted(fitness, reverse=True)))
        
fitness = []
for ind in populacao:
    fitness.append(calcular_fitness(jogo, ind))