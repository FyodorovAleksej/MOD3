from pprint import pprint

import query_utils as qu
from GraphWrapper import GraphWrapper


def initGraph():
    wrapper = GraphWrapper()

    wrapper.add_node("2000")  # 0
    wrapper.add_node("1000")  # 1
    wrapper.add_node("2010")  # 2
    wrapper.add_node("1010")  # 3
    wrapper.add_node("2011")  # 4
    wrapper.add_node("1001")  # 5
    wrapper.add_node("1011")  # 6
    wrapper.add_node("2111")  # 7
    wrapper.add_node("1111")  # 8
    wrapper.add_node("2211")  # 9
    wrapper.add_node("1211")  # 10

    wrapper.add_edge("2000", "1000", "1") \
 \
        .add_edge("1000", "2010", "1") \
        .add_edge("2010", "1000", "q1") \
        .add_edge("2011", "1000", "q1*q2") \
 \
        .add_edge("2010", "1010", "p1") \
        .add_edge("1010", "2010", "q1") \
        .add_edge("1011", "2010", "q1*q2") \
        .add_edge("1001", "2010", "q2") \
 \
        .add_edge("1001", "2011", "p2") \
        .add_edge("2011", "1001", "q1*p2") \
 \
        .add_edge("2011", "1010", "p1*q2") \
        .add_edge("2011", "1011", "p1*p2") \
        .add_edge("1010", "2011", "p1") \
        .add_edge("1011", "2011", "q1*p2+p1*q2") \
        .add_edge("1111", "2011", "q1*q2") \
 \
        .add_edge("1011", "2111", "p1*p2") \
        .add_edge("2111", "1011", "q1*p2+p1*q2") \
        .add_edge("2211", "1011", "q1*q2") \
 \
        .add_edge("2111", "1010", "q1*q2") \
        .add_edge("2111", "1111", "p1*p2") \
        .add_edge("1111", "2111", "q1*p2+p1*q2") \
        .add_edge("1211", "2111", "q1*q2") \
 \
        .add_edge("1111", "2211", "p1*p2") \
        .add_edge("2211", "1111", "q1*p2+p1*q2") \
 \
        .add_edge("2211", "1211", "p1*p2") \
        .add_edge("1211", "2211", "1-q1*q2")

    wrapper.build()
    return wrapper


if __name__ == "__main__":
    wrapper = initGraph()

    p1 = 0.6
    p2 = 0.5
    q1 = 1 - p1
    q2 = 1 - p2

    pprint(qu.ref_eval(wrapper, q1, q2, p1, p2))
    result = qu.gaus_refs(wrapper, q1, q2, p1, p2)
    pprint(result)

    LOST_NODES = ["1211"]
    PROBABILITY_LOST_NODES = ["p1*p2"]

    pprint("Success service Q = " + str(
        qu.service_probability(wrapper, LOST_NODES, qu.ev_l(PROBABILITY_LOST_NODES, q1, q2, p1, p2), result)))

    COUNT_MASK = [False, True, True, True]
    pprint("Average count of queries Lc = " + str(qu.average_count(wrapper, result, COUNT_MASK)))

    COUNT_MASK = [False, True, False, False]
    pprint("Average len of pool Lr = " + str(qu.average_count(wrapper, result, COUNT_MASK)))
