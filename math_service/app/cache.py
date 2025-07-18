from typing import Dict, Tuple, Optional

class OperationCache:
    def __init__(self):
        self.cache: Dict[Tuple[str, Tuple[int, ...]], int] = {}

    def get(self, op_type: str, operands: Tuple[int, ...]) -> Optional[int]:
        return self.cache.get((op_type, operands))

    def set(self, op_type: str, operands: Tuple[int, ...], result: int):
        self.cache[(op_type, operands)] = result
