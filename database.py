import itertools
import json
import random
import sys
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

from loguru import logger

from client import Client
from config import USE_MOBILE_PROXY
from constants import DATABASE_FILE_PATH, PRIVATE_KEYS_FILE_PATH, PROXIES_FILE_PATH
from utils import read_from_txt
from wallet_model import Wallet


@dataclass
class Database:
    wallets: List[Wallet]

    @staticmethod
    def _create_database() -> "Database":
        data = []
        private_keys = read_from_txt(file_path=PRIVATE_KEYS_FILE_PATH)

        proxies = read_from_txt(file_path=PROXIES_FILE_PATH)
        if USE_MOBILE_PROXY:
            proxies = proxies * len(private_keys)

        for pk, proxy in itertools.zip_longest(private_keys, proxies, fillvalue=None):
            try:
                wallet = Wallet(account=Client(private_key=pk, proxy=proxy))
            except TypeError:
                logger.error(
                    f"Amount of proxies is greater than amount of private keys. Proxies count: `{len(proxies)}`. Private keys count: `{len(private_keys)}`"
                )
                sys.exit(1)
            data.append(wallet)
        logger.success("Database created")
        return Database(wallets=data)

    def _to_dict(self) -> List[Dict[str, Any]]:
        return [vars(wallet) for wallet in self.wallets]

    @classmethod
    def read_from_json(cls, file_path: str = DATABASE_FILE_PATH) -> "Database":
        try:
            with open(file=file_path, mode="r") as json_file:
                data_dict = json.load(fp=json_file)
        except Exception as e:
            logger.error(f"Failed to read database: {e}")
            sys.exit(1)
        wallets = []
        for item in data_dict:
            wallet_data = {
                "private_key": item.pop("private_key"),
                "proxy": item.pop("proxy"),
            }
            item.pop("address")
            client = Client(**wallet_data)
            wallet = Wallet(account=client, **item)
            wallets.append(wallet)
        return cls(wallets=wallets)

    def get_random_wallet(self) -> Optional[Tuple[Wallet, int]]:
        if self.wallets:
            random_index = random.randrange(len(self.wallets))
            return self.wallets[random_index], random_index
        return None

    def delete_wallet(self, wallet_index: int) -> None:
        self.wallets.pop(wallet_index)
        self.save_database()

    def save_database(self, file_path: str = DATABASE_FILE_PATH) -> None:
        data_dict = self._to_dict()
        with open(file=file_path, mode="w") as json_file:
            json.dump(obj=data_dict, fp=json_file, indent=4)

    def is_empty(self) -> bool:
        return not bool(self.wallets)

    @staticmethod
    def create_database():
        db = Database._create_database()
        db.save_database()
