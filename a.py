import notify2
import gemini
import sys
query=sys.argv[1].replace('+',' ')
print('query : ',query)
result=gemini.ask_gemini(query)
notify2.init("Gemini Answers!")
notification = notify2.Notification(query,result)
notification.show()
with open('/home/anishudupan/projects/notifications/aa.txt' ,'a') as f:
    f.write(query+'\n'+result+'\n\n')
    f.close()

