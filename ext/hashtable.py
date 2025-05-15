import time
import random
import string


class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [[] for i in range(size)]

    def h(self, key):
        return sum(ord(c) for c in str(key)) % self.size

    def put(self, key, data):
        if [key, data] in self.table[self.h(key)]:
            return None
        flag = False
        for i in self.table[self.h(key)]:
            if i[0] == key:
                i[1] = data
                flag = True
        if flag == False:
            self.table[self.h(key)].append([key, data])

    def get(self, key):
        for i in self.table[self.h(key)]:
            if i[0] == key:
                return i
        return None

    def delkey(self, key):
        tmp = []
        for i in self.table[self.h(key)]:
            if i[0] == key:
                tmp = i
                self.table[self.h(key)].remove(i)
                return tmp
        return None

    def kof(self):
        count = 0
        for i in self.table:
            if i != []:
                count += 1
        return f"Коэфициент заполнения {count/self.size}"

    def __str__(self):
        return str(self.table)


def generate_random_string(length=10):
    """Генерирует случайную строку заданной длины (по умолчанию 10 символов)."""
    characters = string.ascii_letters + string.digits  # буквы (A-Z, a-z) + цифры (0-9)
    return "".join(random.choice(characters) for _ in range(length))


def main():
    st = time.time()
    ht = HashTable(200000)
    ft = time.time()
    print(
        f"Время создания таблицы размером {ht.size}: {ft-st} секунд\nКоэфициент заполнения: {ht.kof()}"
    )
    st = time.time()
    for i in range(140000):
        ht.put(generate_random_string(random.randint(1, 200)), random.randint(1, 5000))
    ft = time.time()
    # print(ht)
    print(f"Время выполнения: {ft-st} секунд\nКоэфициент заполнения: {ht.kof()}")
    print("\n_______________________________________________________________\n")

    st = time.time()
    ht = HashTable(10)
    ft = time.time()
    print(
        f"Время создания таблицы размером {ht.size}: {ft-st} секунд\nКоэфициент заполнения: {ht.kof()}"
    )
    st = time.time()
    ht.put("Alex", random.randint(1, 5000))
    ht.put("lexA", random.randint(1, 5000))
    ht.put("Alex", random.randint(1, 5000))
    ht.put(generate_random_string(128), random.randint(1, 5000))
    print(ht.get("Alex"))
    # print(ht.delkey("Alex"))
    print(ht.delkey("Applr"))
    ft = time.time()
    print(ht)
    print(f"Время выполнения: {ft-st} секунд\nКоэфициент заполнения: {ht.kof()}")


if __name__ == "__main__":
    main()
