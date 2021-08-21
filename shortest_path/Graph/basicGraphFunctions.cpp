//
//  basicGraphFunctions.cpp
//  Data-Structures-and-Algorithms
//
//  Created by YzFENG on 2021/6/1.
//

#include "Graph.hpp"

Graph::Graph(int numOfNodes)
{
    graph = vector<vector<pair<int, double>>>(numOfNodes);
    edges = vector<tuple<int, int, double>>();
}

void Graph::addEdge(int i, int j, double length, bool isDirected)
{
    graph[i].push_back(std::make_pair(j, length));
    if (!isDirected) {
        graph[j].push_back(std::make_pair(i, length));
    }
    edges.push_back(tuple<int, int, double>{i, j, length});
}

void Graph::printGraph()
{
    for (int i = 0; i < graph.size(); i++) {
        printf("Node %d: ", i);
        if (graph.at(i).size() == 0) {
            printf("no neighbour.\n");
            continue;
        }
        for (int j = 0; j < graph.at(i).size(); j++) {
            printf("%d(%.2f) ", graph.at(i).at(j).first, graph.at(i).at(j).second);
        }
        printf("\n");
    }
}
