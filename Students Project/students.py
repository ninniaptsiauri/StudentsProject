import json

class Student:
    def __init__(self, name, roll_number, grade):
        self.__name = name
        self.__roll_number = roll_number
        self.__grade = grade

    @property
    def name(self):
        return self.__name

    @property
    def roll_number(self):
        return self.__roll_number


    @property
    def grade(self):
        return self.__grade
    

    @grade.setter
    def grade(self, new_grade):
        self.__grade = new_grade
    

    def __str__(self):
        return f'Name: {self.name}\nRoll Number: {self.roll_number}\nGrade: {self.grade}\n'
    
    



class StudentSerializer:

    @staticmethod
    def custom_deserializer(json_obj):
        return Student(json_obj['name'], json_obj['roll_number'], json_obj['grade'])
    


    @staticmethod
    def custom_serializer(obj):
        if isinstance(obj, Student):
            return {
                'name': obj.name, 
                'roll_number': obj.roll_number, 
                'grade': obj.grade}
        
        raise TypeError(f'Object of {type(obj)} is not JSON serializable')





class StudentFileManager:

    @staticmethod
    def load_students_from_json():
        try:
            with open('Students Project/students.json', 'r') as json_file:
                students = json.load(json_file, object_hook=StudentSerializer.custom_deserializer)
                return students if isinstance(students, list) else []
            
        except json.JSONDecodeError:
            print("Error decoding the JSON data. Starting with an empty list.")
            return[]
        
        except FileNotFoundError:
            print("File not found. Starting with an empty list.")
            return[]
            
        except IOError as e:
            print(f"There was an error with the file: {e}.")
            return[]




    @staticmethod
    def save_students_to_json(students):
        try:
            with open('Students Project/students.json', 'w') as json_file:
                json.dump(students,json_file, default=StudentSerializer.custom_serializer, indent=4)

        except (TypeError, json.decoder.JSONDecodeError) as e:
            print(f"Error saving students to JSON: {e}")
        
        except Exception as e:
            print(f"An unexpected error occurred: {e}")





class UserInput:

    @staticmethod
    def get_valid_name(prompt):
        while True:
            name = input(prompt).strip()
            if name.isalpha() and len(name) > 1:
                return name
            
            elif name == "":
                print("You can't leave this field empty.")
            
            else:
                print("Please use only alphabetic characters.")



    @staticmethod
    def get_valid_roll_number():
        while True:
            roll_number_str = input("Enter Student's Roll Number: ").strip()
            if not roll_number_str:  
                print("This field cannot be left empty.")
                continue  

            try:
                roll_number = int(roll_number_str)
                if  roll_number > 0:
                    return roll_number
                else:
                    print("The student's roll number must be a positive number.")
            
            except ValueError:
                print("Invalid input. The student's roll number must be a positive number.")



    @staticmethod
    def get_valid_grade():
        while True:
            grade_str = input("Enter student's grade: ").strip()
            if not grade_str:  
                print("This field cannot be left empty.")
                continue

            try:
                grade = int(grade_str)
                if 0 <= grade <= 100:
                    return grade
                else:
                    print("Invalid input. Grade must be between 0 and 100.")

            except ValueError:
                print("Invalid input. The student's grade must be a number.")





class StudentManager():
    def __init__(self) -> None:
        self.__students = StudentFileManager.load_students_from_json()



    def add_new_student(self):
        first_name = UserInput.get_valid_name("Enter Student's First Name: ")
        last_name = UserInput.get_valid_name("Enter Student's Last Name: ")
        name = f"{first_name} {last_name}".title()

        while True: 
            roll_number = UserInput.get_valid_roll_number()
            if any(student.roll_number == roll_number for student in self.__students):
                print(f"Student with roll number {roll_number} already exists. Please choose new roll number.")
            else:
                break
        
        grade = UserInput.get_valid_grade()
       
        new_student = Student(name, roll_number, grade)
        self.__students.append(new_student)
        StudentFileManager.save_students_to_json(self.__students)
        print(f"Student {name} has been added successfully.")
        



    def all_students_info(self):
        if not self.__students:
            print("No students found.")
            return
        else:   
            for current_student in self.__students:
                print(current_student)




    def search_by_roll_number(self):
        roll_number = UserInput.get_valid_roll_number()
        student_found = False
        for student in self.__students:
            if student.roll_number == roll_number:
                print(f"\nStudent found:\nStudent Name: {student.name} | Roll Number: {student.roll_number} | Grade: {student.grade}")
                student_found = True
                break
                
        if not student_found:
            print(f"No student found with roll number: {roll_number}.")
               
                


    def update_student_grade(self):
        roll_number = UserInput.get_valid_roll_number()
        
        for student in self.__students:
            if student.roll_number == roll_number:
                print(f"Updating grade for {student.name} | Roll Number: {student.roll_number} | Current Grade: {student.grade}")

                new_grade = UserInput.get_valid_grade()
                if new_grade != student.grade:
                    student.grade = new_grade
                    print(f"Grade updated successfully.")

                    StudentFileManager.save_students_to_json(self.__students)
                    return
                
                else:
                    print("You entered the same grade. No changes have been made.")
                
        print(f"No student found with roll number {roll_number}.")




    def remove_student_by_roll_number(self):
        roll_number = UserInput.get_valid_roll_number()

        student_to_remove = None
        for student in self.__students:
            if student.roll_number == roll_number:
                student_to_remove = student
                break

        if student_to_remove:
            self.__students.remove(student_to_remove)
            StudentFileManager.save_students_to_json(self.__students)
            print(f"The student with roll number {roll_number} has been removed successfully.")

        else:
            print(f"No student found with roll number: {roll_number}.")





class MenuManager:
    def __init__(self, student_manager) -> None:
        self.student_manager = student_manager


    def menu(self): 
        options = {
            1: self.student_manager.add_new_student,
            2: self.student_manager.all_students_info,
            3: self.student_manager.search_by_roll_number,
            4: self.student_manager.update_student_grade,
            5: self.student_manager.remove_student_by_roll_number,
            6: self.exit_app
        }

        self.print_menu()

        while True: 
            try:  
                option = int(input("\nChoose an option -> "))
                if option in options:
                    options[option]()
                else:
                    print("Please select a valid number from the menu.")
                    
            except ValueError:
                print("Invalid input. Please enter a number.")



    def print_menu(self):
        print("------------ M e n u ------------")
        print("Select an option:")
        print("1. Add New Student")
        print("2. See All Students")
        print("3. Search Student by Roll Number")
        print("4. Update Student Grade")
        print("5. Remove Student by Roll Number")
        print("6. Exit")
        print("---------------------------------")
        print("For example, if you want to add a new student, type -> 1")


    
    def exit_app(self):
        print("Exiting the application. Goodbye!")   
        exit()
   




if __name__ == "__main__":
    student_manager = StudentManager()
    menu_manager = MenuManager(student_manager)
    menu_manager.menu()
