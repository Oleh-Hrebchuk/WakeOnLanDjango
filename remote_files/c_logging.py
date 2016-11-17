import logging


class LoggingData(object):
    def loger(self, e, level):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler('wakeonlan.log')
        handler.setLevel(logging.INFO)
        formater = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formater)
        logger.addHandler(handler)

        if level == 'info':
            return logger.info(e)
        elif level == 'debug':
            return logger.debug(e)
        elif level == 'warning':
            return logger.warning(e)
        elif level == 'error':
            return logger.info(e)
        elif level == 'critical':
            return logger.critical(e)
