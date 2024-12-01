import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Database setup
def initialize_db():
    global conn, cursor
    conn = sqlite3.connect("fitness_app.db")
    cursor = conn.cursor()
    
    # Create tables for organizing data
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS activity_levels (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            level TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS phases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phase TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            gender TEXT,
            age INTEGER,
            weight REAL,
            height REAL,
            activity_level_id INTEGER,
            phase_id INTEGER,
            tdee REAL,
            FOREIGN KEY (activity_level_id) REFERENCES activity_levels(id),
            FOREIGN KEY (phase_id) REFERENCES phases(id)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS macronutrients (
            user_id INTEGER PRIMARY KEY,
            protein REAL,
            fat REAL,
            carbs REAL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    
    conn.commit()

# Query 1: SELECT statement with JOIN
def select_users_with_activity_and_phase():
    cursor.execute("""
        SELECT u.id, u.name, u.age, u.weight, u.height, a.level AS activity_level, p.phase
        FROM users u
        JOIN activity_levels a ON u.activity_level_id = a.id
        JOIN phases p ON u.phase_id = p.id;
    """)
    return cursor.fetchall()

# Query 2: UPDATE statement to modify existing records
def update_user_weight_and_height(user_id, weight, height):
    cursor.execute("""
        UPDATE users
        SET weight = ?, height = ?
        WHERE id = ?;
    """, (weight, height, user_id))
    conn.commit()

# Query 3: DELETE statement to remove records
def delete_user(user_id):
    cursor.execute("""
        DELETE FROM users
        WHERE id = ?;
    """, (user_id,))
    conn.commit()

# Query 4: Aggregate function (COUNT) to count users by activity level
def count_users_by_activity_level():
    cursor.execute("""
        SELECT a.level, COUNT(u.id) AS user_count
        FROM users u
        JOIN activity_levels a ON u.activity_level_id = a.id
        GROUP BY a.level;
    """)
    return cursor.fetchall()

# Query 5: Complex query using subqueries and aggregation
def total_macronutrients_by_phase(phase_name):
    cursor.execute("""
        SELECT p.phase, SUM(m.protein) AS total_protein, SUM(m.fat) AS total_fat, SUM(m.carbs) AS total_carbs
        FROM macronutrients m
        JOIN users u ON m.user_id = u.id
        JOIN phases p ON u.phase_id = p.id
        WHERE p.phase = ?
        GROUP BY p.phase;
    """, (phase_name,))
    return cursor.fetchall()

# Example usage:
def main():
    # Initialize database and create tables
    initialize_db()

    # Example of inserting some data
    user_data = {
        'name': 'John Doe',
        'gender': 'Male',
        'age': 28,
        'weight': 80.0,
        'height': 1.75,
        'activity_level': 'Moderate',
        'phase': 'Cut'
    }
    tdee = 2500
    macronutrients = {'protein': 150, 'fat': 70, 'carbs': 200}
    save_to_db(user_data, tdee, macronutrients)

    # Query 1 - Get all users with activity and phase details
    users_with_activity_and_phase = select_users_with_activity_and_phase()
    print("Users with Activity and Phase:", users_with_activity_and_phase)

    # Query 2 - Update user data
    update_user_weight_and_height(1, 75.0, 1.80)

    # Query 3 - Delete a user
    delete_user(2)

    # Query 4 - Get count of users by activity level
    activity_level_count = count_users_by_activity_level()
    print("Activity Level Count:", activity_level_count)

    # Query 5 - Get total macronutrients for users in a specific phase (e.g., "Cut")
    macronutrients_in_cut_phase = total_macronutrients_by_phase('Cut')
    print("Macronutrients in Cut Phase:", macronutrients_in_cut_phase)

# Function to save user and macronutrient data to the database
def save_to_db(user_data, tdee, macronutrients):
    # Insert activity level if not already in the table
    cursor.execute("SELECT id FROM activity_levels WHERE level = ?", (user_data['activity_level'],))
    activity_level_id = cursor.fetchone()
    if not activity_level_id:
        cursor.execute("INSERT INTO activity_levels (level) VALUES (?)", (user_data['activity_level'],))
        activity_level_id = cursor.lastrowid
    else:
        activity_level_id = activity_level_id[0]
    
    # Insert phase if not already in the table
    cursor.execute("SELECT id FROM phases WHERE phase = ?", (user_data['phase'],))
    phase_id = cursor.fetchone()
    if not phase_id:
        cursor.execute("INSERT INTO phases (phase) VALUES (?)", (user_data['phase'],))
        phase_id = cursor.lastrowid
    else:
        phase_id = phase_id[0]

    # Insert user data into the users table
    cursor.execute("""
        INSERT INTO users (name, gender, age, weight, height, activity_level_id, phase_id, tdee)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        user_data['name'],
        user_data['gender'],
        user_data['age'],
        user_data['weight'],
        user_data['height'],
        activity_level_id,
        phase_id,
        tdee
    ))
    user_id = cursor.lastrowid

    # Insert macronutrient data
    cursor.execute("""
        INSERT INTO macronutrients (user_id, protein, fat, carbs)
        VALUES (?, ?, ?, ?)
    """, (user_id, macronutrients['protein'], macronutrients['fat'], macronutrients['carbs']))
    
    conn.commit()
    
def update_user_data():
    new_age = int(age_entry.get())
    new_weight = float(weight_entry.get())
    new_height = float(height_entry.get())
    
    # Update user data dictionary
    user_data.update({"age": new_age, "weight": new_weight, "height": new_height})
    
    # Update database record
    cursor.execute("""
        UPDATE users SET age = ?, weight = ?, height = ?
        WHERE name = ? AND gender = ?
    """, (new_age, new_weight, new_height, user_data['name'], user_data['gender']))
    conn.commit()

    messagebox.showinfo("Update Successful", "Your information has been updated!")
    main_screen.pack_forget()
    result_screen.pack()
def load_existing_user(name, gender):
    cursor.execute("SELECT age, weight, height, tdee FROM users WHERE name = ? AND gender = ?", (name, gender))
    user_info = cursor.fetchone()
    if user_info:
        user_data['age'], user_data['weight'], user_data['height'], user_data['tdee'] = user_info
        return True
    return False
def save_to_db(user_data, tdee, macronutrients):
    cursor.execute("SELECT id FROM users WHERE name = ? AND gender = ?", (user_data['name'], user_data['gender']))
# Initialize the database
initialize_db()

#End of Database









def validate_name_input(new_value):
    # This will allow only alphabets and spaces, no numbers or special characters
    if all(c.isalpha() or c.isspace() for c in new_value) or new_value == "":
        return True
    else:
        messagebox.showerror("Invalid Input", "Name must contain only letters!")
        return False


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
    bmr = calculate_bmr(user_data["gender"], user_data["weight"], user_data["height"], user_data["age"])
    tdee = round(calculate_tdee(bmr, user_data["activity_level"])) 
    weekly_calories = tdee * 7
    macronutrients = calculate_macronutrients(tdee, user_data["phase"])

    # Round macronutrient values to whole numbers
    protein = round(macronutrients["protein"])
    fat = round(macronutrients["fat"])
    carbs = round(macronutrients["carbs"])

    result_text.set(
        f"Greetings, {user_data['name']}.\n"
        f"You are a {user_data['age']}-year-old {user_data['gender'].lower()} who weighs {user_data['weight']} kg and\n"
        f"height of {user_data['height']} cm tall. You perform {user_data['phase'].lower()} exercises \nand "
        f"{user_data['activity_level'].lower()}.\n\n"
        f"Daily Intake: {tdee} calories\n"
        f"Weekly Intake: {weekly_calories} calories\n\n"
        f"Macronutrients:\n"
        f"  - Protein: {protein} grams\n"
        f"  - Fats: {fat} grams\n"
        f"  - Carbs: {carbs} grams"
    )

    phase_screen.pack_forget()
    result_screen.pack()


def show_workout_schedule():
    result_screen.pack_forget()  
    workout_schedule_screen.pack()  


def back_to_results():
    workout_schedule_screen.pack_forget() 
    result_screen.pack()  


# Function to show workout for a specific day
def show_day_workout(day):
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
   - basketball
   - jogging
ABS Exercise
3 sets / 8 - 12 reps
   - crunches
   - russian twist
   - leg raise
   - plank (30 seconds to 1 minute)"""
    }
    workout_label.config(text=f"Workout plan for {day}:\n\n{workout_plans[day]}")

user_data = {}

# Main Window
root = tk.Tk()
root.title("Fitness Macro Calculator System")
root.geometry("550x610")
root.config(bg="#b3e0ff")  

# Set styles
style = ttk.Style()
style.configure("TButton", font=("Arial", 12, "bold"), padding=6, background="#0056b3", foreground="black")  
style.configure("TCombobox", font=("Arial", 12), padding=5)

# === MAIN SCREEN ===
main_screen = tk.Frame(root, bg="#b3e0ff", padx=20, pady=20)

tk.Label(main_screen, text="Welcome to Macro Mate!", font=("Arial", 20, "bold"), bg="#b3e0ff", fg="#004d80").pack(pady=15)  

tk.Label(main_screen, text="Name:", bg="#b3e0ff", font=("Arial", 12, "bold")).pack(anchor="w", pady=2)
validate_name = root.register(validate_name_input)  

name_entry = ttk.Entry(main_screen, width=40, validate="key", validatecommand=(validate_name, "%P"))
name_entry.pack(pady=5)

tk.Label(main_screen, text="Gender:", bg="#b3e0ff", font=("Arial", 12, "bold")).pack(anchor="w", pady=2)
gender_var = tk.StringVar()
gender_combobox = ttk.Combobox(main_screen, textvariable=gender_var, values=["Male", "Female"], width=38, state="readonly")
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
], width=40, state="readonly")
activity_combobox.pack(pady=5)

