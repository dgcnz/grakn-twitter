from graph import Node, bfs, dfs
from twitter_controller import check_rate_limit, get_current_id_name, get_next_mutuals
from grakn.client import GraknClient
from functools import partial


def grakn_write(grakn_session, raw_query, n_args, u, v):
    if (n_args == 1 and (u is None and v is None)):
        return
    if (n_args == 2 and (u is None or v is None)):
        return

    with grakn_session.transaction().write() as write_transaction:
        print(f"Inserting: {u} -> {v}", end="")
        write_transaction.query(raw_query.format(**locals()))
        write_transaction.commit()
        print(f"\tSUCCESS")


def grakn_save(root):
    with GraknClient(uri="localhost:48555") as client:
        with client.session(keyspace="twitter") as session:
            insert_person = partial(
                grakn_write, session,
                'insert $x isa person, has full-name "{v.name}", has uuid "{v.id}";',
                1)
            insert_friendship = partial(
                grakn_write, session,
                'match $p1 isa person, has uuid "{u.id}"; $p2 isa person, has uuid "{v.id}";insert $new_friendship (friend: $p1, friend: $p2) isa friendship;',
                2)

            print("INSERTING PEOPLE")
            dfs(root, lambda v: v.neighbors, None, insert_person)
            print("INSERTING FRIENDSHIPS")
            dfs(root, lambda v: v.neighbors, None, insert_friendship)


def main():
    check_rate_limit()

    user_id, user_name = get_current_id_name()
    root = Node(user_id, user_name)
    root = dfs(root, get_next_mutuals, 2)
    bfs(root, lambda v: v.neighbors, print, 3)
    check_rate_limit()

    grakn_save(root)


if __name__ == "__main__":
    main()
