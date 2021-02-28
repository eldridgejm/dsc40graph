"""Efficient undirected and directed graph data structures."""


MAX_NODES_DISPLAYED = 20
MAX_EDGES_DISPLAYED = 10


class Error(Exception):
    """Base class for all errors specific to this module."""


class DoesNotExistError(Error):
    """The node/edge does not exist."""


def _take(iterable, n):
    for i, x in enumerate(iterable):
        if i >= n:
            break
        yield x


class _NodesView:
    """A view into a graph's nodes."""

    def __init__(self, nodes):
        self._nodes = nodes

    def __contains__(self, node):
        """Membership query."""
        return node in self._nodes

    def __len__(self):
        return len(self._nodes)

    def __iter__(self):
        yield from self._nodes

    def __repr__(self):
        limit = MAX_NODES_DISPLAYED
        over_limit = len(self._nodes) > limit

        if over_limit:
            nodes_to_print = list(_take(self._nodes, MAX_NODES_DISPLAYED))
            suffix = "..."
        else:
            nodes_to_print = self._nodes
            suffix = ""

        node_string = ", ".join(repr(node) for node in nodes_to_print) + suffix
        return f"<{len(self._nodes)} nodes: {node_string}>"


class _EdgeView:
    """Base class for views into a graph's edges."""

    def __init__(self, adj, number_of_edges):
        self._adj = adj
        self._number_of_edges = number_of_edges

    def __contains__(self, edge):
        """Perform an edge query.
        
        Average case time complexity: Theta(1)
        """
        u, v = edge
        try:
            return v in self._adj[u]
        except KeyError:
            return False

    def __len__(self):
        """The number of edges.

        Average case time complexity: Theta(1)
        """
        return self._number_of_edges

    def __repr__(self):
        limit = MAX_EDGES_DISPLAYED
        over_limit = len(self) > limit

        if over_limit:
            edges_to_print = list(_take(self, MAX_EDGES_DISPLAYED))
            suffix = "..."
        else:
            edges_to_print = list(self)
            suffix = ""

        edges_string = ", ".join(repr(edge) for edge in edges_to_print) + suffix
        return f"<{len(self)} edges: {edges_string}>"


class _UndirectedEdgeView(_EdgeView):
    """A view into an undirected graph's edges."""

    def __iter__(self):
        """Iterate through the edges.

        Each edge in the graph is yielded exactly once as a pair whose order is
        arbitrary. That is, suppose that a graph has an edge between node 1 and
        node 2. Then the pair (1,2) may be yielded, or (2,1), but not both.

        Yields
        ------
        edge
            The edge as a pair of labels.

        """
        seen = set()

        for u, neighbors in self._adj.items():
            for v in neighbors:
                edge = frozenset((u, v))
                if edge not in seen:
                    seen.add(edge)
                    yield (u, v)
                else:
                    continue


class _DirectedEdgeView(_EdgeView):
    def __iter__(self):
        """Iterate through the edges.

        Yields
        ------
        edge
            The edge as an ordered pair of labels.

        """
        for u, neighbors in self._adj.items():
            for v in neighbors:
                yield (u, v)


class _Graph:
    """Base class for graph data structures."""

    def __init__(self, _edge_view_factory):
        self.adj = dict()
        self._number_of_edges = 0
        self._edge_view_factory = _edge_view_factory

    def __repr__(self):
        return f"<{self.__class__.__name__} with {len(self.nodes)} nodes and {len(self.edges)} edges>"

    def add_node(self, label):
        """
        Add a node with the given label.

        If the node already exists, nothing is done.

        Average case time complexity: Theta(1).

        Parameters
        ----------
        label
            The label of the node.

        """
        if label not in self.nodes:
            self.adj[label] = set()

    @property
    def nodes(self):
        """A view into the graph's nodes.

        Supports average case constant time node query. 

        Example
        -------
        >>> graph = UndirectedGraph()
        >>> graph.add_node('Red')
        >>> graph.add_node('Blue')
        >>> graph.add_node('Green')
        >>> 'Orange' in graph.nodes
        False
        >>> 'Red' in graph.nodes
        True
        >>> len(graph.nodes)
        3

        """
        return _NodesView(self.adj.keys())

    def arbitrary_node(self):
        """Return an arbitrary graph node. How the node is chosen is undefined.

        Takes Theta(1) time.

        Raises
        ------
        DoesNotExistError
            If the graph is empty.

        Example
        -------
        >>> graph = UndirectedGraph()
        >>> graph.add_node(1)
        >>> graph.add_node(2)
        >>> graph.add_node(3)
        >>> graph.arbitrary_node()
        2

        """
        try:
            return next(iter(self.nodes))
        except StopIteration:
            raise DoesNotExistError("The graph is empty.")

    @property
    def edges(self):
        """A view into the graph's edges.

        Supports average case constant time edge query.

        Example
        -------
        >>> graph = UndirectedGraph()
        >>> graph.add_edge('Red', 'Blue')
        >>> graph.add_edge('Blue', 'Green')
        >>> ('Red', 'Blue') in graph.edges
        True
        >>> ('Blue', 'Red') in graph.edges
        True
        >>> ('Red', 'Green') in graph.edges
        False
        
        """
        return self._edge_view_factory(self.adj, self._number_of_edges)


