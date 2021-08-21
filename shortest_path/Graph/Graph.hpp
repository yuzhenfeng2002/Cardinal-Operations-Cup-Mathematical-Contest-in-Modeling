//
//  Graph.hpp
//  Data-Structures-and-Algorithms
//
//  Created by YzFENG on 2021/5/18.
//

#ifndef Graph_hpp
#define Graph_hpp

#include <stdio.h>
#include <queue>
#include <stack>
#include <vector>
#include <list>
#include <string>
#include <algorithm>

using std::queue;
using std::stack;
using std::vector;
using std::list;
using std::pair;
using std::tuple;
using std::string;
using std::priority_queue;

class Graph
{
private:
    const int null = -1;
    const int visited = -2;
    const int explored = -3;
    const int inf = 65535;
    vector<vector<pair<int, double>>> graph; // pair<nodeIndex, length>
    vector<tuple<int, int, double>> edges; // tuple<u, v, length>
    // if it is a directed graph, u means O, v means D
    // else u and v have no difference

    vector<pair<int, double>> DijkstraShortestPath(int s);
    void printPath(int sourceNode, int destNode, vector<pair<int, double>> preEdgeVec);
public:
    Graph(int numOfNodes);
    void addEdge(int i, int j, double length=1, bool isDirected=1);
    void printGraph();
    double printShortestPath(int sourceNode, int destNode, string mode);
};

#endif /* Graph_hpp */
