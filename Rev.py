import hashlib


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


## END DATATYPES


class Commit:
    
    def __init__(self, repo, obj_sha, message, parents):
        # @@@ doesn't store author/committer/timestamp yet
        self.repo = repo
        self.obj_sha = obj_sha
        self.message = message
        self.parents = parents
        self.content = repo.shrink((obj_sha, parents, message))
    
    def __bytes__(self):
        return ("%s\n%r" % (self.__class__, self.content)).encode("utf-8")


class Repo:
    
    def __init__(self):
        self.objects = {}
        self.refs = {}
        self.HEAD = "master"
    
    def store(self, obj):
        sha = hashlib.sha1(bytes(obj)).hexdigest()
        self.objects[sha] = obj
        
        return sha
    
    def shrink(self, content):
        if isinstance(content, dict):
            return self.store(Dictionary(self, content))
        elif isinstance(content, list):
            return self.store(List(self, content))
        elif isinstance(content, tuple):
            return self.store(Tuple(self, content))
        else:
            return self.store(Atom(self, content))
        
        return store(obj)
    
    def expand(self, sha):
        return self.objects[sha].expand()
    
    def create_commit(self, obj_sha, message, parents=None):
        if parents is None:
            parents = []
        
        return self.store(Commit(self, obj_sha, message, parents))
    
    def commit(self, obj, message):
        obj_sha = self.shrink(obj)
        commit_sha = self.create_commit(obj_sha, message, parents=[self.refs[self.HEAD]])
        self.refs[self.HEAD] = commit_sha
        
        return commit_sha
        
    def retrieve_commit(self, commit_sha=None):
        if commit_sha is None:
            commit_sha = self.refs[self.HEAD]
        
        return self.expand(self.objects[commit_sha].obj_sha)
    
    def create_branch(self, branch_name, commit_sha=None):
        if commit_sha is None:
            commit_sha = self.refs[self.HEAD]
        
        self.refs[branch_name] = commit_sha or self.refs[self.HEAD]
    
    def checkout_branch(self, branch_name):
        self.HEAD = branch_name
        # @@@ do anything to index?

