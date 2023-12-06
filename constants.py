# regex for matching the valid proxy format
PROXY_PATTERN = r"^([^:@\s]+):([^:@\s]+)@([a-zA-Z0-9.-]+|\d+\.\d+\.\d+\.\d+):(\d+)$"

# client configuration
REQUEST_MAX_RETRIES = 10
RETRY_DELAY_RANGE = [5, 10]
VERIFY_TX_TIMEOUT = 300
REQUEST_TIMEOUT = 100

# files configuration
DATABASE_FILE_PATH = "data/database.json"
PRIVATE_KEYS_FILE_PATH = "data/private_keys.txt"
PROXIES_FILE_PATH = "data/proxies.txt"

# zkpepe
CLAIMABLE_AMOUNT_URL = "https://www.zksyncpepe.com/resources/amounts/{}.json"
PROOF_URL = "https://www.zksyncpepe.com/resources/proofs/{}.json"
CLAIMER_CONTRACT_ADDRESS = "0x95702a335e3349d197036Acb04BECA1b4997A91a"
CLAIMER_CONTRACT_ABI_FILE_PATH = "claimerABI.json"
ZKPEPE_DECIMALS = 18
