from gyt import Repo

repo = Repo()

# first we'll do this a very low level way...

# 1. create some blobs

b1 = repo.create_blob("version 1")
b2 = repo.create_blob("version 2")
b3 = repo.create_blob("new file")

# 2. add them to the index

repo.update_index({
    "test.txt": b1,
    "new.txt": b3,
}, add=True)

# 3. write the index to a tree object
t1 = repo.write_tree()

# 4. create a commit object out of it

c1 = repo.create_commit(t1, "my first commit")

# 5. and move the HEAD 

repo.refs[repo.HEAD] = c1

# now let's make a change to a file...

repo.update_index({
    "test.txt": b2,
})
t2 = repo.write_tree()

parent = repo.refs[repo.HEAD]
c2 = repo.create_commit(t2, "second commit", parents=[parent])
repo.refs[repo.HEAD] = c2

# let's create a subdirectory now

b4 = repo.create_blob("file in subdir")
t3 = repo.create_tree({
    "foo.txt": b4,
})
repo.update_index({
    "subdir": t3,
}, add=True)

t4 = repo.write_tree()

# this time we'll use the higher-level commit method

c3 = repo.commit(t4, "added subdir")

# retrieve subdir/foo.txt from HEAD

print(repo.expand(repo.refs[repo.HEAD])["subdir"]["foo.txt"])

# now let's create a branch

repo.create_branch("branch-test")
repo.checkout_branch("branch-test")

b5 = repo.create_blob("changed!")
t5 = repo.create_tree({
    "foo.txt": b5,
})
repo.update_index({
    "subdir": t5,
})
t6 = repo.write_tree()
c4 = repo.commit(t6, "changed file in subdirectory")

# this should print "changed!"

print(repo.expand(repo.refs[repo.HEAD])["subdir"]["foo.txt"])

# now checkout master again

repo.checkout_branch("master")

print(repo.expand(repo.refs[repo.HEAD])["subdir"]["foo.txt"])
