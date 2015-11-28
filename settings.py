import os

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

# verify everything exists
files_to_verify = [student_raw_path, fac_staff_raw_path]
dirs_to_verify = [
    student_raw_dir, fac_staff_raw_dir,
    student_clean_dir, fac_staff_clean_dir,
    student_stats_dir, fac_staff_stats_dir
]

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