ttk.Button(activity_screen, text="Next", command=show_phase_screen).pack(pady=15)

# === PHASE SCREEN ===
phase_screen = tk.Frame(root, bg="#b3e0ff", padx=20, pady=20)
tk.Label(phase_screen, text="Select Dietary Phase", font=("Arial", 16, "bold"), bg="#b3e0ff", fg="#004d80").pack(pady=15)

phase_var = tk.StringVar()
phase_combobox = ttk.Combobox(phase_screen, textvariable=phase_var, values=["Maintenance", "Cutting", "Bulking"], width=40, state="readonly")
phase_combobox.pack(pady=5)

ttk.Button(phase_screen, text="Next", command=show_result_screen).pack(pady=15)

# === RESULT SCREEN ===
result_screen = tk.Frame(root, bg="#b3e0ff", padx=20, pady=20)
result_text = tk.StringVar()
result_label = tk.Label(result_screen, textvariable=result_text, font=("Arial", 12), bg="#b3e0ff", fg="#004d80")
result_label.pack(pady=20)

ttk.Button(result_screen, text="See Workout Schedule", command=show_workout_schedule).pack(pady=15)

def update_user_data():
    result_screen.pack_forget()
    main_screen.pack()

    name_entry.delete(0, tk.END)
    name_entry.insert(0, user_data.get("name", "")) 
    name_entry.config(state="disabled") 

    gender_var.set(user_data.get("gender", ""))
    gender_combobox.config(state="disabled") 

    # Make age, weight, height editable
    age_entry.delete(0, tk.END)
    age_entry.insert(0, user_data.get("age", ""))

    weight_entry.delete(0, tk.END)
    weight_entry.insert(0, user_data.get("weight", ""))

    height_entry.delete(0, tk.END)
    height_entry.insert(0, user_data.get("height", ""))

    # Disable the activity level combobox (read-only)
    activity_combobox.config(state="disabled")  

    # Disable the phase combobox (read-only)
    phase_combobox.config(state="disabled")  
 
# === RESULT SCREEN ===
def reset_all_fields():
    user_data.clear()
    name_entry.delete(0, tk.END)
    gender_var.set("")
    age_entry.delete(0, tk.END)
    weight_entry.delete(0, tk.END)
    height_entry.delete(0, tk.END)
    activity_var.set("")
    phase_var.set("")

    name_entry.config(state="normal")
    gender_combobox.config(state="normal")
    activity_combobox.config(state="normal")
    phase_combobox.config(state="normal")

    # Go back to the first screen
    result_screen.pack_forget()  
    main_screen.pack()

result_screen = tk.Frame(root, bg="#b3e0ff", padx=20, pady=20)
result_text = tk.StringVar()
result_label = tk.Label(result_screen, textvariable=result_text, font=("Arial", 12), bg="#b3e0ff", fg="black")
result_label.pack(pady=20)

ttk.Button(result_screen, text="See Workout Schedule", command=show_workout_schedule).pack(pady=15)

# Adding the Reset Button (this will completely reset and start from the beginning)
ttk.Button(result_screen, text="Reset", command=reset_all_fields).pack(pady=10)

# Adding the Update Button
ttk.Button(result_screen, text="Update Info", command=update_user_data).pack(pady=10)


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
