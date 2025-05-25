import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import networkx as nx

# ----- B-Tree Node Implementation -----
class BTreeNode:
    def __init__(self, t, leaf=False):
        self.t = t  # Minimum degree
        self.keys = []
        self.children = []
        self.leaf = leaf

    def insert_non_full(self, key):
        i = len(self.keys) - 1
        if self.leaf:
            self.keys.append(0)
            while i >= 0 and key < self.keys[i]:
                self.keys[i + 1] = self.keys[i]
                i -= 1
            self.keys[i + 1] = key
        else:
            while i >= 0 and key < self.keys[i]:
                i -= 1
            i += 1
            if len(self.children[i].keys) == 2 * self.t - 1:
                self.split_child(i)
                if key > self.keys[i]:
                    i += 1
            self.children[i].insert_non_full(key)

    def split_child(self, i):
        t = self.t
        y = self.children[i]
        z = BTreeNode(t, y.leaf)

        # Correct split and median key push
        mid_key = y.keys[t - 1]

        # Divide keys
        z.keys = y.keys[t:]         # Right half
        y.keys = y.keys[:t - 1]     # Left half

        # Divide children if not leaf
        if not y.leaf:
            z.children = y.children[t:]
            y.children = y.children[:t]

        # Link new child and promote median key
        self.children.insert(i + 1, z)
        self.keys.insert(i, mid_key)

# ----- B-Tree Implementation -----
class BTree:
    def __init__(self, t):
        self.root = BTreeNode(t, True)
        self.t = t

    def insert(self, key):
        r = self.root
        if len(r.keys) == 2 * self.t - 1:
            s = BTreeNode(self.t, False)
            s.children.insert(0, r)
            s.split_child(0)
            self.root = s
            s.insert_non_full(key)
        else:
            r.insert_non_full(key)

# ----- GUI & Visualization -----
class BTreeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("B-Tree Visualizer")

        self.label = tk.Label(root, text="Enter numbers (comma-separated):")
        self.label.pack()

        self.entry = tk.Entry(root, width=50)
        self.entry.pack()

        self.button = tk.Button(root, text="Build B-Tree", command=self.draw_tree)
        self.button.pack()

    def draw_tree(self):
        input_text = self.entry.get()
        try:
            nums = [int(x.strip()) for x in input_text.split(",")]
        except:
            messagebox.showerror("Invalid Input", "Please enter valid integers separated by commas.")
            return

        btree = BTree(t=2)
        for num in nums:
            btree.insert(num)

        G = nx.DiGraph()
        pos = {}
        labels = {}
        self._build_graph(btree.root, G, pos, labels)

        plt.figure(figsize=(12, 6))
        nx.draw(G, pos, with_labels=True, labels=labels,
                node_color="skyblue", node_size=1800, font_size=10)
        plt.title("B-Tree Visualization")
        plt.axis('off')
        plt.tight_layout()
        plt.show()

    def _build_graph(self, node, G, pos, labels, level=0, x=0, counter=[0]):
        key_label = ",".join(str(k) for k in node.keys) if node.keys else "•"
        node_id = f"{id(node)}-{key_label}"
        pos[node_id] = (x + counter[0], -level)
        labels[node_id] = key_label
        G.add_node(node_id)

        for i, child in enumerate(node.children):
            counter[0] += 1
            self._build_graph(child, G, pos, labels, level + 1, x + i, counter)
            child_label = ",".join(str(k) for k in child.keys) if child.keys else "•"
            child_id = f"{id(child)}-{child_label}"
            G.add_edge(node_id, child_id)

# ----- Run App -----
if __name__ == "__main__":
    window = tk.Tk()
    app = BTreeGUI(window)
    window.mainloop()
