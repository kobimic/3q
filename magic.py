from dataclasses import dataclass

@dataclass
class Person:
    age: int = 1

    def __str__(self):
        return str(self.age)


class MagicList(list):
    def __init__(self, cls_type=None):
        super(MagicList, self).__init__()
        if cls_type:
            super(MagicList, self).append(cls_type())

    def __setitem__(self, key, value):
        if super(MagicList, self).__len__() == 0:
            super(MagicList, self).append(value)
        else:
            if super(MagicList, self).__len__()-1-abs(key)>0:
                super(MagicList, self).__setitem__(key, value)
            else:
                raise IndexError()



x = MagicList()
x[0] = 5
print(x)


a = MagicList(cls_type=Person)
a[0].age = 5
print(a)
print(a[0].age)

# a = MagicList(cls_type=Person)
# a[1].age = 5


a = MagicList(cls_type=Person)
b = Person()
a.append(b)
print(a)
print()