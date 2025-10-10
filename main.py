import database
import sys

def input_int(prompt: str, allow_empty: bool = False):
    """Prompt until a valid integer is entered (or None if allow_empty and blank)."""
    while True:
        s = input(prompt).strip()
        if s == "" and allow_empty:
            return None
        try:
            return int(s)
        except ValueError:
            print("Please enter a valid integer (e.g. 21). Try again.")

def menu():
    while True:
        print("\n--- Student Record Manager ---")
        print("1. Add Student")
        print("2. View Students")
        print("3. Update Student")
        print("4. Delete Student")
        print("5. Exit")

        choice = input("Enter choice: ").strip()

        if choice == '1':
            name = input("Name: ").strip()
            if not name:
                print("Name cannot be empty.")
                continue
            age = input_int("Age: ")
            course = input("Course: ").strip()
            if not course:
                print("Course cannot be empty.")
                continue
            database.add_student(name, age, course)
            print("Student added successfully!")

        elif choice == '2':
            students = database.view_students()
            if not students:
                print("No students found.")
                continue
            print("{:<4} {:<20} {:<5} {:<20}".format("ID","Name","Age","Course"))
            for s in students:
                age_display = s['age'] if s['age'] is not None else "-"
                print("{:<4} {:<20} {:<5} {:<20}".format(s['id'], s['name'], age_display, s['course']))

        elif choice == '3':
            student_id = input_int("Enter ID to update: ")
            if student_id is None:
                print("ID is required for update.")
                continue
            # Fetch current record to allow partial updates
            students = database.view_students()
            current = next((x for x in students if x['id'] == student_id), None)
            if not current:
                print(f"No student found with ID {student_id}.")
                continue
            print("Leave blank to keep current value.")
            name = input(f"New Name [{current['name']}]: ").strip() or current['name']
            age_input = input(f"New Age [{current['age']}]: ").strip()
            age = int(age_input) if age_input else current['age']
            course = input(f"New Course [{current['course']}]: ").strip() or current['course']
            updated = database.update_student(student_id, name, age, course)
            if updated:
                print("Record updated successfully!")
            else:
                print("No changes were made.")

        elif choice == '4':
            student_id = input_int("Enter ID to delete: ")
            if student_id is None:
                print("ID is required for deletion.")
                continue
            deleted = database.delete_student(student_id)
            if deleted:
                print("Record deleted successfully!")
            else:
                print("No record found with that ID.")

        elif choice == '5':
            print("Goodbye!")
            break

        else:
            print("Invalid choice! Try again.")

if __name__ == "__main__":
    try:
        menu()
    except KeyboardInterrupt:
        print("\nInterrupted by user. Exiting.")
        sys.exit(0)
