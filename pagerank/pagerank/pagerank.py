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
    # Markov transition, Iterate 4 times
    page_pub = {}
    links = corpus[page]
    N = len(corpus)
    
    if len(links) == 0:
        for _page_ in corpus:
            page_pub[_page_] = 1 / N
        return page_pub

    for _page_ in corpus:
        page_pub[_page_] = (1 - damping_factor) / N
        if _page_ in links:
            page_pub[_page_] += damping_factor / len(links)

    return page_pub


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # return each page -> PageRank
    # Analog Sampling, For Example Monte Carlo simulation
    page_ranks = {}
    each_page = {}

    # Initial
    each_page = {page: 0 for page in corpus}
    # random.choice() has a parameter
    random_page = random.choice(list(corpus.keys()))
    for _ in range(n):
        # random.choice() items, Because We random choice one page, so we +=1
        each_page[random_page] += 1
        random_page_pub = transition_model(corpus,
                                            random_page,
                                            damping_factor)
        # sampling k=1 choice 1 
        # random.choices() has 5 parameters, random_page has list ['1.html']
        # we need [0] -> return '1.html'
        random_page = random.choices(population=list(random_page_pub.keys()),
                                    weights=list(random_page_pub.values()),
                                    k=1)[0]

    for page, count in each_page.items():
        page_ranks[page] = count / n

    return page_ranks


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Iterator Pagerank
    # We use $PR(p) = \frac{1 - d}{N} + d \sum_{i \in 
    # \text{In}(p)} \frac{PR(i)}{NumLinks(i)}$
    N = len(corpus)
    page_ranks = {page: 1 / N for page in corpus}
    new_page_ranks = page_ranks.copy()

    # Use while True Very slow, Maybe fail to converge
    for _ in range(100):
        for pages in corpus:

            # $\sum_{i \in \text{In}(p)} \frac{PR(i)}{NumLinks(i)}$
            value = 0
            for page in corpus:
                links = corpus[page]
                if pages in links:
                    value += page_ranks[page] / len(links)
                elif not links:
                    value += page_ranks[page] / N

            # $\frac{1 - d}{N} + d \sum_{i \in 
            # \text{In}(p)} \frac{PR(i)}{NumLinks(i)}$
            new_page_ranks[pages] = (1 - damping_factor) /\
                                N + damping_factor * value
        
        # $\max_{p} |PR_{\text{new}}(p) - PR_{\text{old}}(p)| < 0.001$
        if max([abs(new_page_ranks[page] - page_ranks[page])
                                for page in corpus]) < 0.001:
            break
    
    page_ranks = new_page_ranks.copy()

    return page_ranks


if __name__ == "__main__":
    main()
