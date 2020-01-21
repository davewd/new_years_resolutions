from enum import Enum

#Goal Category
class GOAL_CATEGORY(Enum):
    PROFFESIONAL = "PROFESSIONAL"
    HEALTH = "HEALTH"
    WEALTH = "WEALTH"
    EDUCATION = "EDUCATION"
    FAMILY = "FAMILY"
    MENTAL = "MENTAL"

# Goal Type - used to specifically identify the calcuklation functions.  
# Also Any automated data extraction e.g. Github Commits
class GOAL_TYPE(Enum):
    PROFFESIONAL = "PROFESSIONAL"
    HEALTH = "HEALTH"
    WEALTH = "WEALTH"
    EDUCATION = "EDUCATION"
    FAMILY = "FAMILY"
    MENTAL = "MENTAL"
