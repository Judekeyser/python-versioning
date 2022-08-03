import re


class Version:
    def __init__(self, first, second, third=0):
        self.expand = (first, second, third)
        self.cursor = None

    def __lt__(self, other):
        for s, o in zip(self.expand, other.expand):
            if s < o: return True
            elif s > o: return False
        return False

    def increment(self):
        return Version(*(a+b for a,b in zip(self.expand, (0,0,1))))


class GitTag(Version):
    __PATTERN = re.compile(r'(\d+)\.(\d+)\.(\d+)([^\d].)*')

    def __init__(self, version):
        m = GitTag.__PATTERN.match(version['name'])
        Version.__init__(self, *(int(m.group(_)) for _ in range(1,4)))
        self.cursor = version['cursor']


def get_next_version(collection=[], lower_bound='0.0', cursor=None):
    """
    Get the next version based on the provided collection.
    The next version is guaranteed to be higher than the provided lower_bound,
    only if the highest point in the collection corresponds to a different cursor than the provided one.
    
    Parameters
    ----------
    collection
        The collection of versions to consider
    lower_bound
        The lower bound we guarantee to be higher
    cursor
        The cursor we are in. Versions might be associated to cursors.
    
    Returns
    -------
      next_version
        The next version, as a triplet
    """
    next_version = Version(*(int(_) for _ in lower_bound.split('.')))
    highest_git_tag = max((GitTag(_) for _ in collection), default=next_version)

    # Combine and retrieve if we are higher than git version
    if next_version < highest_git_tag or not highest_git_tag < next_version:
        next_version = highest_git_tag
        if cursor != next_version.cursor:
            next_version = next_version.increment()
    
    return next_version.expand


if __name__ == '__main__':
    import sys
    import git
    # Information from git repository
    repo = git.Repo(search_parent_directories=True)
    # Information from auxiliary file
    with open(sys.argv[1], 'r') as f:
        lower_bound = f.readline().strip()
    # Calling the function
    next_version = get_next_version(
        collection=({ 'name': str(_)[1:], 'cursor': _.commit }
            for _ in repo.tags if str(_).startswith('v')),
        lower_bound=lower_bound,
        cursor=repo.head.commit
    )
    print('.'.join((str(i) for i in next_version)))
