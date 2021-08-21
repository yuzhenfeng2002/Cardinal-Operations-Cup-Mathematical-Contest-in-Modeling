//
//  main.cpp
//  Graph
//
//  Created by YzFENG on 2021/5/18.
//

#include <iostream>
#include <cstdlib>
#include "Graph.hpp"
#include "Tree.hpp"

using std::cout;

int main(int argc, const char * argv[]) {
    // insert code here...
    Graph graph = Graph(40 + 1);
    
    graph.addEdge(1, 22, 2.060, 0);
    graph.addEdge(1, 40, 16.758, 0);
    graph.addEdge(2, 40, 6.680, 0);
    graph.addEdge(3, 38, 8.891, 0);
    graph.addEdge(4, 38, 4.851, 0);
    graph.addEdge(5, 23, 15.344, 0);
    graph.addEdge(5, 39, 13.502, 0);
    graph.addEdge(6, 37, 4.904, 0);
    graph.addEdge(6, 39, 6.964, 0);
    graph.addEdge(7, 21, 24.871, 0);
    graph.addEdge(7, 24, 6.223, 0);
    graph.addEdge(8, 26, 1.997, 0);
    graph.addEdge(9, 10, 9.383, 0);
    graph.addEdge(9, 28, 4.272, 0);
    graph.addEdge(10, 25, 0.845, 0);
    graph.addEdge(11, 36, 1.977, 0);
    graph.addEdge(12, 34, 7.128, 0);
    graph.addEdge(13, 33, 24.214, 0);
    graph.addEdge(13, 34, 5.229, 0);
    graph.addEdge(14, 32, 11.519, 0);
    graph.addEdge(14, 33, 5.568, 0);
    graph.addEdge(15, 32, 16.328, 0);
    graph.addEdge(16, 17, 20.079, 0);
    graph.addEdge(16, 29, 14.434, 0);
    graph.addEdge(17, 18, 4.665, 0);
    graph.addEdge(19, 28, 3.470, 0);
    graph.addEdge(20, 27, 5.105, 0);
    graph.addEdge(21, 27, 29.909, 0);
    graph.addEdge(22, 23, 11.022, 0);
    graph.addEdge(22, 30, 7.620, 0);
    graph.addEdge(23, 24, 2.683, 0);
    graph.addEdge(24, 25, 13.076, 0);
    graph.addEdge(25, 26, 23.657, 0);
    graph.addEdge(26, 27, 4.706, 0);
    graph.addEdge(27, 28, 10.384, 0);
    graph.addEdge(28, 29, 8.064, 0);
    graph.addEdge(29, 30, 12.319, 0);
    graph.addEdge(30, 31, 25.451, 0);
    graph.addEdge(31, 32, 12.606, 0);
    graph.addEdge(31, 36, 7.802, 0);
    graph.addEdge(33, 35, 4.150, 0);
    graph.addEdge(34, 35, 23.135, 0);
    graph.addEdge(35, 36, 17.740, 0);
    graph.addEdge(36, 37, 19.937, 0);
    graph.addEdge(37, 38, 3.126, 0);
    graph.addEdge(39, 40, 6.787, 0);

    // graph.printGraph();
    
    for (int i = 1; i <= 21; i++) {
        for (int j = 1; j <= 21; j++) {
            printf("<%d, %d>\n", i, j);
            try {
                graph.printShortestPath(i, j, "Dijkstra");
            } catch (const char* msg) {
                std::cout << msg << std::endl;
            }
        }
    }
    return 0;
}
