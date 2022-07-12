from typing import List, Optional


def range2d(start: int, stop: Optional[int] = None) -> List[int]:
    r = range(start, stop) if stop is not None else range(start)
    return [(i, j) for i in r for j in r]
