from pprint import pp

from chonkie import Visualizer

from core.chunker.chonk.code import ChonkCodeChunker

vis = Visualizer()

TEST_PYTHON_CODE = '''
def fibonacci(n):
    """Calculate the fibonacci sequence up to n."""
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]

    fib_sequence = [0, 1]
    for i in range(2, n):
        next_fib = fib_sequence[i-1] + fib_sequence[i-2]
        fib_sequence.append(next_fib)

    return fib_sequence


class Calculator:
    """A simple calculator class."""

    def __init__(self):
        self.history = []

    def add(self, a, b):
        """Add two numbers."""
        result = a + b
        self.history.append(f"{a} + {b} = {result}")
        return result

    def multiply(self, a, b):
        """Multiply two numbers."""
        result = a * b
        self.history.append(f"{a} * {b} = {result}")
        return result

    def get_history(self):
        """Get calculation history."""
        return self.history.copy()


def main():
    """Main function to demonstrate the calculator."""
    calc = Calculator()

    # Test fibonacci
    fib_result = fibonacci(10)
    print(f"Fibonacci(10): {fib_result}")

    # Test calculator
    sum_result = calc.add(5, 3)
    product_result = calc.multiply(4, 6)

    print(f"5 + 3 = {sum_result}")
    print(f"4 * 6 = {product_result}")
    print(f"History: {calc.get_history()}")


if __name__ == "__main__":
    main()
'''

TEST_JAVASCRIPT_CODE = """
class TodoList {
    constructor() {
        this.todos = [];
        this.nextId = 1;
    }

    addTodo(text) {
        const todo = {
            id: this.nextId++,
            text: text,
            completed: false,
            createdAt: new Date()
        };
        this.todos.push(todo);
        return todo;
    }

    completeTodo(id) {
        const todo = this.todos.find(t => t.id === id);
        if (todo) {
            todo.completed = true;
            return true;
        }
        return false;
    }

    deleteTodo(id) {
        const index = this.todos.findIndex(t => t.id === id);
        if (index !== -1) {
            this.todos.splice(index, 1);
            return true;
        }
        return false;
    }

    getAllTodos() {
        return this.todos.slice();
    }

    getCompletedTodos() {
        return this.todos.filter(t => t.completed);
    }

    getPendingTodos() {
        return this.todos.filter(t => !t.completed);
    }
}

function createTodoApp() {
    const todoList = new TodoList();

    todoList.addTodo("Learn JavaScript");
    todoList.addTodo("Build a todo app");
    todoList.addTodo("Write tests");

    todoList.completeTodo(1);

    console.log("All todos:", todoList.getAllTodos());
    console.log("Completed todos:", todoList.getCompletedTodos());
    console.log("Pending todos:", todoList.getPendingTodos());
}

createTodoApp();
"""


def test_python_code_chunker():
    chunker = ChonkCodeChunker(language="python", chunk_size=1024)
    result = chunker.chunk(TEST_PYTHON_CODE)

    pp("-" * 20 + "python code chunker result:" + "-" * 20)
    vis.print(chunker.chunker.chunk(TEST_PYTHON_CODE))  # type: ignore
    pp("-" * 20 + "python code chunker finish" + "-" * 20)

    assert result is not None
    assert isinstance(result, list)
    assert len(result) > 0
    assert all(isinstance(chunk, str) for chunk in result)


def test_javascript_code_chunker():
    chunker = ChonkCodeChunker(language="javascript", chunk_size=1024)
    result = chunker.chunk(TEST_JAVASCRIPT_CODE)

    pp("-" * 20 + "javascript code chunker result:" + "-" * 20)
    vis.print(chunker.chunker.chunk(TEST_JAVASCRIPT_CODE))  # type: ignore
    pp("-" * 20 + "javascript code chunker finish" + "-" * 20)

    assert result is not None
    assert isinstance(result, list)
    assert len(result) > 0
    assert all(isinstance(chunk, str) for chunk in result)
