import datetime; print("\n")

issue = datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30) #Adding 5:30 hrs to UCT Time
issue = datetime.datetime.strftime(issue,"%d %B %Y")
print(f"Date of issue:    {issue}\n")
issue = datetime.datetime.strptime(issue,"%d %B %Y")        #Date of Issue

reissue = issue + datetime.timedelta(days=21)               #Adding 21 days to issue date
reissue = datetime.datetime.strftime(reissue,"%d %B %Y")    #Book return date
print(f"Book return date: {reissue}")
