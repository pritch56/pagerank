import os
from bs4 import BeautifulSoup
import networkx as nx

def build_graph_and_rank(upload_folder):
    G = nx.DiGraph()
    file_map = {}

    # Parse files and collect links
    for file in os.listdir(upload_folder):
        if file.endswith('.html'):
            path = os.path.join(upload_folder, file)
            with open(path, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f, 'html.parser')
                links = [a['href'] for a in soup.find_all('a', href=True)]
                file_map[file] = links

    # Build graph
    for src, links in file_map.items():
        for link in links:
            if link in file_map:
                G.add_edge(src, link)

    # Compute PageRank
    pr = nx.pagerank(G)
    return pr