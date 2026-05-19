# PageRank Algorithm: Stochastic and Algebraic Approaches

Este repositório contém a implementação e a análise comparativa do algoritmo **PageRank**, a célebre mecânica de ordenação de páginas web desenvolvida por Larry Page e Sergey Brin. O projeto foi desenvolvido em **Python**, utilizando abordagens de simulação estocástica (Random Walk) e métodos algébricos exatos vetorizados com **NumPy**.

O objetivo principal é avaliar a convergência e o comportamento de ambos os métodos sobre um corpus de teste (*Mini Web Gamer*), analisando variáveis fundamentais como o fator de amortecimento ($d$) e a presença de armadilhas topológicas (*dead ends*).

---

## 🚀 Funcionalidades

* **Amostragem Estocástica (Random Walk):** Simulação de um usuário navegando aleatoriamente pela rede por meio de Cadeias de Markov, calculando as probabilidades com base na Lei dos Grandes Números.
* **Método da Potência Vetorizado:** Abordagem algébrica linear exata utilizando multiplicação de matrizes com NumPy (`@`), garantindo alta performance na busca pelo autovetor dominante.
* **Tratamento de *Dead Ends*:** Modelagem probabilística para evitar perda de fluxo em nós sorvedouros (sem links de saída), redistribuindo a massa estocástica uniformemente pela rede.
* **Relatório Técnico em LaTeX:** Documentação científica analítica detalhada com os resultados obtidos.

---

## 📁 Estrutura do Projeto

```text
pagerank-analysis/
│
├── corpus/                 # Amostra de páginas HTML para teste (Mini Web Gamer)
│
├── docs/                   # Documentação científica do projeto
│   ├── relatorio.tex       # Código-fonte do relatório analítico em LaTeX
│   └── relatorio.pdf       # Relatório compilado pronto para leitura
│
├── src/                    # Código-fonte do algoritmo
│   └── pagerank.py         # Script principal (Vetorização NumPy + Random Walk)
│
├── .gitignore              # Filtro de arquivos temporários do sistema e do LaTeX
└── requirements.txt        # Dependências do projeto (NumPy)
