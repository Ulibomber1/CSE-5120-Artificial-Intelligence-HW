import tkinter as tk
import numpy as np

GAMMA = 0.9
NOISE = 0.2

SMALL_ENOUGH = 0.0001

# Define all states. Here I did not create a tree structure (where the root should be 0,0 where the agent starts). 
# You can convert this line to implement a tree structure with children nodes of each node to be its neighbors
all_states=[(0,3),(1,3),(1,1),(2,0),(1,0),(2,1),(0,0),(2,2),(2,3),(0,1),(1,2),(0,2)]

rewards = {}
policy={}
V={}

#Dictionnary of possible actions. We have two "end" states (1,4 and 2,4)
actions = {
    (0,0):('v', '>'),
    (0,1):('>', '<'),
    (0,2):('v', '<', '>'),
    (1,0):('v', '^'),
    (1,2):('v', '^', '>'),
    (2,0):('^', '>'),
    (2,1):('<', '>'),
    (2,2):('^','<', '>'),
    (2,3):('<', '^'),
    }

class GridApp:
    def __init__(self, root):
        self.root = root
        self.root.title("3x4 Grid Example for MDP")

        self.canvas_list = []
        self.colors = [
            ["#FFFFFF", "#FFFFFF", "#FFFFFF", "#3DED97"],
            ["#FFFFFF", "#808080", "#FFFFFF", "#FF2424"],
            ["#FFFFFF", "#FFFFFF", "#FFFFFF", "#FFFFFF"]
        ]
        self.draw_grid()


        # For demonstration purposes, change the color of the (0,0) cell after 2 seconds
        #self.root.after(2000, self.modify_canvas)

    def draw_grid(self):
        for i in range(3):
            row_canvases = []
            for j in range(4):
                canvas = tk.Canvas(self.root, bg=self.colors[i][j], height=200, width=300)
                canvas.create_text(150, 100, text=f"({i+1}, {j+1})", fill="black", font=('Helvetica 15 bold'))
                canvas.grid(row=i, column=j, padx=5, pady=5)

                row_canvases.append(canvas)
            self.canvas_list.append(row_canvases)


    def modify_canvas(self):
        self.canvas_list[0][0].config(bg="#FFFFFF")

# This function displays the final state values on the grid after they are computed from computeValueIteration function
def finalGridValues(app):
    for s in all_states:
        x = s[0]
        y = s[1]
        if s not in policy:
            v = ""
        if s in V:
            v = "{:.2f}".format(V[s])
        canvas = tk.Canvas(app.root, bg=app.colors[x][y], height=200, width=300)
        canvas.create_text(150, 100, text=f"{v}", fill="black", font=('Helvetica 15 bold'))
        if s in policy:
            if policy[s] =='>':
                canvas.create_line(180, 100, 220, 100, fill="#090C9B",arrow=tk.LAST, width=10)
            if policy[s] =='<':
                canvas.create_line(120, 100, 80, 100, fill="#090C9B",arrow=tk.LAST, width=10)
            if policy[s] =='^':
                canvas.create_line(150, 80, 150, 40, fill="#090C9B",arrow=tk.LAST, width=10)
            if policy[s] =='v':
                canvas.create_line(150, 120, 150, 160, fill="#090C9B",arrow=tk.LAST, width=10)

        canvas.grid(row=x, column=y, padx=5, pady=5)
        app.canvas_list[x][y] = canvas

