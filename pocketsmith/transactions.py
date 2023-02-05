from typing import List, Optional
from pydantic import BaseModel
import datetime
from .client_base import ClientBase
from enum import Enum
from .accounts import Account


class TransactionType(Enum):
    DEBIT = "debit"
    CREDIT = "credit"


class MeResult(BaseModel):
    pass


class TransactionCategory(BaseModel):
    id: int  # 11915947,
    title: str  # "Transfers",
    colour: Optional[str]  # null,
    is_transfer: str  # true,
    is_bill: bool  # false,
    refund_behaviour: Optional[str]  # null,
    children: Optional[List["TransactionCategory"]]  # [],
    parent_id: Optional[int]  # null,
    roll_up: bool  # false,
    created_at: datetime.datetime  # "2023-01-23T10:23:40Z",
    updated_at: datetime.datetime  # "2023-02-04T03:50:11Z"


class Transaction(BaseModel):

    id: int  # 546270181,
    payee: str  # "INTERNET TRANSFER CREDIT",
    original_payee: str  # "INTERNET TRANSFER CREDIT",
    date: datetime.date  # "2023-01-30",
    upload_source: str  # "data_feed",
    category: Optional[TransactionCategory]
    closing_balance: float  # 413.0,
    cheque_number: Optional[str]  # null,
    memo: Optional[str]  # null,
    amount: float  # 12.07,
    amount_in_base_currency: float  # 12.07,
    type: TransactionType  # "credit",
    is_transfer: Optional[bool]  # true,
    needs_review: bool  # false,
    status: str  # "posted",
    note: Optional[str]  # null,
    labels: Optional[List[str]]  # [],
    transaction_account: Account
    # "id": 1988428,
    # "account_id": 1916146,
    # "name": "LIFESTYLE",
    # "latest_feed_name": "LIFESTYLE",
    # "number": "4847994760042",
    # "type": "bank",
    # "offline": false,
    # "is_net_worth": false,
    # "currency_code": "aud",
    # "current_balance": 584.09,
    # "current_balance_in_base_currency": 584.09,
    # "current_balance_exchange_rate": null,
    # "current_balance_date": "2023-02-05",
    # "current_balance_source": "data_feed",
    # "data_feeds_balance_type": "balance",
    # "safe_balance": null,
    # "safe_balance_in_base_currency": null,
    # "has_safe_balance_adjustment": false,
    # "starting_balance": 195.99,
    # "starting_balance_date": "2023-01-23",
    # "institution": {
    #   "id": 724300,
    #   "title": "Suncorp",
    #   "currency_code": "aud",
    #   "created_at": "2023-01-23T10:23:31Z",
    #   "updated_at": "2023-01-23T10:23:31Z"
    # },
    # "data_feeds_account_id": "334992",
    # "data_feeds_connection_id": "140530",
    # "created_at": "2023-01-23T10:23:32Z",
    # "updated_at": "2023-02-05T03:24:53Z"
    # },
    created_at: datetime.datetime  # "2023-01-30T16:26:00Z",
    updated_at: datetime.datetime  # "2023-01-31T09:22:35Z"


def bool_to_int(value: bool) -> int:
    if value is None:
        return None
    if value:
        return 1
    return 0


class Transactions(ClientBase):
    def list_transactions_in_user(
        self,
        user_id: int,
        start_date: datetime.datetime = None,
        end_date: datetime.datetime = None,
        updated_since: datetime.datetime = None,
        uncategorised: bool = False,
        transaction_type: TransactionType = None,
        needs_review: bool = None,
        search: str = None,
        page: int = None,
    ) -> List[Transaction]:
        if start_date is None:
            start_date = datetime.datetime.utcnow() - datetime.timedelta(days=7)
        if end_date is None and start_date is not None:
            end_date = datetime.datetime.utcnow()

        params = {
            "start_date": start_date.isoformat() if start_date is not None else None,
            "end_date": end_date.isoformat() if end_date is not None else None,
            "updated_since": updated_since.isoformat()
            if updated_since is not None
            else None,
            "uncategorised": bool_to_int(uncategorised),
            "type": transaction_type.value if transaction_type is not None else None,
            "needs_review": bool_to_int(needs_review),
            "search": search,
            "page": page,
        }

        return [
            Transaction(**trans)
            for trans in self.api.get(
                f"/users/{user_id}/transactions",
                params={k: v for k, v in params.items() if v is not None},
            )
        ]
