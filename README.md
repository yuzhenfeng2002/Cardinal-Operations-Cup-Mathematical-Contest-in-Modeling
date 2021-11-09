2021年度“杉数杯”数学建模联赛B题。利用Gurobi求解器实现B&C算法，求解混合整数规划模型，解决（M）TSP问题。

`data/`:论文所用到的数据，包括：
`distance.csv`（巡检点之间最短路径长度矩阵）、
`distance`（二进制文件，用于Python加载）、
`expected_service_time.csv`（巡检点发生故障后的处理时间）

`shortest_path/`:求解巡检点之间最短路径的代码

`optimization/`:模型求解所用的代码，包括：
`preprocessing_distance`（对距离数据的预处理）、
`simple_vehicle_routing_problem`（第一问代码）、
`vehicle_routing_problem_with_service_time`（第二问带期望处理时间模型代码）、
`vehicle_routing_problem_with_failure_occurrence`（第二问基于真实发生故障的路径再规划模型代码）、
`location_routing_problem`（第三问代码）、
`vehicle_routing_problem_with_multi_time_periods`（第四问代码）

`result/`: 结果输出，包括：
`RESULT_P1`（第一问）、
`RESULT_P2_1`（第二问带期望处理时间模型结果输出）、
`RESULT_P2_2_1`（第二问基于真实发生故障的路径再规划模型的算例1结果输出）、
`RESULT_P2_2_2`（第二问基于真实发生故障的路径再规划模型的算例2结果输出）、
`RESULT_P3_1`（第三问寻找最佳常驻点结果输出）、
`RESULT_P3_2`（第三问以1作为常驻点结果输出）、
`RESULT_P4_1`（第四问模型基于小规模巡检点的结果输出）、
`RESULT_P4_2`（第一问模型基于小规模巡检点的结果输出）、
`SHORTEST_PATHS`（最短路径求解结果输出）
