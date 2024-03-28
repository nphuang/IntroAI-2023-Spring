import csv
edgeFile = 'edges.csv'
heuristicFile = 'heuristic.csv'
from queue import PriorityQueue
import pandas as pd

def astar_time(start, end):
    # Begin your code (Part 6)
    """
    Basically same as astar.py, the main difference is the fastest time to travel an edge is calculated
    and stored instead of distance, import pandas to get the maximum speed limit,
    and the heuristic value is evaluted by dividing it by the maximum speed limit, that is estimated time.
    """
    adjList = {}
    with open(edgeFile, newline='') as csvFile:
        rows = csv.reader(csvFile)
        next(rows) # skip first row(header)
        for row in rows:
            startNode = int(row[0])
            endNode = int(row[1])
            distance = float(row[2])
            speedLim = float(row[3])
            time = distance / (speedLim * 1000 / 3600)  # calculate the fastest time to travel the edge
            if startNode not in adjList:
                adjList[startNode] = []
            adjList[startNode].append((endNode, time))  # store the time instead of the distance
    
    df = pd.read_csv(edgeFile)
    MAX = float(df['speed limit'].max())
    MAX = MAX * 1000 / 3600
    heuristic = {}
    with open(heuristicFile, newline='') as csvFile:
        rows = csv.reader(csvFile)
        header = next(rows)  # skip first row(header)
        endIndex = header.index(str(end))
        for row in rows:
            node = int(row[0])
            heuristic[node] = float(row[endIndex]) / MAX

    pq = PriorityQueue()
    visited = set()
    h = heuristic[start]
    pq.put((h, 0, start, [start]))
    while not pq.empty():
        h, t, curNode, path = pq.get()
        visited.add(curNode)
        if curNode == end:
            return path, t, len(visited)
        for adj, edgeTime in adjList.get(curNode, []):
            if adj not in visited:
                h = heuristic[adj]
                pq.put((t + edgeTime + h, t + edgeTime, adj, path + [adj]))
    # time :float, the time of path
    # End your code (Part 6)


if __name__ == '__main__':
    path, time, num_visited = astar_time(2270143902, 1079387396)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total second of path: {time}')
    print(f'The number of visited nodes: {num_visited}')
