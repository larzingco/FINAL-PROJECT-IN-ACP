<div align="center"> <img src="https://github.com/user-attachments/assets/24418ef3-3b22-4106-8352-04cebf4daecf">  

**Ingco, Larz Byron E.**

***IT-2104***

🏋️‍♂️🏋️‍♂️🏋️‍♂️</div>


## I. Project Overview 💪
Fitness Macro Calculator System is a Python-based application designed to assist users in calculating their daily caloric needs and macronutrient distribution based on their personal fitness goals. The system also provides a customized weekly workout schedule. Users can input their personal details like name, age, weight, height, and activity level to receive precise caloric recommendations tailored to their dietary phase: Maintenance, Cutting, or Bulking.

This program aims to make fitness planning more accessible by offering an intuitive user interface where users can seamlessly navigate between screens, view personalized macronutrient breakdowns, and follow structured workout routines. The system integrates both nutritional and workout guidance in one easy-to-use application.

---

## II. Python Concepts, Libraries, and Features 🐍
In developing this Fitness Macro Calculator and Workout Scheduler, several Python concepts and libraries were utilized to ensure efficient functionality and scalability, including:

1. Object-Oriented Programming (OOP)
The project applies key Object-Oriented Programming principles for better structure and maintainability:
- **Encapsulation**
   - In this system, user data (age, weight, height, gender) is stored in the user_data dictionary, and calculations are handled via dedicated functions like calculate_bmr(), calculate_tdee(), and calculate_macronutrients().
The main UI elements and logic are encapsulated within the Tkinter frames and functions that control screen transitions and user interactions.

- **Inheritance**
   - For instance, the classes ttk.Combobox, ttk.Button, and ttk.Label inherit from base Tkinter classes, and they are extended with specific functionality such as button clicks and screen transitions.

- **Polymorphism**
   - Methods like show_day_workout() dynamically update the workout plan based on the selected day (Monday, Tuesday, etc.).
   - The show_result_screen() and show_workout_schedule() functions use polymorphism to manage different types of screens and their respective data, ensuring the right information is shown to the user at each stage.

- **Abstraction**
   - The calculations for BMR, TDEE, and macronutrient distribution are abstracted into functions, simplifying the user experience by not requiring them to understand the underlying math.
   - The detailed workout plans for each day are stored as dictionary entries, and users only need to interact with the buttons without worrying about the data structure.

2. **GUI with Tkinter**
   - The graphical user interface (GUI) is built using Tkinter to create an interactive and dynamic user experience:
     - Multiple screens (Main, Activity Level, Phase, Results, Workout Schedule) are implemented using tk.Frame, which is switched dynamically using .pack_forget() and .pack().
     - The interface contains user input fields for name, age, weight, height, gender, activity level, and dietary phase.
     - Buttons and dropdown menus (ttk.Combobox) are used to navigate between screens and make selections.
     - Text information and results are displayed dynamically using tk.Label and tk.StringVar().

3. **Data Validation and Error Handling**
   - To ensure users provide complete and valid information before proceeding, the following validation checks are implemented:
     - Required fields: If any input field is missing (such as name, age, weight, or height), the program will show a pop-up error: "Please fill out all the information!"
     - Numeric validation: If age, weight, or height are not numeric, an error message is shown: "Age, Weight, and Height must be numeric values!"
     - Activity and phase validation: If the user does not select an activity level or dietary phase, they are prompted with a message like: "Please select an activity level!" or "Please select a dietary phase!"
     - These checks prevent incomplete or invalid data from being processed and ensure smooth user interaction.

4. **Calculations**
   - The system performs essential calculations based on user input:
     - BMR Calculation: The Basal Metabolic Rate (BMR) is calculated based on the Mifflin-St Jeor equation for both males and females.
     - TDEE Calculation: The Total Daily Energy Expenditure (TDEE) is calculated by applying an activity factor based on the user’s selected activity level.
     - Macronutrient Calculation: The macronutrient distribution (protein, fats, and carbohydrates) is calculated according to the selected dietary phase (maintenance, cutting, bulking).

