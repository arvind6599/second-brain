from abc import ABC, abstractmethod

class classDesign(ABC):
    """
    Class definition to set a layout for the different classes that inherit this class
    to maintain a level of consistency  
    """

    @abstractmethod
    def speak(self):
        pass


class class2(classDesign):

    def speak(self):

        return "Wolf!"


#### To illustrate the use of await and async in python for asynchronous programming in python


import asyncio

async def Hello():
    print("Hello")
    await asyncio.sleep(2)

    print("World")

async def main():

    await Hello()

# asyncio.run(main())


## Different types in python, some defined using pydantic and others just the default ones



from typing import List, Dict, Optional, Union, Tuple


def operations(s: str, arr: List[int], var: float) -> Optional[int]:
    pass

def operations2(arr: List[int])-> Optional[int]:
    pass

from pydantic import BaseModel

class Note(BaseModel):
    text: str
    name: str
    age: int
    email: str


## Learning more about other typing features such as Literal, Final, TypeDict
# 

from typing import Literal

def roll_die(roll: Literal[6,20]) -> str:

    print(roll)

    return str(roll)

print(roll_die(3))