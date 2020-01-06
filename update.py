from python_json_config import ConfigBuilder
import os
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)



# create config parser
builder = ConfigBuilder()

# parse config
config = builder.parse_config('/Users/daviddawson/Documents/projects/mi.capital/python_batch/data.json')

# access elements
goals = config.get("goals")

for goal in goals:
    logger.info(f"Working on goal:{goal.get('goal_title')}")