5. **Workout Schedule**
   - The system also provides a personalized workout schedule for each day of the week. The workout routine is displayed dynamically when the user clicks on a day:
     - Workouts include exercises for muscle groups such as chest, triceps, biceps, back, shoulders, legs, and cardio.
     - The user can view the workout plan for each day and switch between different days by clicking the corresponding buttons (Monday, Tuesday, etc.).
     - The workout plans are predefined in a dictionary and displayed using tk.Label.

6. **Libraries Used**
   - tkinter: The core library for building the GUI, handling user interactions, and managing different screens.
   - ttk: For additional styling of widgets like buttons and comboboxes.
   - messagebox: For displaying pop-up messages and alerts for user notifications and error handling.
  
7. **Database Integration with SQLite**
   - SQLite is integrated to store user data persistently:
     - sqlite3.connect("fitness_app.db") establishes a connection to the SQLite database.
     - cursor.execute runs SQL commands like CREATE TABLE and INSERT INTO.
     - save_to_db() inserts user data and calculated results into the database, enabling future retrieval or analysis.
    
8. **Data Persistence & Update Handling**
   - The system allows users to update certain fields (age, weight, height) while keeping others locked (name, gender, activity level, phase):
     - Pre-filled Fields: update_user_data() reopens the main screen with pre-filled data while locking name and gender fields, preserving integrity.
     - Reset Functionality: reset_all_fields() clears all inputs and resets the program to its initial state.


---

## III. Sustainable Development Goal (SDG) 🏗️
<div align="center"> <img src="https://github.com/user-attachments/assets/3b5d1779-48a7-486a-a57d-bddca83edb1f"> 

### SDG 3: Good Health and Well-Being </div>
The Macro Mate system plays a crucial role in promoting good health and well-being by empowering users to take charge of their physical fitness and nutrition. Here’s how it supports SDG 3:

1. **Promoting Healthy Lifestyles**
   - Personalized Fitness and Nutrition Guidance: By calculating BMR (Basal Metabolic Rate), TDEE (Total Daily Energy Expenditure), and macronutrient requirements based on personal data (age, weight, height, gender, activity level), your system helps users understand their body’s energy needs. This personalization encourages better lifestyle choices, such as maintaining a balanced diet or exercising at an appropriate intensity level, which are key to overall well-being.
   - Dietary Phase Customization: The system gives users options to choose between different dietary phases (Maintenance, Cutting, or Bulking), allowing them to align their nutrition with their fitness goals. Whether a user is trying to lose weight (cutting), maintain current weight (maintenance), or gain muscle (bulking), the system provides tailored nutritional guidance. This helps users make informed decisions to improve their health outcomes.

2. **Supporting Mental and Physical Health**
   - Goal-Oriented Fitness Plans: Your system’s built-in workout schedule feature provides users with a structured plan to follow, which can help individuals stay motivated and achieve their fitness goals. Regular physical activity, along with proper nutrition, is essential for improving mental and physical health. By providing a daily workout plan, your system helps users stay active and improve their overall fitness.
    - Building Healthy Habits: By offering a structured approach to fitness (through daily workouts and personalized macronutrient intake), your system helps users build consistent and healthy habits. Regular exercise and proper nutrition not only improve physical health but also reduce stress, anxiety, and depression, thus enhancing mental well-being.

3. **Reducing Health Risks**
   - Preventive Health: With personalized advice on calorie intake, macronutrient distribution, and exercise routines, the system encourages users to adopt healthier lifestyles that can prevent the development of chronic diseases such as obesity, diabetes, and heart disease. Proper nutrition and exercise play a major role in preventing these conditions.
   - Promoting Balance: By helping users maintain a healthy balance between nutrition and exercise, your system contributes to the prevention of malnutrition, both undernutrition and overnutrition, which are major global health issues. Educating users about their body’s caloric and macronutrient needs also ensures they make healthier choices in their daily lives.

