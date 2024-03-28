import csv
from queue import Queue

edgeFile = 'edges.csv'


def bfs(start, end):
    # Begin your code (Part 1)
    """
    First, read edges.csv and construct an adjacency list representation of a graph, 
    where each edge has a distance. It then performs BFS using queue and keeps track of the visited nodes. 
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

    q = Queue()
    visited = set()
    q.put((start, [start], 0))

    while not q.empty():
        curNode, path, curDistance = q.get()
        visited.add(curNode)
        if curNode == end:
            return path, curDistance, len(visited)
        for adj, dist in adjList.get(curNode, []):
            if adj not in visited:
                q.put((adj, path+[adj], curDistance+dist))

    return path, dist, len(visited)
    # path: list of node IDs. first start, last end.
    # End your code (Part 1)


if __name__ == '__main__':
    path, dist, num_visited = bfs(2270143902, 1079387396)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')
