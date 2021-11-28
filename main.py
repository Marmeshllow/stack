from collections import deque


def balance(string: str):
    is_balanced = True
    op = ('(', '[', '{')
    end = (')', ']', '}')
    data = list(string)
    stack = MyStack()
    for item in data:
        if item in op:
            stack.push(item)
        else:
            if stack.size() > 0 and op.index(stack.peak()) == end.index(item):
                stack.pop()
            else:
                is_balanced = False
                break
    if stack.size() > 0 or is_balanced == False:
        print('Несбалансированно')
    else:
        print('Сбалансированно')


class MyStack:
    def __init__(self):
        self.stack = deque()

    def push(self, item):
        self.stack.append(item)

    def push_all(self, *args):
        self.stack.extend(args)

    def is_empty(self):
        if len(self.stack) > 0:
            return False
        else:
            return True

    def pop(self):
        if len(self.stack) > 0:
            return self.stack.pop()
        else:
            return None

    def peak(self):
        if len(self.stack) > 0:
            return self.stack[-1]
        else:
            return None

    def size(self):
        return len(self.stack)


if __name__ == '__main__':
    s = MyStack()
    s.push(1)
    s.push(2)
    s.push(3)
    print(s.stack)
    print(s.is_empty())
    print(s.pop())
    print(s.peak())
    print(s.size())
    balance('(((([{}]))))')
    balance('[([])((([[[]]])))]{()}')
    balance('{{[()]}}')
    balance('}{}')
    balance('{{[(])]}}')
    balance('[[{())}]')
