#!/usr/bin/env python3

from rev import Repo

repo = Repo()

## first we'll do this a very low level way...

# 1. create a directory tree

t = {
    "test.txt": "version 1",
    "new.txt": "new file",
}

# 2. shrink and store it

t1 = repo.shrink(t)

# 3. create a commit object out of it

c1 = repo.create_commit(t1, "my first commit")

# 4. and move the HEAD

repo.refs[repo.HEAD] = c1

assert t == repo.expand(repo.get_object(c1).obj_sha)


## now let's make a change to a file...

t["test.txt"] = "version 2"

t2 = repo.shrink(t)

parent = repo.refs[repo.HEAD]
c2 = repo.create_commit(t2, "second commit", parents=[parent])
repo.refs[repo.HEAD] = c2


## let's create a subdirectory now


t["subdir"] = {
    "foo.txt": "file in subdir"
}


## this time we'll use the higher-level commit method

c3 = repo.commit(t, "added subdir")


## retrieve subdir/foo.txt from HEAD

assert repo.retrieve_commit()["subdir"]["foo.txt"] == "file in subdir"


# now let's create a branch

repo.create_branch("branch-test")
repo.checkout_branch("branch-test")

t = repo.retrieve_commit()

t["subdir"]["foo.txt"] = "changed!"

c4 = repo.commit(t, "changed file in subdirectory")


## this should print "changed!"

assert repo.retrieve_commit()["subdir"]["foo.txt"] == "changed!"


## now checkout master again

repo.checkout_branch("master")

assert repo.retrieve_commit()["subdir"]["foo.txt"] == "file in subdir"

print("all tests passed.")
