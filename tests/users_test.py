from pocketsmith.client import Client


def test_me(client: Client):
    user = client.get_me()
    assert user.id == 345634

    them = client.get_user(user.id)
    assert them.id == 345634
