import tkinter as tk
import tkinter.font as tkFont
import os
import json
from tkinter import simpledialog
from tkinter import ttk
import customtkinter as ctk
import pushup
import squat
import jumpingjacks
import situp
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
from json_generate import create
from ask_trainer import initialize

class App:
    saveData = ""
    ctk.set_default_color_theme("dark-blue")

    def __init__(self, root):
        # setting title
        root.title("FitSense")
        App._root = root
        # setting window size
        App._width = 880
        App._height = 700
        width = App._width
        height = App._height
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height,
                                    (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        homeFrame = tk.Frame(root, bg="#2C2F33")
        App._homeFrame = homeFrame
        homeFrame.pack(fill="both", expand=True)

        # Add title with icon
        title_font = tkFont.Font(family='Impact', size=75, weight="bold")
        title_label = tk.Label(homeFrame, text="FitSense", font=title_font, bg="#2C2F33", fg="#FFD700")
        title_label.place(relx=0.5, y=110, anchor="center")
        options = ['Squat', 'Pushup', 'JumpingJacks', 'Situp']

        combo = ctk.CTkComboBox(
            master=homeFrame, values=options, height=45, width=200, corner_radius=10, fg_color="#FFFFFF", text_color="#000000")
        combo.place(x=App._width / 2 - 100, y=App._height / 2 - 100)

        combo.set(options[0])
        self.__comboDd__ = combo
        button_style_green = {
            "width": 250, "height": 70, "corner_radius": 10,
            "fg_color": "#28A745", "text_color": "#FFFFFF",
            "font": ctk.CTkFont(family="Helvetica", size=24, weight="bold")
        }  # Green button

        button_style_blue = {
            "width": 250, "height": 70, "corner_radius": 10,
            "fg_color": "#007BFF", "text_color": "#FFFFFF",
            "font": ctk.CTkFont(family="Helvetica", size=24, weight="bold")
        }  # Blue button

        DropDownButton = ctk.CTkButton(
            master=homeFrame, text="Start Counting Reps!",
            command=self.DropDownButton_command, **button_style_blue
        )
        DropDownButton.place(x=App._width / 2 - 275, y=App._height / 2 - 35)

        TrainerButton = ctk.CTkButton(
            master=homeFrame, text="AI Trainer",
            command=self.TrainerButton_command, **button_style_green
        )
        TrainerButton.place(x=App._width / 2 + 25, y=App._height / 2 - 35)

        GoalLabel = ctk.CTkLabel(
            master=homeFrame, text="Goal (No. of reps):",
            width=150, height=30,
            font=ctk.CTkFont(family="Helvetica", size=18, weight="bold"),
            corner_radius=10, fg_color="white", text_color="#000000"
        )
        GoalLabel.place(x=App._width / 2 - 100, y=App._height / 2 + 80)

        GoalEntry = ctk.CTkEntry(
            master=homeFrame, width=100, height=30,
            font=ctk.CTkFont(family="Helvetica", size=18, weight="bold"),
            corner_radius=10, fg_color="white", text_color="#000000"
        )
        GoalEntry.place(x=App._width / 2 + 100, y=App._height / 2 + 80)
        GoalEntry.insert(0, 10)

        App._workout_GoalEntry = GoalEntry
        button_style_orange = {
            "width": 250, "height": 70, "corner_radius": 10,
            "fg_color": "#FF8C00", "text_color": "#FFFFFF",
            "font": ctk.CTkFont(family="Helvetica", size=24, weight="bold")
        }  # Orange button

        PreferencesButton = ctk.CTkButton(
            master=homeFrame, text="Preferences",
            command=self.PreferencesButton_command, **button_style_orange
        )
        PreferencesButton.place(x=App._width / 2 - 125, y=App._height / 2 + 130)

    def DropDownButton_command(self):
        print("command")
        goal = App._workout_GoalEntry.get()
        App._goal_val = goal
        exercise = self.__comboDd__.get()
        match exercise:
            case "Pushup":
                pushup.start(goal)
                App._exercise = 0  # Pushups
                self.ShowResultsPage()
            case "Squat":
                squat.start(goal)
                App._exercise = 3  # Squats
                self.ShowResultsPage()
            case "JumpingJacks":
                jumpingjacks.start(goal)
                App._exercise = 2  # Jumping Jacks
                self.ShowResultsPage()
            case "Situp":
                situp.start(goal)
                App._exercise = 3  # Situps
                self.ShowResultsPage()

    def PreferencesButton_command(self):
        preferencesFrame = tk.Frame(App._root, bg="#2C2F33")  # Dark background
        App._homeFrame.pack_forget()
        preferencesFrame.pack(fill="both", expand=True)
        App._preferencesFrame = preferencesFrame

        title_font = tkFont.Font(family='Impact', size=48, weight="bold")

        title_label = tk.Label(preferencesFrame, text="PREFERENCES", font=title_font, 
                            bg="#2C2F33", fg="#FFD700")  # Gold title
        title_label.place(relx=0.5, y=60, anchor="center")

        labels = ["Height (cm)", "Weight (kg)", "Age", "Type of Workout", "Days per Week", "Location", "Experience"]
        y_positions = [140, 200, 260, 320, 380, 440, 500]
        self.entries = []

        for i, label_text in enumerate(labels):
            lbl = tk.Label(preferencesFrame, text=label_text, font=("Helvetica", 15, "bold"), 
                        bg="#2C2F33", fg="#FFFFFF")  # White text
            lbl.place(x=App._width / 2 - 200, y=y_positions[i])

            if label_text in ["Type of Workout", "Location", "Experience"]:  # Dropdown fields
                options = {
                    "Type of Workout": ["Ab Development", "Muscle Gain", "Weight Loss", "Weight Gain", "Cardio"],
                    "Location": ["Home", "Gym"],
                    "Experience": ["Beginner", "Intermediate", "Professional"]
                }
                combo = ctk.CTkComboBox(master=preferencesFrame, values=options[label_text], 
                                        height=30, width=170, corner_radius=15, 
                                        fg_color="#3B3F45", text_color="#FFFFFF")
                combo.place(x=App._width / 2 + 20, y=y_positions[i])
                self.entries.append(combo)
            else:
                entry = ctk.CTkEntry(master=preferencesFrame, width=220, height=40, 
                                    font=("Helvetica", 18), corner_radius=15, 
                                    fg_color="#3B3F45", text_color="#FFFFFF")
                entry.place(x=App._width / 2 + 20, y=y_positions[i])
                self.entries.append(entry)
        button_style_save = {"width": 180, "height": 60, "corner_radius": 20, 
                            "fg_color": "#28A745", "text_color": "#FFFFFF", "font": ("Helvetica", 18, "bold")}  # Green button


        button_style_back = {"width": 180, "height": 60, "corner_radius": 20, 
                            "fg_color": "#007BFF", "text_color": "#FFFFFF", "font": ("Helvetica", 18, "bold")}

        SaveButton = ctk.CTkButton(master=preferencesFrame, text="Save Preferences", 
                                command=self.SavePreferences_command, **button_style_save)
        SaveButton.place(x=App._width / 2 - 200, y=570)  # Shifted left

        BackButton = ctk.CTkButton(master=preferencesFrame, text="Back", 
                                command=self.BackButton_command, **button_style_back)
        BackButton.place(x=App._width / 2 + 20, y=570)  # Shifted right

    def SavePreferences_command(self):
        preferences = {
            "height": self.entries[0].get(),
            "weight": self.entries[1].get(),
            "age": self.entries[2].get(),
            "workout_type": self.entries[3].get(),
            "days_per_week": self.entries[4].get(),
            "location": self.entries[5].get(),
            "experience": self.entries[6].get()
        }
        with open('input.txt', 'w') as f:
            for key, value in preferences.items():
                f.write(f"{key}: {value}\n")
        print("Preferences saved:", preferences)
        create()
        self.ShowOutputPage()

    def ShowOutputPage(self):
        outputFrame = tk.Frame(App._root, bg="#2C2F33")
        App._preferencesFrame.pack_forget()
        outputFrame.pack(fill="both", expand=True)
        App._outputFrame = outputFrame

        title_font = tkFont.Font(family='Impact', size=50, weight="bold")

        title_label = tk.Label(outputFrame, text="Workout Plan", font=title_font, bg="#2C2F33", fg="#FFD700")
        title_label.place(x=App._width / 2 - 200, y=20)

        with open('output.txt', 'r') as f:
            output_text = f.read()

        text_widget = tk.Text(outputFrame, font=tkFont.Font(family='Helvetica', size=14, weight="bold"), bg="#2C2F33", fg="#FFFFFF", wrap="word")
        text_widget.insert(tk.END, output_text)
        text_widget.config(state=tk.DISABLED)
        text_widget.place(x=20, y=120, width=App._width - 40, height=App._height - 200)

        scrollbar = tk.Scrollbar(outputFrame, command=text_widget.yview)
        text_widget.config(yscrollcommand=scrollbar.set)
        scrollbar.place(x=App._width - 20, y=120, height=App._height - 200)

        BackButton = ctk.CTkButton(master=outputFrame, text="Back",
                                width=150, height=60, command=self.BackButton_command_from_output, font=ctk.CTkFont(size=24), corner_radius=10, fg_color="#28A745", text_color="#FFFFFF")
        BackButton.place(x=App._width / 2 - 125, y=App._height - 70)

        # Apply styling to the text
        text_widget.tag_configure("heading", font=tkFont.Font(family='Helvetica', size=18, weight="bold"), foreground="#FF4500")
        text_widget.tag_configure("subheading", font=tkFont.Font(family='Helvetica', size=16, weight="bold"), foreground="#0000FF")
        text_widget.tag_configure("body", font=tkFont.Font(family='Helvetica', size=14, weight="normal"), foreground="#000000")

        # Apply tags to the text
        lines = output_text.split('\n')
        for line in lines:
            if line.startswith("**") and line.endswith("**"):
                text_widget.insert(tk.END, line + '\n', "heading")
            elif line.startswith("* "):
                text_widget.insert(tk.END, line + '\n', "subheading")
            else:
                text_widget.insert(tk.END, line + '\n', "body")

        text_widget.config(state=tk.DISABLED)

    def BackButton_command(self):
        App._preferencesFrame.pack_forget()
        App._homeFrame.pack(fill="both", expand=True)

    def BackButton_command_from_output(self):
        App._outputFrame.pack_forget()
        App._homeFrame.pack(fill="both", expand=True)

    def TrainerButton_command(self):
        BG_GRAY = "#ABB2B9"
        BG_COLOR = "#17202A"
        TEXT_COLOR = "#EAECEE"

        FONT = "Helvetica 14"
        FONT_BOLD = "Helvetica 13 bold"

        trainerFrame = tk.Frame(App._root, bg="#2C2F33")
        App._homeFrame.pack_forget()
        trainerFrame.pack(fill="both", expand=True)
        App._trainerFrame = trainerFrame
     
       # Define consistent button styles
        button_style_green = {
            "width": 70, "height": 40, "corner_radius": 10,
            "fg_color": "#28A745", "text_color": "#FFFFFF",
            "font": ctk.CTkFont(family="Helvetica", size=18, weight="bold")
        }  # Green button

        button_style_blue = {
            "width": 70, "height": 40, "corner_radius": 10,
            "fg_color": "#007BFF", "text_color": "#FFFFFF",
            "font": ctk.CTkFont(family="Helvetica", size=18, weight="bold")
        }  # Blue button

        # Back Button
        CloseButton = ctk.CTkButton(
            master=trainerFrame, text="Back",
            command=self.CloseButtonTrainer_command, **button_style_blue
        )
        CloseButton.place(x=76, y=600)

        # Send Button
        send = ctk.CTkButton(
            master=trainerFrame, text="Send",
            command=self.send_command, **button_style_green
        )
        send.place(x=100+630, y=600)

        # Entry Field
        e = ctk.CTkEntry(trainerFrame, fg_color="#2C3E50",
                        width=540, height=50, text_color="#FFFFFF")
        e.place(x=180, y=600)
        e.focus()
        App._e = e

        # Title Label
        title_font = tkFont.Font(family='Impact', size=50, weight="bold")
        title_label = tk.Label(trainerFrame, text="AI Trainer", font=title_font, bg="#2C2F33", fg="#FFD700")
        title_label.place(relx=0.5, y=50, anchor="center")

        # Textbox
        txt = ctk.CTkTextbox(trainerFrame, fg_color=BG_COLOR, width=670, height=450, pady=2, text_color="#FFFFFF",
                            font=ctk.CTkFont(size=18, weight="bold"))
        txt.place(x=100, y=100)
        App._txt = txt

    def send_command(self):
        send = "You -> " + App._e.get()
        App._txt.insert("end", "\n", None)  
        App._txt.insert("end", send, "user")

        user_q = App._e.get().lower()
        response = initialize(user_q)

        App._e.delete(0, "end")
        App._txt.insert("end", "\n", None)  
        App._txt.insert("end", "Bot -> " + response, "bot")

        # Configure text colors using different insert calls
        App._txt.tag_config("user", foreground="#33A1FF")  # Blue for user
        App._txt.tag_config("bot", foreground="#FFD700")  # Gold for bot
        pass

    def ShowResultsPage(self):
        resultsFrame = tk.Frame(App._root, bg="#2C2F33")  # Updated background
        App._homeFrame.pack_forget()
        resultsFrame.pack(fill="both", expand=True)
        App._resultsFrame = resultsFrame

        # Title Label
        title_font = tkFont.Font(family='Impact', size=50, weight="bold")
        title_label = tk.Label(resultsFrame, text="Progress & Results", font=title_font, 
                            bg="#2C2F33", fg="#FFD700")  # Gold text for contrast
        title_label.place(relx=0.5, y=37, anchor="center")

        ResultsLabel = tk.Label(resultsFrame, bg="#2C2F33", fg="#FFFFFF")  # Adjusted colors
        ResultsLabel.place(x=440 - 800 / 2, y=80, width=800, height=500)

        with open('results.json', 'r') as f:
            data = json.load(f)

        results = "N/A"
        t_goal = "N/A"
        if len(data[App._exercise]) != 0:
            results = data[App._exercise][-2]
            t_goal = data[App._exercise][-1]

        # Goal Header
        GoalHeader = tk.Label(ResultsLabel, bg="#2C2F33", fg="#FFFFFF", font=tkFont.Font(family='Helvetica', size=20, weight="bold"),
                            justify="left", anchor="w", text=f"Goal: {t_goal} reps.")
        GoalHeader.place(x=20, y=20, width=250, height=30)

        # Results Header
        ResultsHeader = tk.Label(ResultsLabel, bg="#2C2F33", fg="#FFFFFF", font=tkFont.Font(family='Helvetica', size=20, weight="bold"),
                                justify="left", anchor="w", text=f"Results: {results} reps.")
        ResultsHeader.place(x=20, y=70, width=250, height=30)
        # Message Box
        if results <= 0.8 * t_goal:
            message = "Not quite enough - more work is needed!"
        elif results >= 1.2 * t_goal:
            message = "Nice! You exceeded your goal."
        else:
            message = "Nice! You met your goal."

        resultsMessage = tk.Label(resultsFrame, bg="#2C2F33", fg="#FFFFFF", font=tkFont.Font(family='Helvetica', size=15, weight="bold"),
                                justify="center", text=message, wraplength=700)
        resultsMessage.place(relx=0.5, y=650, anchor="center", width=700, height=100)

        # Updated Button Styling
        button_style_blue = {
                "fg_color": "#1E90FF",  # DodgerBlue
                "hover_color": "#1C86EE",  # Slightly darker blue on hover
                "text_color": "white",
                "corner_radius": 8,
                "font": ("Helvetica", 18, "bold"),
                "width": 150,
                "height": 40
            }
        CloseButton = ctk.CTkButton(
            master=resultsFrame, text="Close", command=self.CloseButtonResults_command, **button_style_blue
        )
        CloseButton.place(x=30, y=App._height - 80)

        results_arr, goals_arr = [], []
        for i, value in enumerate(data[App._exercise]):
            (results_arr if i % 2 == 0 else goals_arr).append(value)

        # Limit to last 7 sessions
        max_sessions = 7
        results_arr = results_arr[-max_sessions:]
        goals_arr = goals_arr[-max_sessions:]
        x_axis = list(range(1, len(results_arr) + 1))
        y_axis = [results_arr[i] / goals_arr[i] * 100 for i in range(len(results_arr))]

        fig, ax = plt.subplots()
        ax.set_ylim(0, 100)
        ax.set_xlim(0.5, len(x_axis) + 0.5)
        plt.scatter(x_axis, y_axis)
        plt.plot(x_axis, y_axis, color="#FFD700")  # Gold line for better visibility
        plt.xlabel("Workout Number")
        plt.ylabel("Goal Completion (%)")
        plt.grid(True)
        plt.savefig("graph1.png")
        test = ImageTk.PhotoImage(Image.open("graph1.png").resize((420, 370), Image.Resampling.LANCZOS))

        # Graph Placement
        label1 = tk.Label(resultsFrame, image=test, bg="#2C2F33")
        label1.image = test
        label1.place(relx=0.5, y=400, anchor="center")

    def CloseButtonTrainer_command(self):
        App._trainerFrame.pack_forget()
        App._homeFrame.pack(fill="both", expand=True)

    def CloseButtonResults_command(self):
        App._resultsFrame.pack_forget()
        App._homeFrame.pack(fill="both", expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()



