#kevin fink
#kevin@shorecode.org
#Sun Apr 28 06:40:48 PM +07 2024
#log_template.py
#kevin fink
#kevin@shorecode.org
#Oct 7 2023

import logging
import platform
import os
from valdec.decorators import validate

@validate
def set_logging(name: str, filename: str) -> logging.Logger:
    """
    Creates a logging directory if one does not exist and initializes and configures a logger
    
    Args:
    name (str) : Name of the logger
    filename (str) : Name of the file to output the log to
    
    Returns:
    logging.Logger: Logger object
    """    
    # Checks for a logging directory and creates one if it does not exist
    if not os.path.isdir('logging'):
        os.mkdir('logging')

    # Create a logger
    logger = logging.getLogger(name)
    
    if os.path.exists(filename):
        # Get the size of the logging file
        file_size = os.path.getsize(filename)
    
        # Delete the logging file if it is greater than 10Mb
        if file_size > 10000000:
            os.remove(filename)
            with open(filename, 'w', encoding='utf-8') as fn:
                fn.write('New log')        

    # Setup logging configuration
    logging.basicConfig(filename=filename, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

    # Create a file handler
    console_handle = logging.StreamHandler()
    
    # Add the file handler to the logger
    logger.addHandler(console_handle)

    return logger