4. **Enhancing Community Health**
   - Accessibility and Inclusivity: The system’s user-friendly interface ensures that a broad demographic can access personalized fitness and nutrition advice. This makes health and wellness tools more inclusive, empowering individuals from various backgrounds to take care of their health, contributing to the well-being of the broader community.
   - Encouraging Physical Activity: Through tailored workout plans and nutrition guidance, your system helps people incorporate more physical activity into their daily lives. This is crucial in improving community health and reducing the risks associated with sedentary lifestyles, such as obesity and cardiovascular diseases.

5. **Education and Empowerment**
   - Informed Health Decisions: By providing detailed information about BMR, TDEE, and macronutrients, the system educates users on the importance of nutrition and physical activity in maintaining health. This empowerment encourages individuals to make informed decisions about their diet and fitness routines, leading to healthier lifestyles.

--- 

## IV. Instructions for Running the Program 📌
**Prerequisites: 📜**
   1. Python (version 3.x or higher)
     - Download and install Python from python.org if not already installed.
   2. Tkinter (for GUI interface)
     - Tkinter is bundled with Python, so you should have it installed by default. 
   3. IDE or Text Editor
     - You can use any IDE like Visual Studio Code, PyCharm, Sublime Text, or Notepad++ to run your code.
      
**Steps to Run the Program: 🏃‍♂️**
   1. Download the Code:
     - Copy or clone the Python script to your local machine. If you are using GitHub, you can use the following commands:
      ```bash
      git clone https://github.com/your-username/fitness-macro-calculator.gitcd fitness-macro-calculator
   2. Run the Program:
     - Open a terminal (or command prompt) and navigate to the folder containing the Python script.

**Folder Structure: 📂**
  ```bash
ACP FINAL PROJECT
  │
  ├── src/
  │   ├── Fitness Macro Calculator System.py              # Main file
  ├── fitness_app.db              # Data Base
  └── README.md                   # Documentation
```

**Program Controls: 📚**

**Main Screen:**
   - Input your name, age, weight, height, and gender.
   - Click "Next" to proceed to the Activity Level screen.

**Activity Level Screen:**
   - Select your activity level (e.g., "Light Exercise", "Moderate Exercise", etc.).
   - Click "Next" to proceed to the Dietary Phase screen.

**Dietary Phase Screen:**
   - Select a dietary phase ("Maintenance", "Cutting", or "Bulking").
   - Click "Next" to calculate your BMR, TDEE, and macronutrients.

**Result Screen:**
   - View your results, including BMR, TDEE, daily and weekly calorie intake, and macronutrient breakdown.
   - "See Workout Schedule" Navigates to a personalized workout plan screen.
   - "Update Info" Allows users to modify age, weight, and height without resetting other inputs. Name and gender fields are disabled to avoid major data changes while allowing precise updates for TDEE recalculation.
   - "Reset" Clears all user inputs and resets the application to the Main Screen for new entries.

**Workout Schedule Screen:**
   - Click on the buttons for each day (e.g., Monday, Tuesday) to view the workout plan for that day.
   - Click "Back to Results" to return to the result screen.

**Functionality Controls: ⚙️**
   - Submit and Proceed: After filling in the details, click "Next" to proceed to the next screen.
   - Calculate Results: The program will calculate your daily calorie needs, macronutrient requirements, and display a tailored workout schedule.
   - Workout Plan: The program offers a personalized workout schedule for each day of the week, which you can view by clicking on the respective days.

---

## Thank You for Using Macro Mate!

I sincerely appreciate you choosing Macro Mate as your fitness and nutrition guide. I hope it has helped you gain valuable insights into your health, nutrition, and workout plans. Remember, consistency is key, and Macro Mate are here to support you on your wellness journey.

Stay healthy, stay strong, and come back anytime to keep track of your fitness progress!

## Happy training and healthy living! 💪🏋️‍♂️
