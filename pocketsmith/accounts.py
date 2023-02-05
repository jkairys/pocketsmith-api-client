import datetime

from typing import List, Union, Optional
from pydantic import BaseModel, Field

from .client_base import ClientBase


class Institution(BaseModel):
    currency_code: str  # "NZD",
    title: str  # "Bank of Foo",
    updated_at: datetime.datetime  # "2015-04-21T22:42:22Z",
    created_at: datetime.datetime  # "2015-04-21T22:42:22Z",
    id: int  # 57


class Account(BaseModel):
    id: int  # 96027,
    name: str  # "Sample Credit",
    number: str  # "ASBCRD44554",
    current_balance: float  # 2694.39,
    current_balance_date: datetime.date  # "2015-07-03",
    current_balance_in_base_currency: str  # 4041.59,
    current_balance_exchange_rate: Union[float, None]  # 1.5,
    safe_balance: Optional[float]  # 2694.39,
    safe_balance_in_base_currency: Optional[float]  # 4041.59,
    starting_balance: Optional[float]  # 3547.45,
    starting_balance_date: datetime.date  # "2015-03-15",
    created_at: datetime.datetime  # "2015-03-17T02:42:10Z",
    updated_at: datetime.datetime  # "2015-07-02T22:14:49Z",
    institution: Institution
    currency_code: str  # "NZD"
    type: str  # "Bank"


class Scenario(BaseModel):
    id: int  # 42,
    title: str  # "Wedding",
    description: Union[str, None]  # "string",
    interest_rate: float  # 2.4,
    interest_rate_repeat_id: int  # 4,
    type: str  # "no-interest",
    minimum_value: Union[float, None] = Field(alias="minimum-value")  # 4000,
    maximum_value: Union[float, None] = Field(alias="maximum-value")  # 42,
    achieve_date: Union[datetime.date, None]  # "string",
    starting_balance: Union[float, None]  # 2450,
    starting_balance_date: datetime.date  # "2018-02-27",
    closing_balance: Union[float, None]  # 5431.2,
    closing_balance_date: Optional[datetime.date]  # "2018-02-27",
    current_balance: Union[float, None]  # 5431.2,
    current_balance_date: Optional[datetime.date]  # "2018-02-27",
    current_balance_in_base_currency: Union[float, None]  # 8146.8,
    current_balance_exchange_rate: Union[float, None]  # 1.5,
    safe_balance: Union[float, None]  # 5431.2,
    safe_balance_in_base_currency: Union[float, None]  # 8146.8,
    created_at: datetime.datetime  # "2015-04-21T22:42:22Z",
    updated_at: datetime.datetime  # "2015-04-21T22:42:22Z"


class ListAccountsInUserResult(BaseModel):
    """
    Gets the user that corresponds to the access token used in the request.
    """

    id: int  # 42,
    title: str  # "Bank of Foo",
    currency_code: str  # "NZD",
    type: str  # "bank",
    is_net_worth: bool  # false,
    primary_transaction_account: Account
    primary_scenario: Scenario
    transaction_accounts: List[Account]
    scenarios: List[Scenario]
    created_at: Optional[datetime.datetime]  # "2018-02-27",
    updated_at: Optional[datetime.datetime]  # "2018-02-27",
    current_balance: float  # 2694.39,
    current_balance_date: Optional[datetime.date]  # "2018-02-27",
    current_balance_in_base_currency: Optional[float]  # 4041.59,
    current_balance_exchange_rate: Optional[float]  # 1.5,
    safe_balance: Optional[float]  # 2694.39,
    safe_balance_in_base_currency: Optional[float]  # 4041.59


def parse_accounts_record(data: dict) -> ListAccountsInUserResult:
    return ListAccountsInUserResult(**data)


class Accounts(ClientBase):
    """
    User details
    """

    def list_accounts_in_user(self, user_id) -> List[ListAccountsInUserResult]:
        """
        Gets the user that corresponds to the access token used in the request.
        """
        return [
            parse_accounts_record(result)
            for result in self.api.get(f"/users/{user_id}/accounts")
        ]

    def list_transaction_accounts_in_user(self, user_id) -> List[Account]:
        return [
            Account(**result)
            for result in self.api.get(f"/users/{user_id}/transaction_accounts")
        ]
