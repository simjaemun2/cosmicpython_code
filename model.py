from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from typing import List, NamedTuple, Optional


@dataclass(frozen=True)  #(1)(2)
class OrderLine:
    orderid: str
    sku: str
    qty: int

@dataclass(frozen=True)
class Name:
    first_name: str
    surname: str

class Money(NamedTuple):
    currency: str
    value: int

class Person:
    def __init__(self, name: Name) -> None:
        self.name = name


class Batch:
    def __init__(self, ref: str, sku: str, qty: int, eta: Optional[date]):  #(2)
        self.reference = ref
        self.sku = sku
        self.eta = eta
        self._purchased_quantity = qty
        self._allocations = set()
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Batch):
            return False
        return other.reference == self.reference
    
    def __gt__(self, other):
        if self.eta is None:
            return False
        if other.eta is None:
            return True
        return self.eta > other.eta

    def __hash__(self) -> int:
        return hash(self.reference)


    def allocate(self, line: OrderLine):  #(3)
        if self.can_allocate:
            self._allocations.add(line)
    
    def deallocate(self, line:OrderLine):
        if line in self._allocations:
            self._allocations.remove(line)

    @property
    def allocated_quantity(self)-> int:
        return sum(line.qty for line in self._allocations)

    @property
    def available_quantity(self) -> int:
        return self._purchased_quantity - self.allocated_quantity

    def can_allocate(self, line:OrderLine) -> bool:
        return self.sku == line.sku and self.available_quantity >= line.qty

def allocate(line: OrderLine, batches: List[Batch]) -> str:
    try:
        batch = next(b for b in sorted(batches) if b.can_allocate(line))
        batch.allocate(line)
        return batch.reference
    except StopIteration:
        raise OutOfStock(f"Out of stock for sku {line.sku}")

class OutOfStock(Exception):
    pass