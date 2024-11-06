#ex1

class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if self.items:
            return self.items.pop()
        return None

    def peek(self):
        if self.items:
            return self.items[-1]
        return None


#ex2

class Queue:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if self.items:
            return self.items.pop(0)
        return None

    def peek(self):
        if self.items:
            return self.items[0]
        return None

#ex3

class Matrix:
    def __init__(self, n, m, data=None):
        self.n = n
        self.m = m
        if data:
            if len(data) != n or any(len(row) != m for row in data):
                raise ValueError("Data dimensions do not match specified size.")
            self.data = data
        else:
            self.data = [[0 for _ in range(m)] for _ in range(n)]

    def get(self, i, j):
        if 0 <= i < self.n and 0 <= j < self.m:
            return self.data[i][j]
        else:
            raise IndexError("Index out of bounds.")

    def set(self, i, j, value):
        if 0 <= i < self.n and 0 <= j < self.m:
            self.data[i][j] = value
        else:
            raise IndexError("Index out of bounds.")

    def transpose(self):
        transposed_data = [[self.data[i][j] for i in range(self.n)] for j in range(self.m)]
        return Matrix(self.m, self.n, transposed_data)

    def __mul__(self, other):
        if not isinstance(other, Matrix):
            raise ValueError("Operand must be an instance of Matrix.")
        if self.m != other.n:
            raise ValueError("Incompatible dimensions for multiplication.")
        result = Matrix(self.n, other.m)
        for i in range(self.n):
            for j in range(other.m):
                result.data[i][j] = sum(self.data[i][k] * other.data[k][j] for k in range(self.m))
        return result

    def apply(self, func):
        new_data = [[func(self.data[i][j]) for j in range(self.m)] for i in range(self.n)]
        return Matrix(self.n, self.m, new_data)

    def __str__(self):
        return '\n'.join(['\t'.join(map(str, row)) for row in self.data])

    def __repr__(self):
        return f"Matrix(N={self.n}, M={self.m}, data={self.data})"


print("Testing Stack class:")
stack = Stack()

stack.push(10)
stack.push(20)
stack.push(30)
print("Stack after pushes:", stack.items)

print("Peek top element:", stack.peek())

print("Popped element:", stack.pop())
print("Stack after pop:", stack.items)

stack.pop()
stack.pop()
print("Pop on empty stack returns:", stack.pop())

queue = Queue()

queue.push('a')
queue.push('b')
queue.push('c')

print("Queue after pushes:", queue.items)

print("Peek front element:", queue.peek())

print("Popped element:", queue.pop())
print("Queue after pop:", queue.items)

queue.pop()
queue.pop()
print("Pop on empty queue returns:", queue.pop())


print("\nTesting Matrix class:")
matrix_data = [
    [1, 2, 3],
    [4, 5, 6]
]
matrix = Matrix(2, 3, matrix_data)
print("Original Matrix:")
print(matrix)

print("\nElement at position (1, 2):", matrix.get(1, 2))

matrix.set(0, 1, 9)
print("\nMatrix after setting element at (0, 1) to 9:")
print(matrix)

transposed_matrix = matrix.transpose()
print("\nTransposed Matrix:")
print(transposed_matrix)

other_matrix_data = [
    [7, 8],
    [9, 10],
    [11, 12]
]
other_matrix = Matrix(3, 2, other_matrix_data)
product_matrix = matrix * other_matrix
print("\nProduct of matrix and other_matrix:")
print(product_matrix)

applied_matrix = matrix.apply(lambda x: x ** 2)
print("\nMatrix after applying lambda x: x ** 2:")
print(applied_matrix)