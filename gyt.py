import hashlib

class Blob:
    
    def __init__(self, repo, content):
        self.repo = repo
        self.content = content
        self.obj_type = "blob"
    
    def __bytes__(self):
        header_text = "%s\n" % self.obj_type
        data = header_text + self.content
        return data.encode("utf-8")
    
    def expand(self):
        return self.content


class Tree:
    
    def __init__(self, repo, children):
        self.repo = repo
        self.children = {
            name: (self.repo.objects[key].obj_type, key)
            for name, key in children.items()
        }
        self.obj_type = "tree"
    
    def __bytes__(self):
        header_text = "%s\n" % self.obj_type
        nodes_text = "\n".join(["%s %s %s" % (self.children[name][0],
            self.children[name][1], name)
            for name in sorted(self.children)])
        data = header_text + nodes_text
        return data.encode("utf-8")
    
    def expand(self):
        return {
            name: self.repo.objects[self.children[name][1]].expand()
            for name in self.children
        }


class Commit:
    
    def __init__(self, repo, tree_sha, message, parents):
        # @@@ doesn't store author/committer/timestamp yet
        self.repo = repo
        self.tree_sha = tree_sha
        self.message = message
        self.parents = parents
        self.obj_type = "commit"
    
    def __bytes__(self):
        return (
            "%s\n" % self.obj_type +
            "tree %s\n" % self.tree_sha +
            "\n".join("parent %s\n" % parent for parent in self.parents) +
            "\n" + self.message).encode("utf-8")
    
    def expand(self):
        return self.repo.expand(self.tree_sha)


class Repo:
    
    def __init__(self):
        self.objects = {}
        self.index = {}
        self.refs = {}
        self.HEAD = "master"
    
    def store(self, obj):
        key = hashlib.sha1(bytes(obj)).hexdigest()
        self.objects[key] = obj
        return key
    
    def create_blob(self, content):
        return self.store(Blob(self, content))
    
    def create_tree(self, nodes):
        return self.store(Tree(self, nodes))
    
    def create_commit(self, tree_sha, message, parents=None):
        if parents is None:
            parents = []
        return self.store(Commit(self, tree_sha, message, parents))
    
    def update_index(self, children, add=False):
        for name, key in children.items():
            if add or name in self.index:
                self.index[name] = key
    
    def write_tree(self):
        return self.create_tree(self.index)
    
    def expand(self, key):
        return self.objects[key].expand()
    
    def commit(self, tree_sha, message):
        commit_sha = self.create_commit(tree_sha, message, parents=[self.refs[self.HEAD]])
        self.refs[self.HEAD] = commit_sha
        return commit_sha
        
    def create_branch(self, branch_name, commit_sha=None):
        self.refs[branch_name] = commit_sha or self.refs[self.HEAD]
    
    def checkout_branch(self, branch_name):
        self.HEAD = branch_name
        # @@@ do anything to index?

