# Варіант 44. Підготовка афіш
# Завдання 1. Розподіл записів за оцінкою

from abc import ABC, abstractmethod


# ---------- Записи (поліморфізм: різна формула оцінки) ----------
class Record(ABC):
    def __init__(self, record_id, x):
        self.id = record_id
        self.x = x

    @abstractmethod
    def score(self):
        pass


class RecordA(Record):
    def score(self):
        return 2 * self.x


class RecordB(Record):
    def score(self):
        return 4 * self.x + 3


def make_record(kind, record_id, x):
    return RecordA(record_id, x) if kind == "A" else RecordB(record_id, x)


# ---------- Структури даних ----------
class Container(ABC):
    def __init__(self, capacity):
        self._capacity = capacity
        self._items = []

    def add(self, item):
        """Додає елемент; повертає False, якщо немає місця."""
        if len(self._items) >= self._capacity:
            return False
        self._items.append(item)
        return True

    @abstractmethod
    def remove(self):
        """Вилучає елемент за правилом структури; None, якщо порожньо."""

    @abstractmethod
    def peek(self):
        """Наступний елемент для вилучення без зміни структури."""

    @abstractmethod
    def state(self):
        """Елементи в порядку наступного вилучення."""

    def size(self):
        return len(self._items)

    def total_score(self):
        return sum(item.score() for item in self._items)


class Stack(Container):
    def remove(self):
        return self._items.pop() if self._items else None

    def peek(self):
        return self._items[-1] if self._items else None

    def state(self):
        return list(reversed(self._items))   # від вершини до основи


class Queue(Container):
    def remove(self):
        return self._items.pop(0) if self._items else None

    def peek(self):
        return self._items[0] if self._items else None

    def state(self):
        return list(self._items)             # від початку до кінця


# Одна спільна операція вилучення для стека й черги
def take_one(structure):
    return structure.remove()


# ---------- Система (композиція) ----------
class PosterSystem:
    THRESHOLD = 12
    CAPACITY = 3

    def __init__(self):
        self.stores = {"S": Stack(self.CAPACITY), "Q": Queue(self.CAPACITY)}
        self.accepted = {"S": 0, "Q": 0}
        self.rejected = {"S": 0, "Q": 0}
        self.empty = {"S": 0, "Q": 0}
        self.logs = {"S": [], "Q": []}
        self._add_counter = 0

    def add(self, kind, x):
        self._add_counter += 1                      # номер займає й відхилена команда
        record = make_record(kind, self._add_counter, x)
        key = "S" if record.score() <= self.THRESHOLD else "Q"
        if self.stores[key].add(record):
            self.accepted[key] += 1
        else:
            self.rejected[key] += 1

    def take(self, key, k):
        for _ in range(k):
            record = take_one(self.stores[key])
            if record is None:
                self.empty[key] += 1
            else:
                self.logs[key].append(record.id)


def ids_line(ids):
    return " ".join(map(str, ids)) if ids else "-"


def main():
    n = int(input())
    system = PosterSystem()
    for _ in range(n):
        parts = input().split()
        if parts[0] == "ADD":
            system.add(parts[1], int(parts[2]))
        else:
            system.take(parts[1], int(parts[2]))

    s, q = system.stores["S"], system.stores["Q"]
    print("S:", ids_line([r.id for r in s.state()]))
    print("Q:", ids_line([r.id for r in q.state()]))
    print("Сума S:", s.total_score())
    print("Сума Q:", q.total_score())
    for key in ("S", "Q"):
        print(f"Вилучено {key}:", ids_line(system.logs[key]))
    for key in ("S", "Q"):
        print(f"Прийнято {key}: {system.accepted[key]}")
    for key in ("S", "Q"):
        print(f"Порожньо {key}: {system.empty[key]}")
    for key in ("S", "Q"):
        print(f"Відхилено {key}: {system.rejected[key]}")


if __name__ == "__main__":
    main()