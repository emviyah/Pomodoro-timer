'''Pomodoro Buddy
A retro-style Pomodoro timer with:
- 25-minute work / 5-minute break cycles
- SQLite database for To-Dos
- Piu avatar with speech bubble
- Unit tests for timer formatting and input validation'''
#https://youtu.be/Npx227lXvEc - screen recording of my app walkthru


import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import random
from database import initialize_db, add_todo, get_all_todos, delete_task

def is_valid_task(task: str) -> bool:
    #return True if task is non-empty after stripping whitespace
    return bool(task and task.strip())


running = False          #check if the timer is counting down
mode = "work"
work_time_left = 25 * 60 
break_time = 5 * 60 
time_left = work_time_left     #time in seconds (25 minutes)


#set up main window
root = tk.Tk() 
initialize_db() 
root.title("Pomodoro Buddy")
root.geometry("320x500")
root.resizable(False, False) #lock window so its not resizable
root.configure(bg= "#D6DEC3")
s = ttk.Style()
s.theme_use('default') #use a theme that is easier to override
s.configure('Dark.TButton', 
            background='#456340',      #dark Green BG
            foreground='#FFFFFF',      #white Text
            font=("Press Start 2P", 14),
            bordercolor="#000000",
            borderwidth=3)


s.map('Dark.TButton', #using map to control the look of the button in certain states
      background=[('active', '#7B9B6A'),  #medium Green-Grey when hovering/active
                  ('pressed', '#7B9B6A')], #medium Green-Grey when pressed
      foreground=[('active', '#FFFFFF')]
     )


#set up time label and its frame to look like a retro screen
screen_frame = tk.Frame(
    root,
    bg="#7B9B6A",
    bd=3,
    relief="sunken",
    highlightbackground="#456340", #dark border
    highlightcolor="#456340",
    highlightthickness=2 
)
#pack the frame 
screen_frame.pack(pady=30)


#now the label for the timerrr
timer_label = tk.Label(
    screen_frame,
    text="25:00",
    font=("Press Start 2P", 30),
    fg="#bde0fe",
    bg="#7B9B6A"
)
timer_label.pack(padx=20, pady = 15)
timer_label.config(fg="#456340")

start_button = ttk.Button( #at first i tried the tk.Button i guess my macOS overrides the colors i wanted to apply
    root,
    text="Start Pomodoro",
    style='Dark.TButton', #apply the custom style
    
)
start_button.pack(pady=10)


#time format
def format_time(seconds):
    minutes = seconds // 60 #division for minutes
    secs = seconds % 60 #modulo for second
    return f"{minutes:02}:{secs:02}"  #format as str


#function to start the timer!
def start_timer():
    global running, time_left #we use global keyword to use the variables outside the function
    #https://www.w3schools.com/python/python_variables_global.asp
    
    if running and time_left > 0: #if the timer is running and there is time we decease it by 1 second
        time_left -= 1
        timer_label.config(text=format_time(time_left)) #update th elabel w the new time
        
        # call this function again after 1 second (or 1000 milliseconds) to create the countdown
        root.after(1000, start_timer)
    
    elif time_left == 0: #if time is up!
        running = False #stop timer - Timer finished!!!
        if mode == "work":
            start_button.config(text="Start Pomodoro") #andd we change back to the og text on the button
        else:
            start_button.config(text="Start Pomodoro")
            back_button_frame.pack_forget()
         #note: could add sound notification here later


def toggle_timer(): #toggle between start and pause
    global running, time_left , mode
    if running: #if timer is running
        running = False #we stop it 
        if mode == "work": #if in working mode
             start_button.config(text="Resume Pomodoro") #toggle the button text
        else: #if in break mode
            start_button.config(text="Resume Break") #toggle the button text
    else:  #if timer not running
        if time_left > 0: 
            running = True  #we start it
            if mode == "work": 
                start_button.config(text="Pause") #toggle buttin text 
            else:
                start_button.config(text="Pause Break") 
            start_timer() #the timer function


def start_break():
    global running, time_left, mode, work_time_left
    if mode == "work": #if we are in working mode
        work_time_left = time_left #we save and remeber the time left 
    running = False #we stop the timer
    mode = "break" #we chnage the mode to break 
    time_left = break_time #we add the 5 min for the break 
    timer_label.config(text="05:00") #we update the label
    start_button.config(text="Start Break") #we change the button text 
    back_button_frame.pack(pady=10) #show back to work button


