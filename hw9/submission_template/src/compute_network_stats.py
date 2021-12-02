import argparse
import json
import os

import networkx as nx

def main(args):
    input_path = os.path.abspath(args.input)
    with open(input_path, 'r') as f:
        interactions = json.load(f)

    g = nx.Graph()
    for pony_a in interactions:
        for pony_b in interactions[pony_a]:
            g.add_edge(pony_a, pony_b, weight=interactions[pony_a][pony_b])

    stats = {}

    top_degree = sorted(list(g.degree()), key=lambda x: x[1], reverse=True)
    stats['most_connected_by_num'] = [char for char, _ in top_degree][:3]

    top_degree_weight = sorted(list(g.degree(weight='weight')), key=lambda x: x[1], reverse=True)
    stats['most_connected_by_weight'] = [char for char, _ in top_degree_weight][:3]

    top_betweenness = sorted(nx.algorithms.centrality.betweenness_centrality(g).items(), key=lambda x: x[1], reverse=True)
    stats['most_central_by_betweenness'] = [char for char, _ in top_betweenness][:3]

    output_path = os.path.abspath(args.output)
    out_dir_path = os.path.dirname(output_path)

    if not os.path.exists(out_dir_path):
        os.mkdir(out_dir_path)

    with open(output_path, 'w') as f:
        json.dump(stats, f, indent=4)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input')
    parser.add_argument('-o', '--output')
    args = parser.parse_args()

    main(args)