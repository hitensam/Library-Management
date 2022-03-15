import datetime; # print("\n")

INDIA_TIME = datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30) #Adding 5:30 hrs to UCT Time

def ISSUE():
    global INDIA_TIME
    issue = datetime.datetime.strftime(INDIA_TIME,"%d %B %Y")  #Date of Issue
    # issue = datetime.datetime.strptime(issue,"%d %B %Y")   
    return (issue)
# print(f"Date of issue:    {issue}\n")
   


def REISSUE(issue):
    # global INDIA_TIME  #is not using global time as Uday Says
    issue = datetime.datetime.strptime(issue,"%d %B %Y") #converts string to datetime format.
    reissue = issue + datetime.timedelta(days=25)              #Here issue type should be datetime for it to work.
    reissue = datetime.datetime.strftime(reissue,"%d %B %Y") #Book return date
    return (reissue)

# print(f"Book return date: {reissue}")

# a0 = ISSUE()
# print(a0)
# a = REISSUE('22 March 2022')
# print(a)
