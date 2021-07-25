import git

repo = git.Repo(search_parent_directories = True)
sha = repo.head.object.hexsha
print(repo.tags[-1])            # Current tag version


g = git.cmd.Git()
blob = g.ls_remote('https://github.com/Guitarrunner/VLSI-Express-Chip-Design', sort='-v:refname', tags=True)
tag = blob.split('\n')[0].split('/')[-1]  # 'v3.9.0a6'
print(tag)                      # Remote current tag version
