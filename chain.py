from dataclasses import dataclass
from typing import Optional

from config import MAINNET_RPC_ENDPOINT, ZKSYNC_ERA_RPC_ENDPOINT


@dataclass
class Chain:
    name: str
    chain_id: int
    coin_symbol: str
    rpc: str
    explorer: Optional[str] = None


ZKSYNC = Chain(
    name="ZkSync Era",
    chain_id=324,
    coin_symbol="ETH",
    explorer="https://explorer.zksync.io/",
    rpc=ZKSYNC_ERA_RPC_ENDPOINT,
)

MAINNET = Chain(
    name="Ethereum Mainnet", chain_id=1, coin_symbol="ETH", rpc=MAINNET_RPC_ENDPOINT
)