def reset_timer():
    global running, time_left
    running = False  #stop timer
    mode = "work" #set mode to work
    work_time_left = 25*60 
    time_left = work_time_left #reset to 25 min 
    timer_label.config(text = "25:00") #update the label 
    start_button.config(text="Start Pomodoro") #change button text 
    back_button_frame.pack_forget() #hide back to work button we dont need it in reset


def back_to_work():
    global running, time_left, mode, work_time_left
    running = False
    mode = "work" #make sure we are in work mode!!
    time_left = work_time_left
    minutes = time_left//60
    seconds = time_left % 60
    timer_label.config(text=f"{minutes:02}:{seconds:02}")
    start_button.config(text="Resume Pomodoro")
    #hide back to work button
    back_button_frame.pack_forget()

start_button.config(command=toggle_timer) #here we link the button to the pause

button_frame = tk.Frame(root, bg="#A9D18D") #framing the other buttons
button_frame.pack(pady=10) #packing the frame 


break_button = tk.Button(
    button_frame,
    text="Break",
    font=("Press Start 2P", 10),
    fg="#456340",
    bg="#A9D18D",
    activebackground="#7B9B6A",
    activeforeground="#456340",
    relief = "flat",
    bd = 2,
    highlightthickness=2,
    highlightbackground="#456340", 
    highlightcolor="#456340",
    padx = 12, 
    pady = 4, 
    command=start_break
)
break_button.pack(side=tk.LEFT)

restart_button = tk.Button(
    button_frame,
    text="Restart",
    font=("Press Start 2P", 10),
    bg="#A9D18D",
    fg="#456340",
    bd=2,
    activebackground="#7B9B6A", 
    activeforeground="#456340", 
    relief="flat",
    highlightthickness=2,
    highlightbackground="#456340",
    highlightcolor="#456340",
    padx=12,
    pady=4,
    command=reset_timer
)
restart_button.pack(side=tk.LEFT)

back_button_frame = tk.Frame(root, bg="#D6DEC3", highlightthickness=0, bd=0)
back_button_frame.pack(pady=10)
back_button_frame.pack_forget()

back_button = tk.Button(
    back_button_frame,
    text="Back to Work",
    font=("Press Start 2P", 10),
    bg="#A9D18D",
    fg="#456340",
    bd = 2,
    activebackground="#7B9B6A",
    activeforeground="#456340",
    relief = "flat",
    highlightthickness=2,
    highlightbackground = "#456340",
    highlightcolor = "#456340",
    padx=12,
    pady=4,
    command=back_to_work
)
back_button.pack()


#put avatar on the bottom right corner on the main window 
#load Piu images
piu_normal_img = Image.open("piu.frame1st.png")
piu_wink_img = Image.open("piu.frame2nd.png")

#make em tkinter compatiable
piu_normal = ImageTk.PhotoImage(piu_normal_img)
piu_wink = ImageTk.PhotoImage(piu_wink_img)

#make photo accessible
root.piu_normal = piu_normal
root.piu_wink = piu_wink

piu_frame = tk.Frame(root, bg = "#D6DEC3", width=80, height = 80)
piu_frame.place(relx=1.0, rely = 1.0, anchor = 'se')
#Piu label
piu_label = tk.Label(piu_frame, image=piu_normal, bg="#D6DEC3")
piu_label.pack(expand=True, fill=tk.BOTH) #expand to fill frame 


def speech_bubble():
    #bubble frame
    bubble = tk.Frame(root, bg="#7B9B6A", bd=2, relief="sunken")
    
    #getting window size
    root.update_idletasks()
    win_width = root.winfo_width()
    win_height = root.winfo_height()
    
    bubble_width = 190
    bubble_height = 85
    
    #calculate the placement of bubble
    x = win_width - 80 - bubble_width - 25
    y = win_height - 80 - bubble_height - 7
    
    #place bubble on window
    bubble.place(x=x, y=y, width=bubble_width, height=bubble_height)
    
    #two options for buttons
    #label as buttons = easier to style
    view_label = tk.Label(
        bubble,
        text="View To-Do's",
        bg="#7B9B6A",
        fg="#456340",
        font=("Press Start 2P", 8),
    )
    view_label.place(x=23, y=40)
    view_label.bind("<Button-1>", lambda e: show_view_to_dos(bubble)) #we use lambda to pass the bubble reference and because the function needs an event argument

    add_label = tk.Label(
        bubble,
        text="Add New To-Do",
        bg="#7B9B6A",
        fg="#456340",
        font=("Press Start 2P", 8),
    )
    add_label.place(x=19, y=25) 
    add_label.bind("<Button-1>", lambda e: show_add_to_do(bubble))  #call function with lambda because we dont have an event arg 
    #keeping reference to bubble
    root.bubble = bubble



