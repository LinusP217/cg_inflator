'''
Python script for incrementing student assignment grades. Runs as an interactive program, prompting the user for input.
usage: python cg_inflator.py
'''

# install/import needed packages
try:
    from tabulate import tabulate
    from canvasapi import Canvas
    import canvasapi
    import numpy as np
except:
    import sys, subprocess
    user_install = input("This program needs one or more of the following packages: canvasapi, tabulate, and numpy. Would you like to install them to this python environment (y/n)?\n")
    if user_install.strip().lower() == 'y':
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'canvasapi'])
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'tabulate'])
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'numpy'])
        from tabulate import tabulate
        from canvasapi import Canvas
        import numpy as np
        import pwinput
    else:
        exit()

from datetime import date, datetime

today = date.today()
today_fmt = today.strftime("%b-%d-%Y")
time_now = datetime.now().strftime("%H:%M")
__version__ = 0.1
__license__ = 'MIT'
__github__ = 'https://github.com/LinusP217/cg_inflator'

print(
r"""
-----------------------------------------------------------------
   ____                             ____               _
  / ___|__ _ _ ____   ____ _ ___   / ___|_ __ __ _  __| | ___
 | |   / _` | '_ \ \ / / _` / __| | |  _| '__/ _` |/ _` |/ _ \
 | |__| (_| | | | \ V / (_| \__ \ | |_| | | | (_| | (_| |  __/
  \____\__,_|_| |_|\_/ \__,_|___/  \____|_|  \__,_|\__,_|\___|
            |_ _|_ __  / _| | __ _| |_ ___  _ __
             | || '_ \| |_| |/ _` | __/ _ \| '__|
             | || | | |  _| | (_| | || (_) | |
            |___|_| |_|_| |_|\__,_|\__\___/|_|
 
-----------------------------------------------------------------
A python script 🐍 for instructors wanting to add (or subtract) 
points to student grades on Canvas, a capability not available 
on the web interface 😠💻.
""")
print('------------------------------------\n')
print(f'Version {__version__}')
print(f'Repository link: {__github__}')
print(f'Distributed under an {__license__} License')
print(f'{today_fmt}    {time_now}')
print('\n------------------------------------\n')
print(f'To start, enter your institutional url for Canvas 🏫')
print("e.g. https://uiowa.instructure.com' for The University of Iowa")
CANVAS_URL = input(f'URL input:\n').strip()
print(f'\nURL entered: {CANVAS_URL}\n')
print(f'Now please enter your API key 🔑')
print(f"watch this video if you don't know what that means")
print('https://www.youtube.com/watch?v=cZ5cn8stjM0&ab_channel=DavidSherlock')

while True:
    API_KEY=input("\nCanvas API Key (q to exit):\n")
    if API_KEY.strip().lower() == 'q':
        print("Exiting...")
        exit()
    try:
        canvas = Canvas(CANVAS_URL, API_KEY.strip())
        courses = canvas.get_courses()
        course_names = [course.name for course in courses]
        print("Valid API Key provided.")
        break
    except Exception as error:
        print(f"Error {error}")
        print("Please try again.")
        continue

# print courses with start end dates in tabulate format, then select one
course_id    = [course.id for course in courses]
course_starts = [course.start_at for course in courses]
course_ends = [course.end_at for course in courses]
course_states = [course.workflow_state for course in courses]

courses_num  = len(course_names)
course_indices = np.arange(0,len(course_names))

for i in range(len(course_states)):
    if course_states[i] == 'available':
        course_states[i] = 'Yes'
    elif course_states[i] == 'unpublished':
        course_states[i] = 'No'

course_header = ['Course Title', 'Published?', 'Start Date', 'End Date', 'Course id'] 
course_table = zip(course_names, course_states, course_starts, course_ends, course_id)
print('\nCourse Listing 🏫')
print(tabulate(course_table, course_header, tablefmt='grid', showindex=True))

while True:
    course_index = input(f"\nSelect a course from index number (0-{courses_num}):\n")
    try:
        course_index = int(course_index)
    except ValueError as error:
        print("Please enter a valid index")
        continue
    except Exception as error:
        print(error)
        continue
    if course_index in course_indices:
        break
    if course_index == 'q':
        exit()
    if course_index not in course_indices:
        print("Enter a valid index")
        continue

student_list = []
for student in courses[course_index].get_users(enrollment_type=['student']):
    student_list.append((student.name, student.id, student.email))

