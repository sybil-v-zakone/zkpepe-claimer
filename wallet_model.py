from typing import Optional

from client import Client


class Wallet:
    def __init__(
        self,
        account: Client,
        tokens_claimed: Optional[bool] = False

    ) -> None:
        self.private_key: str = account.private_key
        self.address: str = account.address
        self.proxy: str = account.proxy
        self.tokens_claimed: bool = tokens_claimed

    def _to_dict(self):
        return self.__dict__