class UndirectedGraph(_Graph):
    def __init__(self, _edge_view_factory=_UndirectedEdgeView):
        super().__init__(_edge_view_factory)

    def add_edge(self, u_label, v_label):
        """Add an undirected edge to the graph.

        If the edge already exists, nothing is done.

        Average case time complexity: Theta(1).

        Parameters
        ----------
        u_label
            Label of one of the nodes in the edge.
        v_label
            Label of the other node in the edge.

        Notes
        -----
        If either of the nodes is not in the graph, the node is created.

        Raises
        ------
        ValueError
            If an attempt to add a self-loop is made. Undirected graphs do
            not have self-loops.

        """
        if u_label == v_label:
            raise ValueError("Undirected graphs have no self loops.")

        for x in {u_label, v_label}:
            if x not in self.adj:
                self.adj[x] = set()

        if (u_label, v_label) not in self.edges:
            self.adj[u_label].add(v_label)
            self.adj[v_label].add(u_label)
            self._number_of_edges += 1

    def remove_node(self, label):
        """Remove a node grom the graph.

        Average case time complexity: Theta(# of neighbors)
        
        Parameters
        ----------
        label
            The label of the node to be removed.

        Raises
        ------
        DoesNotExistError
            If the node is not in the graph.

        """
        try:
            neighbors = self.adj[label]
        except KeyError:
            raise DoesNotExistError(f'The node "{label}" does not exist.')

        for neighbor in self.adj[label]:
            self.adj[neighbor].discard(label)
            self._number_of_edges -= 1

        del self.adj[label]

    def remove_edge(self, u_label, v_label):
        """Remove the edge from the graph.

        Average case time complexity: Theta(1)

        Parameters
        ----------
        u_label
            The label of one of the nodes in the edge.
        v_label
            The label of the other node.

        Raises
        ------
        DoesNotExistError
            If the edge is not in the graph.

        """
        if (u_label, v_label) not in self.edges:
            raise DoesNotExistError(
                f'The edge "({u_label}, {v_label})" does not exist.'
            )

        self.adj[u_label].discard(v_label)
        self.adj[v_label].discard(u_label)
        self._number_of_edges -= 1

    def neighbors(self, label):
        """The neighbors of the node.

        Parameters
        ----------
        label
            The label of the node whose neighbors should be retrieved.

        Returns
        -------
        set
            The neighbors as a Python set. This set should not be modified.

        Note
        ----
        Since the return value is a set, there is no guarantee about the orders
        of the neighbors.

        """
        return self.adj[label]


class DirectedGraph(_Graph):
    def __init__(self, _edge_view_factory=_DirectedEdgeView):
        super().__init__(_edge_view_factory)
        self.back_adj = dict()

    def add_edge(self, u_label, v_label):
        """Add a directed edge to the graph.

        If the edge already exists, nothing is done.

        Average case time complexity: Theta(1).

        Parameters
        ----------
        u_label
            Label of the parent node.
        v_label
            Label of the child node.

        Note
        ----
        If either of the nodes is not in the graph, the node is created.

        """
        for x in {u_label, v_label}:

            if x not in self.adj:
                self.adj[x] = set()
            if x not in self.back_adj:
                self.back_adj[x] = set()

        self.adj[u_label].add(v_label)
        self.back_adj[v_label].add(u_label)
        self._number_of_edges += 1

    def remove_node(self, label):
        """Remove a node grom the graph.

        Average case time complexity: Theta(# of predecessors)
        
        Parameters
        ----------
        label
            The label of the node to be removed.

        Raises
        ------
        DoesNotExistError
            If the node is not in the graph.

        """
        if label not in self.nodes:
            raise DoesNotExistError(f'The node "{label}" does not exist.')

        # in case there is a self-loop, since we can't modify set while iterating
        if label in self.back_adj[label]:
            self.adj[label].discard(label)
            self.back_adj[label].discard(label)
            self._number_of_edges -= 1

        for parent in self.back_adj[label]:
            self.adj[parent].discard(label)
            self._number_of_edges -= 1

        self._number_of_edges -= len(self.adj[label])
        del self.adj[label]

    def remove_edge(self, u_label, v_label):
        """Remove the edge from the graph.

        Average case time complexity: Theta(1)

        Parameters
        ----------
        u_label
            The label of one of the nodes in the edge.
        v_label
            The label of the other node.

        Raises
        ------
        DoesNotExistError
            If the edge is not in the graph.

        """
        if (u_label, v_label) not in self.edges:
            raise DoesNotExistError(
                f'The edge "({u_label}, {v_label})" does not exist.'
            )

        self.adj[u_label].discard(v_label)
        self.back_adj[v_label].discard(u_label)
        self._number_of_edges -= 1

    def predecessors(self, label):
        """The predecessors of the node.

        Parameters
        ----------
        label
            The label of the node whose predecessors should be retrieved.

        Returns
        -------
        set
            The predecessors as a Python set. This set should not be modified.

        Note
        ----
        Since the return value is a set, there is no guarantee about the orders
        of the neighbors.


        """
        return self.back_adj[label]

    def successors(self, label):
        """The successors of the node.

        Parameters
        ----------
        label
            The label of the node whose successors should be retrieved.

        Returns
        -------
        set
            The successors as a Python set. This set should not be modified.

        Note
        ----
        Since the return value is a set, there is no guarantee about the orders
        of the neighbors.

        """
        return self.adj[label]

    def neighbors(self, label):
        """Alias of successors. Provided for convenience."""
        return self.successors(label)
