from typing import List, Optional, Tuple

from loguru import logger
from web3.contract.async_contract import AsyncContract

from client import Client
from config import GAS_DELAY_RANGE, GAS_THRESHOLD, TX_DELAY_RANGE
from constants import (
    CLAIMABLE_AMOUNT_URL,
    CLAIMER_CONTRACT_ABI_FILE_PATH,
    CLAIMER_CONTRACT_ADDRESS,
    PROOF_URL,
    ZKPEPE_DECIMALS,
)
from database import Database
from utils import gas_delay, menu_message, read_from_json, sleep


class Claimer:
    def __init__(self, client: Client) -> None:
        self.client: Client = client
        self.claimer_contract: AsyncContract = self.client.w3.eth.contract(
            address=CLAIMER_CONTRACT_ADDRESS,
            abi=read_from_json(file_path=CLAIMER_CONTRACT_ABI_FILE_PATH),
        )

    @gas_delay(gas_threshold=GAS_THRESHOLD, delay_range=GAS_DELAY_RANGE)
    async def _claim(self) -> bool:
        if await self._check_if_claimed():
            logger.warning(f"Already claimed for {self.client}")
            return True
        claim_data = await self._get_claim_data()
        if not claim_data:
            logger.error(f"Failed to fetch claim data for {self.client}")
            return False
        amount, proof = claim_data

        logger.info(f"Claiming {amount} $ZKPEPE for {self.client}")
        data = self.claimer_contract.encodeABI(
            fn_name="claim", args=(proof, int(amount * pow(10, ZKPEPE_DECIMALS)))
        )
        tx_hash = await self.client.send_transaction(
            to=self.claimer_contract.address, data=data
        )
        if tx_hash:
            return await self.client.verify_tx(tx_hash=tx_hash)
        return False

    async def _get_proof(self) -> List[str]:
        return await self.client.send_get_request(
            url=PROOF_URL.format(self.client.address.lower()), use_proxy=False
        )

    async def _get_claimable_amount(self) -> int:
        (amount,) = await self.client.send_get_request(
            url=CLAIMABLE_AMOUNT_URL.format(self.client.address.lower()),
            use_proxy=False,
        )
        return amount

    async def _get_claim_data(self) -> Optional[Tuple[int, List[str]]]:
        amount = await self._get_claimable_amount()
        proof = await self._get_proof()
        if amount and proof:
            return amount, proof
        return None

    async def _check_if_claimed(self) -> bool:
        try:
            return await self.claimer_contract.functions.claimRecord(
                self.client.address
            ).call()
        except Exception as e:
            logger.error(f"Couldn't fetch {self.client} claim status: {e}")
            return False

    @staticmethod
    async def claim() -> None:
        database = Database.read_from_json()
        while not database.is_empty():
            wallet, index = database.get_random_wallet()
            if wallet.tokens_claimed:
                database.delete_wallet(wallet_index=index)
                continue
            client = Client(private_key=wallet.private_key, proxy=wallet.proxy)
            claimer = Claimer(client=client)
            tokens_claimed = await claimer._claim()
            if tokens_claimed:
                database.delete_wallet(wallet_index=index)
            await sleep(delay_range=TX_DELAY_RANGE, send_message=False)
        logger.success("Claimed $ZKPEPE on all wallets")

    @staticmethod
    async def menu() -> None:
        menu_message()
        module_num = input("Module number: ")
        if module_num == "1":
            Database.create_database()
        elif module_num == "2":
            await Claimer.claim()
        else:
            logger.error("[MANAGER] Wrong module selected")
