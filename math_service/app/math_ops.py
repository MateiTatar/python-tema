class MathOps:
    @staticmethod
    def pow(a: int, b: int) -> int:
        return a ** b

    @staticmethod
    def fibonacci(n: int) -> int:
        if n < 0:
            raise ValueError("n must be >= 0")
        if n == 0:
            return 0
        a, b = 0, 1
        for _ in range(1, n):
            a, b = b, a + b
        return b

    @staticmethod
    def factorial(n: int) -> int:
        if n < 0:
            raise ValueError("n must be >= 0")
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result
