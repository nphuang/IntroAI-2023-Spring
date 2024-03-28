import csv
edgeFile = 'edges.csv'
from queue import PriorityQueue

def ucs(start, end):
    # Begin your code (Part 3)
    """
    First, read edges.csv and construct an adjacency list representation of a graph,
    where each edge has a distance. It then performs UCS using priority queue and keeps track of the visited nodes.
    initializes pq with a tuple current distance from the start node (0), starNode, and a list containing startNode.
    explores the graph by repeatedly selecting connected edge with the lowest cost that have not been visited.
    If the end node is found, returns path, distance, and number of nodes visited.
    """
    adjList = {}
    with open(edgeFile, newline='') as csvFile:
        rows = csv.reader(csvFile)
        next(rows)  # skip first row(header)
        for row in rows:
            startNode = int(row[0])
            endNode = int(row[1])
            distance = float(row[2])
            if startNode not in adjList:
                adjList[startNode] = []
            adjList[startNode].append((endNode, distance))

    pq = PriorityQueue()
    visited = set()
    pq.put((0, start, [start])) # Maintaining order based on distance

    while not pq.empty():
        curDistance, curNode, path = pq.get()
        visited.add(curNode)
        if curNode == end:
            return path, curDistance, len(visited)
        for adj, dist in adjList.get(curNode, []):
            if adj not in visited:
                pq.put((curDistance+dist, adj, path+[adj]))

    return path, dist, len(visited)
    # End your code (Part 3)


if __name__ == '__main__':
    path, dist, num_visited = ucs(2270143902, 1079387396)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')
