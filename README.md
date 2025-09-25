# Robô de Salvamento

Este projeto foi desenvolvido para a disciplina de Serviços Cognitivos. O objetivo é simular o comportamento de um robô de salvamento em um labirinto, que deve encontrar uma pessoa e levá-la em segurança para a saída.

## Funcionalidades

O robô implementado é capaz de:

- Explorar um labirinto desconhecido utilizando um algoritmo de "seguir a parede".
- Mapear o ambiente à medida que o explora.
- Encontrar a pessoa perdida no labirinto.
- Após encontrar a pessoa, calcular o caminho mais eficiente de volta para a saída utilizando o algoritmo A*.
- Gerar um arquivo de log em formato CSV com todos os seus passos e leituras de sensores.
- Exibir uma interface gráfica (opcional) que mostra o robô em ação.

## Como Executar o Projeto

Siga os passos abaixo para executar a simulação.

### 1. Pré-requisitos

- Python 3
- `pip` (gerenciador de pacotes do Python)

### 2. Instalação das Dependências

Para a interface gráfica, o projeto utiliza a biblioteca `pygame`. Para instalá-la, execute o seguinte comando no seu terminal:

```bash
pip install -r requirements.txt
```

### 3. Executando a Simulação

Para iniciar a simulação, você deve executar o módulo `main` que está na pasta `src`, passando como argumento o caminho para o arquivo do labirinto. Por exemplo:

```bash
python3 -m src.main mazes/maze1.txt
```

O projeto inclui 3 labirintos de teste na pasta `mazes/`.

- **Com Interface Gráfica:** Se o `pygame` estiver instalado, uma janela será aberta mostrando o labirinto, o robô e seu progresso.
- **Sem Interface Gráfica (Modo Headless):** Caso o `pygame` não seja encontrado, a simulação rodará em modo "headless" (sem interface gráfica), e apenas o arquivo de log `.csv` será gerado na pasta do labirinto correspondente.

## Estrutura do Projeto

```
/
├── mazes/              # Contém os arquivos de labirinto (.txt) e os logs gerados (.csv)
├── src/                # Contém o código fonte do projeto
│   ├── main.py         # Ponto de entrada da aplicação
│   ├── robot.py        # Lógica do robô (exploração, A*, etc.)
│   ├── maze.py         # Carregamento e representação do labirinto
│   └── gui.py          # Interface gráfica com Pygame
├── tests/              # Testes unitários (não implementados neste exemplo)
├── requirements.txt    # Arquivo com as dependências do projeto
└── README.md           # Este arquivo
```