def show_view_to_dos(bubble):
    for widget in bubble.winfo_children():
        widget.destroy()
    
    all_tasks = get_all_todos()
    tasks = all_tasks[:5] #show only five
    if not tasks:
        tk.Label(
            bubble,
            text="No to-dos yet :(",
            bg="#7B9B6A",
            fg="#456340",
            font=("Press Start 2P", 7)
        ).pack(pady=10)
    else:
        for task_id, description in tasks:
            row = tk.Frame(bubble, bg="#7B9B6A", width=180, height=30)
            row.pack(fill="x", padx=5, pady=2)
            row.pack_propagate(False)

            short_desc = (description[:16] + "...") if len(description) > 16 else description

    #task text
            tk.Label(
                row,
                text=short_desc,
                bg="#7B9B6A",
                fg="#456340",
                font=("Press Start 2P", 6),
                padx=5,
                pady=2
            ).grid(row=0, column=0, sticky="w") #using grid

    #delete option
        del_btn = tk.Label(
            row,
            text="X",
            bg="#7B9B6A",
            fg="#000000",
            font=("Press Start 2P", 6),
            padx=5,
            pady=2
        )
        del_btn.grid(row=0, column=1, sticky="e")
        del_btn.bind("<Button-1>", lambda e, tid=task_id: handle_delete(tid, bubble))


def show_add_to_do(bubble):
    for widget in bubble.winfo_children():
        widget.destroy()
    
    #prompt label
    tk.Label(
        bubble,
        text="What’s on your mind?",
        bg="#7B9B6A",
        fg="#456340",
        font=("Press Start 2P", 7)
    ).pack(pady=4)
    
    #user input time
    #entry field
    entry = tk.Entry(
        bubble,
        width=18,
        bg="#A9D18D",
        fg="#456340",
        font=("Press Start 2P", 6)
    )
    entry.pack(pady=5)
    
    #label as button cuz maybe easier to style (macos changed colors i used)
    add_label = tk.Label(
        bubble,
        text="Add",
        bg="#7B9B6A",
        fg="#456340",
        font=("Press Start 2P", 7),
    )
    add_label.pack(pady=3)


    #make it function
    def give_piu_my_task():
        task = entry.get().strip()
        if is_valid_task(task):
            add_todo(task.strip()) #call the database func to add the todo
            entry.delete(0, tk.END)
            
            #confirm added todo
            for w in bubble.winfo_children():
                w.destroy()
    
            tk.Label(
                bubble,
                text="To-Do Added!",
                bg="#7B9B6A",
                fg="#456340",
                font=("Press Start 2P", 7)
            ).pack(pady=10)

    
    add_label.bind("<Button-1>", lambda e: give_piu_my_task())


def handle_delete(task_id, bubble):
    delete_task(task_id)  #from database.py
    show_view_to_dos(bubble)
    for widget in bubble.winfo_children():
        widget.destroy()
    
    all_tasks = get_all_todos()
    tasks = all_tasks[:5]  #show only five
    if not tasks:
        tk.Label(bubble, text="No to-dos yet :(", bg="#7B9B6A", fg="#456340", font=("Press Start 2P", 7)).pack(pady=10)
    else:
        for task_id, description in tasks: #from todo db
            row = tk.Frame(bubble, bg="#7B9B6A", width=180, height=30)
            row.pack(fill="x", padx=5, pady=2)
            row.pack_propagate(False) #make it placed right

            short_desc = (description[:16] + "...") if len(description) > 16 else description 

            tk.Label(
                row,
                text=short_desc,
                bg="#7B9B6A",
                fg="#456340",
                font=("Press Start 2P", 6),
                padx=5,
                pady=2
            ).grid(row=0, column=0, sticky="w")

            del_btn = tk.Label(
                row,
                text="X",
                bg="#7B9B6A",
                fg="#000000",
                font=("Press Start 2P", 6),
                padx=5,
                pady=2
            )
            del_btn.grid(row=0, column=1, sticky="e")
            del_btn.bind("<Button-1>", lambda e, tid=task_id: handle_delete(tid, bubble))
    
#bind Piu on click to show speech bubble
def on_piu_click(event):
    #switch to wink
    piu_label.config(image=piu_wink)
    root.update_idletasks()
    #switch back after 300ms
    root.after(300, lambda: piu_label.config(image=piu_normal))
    speech_bubble() 

piu_frame.bind("<Button-1>", on_piu_click)
piu_label.bind("<Button-1>", on_piu_click)

start_button.config(command=toggle_timer)

if __name__ == "__main__":
    root.mainloop()
