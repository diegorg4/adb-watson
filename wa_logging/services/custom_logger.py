import logging
import settings

class CustomLogger():
    def __init__ (self, logger_name:str, logger_filepath: str):
        
        self.logger_name = logger_name
        self.logger = logging.getLogger(self.logger_name)
        self.logger.setLevel(logging.INFO)
        
        self.logger_filepath = logger_filepath
        handler = logging.FileHandler(self.logger_filepath)
        handler.setLevel(logging.INFO)
        
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    
    def log(self, level:str, message:str):
        if level == settings.LABEL_INFO:
            self.logger.info(message)

        elif level == settings.LABEL_WARNING:
            self.logger.warning(message)

        elif level == settings.LABEL_DEBUG:
            self.logger.debug(message)

        elif level == settings.LABEL_ERROR:
            self.logger.error(message)

        elif level == settings.LABEL_CRITICAL:
            self.logger.critical(message)

WA_WEBHOOK_LOGGER = CustomLogger(settings.WA_WEBOOK_NAME, settings.WA_WEBHOOK_LOG_PATH)
WA_HISTORY_LOGGER = CustomLogger(settings.WA_HISTORY_NAME, settings.WA_HISTORY_LOG_PATH)
WA_DEFAULT_LOGGER = CustomLogger(settings.WA_DEFAULT_NAME, settings.WA_DEFAULT_LOG_PATH)