import numpy as np

def references(wrapper):
    res = []
    for i in range(len(wrapper.get_nodes())):
        d = wrapper.probability_to_node_index(i)
        result = "P" + str(i) + " = "
        result += " + ".join("P" + str(p) + "*(" + d[p] + ")" for p in d.keys()) if len(d) != 0 else "0"
        res.append(result)
    return res


def ev(expression, q1, q2, p1, p2):
    cur = expression
    cur = cur.replace("q1", str(q1))
    cur = cur.replace("q2", str(q2))
    cur = cur.replace("p1", str(p1))
    cur = cur.replace("p2", str(p2))
    return eval(cur)


def ev_l(expressions, q1, q2, p1, p2):
    return [ev(i, q1, q2, p1, p2) for i in expressions]


def ref_eval(wrapper, q1, q2, p1, p2):
    res = []
    for i in range(len(wrapper.get_nodes())):
        d = wrapper.probability_to_node_index(i)
        result = "P" + str(i) + " = "
        result += " + ".join("P" + str(p) + "*(" + str(ev(d[p], q1, q2, p1, p2)) + ")" for p in d.keys()) if len(
            d) != 0 else "0"
        res.append(result)
    return res


def gaus_refs(wrapper, q1, q2, p1, p2):
    results = []
    lines = []
    for i in range(len(wrapper.get_nodes())):
        line = []
        d = wrapper.probability_to_node_index(i)
        for j in range(len(wrapper.get_nodes())):
            if j in d.keys():
                line.append(ev(d[j], q1, q2, p1, p2))
            elif i == j:
                line.append(-1)
            else:
                line.append(0)
        lines.append(line)
        results.append(0)

    remove_index = len(wrapper.get_nodes())  # DANGER ZONE
    lines = lines[:remove_index - 1] + lines[remove_index:]  # DANGER ZONE
    results = results[:remove_index - 1] + results[remove_index:]  # DANGER ZONE

    lines.append([1 for _ in range(len(wrapper.get_nodes()))])
    results.append(1)
    MTX = np.array(lines)
    RES = np.array(results)

    # pprint(MTX) # verbose output
    # pprint(RES) # verbose output
    return np.linalg.solve(MTX, RES)


def service_probability(wrapper, lost_nodes, probability_lost, result):
    nodes = wrapper.get_nodes()
    return 1 - sum(result[nodes.index(lost_nodes[i])] * probability_lost[i] for i in range(len(lost_nodes)))


def average_count(wrapper, result, mask):
    nodes = wrapper.get_nodes()
    return sum(sum([int(nodes[i][j]) for j in range(len(nodes[i])) if mask[j]]) * result[i] for i in range(len(nodes)))
