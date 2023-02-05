from pocketsmith.client import Client
import datetime


def test_transactions(client: Client, user_id):
    transactions = client.list_transactions_in_user(
        user_id=user_id,
        updated_since=datetime.datetime.strptime(
            "2023-02-05T02:00:00", "%Y-%m-%dT%H:%M:%S"
        ),
    )

    print(
        "\n".join(
            [
                f"{t.updated_at} {t.date} {t.payee} {t.original_payee} {'<' + t.note + '>' if t.note else ''} {t.transaction_account.name} ({t.category.title if t.category else '-'}) {t.labels} {t.amount}"
                for t in transactions
            ]
        )
    )