assign_names, assign_statuses, assign_ids, assign_pts = [], [], [], []
for assignment in courses[course_index].get_assignments():
    assign_names.append(assignment.name)
    if assignment.workflow_state == 'published':
        assign_statuses.append('Yes')
    elif assignment.workflow_state == 'unpublished':
        assign_statuses.append('No')
#    assign_statuses.append(assignment.workflow_state)
    assign_ids.append(assignment.id)
    assign_pts.append(assignment.points_possible)

assignments_num = len(assign_names)

assignment_headers = ['Assignment Name', 'Published?', 'id', 'pts']

print(f"Entered {course_index}\nCourse '{course_names[course_index]}' selected")
print(f' ')
print(f"Student Enrollment: {len(student_list)}")
print(f'Assignments: {len(assign_names)}')
assignment_table = zip(assign_names, assign_statuses, assign_ids, assign_pts)
print('Assignment Listing 🍎')
print(tabulate(assignment_table, assignment_headers, tablefmt='grid', showindex=True))

while True:
    assignment_index = input(f"\nSelect an assignment from the index number (0-{assignments_num}):\n")
    try:
        assignment_index = int(assignment_index)
    except ValueError as error:
        print("Please enter a valid index")
        continue
    except Exception as error:
        print(error)
        continue
    if course_index in course_indices:
        break
    if course_index == 'q':
        exit()
    if course_index not in course_indices:
        print("Enter a valid index")
        continue

selected_assignment = courses[course_index].get_assignment(assign_ids[assignment_index])
student_taking = selected_assignment.get_gradeable_students()
submissions = [sub for sub in selected_assignment.get_submissions()]

print(f"Entered {assignment_index}\nAssignment '{assign_names[assignment_index]}' selected\n")

def get_student_scores(assignment, students):
    score_info  = []
    points_avail = assignment.points_possible
    for name, user_id, email in students:
        submission = assignment.get_submission(user_id)
        state = submission.workflow_state
        grade_pts = submission.score
        if grade_pts == None:
            grade_percent = None
        else:
            grade_percent = round((grade_pts / points_avail * 100), 2)
        score_info.append((f'{name} ({user_id})', state, grade_pts, grade_percent))
    return score_info

student_scores = get_student_scores(selected_assignment, student_list)
average_score = round(np.average([x[2] for x in student_scores if x[2] is not None]), 2)


score_headers = ['Name (id)', 'Grade State', 'Score (pts)', 'Score (%)']
print(f"{assign_names[assignment_index]} Student Scores 🚀")
print(tabulate(student_scores, score_headers, tablefmt='grid', showindex=True))
print(f"Assignment points: {selected_assignment.points_possible}")
print(f'Avg. Score       : {average_score}')

def inflate_grades(assignment, students, increment):
    print(f"\nIncrementing all scores (except None) by {increment} for {assign_names[assignment_index]}")
    print("Name                : Old Score -> New Score")
    print("--------------------------------------------")
    for name, user_id, email in students:
        submission = assignment.get_submission(user_id)
        old_score = submission.score
        if old_score == None:
            new_score = None
            print(f'{name.ljust(20)}:      {old_score} -> {new_score}')
        else:
            new_score = old_score + increment
            submission.edit(submission={'posted_grade': new_score})
            submission.edit(comment={'text_comment': f'curve {round(old_score, 3)} -> {round(new_score, 3)}'})
            print(f'{name.ljust(20)}:      {old_score:.2f} -> {new_score:.2f}')
    print("--------------------------------------------")
    print("Comment 'curve {old_score} -> {new_score}' left on changed submissions")
    print("All done!")

while True:
    inflate_res = input(f"\nAdd or subtract points to student scores for {assign_names[assignment_index]} (y/n)?\n")
    inflate_res = inflate_res.strip().lower()
    if inflate_res == 'y':
        while True:
            scale_num = input("\nEnter increment/decrement amout (e.g. +1.5, -7, etc):\n")
            try:
                scale_num = float(scale_num)
                break
            except Exception as error:
                print(error)
                print("Pleaser enter a valid number")
                continue
        inflate_grades(selected_assignment, student_list, scale_num)
        print("\nThank you for using Canvas Grade Inflator 😃")
        exit()
    elif inflate_res == 'n':
        print("Exiting...")
        exit()
    else:
        print("Not a valid input")
        continue

