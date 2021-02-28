from dsc40graph import UndirectedGraph, DirectedGraph, DoesNotExistError

import pytest


def test_undirected_add_node_and_list():
    # given
    g = UndirectedGraph()

    # when
    g.add_node(1)
    g.add_node("a")
    g.add_node(42)

    # then
    assert set(g.nodes) == {1, 42, "a"}


def test_undirected_graph_add_edge_adds_node():
    # given
    g = UndirectedGraph()

    # when
    g.add_edge(1, 3)

    # then
    assert 1 in g.adj
    assert 3 in g.adj


def test_undirected_add_edge_twice_only_adds_one_edge():
    # given
    g = UndirectedGraph()

    # when
    g.add_edge(1, 3)
    g.add_edge(3, 1)

    # then
    [edge] = g.edges
    assert set(edge) == {1, 3}


def test_directed_add_edge_and_opposite():
    # given
    g = DirectedGraph()

    # when
    g.add_edge(1, 3)
    g.add_edge(3, 1)

    # then
    assert set(g.edges) == {(1, 3), (3, 1)}


def test_undirected_neighbors():
    # given
    g = UndirectedGraph()

    # when
    g.add_edge(1, 3)
    g.add_edge(3, 1)
    g.add_edge(5, 1)
    g.add_edge(1, 6)

    # then
    assert set(g.neighbors(1)) == {3, 5, 6}
    assert set(g.neighbors(6)) == {1}


def test_directed_successors():
    # given
    g = DirectedGraph()

    # when
    g.add_edge(1, 3)
    g.add_edge(3, 1)
    g.add_edge(5, 1)
    g.add_edge(1, 6)

    # then
    assert set(g.successors(1)) == {3, 6}
    assert set(g.successors(6)) == set()


def test_directed_predecessors():
    # given
    g = DirectedGraph()

    # when
    g.add_edge(1, 3)
    g.add_edge(3, 1)
    g.add_edge(5, 1)
    g.add_edge(1, 6)

    # then
    assert set(g.predecessors(1)) == {3, 5}
    assert set(g.predecessors(6)) == {1}


def test_undirected_has_edge():
    # given
    g = UndirectedGraph()

    # when
    g.add_edge(1, 3)
    g.add_edge(3, 1)
    g.add_edge(5, 1)
    g.add_edge(1, 6)

    # then
    assert (1, 3) in g.edges
    assert (3, 1) in g.edges
    assert (5, 1) in g.edges
    assert (1, 5) in g.edges
    assert (1, 999) not in g.edges


def test_undirected_number_of_edges():
    # given
    g = UndirectedGraph()

    # when
    g.add_edge(1, 3)
    g.add_edge(3, 1)
    g.add_edge(5, 1)
    g.add_edge(1, 6)

    assert len(g.edges) == 3


def test_add_node_already_graph_does_nothing():
    # given
    g = UndirectedGraph()

    # when
    g.add_edge(1, 3)
    g.add_edge(3, 1)
    g.add_edge(5, 1)

    g.add_node(3)

    assert len(g.neighbors(3)) == 1
    assert len(g.nodes) == 3


def test_directed_has_edge():
    # given
    g = DirectedGraph()

    # when
    g.add_edge(1, 3)
    g.add_edge(3, 1)
    g.add_edge(5, 1)
    g.add_edge(1, 6)

    # then
    assert (1, 3) in g.edges
    assert (3, 1) in g.edges
    assert (5, 1) in g.edges
    assert (1, 5) not in g.edges


def test_remove_node_removes_edges_too_directed():
    # given
    g = DirectedGraph()

    # when
    g.add_edge(1, 3)
    g.add_edge(3, 1)
    g.add_edge(5, 1)
    g.add_edge(1, 6)
    g.add_edge(1, 1)
    g.remove_node(1)

    assert (1, 3) not in g.edges
    assert (3, 1) not in g.edges
    assert (5, 1) not in g.edges
    assert len(g.edges) == 0


def test_remove_node_removes_edges_too_undirected():
    # given
    g = UndirectedGraph()

    # when
    g.add_edge(1, 3)
    g.add_edge(3, 1)
    g.add_edge(5, 1)
    g.add_edge(1, 6)
    g.remove_node(1)

    assert (1, 3) not in g.edges
    assert (3, 1) not in g.edges
    assert (5, 1) not in g.edges
    assert len(g.edges) == 0


def test_remove_missing_node_raises_undirected():
    # given
    g = UndirectedGraph()
    g.add_node(1)
    g.add_node(2)
    g.add_node(3)

    # when
    with pytest.raises(DoesNotExistError):
        g.remove_node(4)


def test_remove_missing_node_raises_directed():
    # given
    g = DirectedGraph()
    g.add_node(1)
    g.add_node(2)
    g.add_node(3)

    # when
    with pytest.raises(DoesNotExistError):
        g.remove_node(4)


def test_undirected_graphs_have_no_self_loops():
    # given
    g = UndirectedGraph()

    # when
    with pytest.raises(ValueError):
        g.add_edge(1, 1)


def __edge_view_returns_false_if_node_isnt_in_graph():
    # given
    g = DirectedGraph()

    # when
    g.add_edge(1, 3)
    g.add_edge(3, 1)

    # then
    assert (5, 2) not in g


def test_remove_edge_undirected():
    # given
    g = UndirectedGraph()
    g.add_edge(1, 2)
    g.add_edge(2, 3)
    g.add_edge(3, 1)

    # when
    g.remove_edge(2, 1)

    # then
    assert (1, 2) not in g.edges
    assert (2, 1) not in g.edges
    assert len(g.edges) == 2
    assert len(g.nodes) == 3


def test_remove_edge_directed():
    # given
    g = DirectedGraph()
    g.add_edge(1, 2)
    g.add_edge(2, 1)
    g.add_edge(2, 3)
    g.add_edge(3, 1)

    # when
    g.remove_edge(1, 2)

    # then
    assert (1, 2) not in g.edges
    assert (2, 1) in g.edges
    assert len(g.edges) == 3
    assert len(g.nodes) == 3


def test_remove_missing_edge_raises_undirected():
    # given
    g = UndirectedGraph()
    g.add_edge(1, 2)
    g.add_edge(2, 3)
    g.add_edge(3, 1)

    # when
    with pytest.raises(DoesNotExistError):
        g.remove_edge(2, 4)


def test_remove_missing_edge_raises_directed():
    # given
    g = DirectedGraph()
    g.add_edge(1, 2)
    g.add_edge(2, 3)
    g.add_edge(3, 1)

    # when
    with pytest.raises(DoesNotExistError):
        g.remove_edge(2, 4)


def test_arbitrary_node():
    # given
    g = UndirectedGraph()
    g.add_edge(1, 2)
    g.add_edge(2, 3)
    u = g.arbitrary_node()
    assert u in g.nodes


def test_arbitrary_node_raises_if_graph_empty():
    # given
    g = UndirectedGraph()
    with pytest.raises(DoesNotExistError):
        u = g.arbitrary_node()
