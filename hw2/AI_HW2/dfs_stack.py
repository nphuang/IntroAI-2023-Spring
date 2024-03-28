import csv
edgeFile = 'edges.csv'


def dfs(start, end):
    # Begin your code (Part 2)
    """
    First, read edges.csv and construct an adjacency list representation of a graph, 
    where each edge has a distance.Then, perform DFS using stack to keep track of nodes to be 
    visited next. Initialize the stack with a tuple containing startNode, a list with the startNode, and a distance of 0.
    As long as the stack is not empty, it pops element from the stack and adds its node to the set of visited nodes. 
    If the node is endNode, returns the path, distance, and num_visited. 
    Otherwise, it loops through the adjacent nodes of the current node in the adjacency list, 
    adding them to the path and pushing them onto the stack if they have not been visited yet. 
    """
    adjList = {}
    with open(edgeFile, newline='') as csvFile:
        rows = csv.reader(csvFile)
        next(rows)  
        for row in rows:
            startNode = int(row[0])
            endNode = int(row[1])
            distance = float(row[2])
            if startNode not in adjList:
                adjList[startNode] = []
            adjList[startNode].append((endNode, distance))

    stack = [(start, [start], 0)]
    visited = set()
    while stack:
        curNode, path, curDistance = stack.pop()
        visited.add(curNode)
        if curNode == end:
            return path, curDistance, len(visited)
        for adj, dist in adjList.get(curNode, []):
            if adj not in visited:
                stack.append((adj, path+[adj], curDistance+dist))

    return path, dist, len(visited)
    # End your code (Part 2)


if __name__ == '__main__':
    path, dist, num_visited = dfs(2270143902, 1079387396)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')
