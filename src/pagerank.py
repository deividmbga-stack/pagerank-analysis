import os
import random
import re
import sys
import numpy as np

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    all_pages = list(corpus.keys())
    N = len(all_pages)
    distribution = {}

    base_prob = (1 - damping_factor) / N # Probabilidade base para todas as páginas

    links = corpus[page]

    if not links:
        for p in all_pages:
            distribution[p] = 1 / N # Se ficar sem links de saída faz uma distribuição uniforme entre todas as páginas
    else:
        link_prob = damping_factor / len(links)
        for p in all_pages:
            distribution[p] = base_prob
            if p in links:
                distribution[p] += link_prob # Acrescenta a probabilidade adicional para cada link da página atual
    return distribution



def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    all_pages = list(corpus.keys())
    page_counts = {page: 0 for page in all_pages}

    current_page = random.choice(all_pages) # Amostra aleatória, sendo a primeira selecionada.
    page_counts[current_page] += 1

    for _ in range(n - 1): # amostras restantes baseadas na transição do modelo
        distribution = transition_model(corpus, current_page, damping_factor)
        pages = list(distribution.keys())
        probabilities = [distribution[page] for page in pages]
        current_page = random.choices(pages, weights=probabilities, k=1)[0]
        page_counts[current_page] += 1

    ranks = {page: page_counts[page] / n for page in all_pages} # normaliza para obter estimativa de probabilidade de cada página ser visitada.
    return ranks


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    all_pages = list(corpus.keys())
    N = len(all_pages)
    index = {page: i for i, page in enumerate(all_pages)} # mapeamento de página para índice

    M = np.zeros((N, N))

    for page, links in corpus.items():
        j = index[page]
        if not links:
            M[:, j] = 1 / N # Se não houver links de saída, distribui uniformemente
        else:
            for link in links:
                i = index[link]
                M[i, j] = 1 / len(links) # Distribui a probabilidade entre os links de saída
    
    teleport = np.ones((N, 1)) / N # Vetor de teleportação para garantir que o modelo seja irredutível

    rank = np.ones((N, 1)) / N # Inicializa o vetor de PageRank[igual para cada página]

    while True:
        new_rank = damping_factor * M @ rank + (1 - damping_factor) * teleport # Atualiza o vetor de PageRank usando a fórmula iterativa

        if np.max(np.abs(new_rank - rank)) < 0.001: # Verifica a convergência usando a norma L1
            rank = new_rank
            break

        rank = new_rank

    rank = rank / rank.sum() # Normaliza o vetor de PageRank para garantir que os valores somem a 1

    return {page: float(rank[index[page]]) for page in all_pages} # Converte o vetor de PageRank em um dicionário de resultados


if __name__ == "__main__":
    main()
