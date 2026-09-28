"""Connected Components Labeler (CCL) with Disjoint-Set Union-Find
100% Python Standard Library.
"""

class ConnectedComponentsLabeler:
    """Two-pass Connected Components Labeler for binary masks."""
    def __init__(self, connectivity=8):
        self.connectivity = connectivity

    def label_components(self, binary_image):
        h, w = len(binary_image), len(binary_image[0])
        labels = [[0 for _ in range(w)] for _ in range(h)]
        parent = {}

        def find(i):
            path = []
            while parent.get(i, i) != i:
                path.append(i)
                i = parent[i]
            for node in path:
                parent[node] = i
            return i

        def union(i, j):
            root_i = find(i)
            root_j = find(j)
            if root_i != root_j:
                parent[root_j] = root_i

        next_label = 1

        for y in range(h):
            for x in range(w):
                if binary_image[y][x] == 0:
                    continue
                neighbors = []
                if x > 0 and labels[y][x - 1] > 0:
                    neighbors.append(labels[y][x - 1])
                if y > 0 and labels[y - 1][x] > 0:
                    neighbors.append(labels[y - 1][x])
                if self.connectivity == 8 and y > 0:
                    if x > 0 and labels[y - 1][x - 1] > 0:
                        neighbors.append(labels[y - 1][x - 1])
                    if x < w - 1 and labels[y - 1][x + 1] > 0:
                        neighbors.append(labels[y - 1][x + 1])

                if not neighbors:
                    labels[y][x] = next_label
                    parent[next_label] = next_label
                    next_label += 1
                else:
                    m = min(neighbors)
                    labels[y][x] = m
                    for n in neighbors:
                        union(m, n)

        components = {}
        for y in range(h):
            for x in range(w):
                if labels[y][x] > 0:
                    canonical = find(labels[y][x])
                    labels[y][x] = canonical
                    if canonical not in components:
                        components[canonical] = {
                            "label": canonical,
                            "area": 0,
                            "min_x": x, "max_x": x,
                            "min_y": y, "max_y": y
                        }
                    c = components[canonical]
                    c["area"] += 1
                    c["min_x"] = min(c["min_x"], x)
                    c["max_x"] = max(c["max_x"], x)
                    c["min_y"] = min(c["min_y"], y)
                    c["max_y"] = max(c["max_y"], y)

        return {
            "num_components": len(components),
            "components": list(components.values())
        }
