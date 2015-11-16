import csv, json

import settings
import tools

def main():
    print("Loading student raw csv.")

    student_raw_data = []

    with open(settings.student_raw_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            student_raw_data.append(row)

    student_clean_key = []
    student_clean_data = []

    # strip initial entry that is the question each answer coorelates to
    for i in xrange(1, len(student_raw_data)):
        try:
            print('.'),
            raw_entry = student_raw_data[i]
            clean_entry = []

            # ignore timestamp

            # age
            age_number_matcher = {
                "under 18": 17, "18": 18, "19": 19, "20": 20, "21": 21, "22": 22,
                "23": 23, "24 to 30": 27, "31 to 40": 35, "over 40": 45
            }
            age_number = age_number_matcher[raw_entry[1]]
            clean_entry.append(('age', raw_entry[1], age_number))

            # gender
            clean_entry.append(('gender', raw_entry[2], None))

            # grad vs undergrad student
            student_level_matcher = {"an undergrad": "undergrad", "a grad": "grad"}
            student_level = student_level_matcher[raw_entry[3]]
            clean_entry.append(('student_level', raw_entry[3], student_level))

            # college beginning
            transfer_matcher = {"started college at": False, "transfered to": True}
            transfer = transfer_matcher[raw_entry[4]]
            clean_entry.append(('transfer', raw_entry[4], transfer))

            # years at college
            year_number_matcher = {
                "first":1, "second":2, "third":3, "fourth":4,
                "fifth or greater":5
            }
            year_number = year_number_matcher[raw_entry[5]]
            clean_entry.append(('years_at_college', raw_entry[5], year_number))

            # race
            clean_entry.append(('race', raw_entry[6], None))

            # LGBT
            lgbt_matcher = {"do": True, "do not": False}
            lgbt = lgbt_matcher[raw_entry[7]]
            clean_entry.append(('lgbt', raw_entry[7], lgbt))

            # communities
            communities = tools.parse_communities(raw_entry[8])
            clean_entry.append(('communities', raw_entry[8], communities))


            # living location
            living_location_matcher = {
                "off campus": "off campus", "in Mawa or Stuart": "mawa / stuart",
                "in Carriger, Matthews, or Hillman": "carriger / matthews / hillman",
                "in Elm, Hickory, or Sullins": "elm / hickory / sullins",
                "in the Village": "village"
            }
            living_location = living_location_matcher[raw_entry[9]]
            clean_entry.append(("living_location", raw_entry[9], living_location))


            student_clean_data.append(clean_entry)
        except Exception as e:
            print("\nProcessing failed for entry {}".format(i))
            raise(e)


    print('\nFinsihed processing {} students'.format(len(student_clean_data)))

    tools.print_first(5, student_clean_data)






if __name__ == "__main__":
    print("Starting clean_data.py\n")
    main()
    print("\nExiting clean_data.py")
