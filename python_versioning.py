import re
import git


class Version:
    def __init__(self, first, second, third):
        self.expand = (first, second, third)
        self.commit = None

    def __lt__(self, other):
        for s, o in zip(self.expand, other.expand):
            if s < o: return True
            elif s > o: return False
        return False

    def increment(self):
        return Version(*(a+b for a,b in zip(self.expand, (0,0,1))))


class GitVersionTag(Version):
    __PATTERN = re.compile(r'v(\d+)\.(\d+)\.(\d+)([^\d]*)?')

    def __init__(self, git_tag):
        m = GitVersionTag.__PATTERN.match(str(git_tag))
        Version.__init__(self, *(int(m.group(_)) for _ in range(1,4)))
        self.commit = git_tag.commit


def get_next_version(version_file_path):
    """
    Get the next version, based on GIT repository state, content of version file and release type.
    
    Parameters
    ----------
    version_file_path : str
      The path to the file containing the reference {major}.{minor}
    
    Returns
    -------
      next_version : str
        The next version, as a string of the form {major}.{minor}.{patch}
    """
    # Get information from Git Repository
    repo = git.Repo(search_parent_directories=True)
    highest_git_tag = max((GitVersionTag(_) for _ in repo.tags if str(_).startswith('v')), default=Version(0,0,0))

    # Get information from auxiliary file
    with open(version_file_path, 'r') as f:
        line = f.readline().strip()
    m = re.compile(r'(\d+)\.(\d+)').match(line)
    next_version = Version(*(int(m.group(_)) for _ in range(1,3)), 0)

    # Combine and retrieve if we are higher than git version
    if next_version < highest_git_tag:
        next_version = highest_git_tag
    if repo.head.commit != next_version.commit:
        next_version = next_version.increment()
    
    return '.'.join((str(i) for i in next_version.expand))


if __name__ == '__main__':
    import sys    # Return a string representation, based on head commit and release type
    print(get_next_version(sys.argv[1]))
