import logging
import os
from datetime import datetime

class Logger:
    """Custom logger class for the automation framework"""
    
    @staticmethod
    def setup_logger(name="AutomationTest", log_level=logging.INFO):
        """
        Set up a logger with console and file handlers
        
        Args:
            name: Name of the logger
            log_level: Logging level (default: INFO)
        
        Returns:
            logging.Logger: Configured logger instance
        """
        # Create logs directory if it doesn't exist
        log_dir = "logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # Create logger
        logger = logging.getLogger(name)
        logger.setLevel(log_level)
        
        # Remove existing handlers to avoid duplicates
        if logger.hasHandlers():
            logger.handlers.clear()
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # File handler - creates a new log file for each day
        log_file = f"{log_dir}/automation_{datetime.now().strftime('%Y%m%d')}.log"
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        return logger
    
    @staticmethod
    def get_logger(name="AutomationTest", log_level=logging.INFO):
        """Get a logger instance (alias for setup_logger)"""
        return Logger.setup_logger(name, log_level)

# Create a default logger instance
def get_logger():
    """Get a default logger instance"""
    return Logger.setup_logger()