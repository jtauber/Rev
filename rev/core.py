import hashlib

from .datatypes import Atom, Dictionary, List, Tuple
from .datatypes import wrap


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
        self.HEAD = "ref:master"
    
    def resolve(self, ref):
        """
        resolves symbolic refs until a SHA is reached
        """
        if ref.startswith("ref"):
            return self.resolve(self.refs[ref])
        else:
            return ref
    
    def store(self, obj):
        sha = hashlib.sha1(bytes(obj)).hexdigest()
        self.objects[sha] = obj
        
        return sha
    
    def shrink(self, content):
        return self.store(wrap(self, content))
    
    def get_object(self, sha):
        """
        get the shallow version of the object with the given SHA.
        
        In other words, the components of the given object (if non-atomic)
        will be further SHA references.
        """
        return self.objects[sha]
    
    def expand(self, sha):
        """
        get the deep version of the object with the given SHA.
        
        In other words, all components of the given object will be expanded
        recursively to their actual values with no SHA references left.
        """
        return self.get_object(sha).expand()
    
    def create_commit(self, obj_sha, message, parents=None):
        if parents is None:
            parents = []
        
        return self.store(Commit(self, obj_sha, message, parents))
    
    def commit(self, obj, message):
        obj_sha = self.shrink(obj)
        old_head = self.resolve(self.HEAD)
        commit_sha = self.create_commit(obj_sha, message, parents=[old_head])
        # @@@ make thread-safe? HEAD could change during commit
        self.refs[self.HEAD] = commit_sha
        
        return commit_sha
        
    def retrieve_commit(self, commit_sha=None):
        obj = self.get_object(commit_sha or self.resolve(self.HEAD))
        return self.expand(obj.obj_sha)
    
    def create_branch(self, branch_name, commit_sha=None):
        self.refs["ref:" + branch_name] = commit_sha or self.resolve(self.HEAD)
    
    def checkout_branch(self, branch_name):
        self.HEAD = "ref:" + branch_name
