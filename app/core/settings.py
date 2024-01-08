from typing import Final


class Settings:
    PROJECT_NAME = "Base FastAPI Project"
    VERSION = "0.1.0"

    # log
    DEBUG_LOG_FILE: Final = "app.debug.log"
    INFO_LOG_FILE: Final = "app.info.log"
    ERR_LOG_FILE: Final = "app.err.log"
