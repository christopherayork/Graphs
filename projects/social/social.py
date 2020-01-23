import random
import sys
sys.path.append('../graph/')
from util import Queue


class User:
    def __init__(self, name):
        self.name = name


names = ['Bill', 'Tom', 'Brian', 'Hank', 'Joe', 'Sally', 'Susan', 'Ethel', 'Bertha', 'Barbara']


class SocialGraph:
    def __init__(self):
        self.last_id = 0
        self.users = {}
        self.friendships = {}

    def add_friendship(self, user_id, friend_id):
        """
        Creates a bi-directional friendship
        """
        if user_id == friend_id:
            print("WARNING: You cannot be friends with yourself")
        elif friend_id in self.friendships[user_id] or user_id in self.friendships[friend_id]:
            print("WARNING: Friendship already exists")
        else:
            self.friendships[user_id].add(friend_id)
            self.friendships[friend_id].add(user_id)

    def add_user(self, name):
        """
        Create a new user with a sequential integer ID
        """
        self.last_id += 1  # automatically increment the ID to assign the new user
        self.users[self.last_id] = User(name)
        self.friendships[self.last_id] = set()

    def populate_graph(self, num_users, avg_friendships):
        """
        Takes a number of users and an average number of friendships
        as arguments

        Creates that number of users and a randomly distributed friendships
        between those users.

        The number of users must be greater than the average number of friendships.
        """
        if num_users < avg_friendships: return False  # users must be higher
        # Reset graph
        self.last_id = 0
        self.users = {}
        self.friendships = {}
        # !!!! IMPLEMENT ME

        # Add users
        for x in range(1, num_users + 1):
            self.add_user(random.choice(names))
        # Create friendships
        for x in range(1, num_users + 1):
            user = self.users[x]
            user_friends = self.friendships[x]
            possible_ids = set([random.randrange(1, num_users + 1) for x in range(avg_friendships)])
            # the above has the possibility of selecting a user to be it's own friend, which add_friend should handle
            for y in possible_ids:
                # x is the user id, y is the random friend id
                self.add_friendship(x, y)

    def bfs(self, user_id, friend_id):
        queue = Queue()
        queue.enqueue([user_id])
        visited = set()
        while queue.size() > 0:
            path = queue.dequeue()
            vertex = path[-1]
            if vertex not in visited:
                if vertex == friend_id:
                    return path
                visited.add(vertex)
                for next_vert in self.friendships[vertex]:
                    new_path = list(path)
                    new_path.append(next_vert)
                    queue.enqueue(new_path)

    def get_all_social_paths(self, user_id):
        """
        Takes a user's user_id as an argument

        Returns a dictionary containing every user in that user's
        extended network with the shortest friendship path between them.

        The key is the friend's ID and the value is the path.
        """
        visited = {}  # Note that this is a dictionary, not a set
        # !!!! IMPLEMENT ME
        all_friends = set()
        queue = Queue()
        queue.enqueue(user_id)
        while queue.size() > 0:
            vertex = queue.dequeue()
            if vertex not in all_friends:
                all_friends.add(vertex)
                for next_vert in self.friendships[vertex]:
                    queue.enqueue(next_vert)
        for friend in all_friends:
            visited[friend] = self.bfs(user_id, friend)
        return visited


if __name__ == '__main__':
    sg = SocialGraph()
    sg.populate_graph(10, 2)
    print(sg.friendships)
    connections = sg.get_all_social_paths(1)
    print(connections)

    # calculate the degrees of separation for 1000 users with average 5 friends
    st = SocialGraph()
    st.populate_graph(1000, 5)
    st_con = st.get_all_social_paths(1)
    total = 0
    for user_id in st_con:
        total += len(st_con[user_id]) - 1
    print(f'Friends in network: {len(st_con)}')
    print(f'Degrees of separation: {total / len(st_con)}')
