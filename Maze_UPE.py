import requests, json, numpy as np

UID = "305167818"
Base_URL = "http://ec2-34-212-54-152.us-west-2.compute.amazonaws.com"
Start_URL = Base_URL + "/session"
global Game_URL
Game_URL = Base_URL + "/game?token=" 
Levels = 0
#response codes for post movement
Outside = -2
Wall = -1
Success = 0
End = 1

def main():
    print("Code Running")
    token()

def token():
    print("Getting Session Token")
    resp = requests.post(Start_URL, data = {"uid":UID}) # start new session(POST)
    if not resp:
        print("Error with Post")
    body = resp.json()
    access_token = body["token"] # retrieve access token from response body
    global Game_URL
    Game_URL += access_token
    initialize()

def initialize():
    print("Starting game")
    global Game_URL
    resp = requests.get(Game_URL) # get maze information(GET)
    body = resp.json()
    Levels = body["total_levels"]
    for i in range(5):
        resp = requests.get(Game_URL) # get maze information(GET)
        body = resp.json()
        # retrieve information about the maze from response body
        status = body["status"] #PLAYING, GAME_OVER, NONE, FINISHED
        Levels = body["total_levels"]
        max_x = body["size"][0]
        max_y = body["size"][1]
        print("Solving Level: " + str(body["levels_completed"] + 1))
        path = np.zeros((max_y, max_x), dtype = int) #array to mark visited loacation!!!!!!!!!!!!!!!!!!!
        #print(path)
        #print(body)
        stack = []
        x = body["cur_loc"][0]
        y = body["cur_loc"][1]
        while(status == "PLAYING"): #game is being played
            #resp = requests.get(Game_URL) # get maze information(GET)
           # body = resp.json()
           # status = body["status"]
           # x = body["cur_loc"][0]
           # y = body["cur_loc"][1]
            No_Move = False #if no move available pop from stack
            if (x - 1 >= 0) and path[y][x - 1] == 0: #LEFT
                dir = "left"
            elif (y - 1 >= 0) and path[y - 1][x] == 0: #UP
                dir = "up"
            elif (x + 1 < max_x) and path[y][x + 1] == 0: #RIGHT
                dir = "right"
            elif (y + 1 < max_y) and path[y + 1][x] == 0: #DOWN
                dir = "down"
            else:
                No_Move = True
                dir = stack.pop()
                path[y][x] = 1
            resp = requests.post(Game_URL, data = {"action": dir})
            body = resp.json()
            result = body["result"] 
            #look through results from intended movement
            if(result == Success):
                #print("Moved " + dir + " from " + str(y) + ", "+str(x))
                path[y][x] = 1
                #print(path)
                 #append direction back to coord
                if dir == "left":
                    x-=1
                    if not No_Move:
                        stack.append("right")
                elif dir == "up":
                    y-=1
                    if not No_Move:
                        stack.append("down")
                elif dir == "right":
                    x+=1
                    if not No_Move:
                       stack.append("left")
                elif dir == "down":
                    y+=1
                    if not No_Move:
                        stack.append("up")
            elif(result == Wall):
                if dir == "left":
                    path[y][x - 1] = 3
                elif dir == "up":
                    path[y - 1][x] = 3
                elif dir == "right":
                    path[y][x + 1] = 3
                elif dir == "down":
                    path[y + 1][x] = 3
            elif(result == End):
                print("Level Finished \n Starting New Level")
                break
                        
    #ANALYZE RESULTS
    if body["levels_completed"] == body["total_levels"]:
        print("Succesfully solved challenge")    
    else:
        print("FAILED CHALLENGE")
        print("Levels Completed = " + str(body["levels_completed"]))


main()