from requests import get
from github_markdown2image import readme
from io import BytesIO
proxy   = {}
headers = {}
class UsernameInvalid(Exception):
    pass
class download:
    def __init__(self, url):
        self.url    = url
        self.object = get(self.url, headers=headers, proxies=proxy, stream=True)
        self.size   = int(self.object.headers.get("Content-Length", len(self.object.content)))
    def save(self, filename=False):
        if not filename:
            return BytesIO(self.object.content)
        else:
            open(filename, "wb").write(self.object.content)
    def __repr__(self):
        return f"<[ Length: {self.size} ]>"
class SearchRepos:
    def __init__(self, query, language=None):
        self.query       = query
        self.language    = language
        self.resp        = get(f"https://api.github.com/search/repositories",params={"q":f"{self.query} {f'language:{self.language}' if self.language else ''}"}, headers=headers, proxies=proxy).json()
        self.result      = [repo_object(repos) for repos in self.resp["items"]]
        self.total_count = self.resp["total_count"]
    def __repr__(self) -> str:
        return f"<[ Total: {self.total_count}]>"
class file_gist:
    def __init__(self, js) -> None:
        self.js       = js
        self.filename = self.js["filename"]
        self.type     = self.js["type"]
        self.language = self.js["language"]
        self.size     = self.js["size"]
    def get_raw(self):
        return get(self.js["raw_url"], headers=headers, proxies=proxy).content
    def download(self):
        return download(self.js["raw"])
    def __repr__(self) -> str:
        return f"<[ Filename: {self.js['filename']}   Size: {self.js['size']}  ]>"
class gists:
    def __init__(self, js):
        self.js    = js
        self.files = [file_gist(self.js["files"][url]) for url in self.js["files"].keys()]
        self.url   = self.js["url"]
    def owner(self):
        return owner(self.js["owner"]["login"])
    def get_commits(self):
        return [gists(comuser["url"]) for comuser in get(self.url+"/commits", headers=headers, proxies=proxy).json()]
    def __repr__(self) -> str:
        return f"<[ Gist: {len(self.js['files'].keys())} Files ]>"
class repo_object:
    def __init__(self, js, is_owner=False):
        self.js        = js
        self.id        = self.js["id"]
        self.name      = self.js["name"]
        self.full_name = self.js["full_name"]
        self.language  = self.js["language"]
        self.is_owner  = is_owner
        self.stargazers= self.js["stargazers_count"]
        self.branch    = self.js['default_branch']
        self.watcher   = self.js["watchers_count"]
    def readme(self, filename=False):
        return readme(f"https://github.com/{self.full_name}", filename)
    def owner(self):
        return owner(self.js["owner"]["login"])
    def download(self):
        return download(f"https://github.com/{self.full_name}/archive/{self.branch}.zip")
    def fork(self):
        return [repo_object(i) for i in [x for x in get(f"https://api.github.com/repos/{self.full_name}/forks", headers=headers,proxies=proxy).json()]]
    def __repr__(self):
        if self.is_owner:
            return f"<[ repository: {self.name} ]>"
        else:
            return f"<[ repository: {self.full_name} ]>"
    def __str__(self):
        if self.is_owner:
            return f"<[ repository: {self.name} ]>"
        else:
            return f"<[ repository: {self.full_name} ]>"
class owner:
    def __init__(self, username=None, js={}):
        try:
            self.username    = js["login"] if js else username
            self.js          = js if js else get(f"https://api.github.com/users/{self.username}", headers=headers, proxies=proxy).json()
            self.name        = self.js.get("name", None)
            self.type        = self.js.get("type", None)
            self.bio         = self.js.get("bio", None)
            self.email       = self.js.get("email", None)
            self.location    = self.js.get("location", None)
            self.site_admin  = self.js.get("site_admin", None)
            self.blog        = self.js.get("blog", None)
            self.company     = self.js.get("company", None)
            self.profile_pic = download(self.js["avatar_url"])
            self.hireable    = self.js.get("hireable", None)
        except KeyError:
            raise UsernameInvalid("404")

    def __repr__(self):
        return f"<[ username: {self.username} ]>"
    def get_subcriptions(self):
        return [repo_object(repo) for repo in get(f"https://api.github.com/users/{self.username}/subscriptions", proxies=proxy, headers=headers).json()]
    def owner(self):
        return owner(self.username)
    def get_repos(self):
        return [repo_object(i, is_owner=True) for i in get(f"https://api.github.com/users/{self.username}/repos", headers=headers, proxies=proxy).json() ]
    def get_followers(self):
        return [owner(js=user) for user in get(f"https://api.github.com/users/{self.username}/followers", headers=headers, proxies=proxy).json()]
    def get_following(self):
        return [owner(js=user) for user in get(f"https://api.github.com/users/{self.username}/following", headers=headers, proxies=proxy).json()]
    def get_gists(self):
        return [gists(gist_) for gist_ in get(f"https://api.github.com/users/{self.username}/gists", headers=headers, proxies=proxy).json()]