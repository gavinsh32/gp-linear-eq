class Operator():
    def __init__(self):
        self.kind: int = random.randint(0, 3)
        self.left_child: AnyNode | None = None
        self.right_child: AnyNode | None = None
    
    def get(self) -> int:
        return self.kind
    
    def copy(self) -> 'Operator':
        dst = Operator()
        dst.kind = self.kind
        dst.left_child = self.left_child
        dst.right_child = self.right_child
        return dst
    
    def __str__(self):
        match self.kind:
            case 0:
                return '+'
            case 1:
                return '-'
            case 2:
                return '*'
            case 3:
                return '/'
            case _:
                return 'INVALID OP ' + str(self.kind)

class Variable():
    """A node with the number of the variable it represents (x0, x1, ..., xn)."""
    def __init__(self):
        """Spawn a new variable node with the id it represents."""
        self.id: int = random.randrange(NUM_VARS)

    def get(self) -> int:
        return self.id

    def __str__(self):
        return f'x{self.id}'
    
    def copy(self) -> 'Variable':
        dst = Variable()
        dst.id = self.id
        return dst

class Constant():
    """A node with an float value."""
    def __init__(self):
        self.data: float = _generate_value()

    def get(self) -> float:
        return self.data

    def __str__(self):
        return f'{self.data}'
    
    def copy(self) -> 'Constant':
        dst = Constant()
        dst.data = self.data
        return dst