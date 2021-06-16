# How To Use
```bash
> git clone https://github.com/krypton-byte/gitpy3
> python3 -m pip install -r gitpy3/requirements.txt
> python3
```
```python3
>>> from gitpy3 import owner, SearchRepos
>>> owner("krypton-byte")
<[ username: krypton-byte ]>
>>> owner("krypton-byte).gists
[<[ Gist: 1 Files ]>]
>>> SearchRepos("gitpy")
<[ Total: 2]>
```
# Features

|Feature  |Status
|---------|----
|get owner | yes
|get repo | yes
|get gist |yes
|download repo|yes
|download gists|yes
|get_follower|yes
|get_following|yes
|screenshot Readme/Markdown|yes
|Search Repo|yes
|commits|yes
|subscription|yes
|fork |yes
