import tkinter as tk
from tkinter import ttk, messagebox



# Functions for Calculations
def calculate_bmr(gender, weight, height, age):
    if gender == "Male":
        return 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    elif gender == "Female":
        return 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)


def calculate_tdee(bmr, activity_level):
    activity_factors = {
        "Light Exercise (1-2 days/week)": 1.2,
        "Moderate Exercise (3-5 days/week)": 1.375,
        "Heavy Exercise (6-7 days/week)": 1.55,
        "Intense Exercise (2x per day)": 1.725,
    }
    return bmr * activity_factors[activity_level]


def calculate_macronutrients(tdee, phase):
    if phase == "Maintenance":
        protein_ratio = 0.3
        fat_ratio = 0.25
        carb_ratio = 0.45
    elif phase == "Cutting":
        protein_ratio = 0.4
        fat_ratio = 0.3
        carb_ratio = 0.3
    elif phase == "Bulking":
        protein_ratio = 0.25
        fat_ratio = 0.2
        carb_ratio = 0.55

    protein_calories = tdee * protein_ratio
    fat_calories = tdee * fat_ratio
    carb_calories = tdee * carb_ratio

    return {
        "protein": protein_calories / 4,
        "fat": fat_calories / 9,
        "carbs": carb_calories / 4,
    }


