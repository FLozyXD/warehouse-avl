import random
import time
import sys

sys.setrecursionlimit(20000)

class Node:
    def __init__(self, key):
        self.key: int = key
        self.left: Node = None
        self.right: Node = None
        self.height: int = 1

class TreeTools:

    def print_tree(self, node: Node, prefix="", is_left=True):
        if node is not None:
            self.print_tree(node.right, prefix + ("│   " if is_left else "    "), False)
            print(prefix + ("└── " if is_left else "┌── ") + str(node.key))
            self.print_tree(node.left, prefix + ("    " if is_left else "│   "), True)

    def get_average_depth(self, root):
        if root is None:
            return 0
        depths_list = []
        self.get_all_node_depths(root, 0, depths_list)
        if not depths_list:
            return 0
        return sum(depths_list) / len(depths_list)

    def get_all_node_depths(self, node, current_depth, depths_list):
        if node is None:
            return
        depths_list.append(current_depth)
        self.get_all_node_depths(node.left, current_depth + 1, depths_list)
        self.get_all_node_depths(node.right, current_depth + 1, depths_list)

    def get_max_depth(self, node):
        if node is None:
            return -1
        left_depth = self.get_max_depth(node.left)
        right_depth = self.get_max_depth(node.right)
        return max(left_depth, right_depth) + 1

    def get_height(self, node):
        if not node:
            return 0
        return node.height
    
    def min_value_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current
        
    def search(self, node, key):
        if node is None or node.key == key:
            return node
        if key < node.key:
            return self.search(node.left, key)
        return self.search(node.right, key)

class BSTree(TreeTools):

    def __init__(self):
        self.root = None

    def insert(self, node, key):
        if node is None:
            return Node(key)
        
        if key < node.key:
            node.left = self.insert(node.left, key)
        elif key > node.key:
            node.right = self.insert(node.right, key)
        
        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))
        return node

    def delete(self, node, key):
        if node is None:
            return node

        if key < node.key:
            node.left = self.delete(node.left, key)
        elif key > node.key:
            node.right = self.delete(node.right, key)
        else:
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            
            temp_val = self.min_value_node(node.right)
            node.key = temp_val.key
            node.right = self.delete(node.right, temp_val.key)
        
        if node:
            node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))
        return node


class AVLTree(TreeTools):
    """
    Класс для AVL-дерева (самобалансирующегося бинарного дерева поиска).
    """
    def __init__(self):
        self.root = None

    def update_height(self, node):
        if node:
            node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))

    def get_balance_factor(self, node):
        if not node:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)

    def right_rotate(self, b):
        a = b.left
        temp = a.right
        a.right = b
        b.left = temp
        self.update_height(b)
        self.update_height(a)
        return a

    def left_rotate(self, a):
        b = a.right
        temp = b.left
        b.left = a
        a.right = temp
        self.update_height(a)
        self.update_height(b)
        return b

    def insert(self, node, key):
        if not node:
            return Node(key)
        elif key < node.key:
            node.left = self.insert(node.left, key)
        elif key > node.key:
            node.right = self.insert(node.right, key)
        else:
            return node 

        self.update_height(node)
        balance = self.get_balance_factor(node)

        if balance > 1 and key < node.left.key:
            return self.right_rotate(node)
        if balance < -1 and key > node.right.key:
            return self.left_rotate(node)
        if balance > 1 and key > node.left.key:
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)
        if balance < -1 and key < node.right.key:
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)
        
        return node

    def delete(self, node, key):
        if not node:
            return node

        if key < node.key:
            node.left = self.delete(node.left, key)
        elif key > node.key:
            node.right = self.delete(node.right, key)
        else:
            if node.left is None:
                temp = node.right
                node = None
                return temp
            elif node.right is None:
                temp = node.left
                node = None
                return temp
            
            temp = self.min_value_node(node.right)
            node.key = temp.key
            node.right = self.delete(node.right, temp.key)

        if node is None:
            return node

        self.update_height(node)
        balance = self.get_balance_factor(node)

        if balance > 1 and self.get_balance_factor(node.left) >= 0: # LL
            return self.right_rotate(node)
        if balance < -1 and self.get_balance_factor(node.right) <= 0: # RR
            return self.left_rotate(node)
        if balance > 1 and self.get_balance_factor(node.left) < 0: # LR
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)
        if balance < -1 and self.get_balance_factor(node.right) > 0: # RL
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)
            
        return node


# --- Генерация данных ---
def generate_random_data(size):
    return random.sample(range(size * 3), size) 

def generate_sorted_data(size):
    return list(range(size))

