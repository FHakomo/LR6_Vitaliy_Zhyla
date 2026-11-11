# Варіант 44. Підготовка афіш
# Завдання 2. Контроль оцінок і виправлення записів

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
        return 3 * self.x


class RecordB(Record):
    def score(self):
        return 2 * self.x + 4


def make_record(kind, record_id, x):
    return RecordA(record_id, x) if kind == "A" else RecordB(record_id, x)


# ---------- Структури даних ----------
class Container(ABC):
    def __init__(self, capacity=None):
        self._capacity = capacity          # None означає без обмеження
        self._items = []

    def is_full(self):
        return self._capacity is not None and len(self._items) >= self._capacity

    def add(self, item):
        """Додає елемент; False, якщо немає місця."""
        if self.is_full():
            return False
        self._items.append(item)
        return True

    @abstractmethod
    def remove(self):
        """Вилучає елемент за правилом структури або None, якщо порожньо."""

    @abstractmethod
    def peek(self):
        """Виведення наступного елементу для вилучення без зміни структури."""

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
    Q_CAPACITY = 4
    THRESHOLD = 21

    def __init__(self):
        self.q = Queue(self.Q_CAPACITY)
        self.s = Stack()
        self.accepted = []       # id остаточно прийнятих
        self.deferred = []       # id записів, відкладених до S
        self.returned = []       # id записів, повернених S -> Q
        self.empty_q = 0
        self.empty_s = 0
        self.blocked = 0
        self.rejected = 0
        self._add_counter = 0

    def add(self, kind, x):
        self._add_counter += 1               # номер займає й відхилена команда
        record = make_record(kind, self._add_counter, x)
        if not self.q.add(record):
            self.rejected += 1

    def check(self, k):
        for _ in range(k):
            record = take_one(self.q)
            if record is None:
                self.empty_q += 1
            elif record.score() <= self.THRESHOLD:
                self.accepted.append(record.id)
            else:
                self.s.add(record)
                self.deferred.append(record.id)

    def fix(self, x):
        record = self.s.peek()
        if record is None:
            self.empty_s += 1
        else:
            record.x = x                     # тип та id зберігаються

    def recover(self, k):
        for _ in range(k):
            if self.s.size() == 0:           # порожнє джерело має перевагу
                self.empty_s += 1
            elif self.q.is_full():
                self.blocked += 1
            else:
                record = take_one(self.s)
                self.q.add(record)
                self.returned.append(record.id)


def ids_line(ids):
    return " ".join(map(str, ids)) if ids else "-"


def main():
    n = int(input())
    system = PosterSystem()
    for _ in range(n):
        parts = input().split()
        command = parts[0]
        if command == "ADD":
            system.add(parts[1], int(parts[2]))
        elif command == "CHECK":
            system.check(int(parts[1]))
        elif command == "FIX":
            system.fix(int(parts[1]))
        else:
            system.recover(int(parts[1]))

    print("S:", ids_line([r.id for r in system.s.state()]))
    print("Q:", ids_line([r.id for r in system.q.state()]))
    print("Сума S:", system.s.total_score())
    print("Сума Q:", system.q.total_score())
    print("Прийнято:", ids_line(system.accepted))
    print("Відкладено:", ids_line(system.deferred))
    print("Повернено:", ids_line(system.returned))
    print("Порожньо Q:", system.empty_q)
    print("Порожньо S:", system.empty_s)
    print("Заблоковано:", system.blocked)
    print("Відхилено:", system.rejected)


if __name__ == "__main__":
    main()