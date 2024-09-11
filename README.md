# Sobre o projeto
Este projeto foi feito usando o código do repositório [chrome-trex-rush](https://github.com/turing-usp/chrome-trex-rush). O jogo do dinossauro é replicado nele usando a bilbioteca [Pygame](https://www.pygame.org). O chrome-trex-rush implementa a parte visual do jogo, além de permitir simular o jogo para vários dinossauros. Para cada frame do jogo, é possível obter o seu estado atual (informações sobre obstáculos, velocidade atual do jogo, etc) e deve-se informar uma ação(pular, agachar ou andar) para cada dinossauro para que se possa ir para o próximo frame.  
Este projeto implementa um algoritmo genética para aprender o jogo. Cada dinossauro é representado por uma rede neural de 2 camadas. A 1º camada é composta por 3 neurônios referentes às 3 possíveis ações que recebem 4 entradas referentes à distância e posição vertical do próximo obstáculo, velocidade do jogo e valor numérico referente a estado lógico do dinossauro estar pulando ou não(1 para verdadeiro e 0 para falso). As saídas destes 3 neurônios são a entrada de 4º neurônio que irá selecionar a saída com maior valor e escolher a respectiva ação.
