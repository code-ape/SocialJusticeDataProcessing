import os
import itertools

working_dir = os.path.dirname(os.path.realpath(__file__))

# data directory
data_file_name = "data"
# combine paths
data_dir = os.path.join(working_dir, data_file_name)


# raw folders
student_raw_folder_name = "raw/student"
fac_staff_raw_folder_name = "raw/fac_staff"
# combine paths
student_raw_dir = os.path.join(data_dir, student_raw_folder_name)
fac_staff_raw_dir = os.path.join(data_dir, fac_staff_raw_folder_name)


# clean folders
student_clean_folder_name = "clean/student"
fac_staff_clean_folder_name = "clean/fac_staff"
# combine paths
student_clean_dir = os.path.join(data_dir, student_clean_folder_name)
fac_staff_clean_dir = os.path.join(data_dir, fac_staff_clean_folder_name)


# stats folders
student_stats_folder_name = "stats/student"
fac_staff_stats_folder_name = "stats/fac_staff"
# combine paths
student_stats_dir = os.path.join(data_dir, student_stats_folder_name)
fac_staff_stats_dir = os.path.join(data_dir, fac_staff_stats_folder_name)


# raw files
student_raw_file_name = "E&H Student Climate Survey Early Fall 2015 (Responses) - Form Responses 1.csv"
fac_staff_raw_file_name = "E&H Faculty - Staff Climate Survey Early Fall 2015 (Responses) - Form Responses 1.csv"
# combine paths
student_raw_path = os.path.join(student_raw_dir, student_raw_file_name)
fac_staff_raw_path = os.path.join(fac_staff_raw_dir, fac_staff_raw_file_name)


# clean files
student_clean_file_name = "student_clean_data.json"
fac_staff_clean_file_name = "fac_staff_clean_data.json"
# combine paths
student_clean_path = os.path.join(student_clean_dir, student_clean_file_name)
fac_staff_clean_path = os.path.join(fac_staff_clean_dir, fac_staff_clean_file_name)

# result files
student_stats_file_name = "student_stats_data.pdf"
fac_staff_stats_file_name = "fac_staff_stats_data.pdf"
# combine paths
student_stats_path = os.path.join(student_stats_dir, student_stats_file_name)
fac_staff_stats_path = os.path.join(fac_staff_stats_dir, fac_staff_stats_file_name)

# result highlight files
student_stats_highlight_file_name = "student_stats_highlight_data.pdf"
fac_staff_stats_hightlight_file_name = "fac_staff_stats_highlight_data.pdf"
# combine paths
student_stats_highlight_path = os.path.join(student_stats_dir, student_stats_highlight_file_name)
fac_staff_stats_highlight_path = os.path.join(fac_staff_stats_dir, fac_staff_stats_hightlight_file_name)

# category highlight files
student_categories_highlight_file_name = "student_categories_highlight_data.txt"
fac_staff_categories_hightlight_file_name = "fac_staff_categories_highlight_data.txt"
# combine paths
student_categories_highlight_path = os.path.join(student_stats_dir, student_categories_highlight_file_name)
fac_staff_categories_highlight_path = os.path.join(fac_staff_stats_dir, fac_staff_categories_hightlight_file_name)

# verify everything exists
files_to_verify = [student_raw_path, fac_staff_raw_path]
dirs_to_verify = [
    student_raw_dir, fac_staff_raw_dir,
    student_clean_dir, fac_staff_clean_dir,
    student_stats_dir, fac_staff_stats_dir
]


cat = "catagory"
num = "numerical"
multi = "multiple"

student_question_types = [
    [num],      # 1
    [cat]*3,    # 2-4
    [num],      # 5
    [cat]*2,    # 6-7
    [multi],    # 8
    [cat],      # 9
    [num]*3,    # 10-12
    [cat],      # 13
    [multi]*3,  # 14-16
    [num]*2,    # 17-18
    [multi]*2,  # 19-20
    [cat],      # 21
    [num]*3,    # 22-24
    [multi],    # 25
    [num]*3,    # 26-28
    [cat]*2,    # 29-30
    [num]*2     # 31-32
]
student_question_types = list(itertools.chain(*student_question_types))
student_num_demographic_questions = 10 # generates 0-9 for questions 1-10
student_demographic_questions = range(student_num_demographic_questions)
student_opinion_questions = range(student_num_demographic_questions, len(student_question_types))

fac_staff_question_types = [
    [cat]*5,    # 1-5
    [num],      # 6
    [cat],      # 7
    [num]*19    # 8-26
]
fac_staff_question_types = list(itertools.chain(*fac_staff_question_types))
fac_staff_num_demographic_questions = 7 # generates 0-7 for questions 1-6
fac_staff_demographics_questions = range(fac_staff_num_demographic_questions)
fac_staff_opinion_questions = range(fac_staff_num_demographic_questions, len(fac_staff_question_types))


failed = False
for f in files_to_verify:
    if not os.path.isfile(f):
        print("Error, the following is not a file:\n\t{}".format(f))
        failed = True

for d in dirs_to_verify:
    if not os.path.isdir(d):
        print("Error, the following is not a dir:\n\t{}".format(f))
        failed = True

if not failed:
    print("Settings data integrity check passed.")
else:
    raise Exception("Necessary files don't exist!")
