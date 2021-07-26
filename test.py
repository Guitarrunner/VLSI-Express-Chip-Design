import git

# Current tag version
repo = git.Repo(search_parent_directories = True)
repoTag = repo.tags[-1]
print(repoTag)           

# Remote current tag version
g = git.cmd.Git()
blob = g.ls_remote('https://github.com/Guitarrunner/VLSI-Express-Chip-Design', sort='-v:refname', tags=True)
remoteTag = blob.split('\n')[0].split('/')[-1]  #
print(remoteTag)                      
