import re
import git


class Version:
    def __init__(self, first, second, third):
        self.expand = (first, second, third)

    def __lt__(self, other):
        for s, o in zip(self.expand, other.expand):
            if s < o: return True
            elif s > o: return False
        return False

    def __str__(self):
        return '.'.join((str(i) for i in self.expand))

    def increment(self):
        return Version(*(a+b for a,b in zip(self.expand, (0,0,1))))


class GitVersionTag(Version):
    __PATTERN = re.compile(r'v(\d+)\.(\d+)\.(\d+)[ab]?(\+\d+)?')

    def __init__(self, git_tag):
        m = GitVersionTag.__PATTERN.match(str(git_tag))
        Version.__init__(self, *(int(m.group(_)) for _ in range(1,4)))
        self.git_tag = git_tag


def get_next_version(version_file_path, release_type='alpha'):
    """
    Get the next version, based on GIT repository state, content of version file and release type.
    
    Parameters
    ----------
    version_file_path : str
      The path to the file containing the reference {major}.{minor}
    release_type : str
      One of "production", "alpha" or "beta". Default is "alpha"
    
    Returns
    -------
      next_version : str
        The next version, as a string of the form {major}.{minor}.{patch}
        for production release, and {major}.{minor}.{patch}[a|b]+[near unique hash]
        for alpha and beta releases.
    """
    # Get information from Git Repository
    repo = git.Repo(search_parent_directories=True)
    head_commit = repo.head.commit
    highest_from_git = max((GitVersionTag(t) for t in repo.tags if str(t).startswith('v')))

    # Get information from auxiliary file
    with open(version_file_path, 'r') as f:
        line = f.readline().strip()
    m = re.compile(r'(\d+)\.(\d+)').match(line)
    next_version = Version(int(m.group(1)), int(m.group(2)), 1)

    # Combine and retrieve if we are higher than git version
    if next_version < highest_from_git or not(highest_from_git < next_version):
        next_version = highest_from_git
        if head_commit != next_version.git_tag.commit:
            next_version = next_version.increment()

    # Return a string representation, based on head commit and release type
    return str(next_version) + ('{}+{}'.format(
        release_type[0],
        str(head_commit)[:7]
    ) if release_type != 'production' else '')


if __name__ == '__main__':
    import sys
    print(get_next_version(sys.argv[1], release_type=sys.argv[2]))
