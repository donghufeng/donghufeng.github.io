# %%
from abc import abstractmethod

class person(object):
    """person
    """
    def __init__(self):
        pass
    
    @abstractmethod
    def set_name(self):
        pass
    
    @classmethod
    def setdoc(cls,doc):
        cls.__doc__=doc
    
    @staticmethod
    def sayhi():
        print("hi")

class woman(person):
    """
    woman
    """
    def __init__(self):
        person.__init__(self)
        self.sex='woman'

    def set_name(self,name):
        self.name=name

# %%
alice=woman()

# staticmethod
alice.sayhi()
woman.sayhi()

# classmethod
print(alice.__doc__)
print(woman.__doc__)
alice.setdoc("set by alice")
print(alice.__doc__)
print(woman.__doc__)
woman.setdoc("set by woman")
print(alice.__doc__)
print(woman.__doc__)
# %%
