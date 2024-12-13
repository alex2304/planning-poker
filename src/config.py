import os


class DefaultConfig:
    # Maximum number of rooms allowed for in-memory storage; older rooms will be deleted if exceeded.
    # Protects API from abuse due to creating a new room on every request.
    IN_MEMORY_ROOMS_LIMIT = int(os.getenv('IN_MEMORY_ROOMS_LIMIT', "100"))
