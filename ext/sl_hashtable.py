import time
import random
import string

import sl


class SL_HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [sl.SL_List() for _ in range(size)]

    def h(self, key):
        return sum(ord(c) for c in str(key)) % self.size

    def put(self, key, data):
        index = self.h(key)
        node = self.get(key)
        if node is not None:
            node.value[1] = data
        else:
            self.table[index].add_front([key, data])

    def get(self, key):
        current = self.table[self.h(key)].head
        while current != None:
            if current.value[0] == key:
                return current
            current = current.next
        return None

    def delkey(self, key):
        index = self.h(key)
        current = self.table[index].head
        prev = None
        while current != None:
            if current.value[0] == key:
                if prev == None:
                    return self.table[index].delete_front()
                else:
                    prev.next = current.next
                    return current
            prev = current
            current = current.next
        return None

    def kof(self):
        count = 0
        for lst in self.table:
            if not lst.is_empty():
                count += 1
        return f"Коэффициент заполнения: {count / self.size}"

    def __str__(self):
        return "\n".join(
            f"Bucket {i}: {lst}"
            for i, lst in enumerate(self.table)
            if not lst.is_empty()
        )


def generate_random_string(length=10):
    characters = string.ascii_letters + string.digits
    return "".join(random.choice(characters) for _ in range(length))


def main():
    st = time.time()
    ht = SL_HashTable(2000)
    ft = time.time()
    print(f"Время создания таблицы размером {ht.size}: {ft-st} секунд\n{ht.kof()}")

    st = time.time()
    for _ in range(1400):
        key = generate_random_string(random.randint(1, 200))
        data = random.randint(1, 5000)
        ht.put(key, data)
    ft = time.time()
    print(f"Время заполнения: {ft-st} секунд\n{ht.kof()}")

    print("\n_______________________________________________________________\n")

    st = time.time()
    ht_small = SL_HashTable(10)
    ft = time.time()
    # print(ht)
    print(
        f"Время создания таблицы размером {ht_small.size}: {ft-st} секунд\n{ht_small.kof()}"
    )

    st = time.time()
    ht_small.put("Alex", random.randint(1, 5000))
    ht_small.put("lexA", random.randint(1, 5000))
    ht_small.put("Alex", random.randint(1, 5000))  # Обновление существующего ключа
    ht_small.put(generate_random_string(128), random.randint(1, 5000))
    print(ht_small.get("Alex"))
    print(ht_small.delkey("Applr"))  # Попытка удалить несуществующий ключ
    ft = time.time()
    print(ht_small)
    print(f"Время выполнения: {ft-st} секунд\n{ht_small.kof()}")


if __name__ == "__main__":
    main()