# Setup initial values (States, actions, reward, gamma)
def initialSetup(app):
    #Define rewards for all states
    for i in all_states:
        if i == (1,3):
            rewards[i] = -1
        if i == (0,3):
            rewards[i] = 1
        else:
            rewards[i] = 0
    #Define an initial policy
    for s in actions.keys():
        policy[s] = np.random.choice(actions[s])

    #Define initial value function
    for s in all_states:
        if s in actions.keys():
            V[s] = 0
        if s == (1,3):
            V[s] = -1
        if s == (0,3):
            V[s] = 1

    # Draw initial random policy with initial value function (0 everywhere)
    for s in all_states:
        x = s[0]
        y = s[1]
        if s not in policy:
            v = ""
        if s in V:
            v = V[s]
        canvas = tk.Canvas(app.root, bg=app.colors[x][y], height=200, width=300)
        canvas.create_text(150, 100, text=f"{v}", fill="black", font=('Helvetica 15 bold'))
        if s in policy:
            if policy[s] =='>':
                canvas.create_line(180, 100, 220, 100, fill="#090C9B",arrow=tk.LAST, width=10)
            if policy[s] =='<':
                canvas.create_line(120, 100, 80, 100, fill="#090C9B",arrow=tk.LAST, width=10)
            if policy[s] =='^':
                canvas.create_line(150, 80, 150, 40, fill="#090C9B",arrow=tk.LAST, width=10)
            if policy[s] =='v':
                canvas.create_line(150, 120, 150, 160, fill="#090C9B",arrow=tk.LAST, width=10)

        canvas.grid(row=x, column=y, padx=5, pady=5)
        app.canvas_list[x][y] = canvas

# This function runs value iteration algorithm on the grid and computes the fnial states values as well as the policy with arrows. 
# You can use the line input("Press any key continue") at the end of this function to see the values being changed on the grid
# after every iteration (or use a logic to display the updated values after every 10th iteration) 
def computeValueIteration():
    iteration = 0

    while iteration < 100:
        biggest_change = 0

        for s in all_states:
            if s in policy:
                old_v = V[s]
                new_v = 0
                for a in actions[s]:
                    if a == '^':
                        nxt = [s[0]-1, s[1]]
                    if a == 'v':
                        nxt = [s[0]+1, s[1]]
                    if a == '<':
                        nxt = [s[0], s[1]-1]
                    if a == '>':
                        nxt = [s[0], s[1]+1]

                    #Choose a new random action to do (transition probability)
                    random_1=np.random.choice([i for i in actions[s] if i != a])
                    if random_1 == '^':
                        act = [s[0]-1, s[1]]
                    if random_1 == 'v':
                        act = [s[0]+1, s[1]]
                    if random_1 == '<':
                        act = [s[0], s[1]-1]
                    if random_1 == '>':
                        act = [s[0], s[1]+1]
                    #Calculate the value
                    nxt = tuple(nxt)
                    act = tuple(act)
                    v = rewards[s] + (GAMMA*((1-NOISE)*V[nxt] + (NOISE*V[act])))
                    if v > new_v:
                        new_v = v
                        policy[s] = a

                        x = s[0]
                        y = s[1]
                        canvas = tk.Canvas(app.root, bg=app.colors[x][y], height=200, width=300)
                        canvas.create_text(150, 100, text=f"{v}", fill="black", font=('Helvetica 15 bold'))
                        if s in policy:
                            if policy[s] =='>':
                                canvas.create_line(180, 100, 220, 100, fill="#090C9B",arrow=tk.LAST, width=10)
                            if policy[s] =='<':
                                canvas.create_line(120, 100, 80, 100, fill="#090C9B",arrow=tk.LAST, width=10)
                            if policy[s] =='^':
                               canvas.create_line(150, 80, 150, 40, fill="#090C9B",arrow=tk.LAST, width=10)
                            if policy[s] =='v':
                               canvas.create_line(150, 120, 150, 160, fill="#090C9B",arrow=tk.LAST, width=10)

                        canvas.grid(row=x, column=y, padx=5, pady=5)
                        app.canvas_list[x][y] = canvas

                V[s] = new_v
                biggest_change = max(biggest_change, np.abs(old_v - V[s]))
        if biggest_change < SMALL_ENOUGH:
            break
        iteration += 1

# Call functions to draw the grid, run value iteration and diaply the results
root = tk.Tk()
app = GridApp(root)
initialSetup(app)


computeValueIteration()
finalGridValues(app)
root.mainloop()
