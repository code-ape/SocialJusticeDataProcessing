# -*- coding: utf-8 -*-

import csv, json
import os
import traceback

import settings
import tools

diverse_matcher = {
    "Very Diverse": 3, "Moderately Diverse": 2,
    "Slightly Diverse": 1, "Not Diverse": 0
}

importance_matcher = {
    "Very Important": 3,
    "Moderately Important": 2,
    "Slightly Important": 1,
    "Slightly  Unimportant": -1, #contains special ascii character
    "Moderately Unimportant": -2,
    "Very Unimporant": -3
}

agreement_matcher = {
    "Strongly Agree": 3,
    "Moderately Agree": 2,
    "Slightly Agree": 1,
    "Slightly Disagree": -1,
    "Moderately Disagree": -2,
    "Strongly Disagree": -3
}


def clean_fac_staff_data(fac_staff_data):
    fac_staff_clean_key = []
    fac_staff_clean_data = []

    # strip initial entry that is the question each answer coorelates to
    for i in xrange(1, len(fac_staff_data)):
        try:
            print('.'),
            raw_entry = fac_staff_data[i]
            clean_entry = []

            # ignore timestamp

            # position
            position_matcher = {"Staff": "staff",
                "Non-Tenured Faculty": "nontenured faculty",
                "Tenured Faculty": "tenured faculty"}
            position = position_matcher[raw_entry[1]]
            clean_entry.append(('position', raw_entry[1], position))

            # race
            race_matcher = {"African American / Black": "black",
                "Asian": "asian", "Hispanic / Latino / Latina": "hispanic",
                "Non-Hispanic White": "white",
                "Pacific Islander / Hawaiian" : "hawaiian", "Not Listed": "not listed"
            }
            race = race_matcher[raw_entry[2]]
            clean_entry.append(('race', raw_entry[2], race))

            # bio gender
            bio_gender_matcher = {"Female": "female", "Male": "male"}
            bio_gender = bio_gender_matcher[raw_entry[3]]
            clean_entry.append(('bio_gender', raw_entry[3], bio_gender))

            # id gender
            id_gender_matcher = {"Man": "male", "Woman": "female",
                "Intersexual": "intersexual", "Transgender": "transgender",
                "Not Listed": "not listed"}
            id_gender = id_gender_matcher[raw_entry[4]]
            clean_entry.append(('id_gender', raw_entry[4], id_gender))

            # sexuality
            sexuality_matcher = {"Asexual": "asexual", "Bisexual": "bisexual",
                "Gay": "gay", "Heterosexual": "heterosexual", "Lesbian": "lesbian",
                "Questioning": "questioning", "Not Listed": "not listed"
            }
            sexuality = sexuality_matcher[raw_entry[5]]
            clean_entry.append(('sexuality', raw_entry[5], sexuality))

            # years at E&H
            years_working_matcher = {"1st year": 1, "2-5": 3.5, "6-10": 8,
                "11-19": 15, "20+": 25
            }
            years_working = years_working_matcher[raw_entry[6]]
            clean_entry.append(('years_working', raw_entry[6], years_working))

            # division
            division_matcher = {"Humanities": "humanities",
                "Life Sciences": "life sciences",
                "Social Sciences": "social sciences", "": None
            }
            division = division_matcher[raw_entry[7]]
            clean_entry.append(('division', raw_entry[7], division))

            # student body diversity perception
            student_body_diversity_perception = diverse_matcher[raw_entry[8]]
            clean_entry.append(("student_body_diversity_perception", raw_entry[8],
                                student_body_diversity_perception))

            # student faculty staff diversity perception
            student_fac_staff_diversity_perception = diverse_matcher[raw_entry[9]]
            clean_entry.append(('student_fac_staff_diversity_perception', raw_entry[9],
                                student_fac_staff_diversity_perception))

            # diversity importance
            diversity_importance = importance_matcher[raw_entry[10]]
            clean_entry.append(('diversity_importance', raw_entry[10], diversity_importance))

            # diversity emphesis
            diversity_emphesis = agreement_matcher[raw_entry[11]]
            clean_entry.append(('', raw_entry[11], diversity_emphesis))

            # experience loop
            categories = (
                'diversity_emphesis', 'race_experience', 'financial_experience',
                'religion_experience', 'gender_experience', 'sexuality_experience',
                'safe_in_buildings', 'safe_walking', 'asking_me_for_help',
                'help_availability', 'student_of_diff_race_seek_help',
                'greek_life_discriminiation', 'non_greek_life_discriminiation',
                'athletics_discrimination', 'non_athletics_discrimination',
                'prc_access'
            )

            number = 11
            for cat in categories:
                raw_val = raw_entry[number]
                clean_val = agreement_matcher[raw_val]
                clean_entry.append((cat, raw_val, clean_val))
                number += 1


            fac_staff_clean_data.append(clean_entry)

        except Exception as e:
            print("\nProcessing failed for entry {}".format(i))
            traceback.print_exc()
            raise(e)

    return fac_staff_clean_data

def main():
    print("Loading fac_staff raw csv.")

    fac_staff_data = []

    with open(settings.fac_staff_raw_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            fac_staff_data.append(row)

    fac_staff_clean_data = clean_fac_staff_data(fac_staff_data)

    print('\nFinished processing {} fac_staff responses.'.format(len(fac_staff_clean_data)))

    # tools.print_first(3, fac_staff_clean_data)

    # deleting old clean data
    if os.path.exists(settings.fac_staff_clean_path):
        print("Deleting old clean data.")
        os.remove(settings.fac_staff_clean_path)
    else:
        print("No old clean data to delete.")

    print("Writing data to: {}".format(settings.fac_staff_clean_path))

    try:
        with open(settings.fac_staff_clean_path, "w") as f:
            f.write(json.dumps(fac_staff_clean_data))
    except Exception as e:
        print("Failed to write clean fac_staff data!")
        raise e


if __name__ == "__main__":
    print("Starting clean_data.py\n")
    main()
    print("\nExiting clean_data.py")
