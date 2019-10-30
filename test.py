import json

# with open('dashboard_static/sports.json', 'r') as f:
#     j = json.load(f)
#
# print(j)
tweetList = []

f = open("dashboard_static/sports.json", "r")


while True:
    try:
        line = f.readline()

        if line:
            obj = json.loads(line)
        else:
            break
    except:
        print("Non-json.")
        print(line)
        continue
    else:
        tweetList.append(obj)
        print(obj)