def generate_pattern_data(size):
    data = []
    current_val = 1
    i = 0
    block_size = 3
    while len(data) < size:

        if len(data) < size:
            data.append(current_val + i * block_size)

        if len(data) < size:
             data.append(current_val + i * block_size + 2)

        if len(data) < size:
            data.append(current_val + i * block_size + 1)
        i += 1
    return data[:size]

# --- Тестирование и сбор статистики ---
def test(tree_class, data):
    tree = tree_class()
    start_time = time.perf_counter()
    for item in data:
        tree.root = tree.insert(tree.root, item)
    end_time = time.perf_counter()
    
    build_time = (end_time - start_time) * 1000 
    avg_depth = tree.get_average_depth(tree.root)
    max_depth = tree.get_max_depth(tree.root)
    
    return build_time, avg_depth, max_depth

def print_results_table(results_list, headers):

    column_widths = [len(header) for header in headers]
    for row in results_list:
        for i, cell in enumerate(row):
            column_widths[i] = max(column_widths[i], len(str(cell)))

    header_line = []
    for i, header in enumerate(headers):
        header_line.append(str(header).ljust(column_widths[i]))
    print(" | ".join(header_line))

    separator_line = []
    for width in column_widths:
        separator_line.append("-" * width)
    print("-|-".join(separator_line))

    for row in results_list:
        row_line_parts = []
        for i, cell in enumerate(row):
            row_line_parts.append(str(cell).ljust(column_widths[i]))
        print(" | ".join(row_line_parts))


if __name__ == "__main__":
    NUM_ELEMENTS = 15

    print(f"--- Тестирование AVL и BST на {NUM_ELEMENTS} элементах ---\n")
    
    if NUM_ELEMENTS <= 15:
        print("Пример построения AVL-дерева:")
        avl_small = AVLTree()
        # small_data_example = [7, 5, 2, 6, 3, 4, 1, 8, 9, 0] # Из лекции
        small_data_example = generate_pattern_data(NUM_ELEMENTS)
        print(f"Вставляемые данные: {small_data_example}")
        for a in small_data_example:
            avl_small.root = avl_small.insert(avl_small.root, a)
            # print(f"\nПосле вставки {a}:")
            # avl_small.print_tree(avl_small.root)
        print("\nФинальное AVL-дерево (малый пример):")
        avl_small.print_tree(avl_small.root)
        print(f"Макс. глубина: {avl_small.get_max_depth(avl_small.root)}")
        print(f"Сред. глубина: {avl_small.get_average_depth(avl_small.root)}\n")

        # Пример удаления
        # elements_to_delete = [small_data_example[len(small_data_example)//2], small_data_example[0]]
        elements_to_delete = [4]
        for el_to_del in elements_to_delete:
            if avl_small.search(avl_small.root, el_to_del):
                print(f"\nУдаляем {el_to_del} из малого AVL дерева:")
                avl_small.root = avl_small.delete(avl_small.root, el_to_del)
                avl_small.print_tree(avl_small.root)
            else:
                print(f"Элемент {el_to_del} не найден для удаления в малом AVL дереве.")
        print("-" * 50 + "\n")


    sets = {
        "Случайные числа": generate_random_data(NUM_ELEMENTS),
        "Отсортированная посл.": generate_sorted_data(NUM_ELEMENTS),
        "Паттерн вставки (1,3,2,...)": generate_pattern_data(NUM_ELEMENTS)
    }

    results_data = []

    for name, data in sets.items():
        print(f"Набор: {name}")
        
        bst_build_time, bst_avg_depth, bst_max_depth = test(BSTree, data)
        results_data.append([name, "BST", f"{bst_build_time:.2f} мс", f"{bst_avg_depth:.2f}", bst_max_depth])
        print(f"  BST: Время={bst_build_time:.2f} мс, Ср.глубина={bst_avg_depth:.2f}, Макс.глубина={bst_max_depth}")

        avl_build_time, avl_avg_depth, avl_max_depth = test(AVLTree, data)
        results_data.append([name, "AVL", f"{avl_build_time:.2f} мс", f"{avl_avg_depth:.2f}", avl_max_depth])
        print(f"  AVL: Время={avl_build_time:.2f} мс, Ср.глубина={avl_avg_depth:.2f}, Макс.глубина={avl_max_depth}\n")

    print("\n" + "="*70 + "\n")
    print("Таблица результатов:")
    table_headers = ["Набор данных", "Тип дерева", "Время построения", "Средняя глубина", "Макс. глубина"]
    print_results_table(results_data, table_headers)