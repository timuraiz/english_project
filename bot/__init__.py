import sys
import os
import logging

script_path = sys.argv[0]
script_directory = os.path.dirname(os.path.abspath(script_path)) + '/logs.log'
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(script_directory)
    ]
)
