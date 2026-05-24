from __future__ import annotations


class SimpleModel:

    def __init__(self, base_value: int = 42) -> None:
        self.base_value = base_value

    def predict(self) -> int:
        return self.base_value


model = SimpleModel()
