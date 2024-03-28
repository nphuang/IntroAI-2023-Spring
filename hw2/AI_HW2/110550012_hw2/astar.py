import csv
edgeFile = 'edges.csv'
heuristicFile = 'heuristic.csv'
from queue import PriorityQueue

def astar(start, end):
    # Begin your code (Part 4)
    """
    store edge information in adjList and store heuristic in dictionary, 
    where each node is a key and its value is heuristic value for reaching endNode.
    Initialize priority queue with startNode, distance from the start (0), 
    its heuristic estimate, and path (startNode).
    Iteratively retrieve the node with the lowest estimated cost from the priority queue and 
    expand it by adding its adjacent nodes to pq with distance to the adjacent node + the heuristic value for reaching endNode.
    Continue until the endNode is reached, and return.
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

    heuristic = {}
    with open(heuristicFile, newline='') as csvFile:
        rows = csv.reader(csvFile)
        header = next(rows)  # skip first row(header)
        endIndex = header.index(str(end))
        for row in rows:
            node = int(row[0])
            heuristic[node] = float(row[endIndex])
    
    pq = PriorityQueue()
    visited = set()
    h = heuristic[start]
    pq.put((h, 0, start, [start]))
    while not pq.empty():
        _, curDistance, curNode, path = pq.get()
        visited.add(curNode)
        if curNode == end:
            return path, curDistance, len(visited)
        for adj, dist in adjList.get(curNode, []):
            if adj not in visited:
                h = heuristic[adj]
                pq.put((curDistance+dist+h, curDistance+dist, adj, path+[adj]))
    
    return path, curDistance, len(visited)
    # End your code (Part 4)


if __name__ == '__main__':
    path, dist, num_visited = astar(2270143902, 1079387396)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')
