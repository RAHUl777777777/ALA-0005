

import sys
import math
import random
from typing import Self

class Vec:
  def __init__(self, src=None) -> Self:
    if src is None:
        self.elements = []
    else:
        elements = list(src)

        for x in elements:
            if not isinstance(x, (int, float)):
                raise TypeError(f"Scalar must be a number: {type(x)}")

        self.elements = elements

  def __add__(self, t: Self) -> Self:
        if not isinstance(t, Vec):
            raise TypeError(f"Expected Vec: {type(t)}")
        if len(self.elements) != len(t):
            raise TypeError(f"Type error - vectors must be of same dimensions")

        return Vec([round(x + y, 5) for x, y in zip(self.elements, t.elements)])

  def __neg__(self):
    return Vec([round(-x, 5) for x in self.elements])



  def __mul__(self, scalar: int| float):
    if not isinstance(scalar, (int, float)):
      raise TypeError(f"Vector multiplication with invalid type: {type(scalar)}")
    return Vec([round(x * scalar, 5) for x in self.elements])

  def __imul__(self, scalar: int | float) -> Self:
        if not isinstance(scalar, (int, float)):
            raise TypeError(f"Vector multiplication with invalid type: {type(scalar)}")

        for i, val in enumerate(self.elements):
            self.elements[i] = round(val * scalar, 5)
        #
        return self

  def __rmul__(self, scalar):
    if not isinstance(scalar, (int, float)):
      raise TypeError( f"Vector multiplication with invalid type: {type(scalar)}" )
    return Vec([ round(x * scalar, 5) for x in self.elements ])


  def __sub__(self, t):
    if not isinstance(t, Vec):
      raise TypeError(f"Expected Vec: {type(t)}")
    if len(self.elements) != len(t):
      raise TypeError( "Type error - vectors must be of same dimensions" )
      return Vec([ round(x - y, 5) for x, y in zip(self.elements, t.elements) ])


  def __imul__(self, scalar: int | float) -> Self:
    if not isinstance(scalar, (int, float)):
      raise TypeError( f"Vector multiplication with invalid type: {type(scalar)}" )
    for i, val in enumerate(self.elements):
      self.elements[i] = round(val * scalar, 5)
    return self


  def __iadd__(self, t):
    if not isinstance(t,Vec):
      raise TypeError(f"Expected Vec: {type(t)}")

    if len(self.elements)!=len(t):
      raise TypeError( "Type error - vectors must be of same dimensions" )
    for i in range(len(self.elements)):
      self.elements[i] = round( self.elements[i] + t.elements[i], 5 )

    return self


  def __repr__(self):
    return repr(self.elements)


  def __len__(self):
    return len(self.elements)

  def mean(self):
    if len(self.elements)==0:
      raise ValueError("Cannot calc mean")
    return sum(self.elements)/len(self.elements)

  def demean(self):
    mean_value=self.mean()

    return Vec([round(x-mean_value, 5) for x in self.elements])

  def std(self):
    if len(self.elements)==0:
      raise ValueError("cannot calc std")
    demeaned=self.demean()

    sq_dev=[x**2 for x in demeaned.elements]

    variance=sum(sq_dev)/len(sq_dev)

    return math.sqrt(variance)


  @classmethod
  def zeros(cls, n):
    if n<0:
      raise ValueError("Vector dimension cannot be negative")
    return cls([0]*n)

  @classmethod
  def ones(cls, n):
    if n<0:
      raise ValueError("Vector cannot be negaytive")
    return cls([1]*n)


  def norm(self):
    return math.sqrt(sum(x**2 for x in self.elements))

if __name__=="__main__":
  v1=Vec([0,1,1.03])
  print(v1)
  v2=v1*2.7
  print(v2)


  v3=2.7*v1
  print(v3)

  v4=Vec([1,2,3])
  v5=Vec([5,6,7])

  print(v4+v5)


  print(v5-v4)
  print(-v4)


  v6=Vec([1,2,3])
  v6*=2
  print(v6)


  print(len(v4))

  print(v4.mean())

  print(v6.std())

  print(v4.demean())
  print(v4.mean())

  print(v4.norm())

