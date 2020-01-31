import calendar
import copy
import datetime
import logging
import math
import os
import pprint
from datetime import date, datetime, timedelta, tzinfo

import colorama
import dateutil
import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
from python_json_config import ConfigBuilder


register_matplotlib_converters()

logger = logging.getLogger(__name__)

# specify colors for different logging levels
LOG_COLORS = {
    logging.ERROR: colorama.Fore.RED,
    logging.INFO: colorama.Fore.GREEN,
    logging.WARNING: colorama.Fore.YELLOW,
    logging.DEBUG: colorama.Fore.WHITE
}


class ColorFormatter(logging.Formatter):
    def format(self, record, *args, **kwargs):
        # if the corresponding logger has children, they may receive modified
        # record, so we want to keep it intact
        new_record = copy.copy(record)
        if new_record.levelno in LOG_COLORS:
            # we want levelname to be in different color, so let's modify it
            def color_text(message,color):
                return "{color_begin}{message}{color_end}".format(
                message=message,
                color_begin=color,
                color_end=colorama.Style.RESET_ALL,
            )

            new_record.levelname = color_text(new_record.levelname,LOG_COLORS[new_record.levelno])
            new_record.msg = color_text(new_record.msg,LOG_COLORS[new_record.levelno])
        # now we can let standard formatting take care of the rest
        return super(ColorFormatter, self).format(new_record, *args, **kwargs)

# we want to display only levelname and message
formatter = ColorFormatter("%(levelname)s %(message)s")

# this handler will write to sys.stderr by default
handler = logging.StreamHandler()
handler.setFormatter(formatter)

# adding handler to our logger
logger.setLevel(logging.INFO)
logger.handlers = []
logger.addHandler(handler)

class simple_utc(tzinfo):
    def tzname(self,**kwargs):
        return "UTC"
    def utcoffset(self, dt):
        return timedelta(0)

def plot_goal(goal, achievements):
    logger.info(f"Plotting current goal:{goal.get('goal_title')}")
    #sort by datetime

    #sort by 
# create config parser
builder = ConfigBuilder()

# parse config
config = builder.parse_config('/Users/daviddawson/Documents/projects/new_years_resolutions/2020.json')
current_year = 2020

# access elements
goals = config.get("goals")
achievements = config.get("achievements")

goals_df = pd.DataFrame(goals)
achievements_df = pd.DataFrame(achievements)

# For Each Goal Build a curve of values.
for goal in goals:
    logger.debug(f"Working on goal ({goal.get('id')}): {goal.get('goal_title')}")
    temp_df = pd.DataFrame()
    for achievement in achievements:
        if goal["id"] == achievement["goal"]:
            logger.debug(f"Found achievement for goal: {achievement.get('goal')} of value : {achievement.get('value')}")
            datetime_str = achievement.get('datetime')
            datetime_dt = dateutil.parser.parse(datetime_str)
            temp_row = achievement
            temp_row["datetime"] = datetime_dt
            temp_df = temp_df.append(temp_row, ignore_index=True)
    
    if len(temp_df) :
        temp_df.sort_values(by='datetime', ascending=False )
        current_quantity = temp_df["value"].sum()
    else :
        current_quantity = 0
        
    logger.debug(temp_df.to_string())
    goal_title = goal.get('goal_title')
    goal_quantity = goal.get("total_quantity")

    if calendar.isleap(current_year) :
        total_days = 366
    else:
        total_days = 365

    first_day_of_year = date(current_year, 1, 1)
    today = date.today()
    current_days = (today - first_day_of_year ).days + 1
    
    
    is_percentage_goal = goal.get("is_percentage", False)
    is_decending_goal = False

    if is_percentage_goal :
        achieved_pct = current_quantity/100
        expected_pct = current_days/total_days * (goal_quantity/100)
        expected_amt = current_days/total_days * (goal_quantity)
    elif is_decending_goal:
        achieved_pct = current_quantity/100
    else:
        expected_pct = current_days/total_days
        expected_amt = math.floor(expected_pct * goal_quantity)
        achieved_pct = current_quantity/goal_quantity


    message = f"({goal.get('id')}): {goal.get('goal_title')} [ Expected: {expected_pct *100:.1f}% ({expected_amt:.1f}/{goal_quantity:.1f}) Achieved: {achieved_pct*100:.1f}% ({current_quantity:.1f}/{goal_quantity:.1f}) ]"
    if current_quantity >= expected_amt:
        logger.info(message)
    else :
        logger.error(message)

"""     from github import Github
    import json
    #with open('../../secrets/github.json') as json_file:
    #data = json.load(json_file)
    #token=data['secret']
    g = Github("davewd","L!ttleDaws0n")
    user = g.get_user()
    for repo in user.get_repos():
        contents = repo.get_views_traffic()
        print(f"{repo.name} :")
        branch = repo.get_branch("master")
        commits = repo.get_commits()
        for commit in commits:
            print( f"{commit.commit.last_modified}|{commit.commit.author.name} > {commit.commit.message}\n" )
        contents = repo.get_contents("")
        while contents:
            file_content = contents.pop(0)
            if file_content.type == "dir":
                contents.extend(repo.get_contents(file_content.path))
            else:
                print(file_content) """


# create data
customdate = datetime(2016, 1, 1, 13, 30)
y = [ 2,4,6,8,10,12,14,16,18,20 ]
rand_y = [ i * np.random.normal() for i in y ]
rand_y_2 = [ i * np.random.normal() for i in y ]
x = [customdate + timedelta(hours=i*24) for i in range(len(y))]

# plot
plt.plot(x,rand_y, '-o', color='red')
plt.plot(x,rand_y_2, '-o', color='blue')
plt.gcf().autofmt_xdate()
#plt.show()
