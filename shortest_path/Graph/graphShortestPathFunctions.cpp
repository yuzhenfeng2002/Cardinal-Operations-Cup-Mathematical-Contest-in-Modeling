//
//  graphShortestPathFunctions.cpp
//  Data-Structures-and-Algorithms
//
//  Created by YzFENG on 2021/6/6.
//

#include <stdio.h>
#include "Graph.hpp"

void Graph::printPath(int sourceNode, int destNode, vector<pair<int, double>> nodeDistanceVec)
{
    if (sourceNode == destNode) {
        printf("%d -> ", sourceNode);
        return;
    }
    else if (nodeDistanceVec.at(destNode).first == null)
    {
        throw "No Path!";
    }
    else
    {
        printPath(sourceNode, nodeDistanceVec.at(destNode).first, nodeDistanceVec);
        printf("%d -> ", destNode);
        return;
    }
}

double Graph::printShortestPath(int sourceNode, int destNode, string mode)
{
    vector<pair<int, double>> nodeDistanceVec;
    if (mode == "Dijkstra")
    {
        nodeDistanceVec = DijkstraShortestPath(sourceNode);
    }
    printf("The distance between the source and destination is %.3f.\n",
           nodeDistanceVec.at(destNode).second);
    printf("The path is:\n");
    printPath(sourceNode, destNode, nodeDistanceVec);
    printf("(end)\n");
    return nodeDistanceVec.at(destNode).second;
}

vector<pair<int, double>> Graph::DijkstraShortestPath(int s)
{
    // copied from Prim's minimum spanning tree algorithm
    vector<tuple<double, int, bool>> nodeVec = vector<tuple<double, int, bool>>(graph.size(), tuple<double, int, bool>(inf, null, true)); // tuple<key, π, isInQ>
    
    // initialize the nodeVec and the priority queue
    nodeVec.at(s) = std::make_tuple(0, null, true);
    auto cmp = [=] (tuple<int, double> a, tuple<int, double> b) -> bool {
        return std::get<1>(a) > std::get<1>(b);
    }; // the lambda function to compare tuple<nodeIndex, key> by key
    priority_queue<tuple<int, double>, vector<tuple<int, double>>, decltype(cmp)> nodeQ(cmp); // tuple<nodeIndex, key>
    nodeQ.push(std::make_tuple(s, 0));
    while (!nodeQ.empty()) {
        tuple<int, double> node = nodeQ.top();
        nodeQ.pop();
        int u = std::get<0>(node);
        // if u should not be in Q, just pass
        if (std::get<2>(nodeVec.at(u)) == false) {
            continue;
        }
        std::get<2>(nodeVec.at(u)) = false; // set isInQ false because the node has been included in the tree
        
        for (int j = 0; j < graph.at(u).size(); j++) {
            int v = graph.at(u).at(j).first;
            double length = graph.at(u).at(j).second;

            if (std::get<0>(nodeVec.at(u)) + length < std::get<0>(nodeVec.at(v))) {
                std::get<0>(nodeVec.at(v)) = std::get<0>(nodeVec.at(u)) + length;
                std::get<1>(nodeVec.at(v)) = u;
                nodeQ.push(std::make_tuple(v, std::get<0>(nodeVec.at(v))));
            }
        }
    }
    
    vector<pair<int, double>> result = vector<pair<int, double>>();
    for (int i = 0; i < nodeVec.size(); i++) {
        result.push_back(std::make_pair(std::get<1>(nodeVec.at(i)), std::get<0>(nodeVec.at(i))));
    }
    return result;
}