# Navigation between screens
def show_activity_screen():
    if not name_entry.get() or not gender_var.get() or not age_entry.get() or not weight_entry.get() or not height_entry.get():
        messagebox.showerror("Error", "Please fill out all the information!")
        return
    try:
        int(age_entry.get())
        float(weight_entry.get())
        float(height_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Age, Weight, and Height must be numeric values!")
        return

    user_data["name"] = name_entry.get()
    user_data["gender"] = gender_var.get()
    user_data["age"] = int(age_entry.get())
    user_data["weight"] = float(weight_entry.get())
    user_data["height"] = float(height_entry.get())

    main_screen.pack_forget()
    activity_screen.pack()


def show_phase_screen():
    if not activity_var.get():
        messagebox.showerror("Error", "Please select an activity level!")
        return

    user_data["activity_level"] = activity_var.get()
    activity_screen.pack_forget()
    phase_screen.pack()


def show_result_screen():
    if not phase_var.get():
        messagebox.showerror("Error", "Please select a dietary phase!")
        return

    user_data["phase"] = phase_var.get()

    # Perform calculations
    bmr = calculate_bmr(
        user_data["gender"], user_data["weight"], user_data["height"], user_data["age"]
    )
    tdee = round(calculate_tdee(bmr, user_data["activity_level"]))  # Rounded TDEE
    weekly_calories = tdee * 7
    macronutrients = calculate_macronutrients(tdee, user_data["phase"])

    # Round macronutrient values to whole numbers
    protein = round(macronutrients["protein"])
    fat = round(macronutrients["fat"])
    carbs = round(macronutrients["carbs"])

    # Update result text
    result_text.set(
        f"Greetings, {user_data['name']}.\n"
        f"You are a {user_data['age']}-year-old {user_data['gender'].lower()} who weighs {user_data['weight']} kg and \nheight of {user_data['height']} cm tall."
        f" You perform {user_data['phase'].lower()} exercises \nand {user_data['activity_level'].lower()}."
        f" Also you intake \n{tdee} calories per day, and {weekly_calories} calories per week.\n\n"
        f"Macronutrient\n"
        f"   - Protein: {protein} grams per day\n"
        f"   - Fats: {fat} grams per day\n"
        f"   - Carbs: {carbs} grams per day\n"
    )

    phase_screen.pack_forget()
    result_screen.pack()


def show_workout_schedule():
    result_screen.pack_forget()  # Hide result screen
    workout_schedule_screen.pack()  # Show workout schedule screen


def back_to_results():
    workout_schedule_screen.pack_forget()  # Hide workout schedule screen
    result_screen.pack()  # Show result screen


# Function to show workout for a specific day
def show_day_workout(day):
    # Workout plans for each day
    workout_plans = {
        "Monday": """Chest Exercise
3 sets / 8 - 12 reps
   - high to low flyes
   - mid chest flyes
3 sets / 12 - 15 reps
   - wide push ups 

Tricep Exercise
3 sets / 8 - 12 reps
   - over head tricep extensions
   - tricep push down
3 sets / 12 - 15 reps
   - diamond push ups""",

        "Tuesday": """Bicep Exercise
3 sets / 8 - 12 reps
   - bicep curls
   - hammer curls
   - cross body hammer curls
Back Exercise
3 sets / 8 - 12 reps
   - arm pull down
   - lat pull down
   - supinated lat pull down
   - under hand row
3 sets / 12 - 15 reps
   - close grip push ups""",

        "Wednesday": """Shoulder Exercise
3 sets / 8 - 12 reps
   - shoulder press
   - lateral raise
   - face pulls
3 sets / 12 - 15 reps
   - pike push ups

Leg Exercise
3 sets / 8 - 12 reps
   - squats 
   - stiff leg dead lift
   - lunges""",

        "Thursday": """Chest Exercise
3 sets / 8 - 12 reps
   - high to low flyes
   - mid chest flyes
3 sets / 12 - 15 reps
   - wide push ups 

Tricep Exercise
3 sets / 8 - 12 reps
   - over head tricep extensions
   - tricep push down
3 sets / 12 - 15 reps
   - diamond push ups""",

        "Friday": """Bicep Exercise
3 sets / 8 - 12 reps
   - bicep curls
   - hammer curls
   - cross body hammer curls
Back Exercise
3 sets / 8 - 12 reps
   - arm pull down
   - lat pull down
   - supinated lat pull down
   - under hand row
3 sets / 12 - 15 reps
   - close grip push ups""",

        "Saturday": """Shoulder Exercise
3 sets / 8 - 12 reps
   - shoulder press
   - lateral raise
   - face pulls
3 sets / 12 - 15 reps
   - pike push ups

Leg Exercise
3 sets / 8 - 12 reps
   - squats 
   - stiff leg dead lift
   - lunges""",

        "Sunday": """Cardio
ABS Exercise
3 sets / 8 - 12 reps
   - crunches
   - russian twist
   - leg raise
   - plank (30 seconds to 1 minute)"""
    }

    # Update the workout label with the workout plan for the selected day
    workout_label.config(text=f"Workout plan for {day}:\n\n{workout_plans[day]}")


# User Data
user_data = {}

# Main Window
root = tk.Tk()
root.title("Fitness Macro Calculator System")
root.geometry("550x610")
root.config(bg="#b3e0ff")  # Set background to a soft blue color

# Set styles
style = ttk.Style()
style.configure("TButton", font=("Arial", 12, "bold"), padding=6, background="#0056b3", foreground="black")  # Set text color to black
style.configure("TCombobox", font=("Arial", 12), padding=5)

# === MAIN SCREEN ===
main_screen = tk.Frame(root, bg="#b3e0ff", padx=20, pady=20)

tk.Label(main_screen, text="Welcome to Macro Mate!", font=("Arial", 20, "bold"), bg="#b3e0ff", fg="#004d80").pack(pady=15)  # Blue text

tk.Label(main_screen, text="Name:", bg="#b3e0ff", font=("Arial", 12, "bold")).pack(anchor="w", pady=2)
name_entry = ttk.Entry(main_screen, width=40)
name_entry.pack(pady=5)

tk.Label(main_screen, text="Gender:", bg="#b3e0ff", font=("Arial", 12, "bold")).pack(anchor="w", pady=2)
gender_var = tk.StringVar()
gender_combobox = ttk.Combobox(main_screen, textvariable=gender_var, values=["Male", "Female"], width=38)
gender_combobox.pack(pady=5)

tk.Label(main_screen, text="Age:", bg="#b3e0ff", font=("Arial", 12, "bold")).pack(anchor="w", pady=2)
age_entry = ttk.Entry(main_screen, width=40)
age_entry.pack(pady=5)

tk.Label(main_screen, text="Weight (kg):", bg="#b3e0ff", font=("Arial", 12, "bold")).pack(anchor="w", pady=2)
weight_entry = ttk.Entry(main_screen, width=40)
weight_entry.pack(pady=5)

tk.Label(main_screen, text="Height (cm):", bg="#b3e0ff", font=("Arial", 12, "bold")).pack(anchor="w", pady=2)
height_entry = ttk.Entry(main_screen, width=40)
height_entry.pack(pady=5)

ttk.Button(main_screen, text="Next", command=show_activity_screen).pack(pady=15)

main_screen.pack()

# === ACTIVITY SCREEN ===
activity_screen = tk.Frame(root, bg="#b3e0ff", padx=20, pady=20)
tk.Label(activity_screen, text="Select Activity Level", font=("Arial", 16, "bold"), bg="#b3e0ff", fg="#004d80").pack(pady=15)

activity_var = tk.StringVar()
activity_combobox = ttk.Combobox(activity_screen, textvariable=activity_var, values=[
    "Light Exercise (1-2 days/week)",
    "Moderate Exercise (3-5 days/week)",
    "Heavy Exercise (6-7 days/week)",
    "Intense Exercise (2x per day)"
], width=40)
activity_combobox.pack(pady=5)

ttk.Button(activity_screen, text="Next", command=show_phase_screen).pack(pady=15)

# === PHASE SCREEN ===
phase_screen = tk.Frame(root, bg="#b3e0ff", padx=20, pady=20)
tk.Label(phase_screen, text="Select Dietary Phase", font=("Arial", 16, "bold"), bg="#b3e0ff", fg="#004d80").pack(pady=15)

phase_var = tk.StringVar()
phase_combobox = ttk.Combobox(phase_screen, textvariable=phase_var, values=["Maintenance", "Cutting", "Bulking"], width=40)
phase_combobox.pack(pady=5)

ttk.Button(phase_screen, text="Next", command=show_result_screen).pack(pady=15)

# === RESULT SCREEN ===
result_screen = tk.Frame(root, bg="#b3e0ff", padx=20, pady=20)
result_text = tk.StringVar()
result_label = tk.Label(result_screen, textvariable=result_text, font=("Arial", 12), bg="#b3e0ff", fg="#004d80")
result_label.pack(pady=20)

ttk.Button(result_screen, text="See Workout Schedule", command=show_workout_schedule).pack(pady=15)

# === WORKOUT SCHEDULE SCREEN ===
workout_schedule_screen = tk.Frame(root, bg="#b3e0ff", padx=20, pady=20)

tk.Label(workout_schedule_screen, text="Your Workout Schedule", font=("Arial", 16, "bold"), bg="#b3e0ff", fg="#004d80").pack(pady=15)

# Create a grid for Monday to Sunday buttons
button_frame = tk.Frame(workout_schedule_screen, bg="#b3e0ff")
button_frame.pack(pady=15)

days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
for i, day in enumerate(days_of_week):
    button = ttk.Button(button_frame, text=day, command=lambda day=day: show_day_workout(day))
    button.grid(row=i//3, column=i%3, padx=10, pady=10, sticky="ew")

# Label to display workout plan
workout_label = tk.Label(workout_schedule_screen, text="", font=("Arial", 12), bg="#b3e0ff", fg="#004d80")
workout_label.pack(pady=15)

ttk.Button(workout_schedule_screen, text="Back to Results", command=back_to_results).pack(pady=10)

root.mainloop()
