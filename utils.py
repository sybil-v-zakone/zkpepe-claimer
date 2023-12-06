import asyncio
import functools
import json
import random
import sys
from typing import Any, Dict, List, Optional

from loguru import logger
from tqdm import tqdm
from web3 import AsyncWeb3

from chain import MAINNET
from constants import RETRY_DELAY_RANGE


def read_from_json(file_path) -> Dict[str, Any]:
    try:
        with open(file_path) as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        logger.error(f"File '{file_path}' not found.")
    except Exception as e:
        logger.error(
            f"Encountered an unexpected error while reading a JSON file '{file_path}': {e}."
        )
    sys.exit(1)


async def sleep(
    delay_range: List[int], send_message: bool = True, pr_bar: bool = True
) -> None:
    delay = random.randint(*delay_range)

    if send_message:
        logger.info(f"Sleeping for {delay} seconds...")

    if pr_bar:
        with tqdm(
            total=delay, desc="Waiting", unit="s", dynamic_ncols=True, colour="blue"
        ) as pbar:
            for _ in range(delay):
                await asyncio.sleep(delay=1)
                pbar.update(1)
    else:
        await asyncio.sleep(delay=delay)


async def get_eth_gas_fee():
    w3 = AsyncWeb3(AsyncWeb3.AsyncHTTPProvider(MAINNET.rpc))
    return await w3.eth.gas_price


def gas_delay(gas_threshold: int, delay_range: list):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            while True:
                current_eth_gas_price = await get_eth_gas_fee()
                threshold = AsyncWeb3.to_wei(gas_threshold, "gwei")
                if current_eth_gas_price > threshold:
                    random_delay = random.randint(*delay_range)
                    logger.warning(
                        f"Current gas fee {round(AsyncWeb3.from_wei(current_eth_gas_price, 'gwei'), 2)} GWEI > Gas threshold {AsyncWeb3.from_wei(threshold, 'gwei')} GWEI. Waiting for {random_delay} seconds..."
                    )
                    await sleep(delay_range=delay_range, send_message=False)
                else:
                    break
            return await func(*args, **kwargs)

        return wrapper

    return decorator


def retry(tries: int, retry_delay_range: Optional[List[int]] = RETRY_DELAY_RANGE):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            for _ in range(tries):
                result = await func(*args, **kwargs)
                if result is None or result is False:
                    await sleep(delay_range=retry_delay_range, send_message=False)
                else:
                    return result
            return False

        return wrapper

    return decorator


def read_from_txt(file_path: str) -> List[str]:
    try:
        with open(file_path, "r") as file:
            return [line.strip() for line in file]
    except FileNotFoundError as e:
        logger.error(f"File `{file_path}` not found.")
    except PermissionError as e:
        logger.error(f"Permission error while reading `{file_path}`: {e}")
    except Exception as e:
        logger.error(f"Error while reading `{file_path}`: {e}")
    sys.exit(1)


def menu_message() -> None:
    logger.debug(
        r"""

                  __  '              _ ,.,              ,.,  ' ‘                       _ ‘     
            ,·:'´/::::/'`;·.,        '/:::::/`,           /:::/';       /:¯:'`:*:^:*:´':¯::/'`;‘  
        .:´::::/::::/:::::::`;     /;: :;/:::\         /;:;/:'i‘      /:: :: : : : : : :::/::'/   
       /:;:· '´ ¯¯'`^·-;::::/' ‘  ,´     `;::';       ,´   'i:'i     ,´¯ '` * ^ * ´' ¯   '`;/    ‘
      /·´           _   '`;/‘     i        \::',      ,:    'i:';    '`,                  ,·'   '   
     'i            ;::::'`;*       ;         ';::\ .,_';     ';:'i'      '`*^*'´;       .´         ‘
      `;           '`;:::::'`:,    ';         ';::/::::';     ;':;            .´     .'      _   ' ‘
        `·,           '`·;:::::';   \          \/::::;'      i:/'°        .´      ,'´~:~/:::/`:, 
      ,~:-'`·,           `:;::/'    '\          '`~'´     ,'/          .´      ,'´::::::/:::/:::'i‘
     /:::::::::';           ';/        \                  /          ,'        '*^~·~*'´¯'`·;:/ 
   ,:~·- . -·'´          ,'´           '`,             ;'           /                        ,'/  
   '`·,               , ·'´                `·.,    ,.·´            ';                      ,.´    
        '`*^·–·^*'´'           ‘               ¯         °         '`*^~–––––-·~^'´       


1. [DATABASE] Создать базу данных | Create database
2. [CLAIMER] Клеймер $ZKPEPE | $ZKPEPE Claimer
"""
    )
