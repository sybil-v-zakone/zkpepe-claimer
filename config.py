# RPCs configuration
ZKSYNC_ERA_RPC_ENDPOINT = "https://mainnet.era.zksync.io"  # советуем getblock
MAINNET_RPC_ENDPOINT = (
    "https://rpc.eth.gateway.fm"  # тоже обязательно заполнить (любая ок)
)

# Proxy (Если используете стандартные прокси, то просто записывайте их в proxies.txt)
USE_MOBILE_PROXY = False

# Диапазон задержки между транзакциями
TX_DELAY_RANGE = [10, 15]

# Максимальный газ в MAINNET
GAS_THRESHOLD = 70
# Диапазон для задержки между проверками газа
GAS_DELAY_RANGE = [10, 10]
