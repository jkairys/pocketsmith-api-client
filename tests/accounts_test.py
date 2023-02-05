from pocketsmith.client import Client


def test_accounts(client: Client):
    accounts = client.list_accounts_in_user(345634)

    account_titles = [account.title for account in accounts]
    assert "BILLS" in account_titles
    assert "LIFESTYLE" in account_titles
