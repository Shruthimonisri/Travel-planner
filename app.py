from flask import Flask, render_template, request
import heapq
import networkx as nx
import matplotlib.pyplot as plt

app = Flask(__name__)

# Graph 
graph = {
    'Chennai Central Railway Station': {'Marina Beach': 5, 'Tidel Park': 10},
    'Marina Beach': {'Chennai Central Railway Station': 5, 'Fort St. George': 3, 'Santhome Cathedral Basilica': 4},
    'Tidel Park': {'Chennai Central Railway Station': 10, 'Phoenix Marketcity': 5, 'Guindy National Park': 4},
    'Fort St. George': {'Marina Beach': 3, 'Valluvar Kottam': 7},
    'Santhome Cathedral Basilica': {'Marina Beach': 4, 'Mylapore': 2},
    'Phoenix Marketcity': {'Tidel Park': 5, 'Guindy National Park': 3, 'Chennai Trade Centre': 4},
    'Guindy National Park': {'Tidel Park': 4, 'Phoenix Marketcity': 3, 'Chennai Trade Centre': 6},
    'Mylapore': {'Santhome Cathedral Basilica': 2, 'Kapaleeshwarar Temple': 1},
    'Chennai Trade Centre': {'Phoenix Marketcity': 4, 'Guindy National Park': 6},
    'Valluvar Kottam': {'Fort St. George': 7},
    'Kapaleeshwarar Temple': {'Mylapore': 1}
}

def dijkstra(graph, start, end):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    pq = [(0, start)]
    shortest_path = {node: None for node in graph}

    while pq:
        current_distance, current_node = heapq.heappop(pq)
        if current_distance > distances[current_node]:
            continue
        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                shortest_path[neighbor] = current_node
                heapq.heappush(pq, (distance, neighbor))

    path = []
    while end:
        path.insert(0, end)
        end = shortest_path[end]
    return path, distances[path[-1]]

def visualize_graph(graph, path, file_path='static/graph.png'):
    G = nx.Graph()
    for node, edges in graph.items():
        for connected_node, weight in edges.items():
            G.add_edge(node, connected_node, weight=weight)
    
    pos = nx.spring_layout(G, k=2, scale=2, seed=42)
    nx.draw(G, pos, with_labels=True, node_size=3000, node_color='lightblue', font_size=10, font_weight='bold')
    nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): d['weight'] for u, v, d in G.edges(data=True)})
    
    path_edges = list(zip(path, path[1:]))
    nx.draw_networkx_nodes(G, pos, nodelist=path, node_color='orange')
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=2)
    
    plt.title("Graph of Important Places in Chennai")
    plt.savefig(file_path)
    plt.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    start = request.form['start']
    end = request.form['end']
    path, distance = dijkstra(graph, start, end)
    
    visualize_graph(graph, path, file_path='static/graph.png')

    return render_template('result.html', path=path, distance=distance, start=start, end=end)

if __name__ == '__main__':
    app.run(debug=True)
