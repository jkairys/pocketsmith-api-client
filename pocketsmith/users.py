import datetime

from pydantic import BaseModel

from .client_base import ClientBase


class MeResult(BaseModel):
    """
    Gets the user that corresponds to the access token used in the request.
    """

    id: int  # 42,
    login: str  # "sampleuser69",
    name: str  # "Foo Barrington",
    email: str  # "user69@sample.com",
    avatar_url: str  # "https://image.com/image.png",
    beta_user: bool  # true,
    time_zone: str  # "Auckland",
    week_start_day: int  # 1,
    is_reviewing_transactions: bool  # true,
    base_currency_code: str  # "NZD",
    always_show_base_currency: bool  # false,
    using_multiple_currencies: bool  # true,
    available_accounts: int  # 3,
    available_budgets: int  # 3,
    forecast_last_updated_at: datetime.datetime  # "2015-07-02T22:14:49Z",
    forecast_last_accessed_at: datetime.datetime  # "2015-07-02T22:14:49Z",
    forecast_start_date: datetime.date  # "2015-07-01",
    forecast_end_date: datetime.date  # "2015-07-15",
    forecast_defer_recalculate: bool  # false,
    forecast_needs_recalculate: bool  # true,
    last_logged_in_at: datetime.datetime  # "2015-07-02T22:14:49Z",
    last_activity_at: datetime.datetime  # "2015-07-02T22:14:49Z",
    created_at: datetime.datetime  # "2015-07-02T22:14:49Z",
    updated_at: datetime.datetime  # "2015-07-02T22:14:49Z"


class GetUserResult(MeResult):
    "Gets a user by ID. You must be authorised as the target user in order to make this request"


class Users(ClientBase):
    """
    User details
    """

    def get_me(self) -> MeResult:
        """
        Gets the user that corresponds to the access token used in the request.
        """
        return MeResult(**self.api.get("/me"))

    # pylint: disable=W0622, C0103
    def get_user(self, id: int) -> GetUserResult:
        """
        Gets a user by ID. You must be authorised as the target
        user in order to make this request.
        """
        return GetUserResult(**self.api.get(f"/users/{id}"))
