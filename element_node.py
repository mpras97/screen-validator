
class ElementNode:
    def __init__(self, name, id=None, className=None):
        self.name = name
        self.id = id
        self.className = className

    def __str__(self):
        if self.id:
            if self.className:
                return self.name + f".{self.className}" + f"#{self.id}"
            else:
                return self.name + f"#{self.id}"
        elif self.className:
            return self.name + f".{self.className}"
        else:
            return self.name

    def __repr__(self):
        if self.id:
            if self.className:
                return self.name + f".{self.className}" + f"#{self.id}"
            else:
                return self.name + f"#{self.id}"
        elif self.className:
            return self.name + f".{self.className}"
        else:
            return self.name

