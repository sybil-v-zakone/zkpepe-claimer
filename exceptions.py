class NoRPCEndpointSpecifiedError(Exception):
    def __init__(
        self,
        chain,
        message: str = "No RPC endpoint specified for {}. Specify one in config.py file.",
        *args: object,
    ) -> None:
        self.message = message.format(chain.name)
        super().__init__(self.message, *args)


class AlreadyClaimedError(Exception):
    def __init__(
        self,
        chain,
        message: str = "No RPC endpoint specified for {}. Specify one in config.py file.",
        *args: object,
    ) -> None:
        self.message = message.format(chain.name)
        super().__init__(self.message, *args)
