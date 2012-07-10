## DATATYPES

# Unlike Git, which has Blobs and Trees; Rev has Atoms, Dictionaries, Lists
# and Tuples (the latter three corresponding to their Python equivalents)
#
# Other datatypes can be defined just by subclassing NodeBase and implementing
# shrink and expand.


class NodeBase:
    
    def __init__(self, repo, content):
        self.repo = repo
        self.content = self.shrink(content)
    
    def __bytes__(self):
        return ("%s\n%r" % (self.__class__, self.content)).encode("utf-8")


class Atom(NodeBase):
    
    def shrink(self, content):
        return content
    
    def expand(self):
        return self.content


class Dictionary(NodeBase):
    
    def shrink(self, content):
        return {
            self.repo.shrink(key): self.repo.shrink(value)
            for key, value in content.items()
        }
    
    def expand(self):
        return {
            self.repo.expand(key): self.repo.expand(value)
            for key, value in self.content.items()
        }


class List(NodeBase):
    
    def shrink(self, content):
        return [self.repo.shrink(item) for item in content]
    
    def expand(self):
        return [self.repo.expand(item) for item in self.content]


class Tuple(NodeBase):
    
    def shrink(self, content):
        return tuple(self.repo.shrink(item) for item in content)
    
    def expand(self):
        return tuple(self.repo.expand(item) for item in self.content)


def wrap(repo, content):
    if isinstance(content, dict):
        return Dictionary(repo, content)
    elif isinstance(content, list):
        return List(repo, content)
    elif isinstance(content, tuple):
        return Tuple(repo, content)
    else:
        return Atom(repo, content)
