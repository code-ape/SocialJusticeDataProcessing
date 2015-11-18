import csv, json

import settings
import tools

generic_matcher_1 = {
    "a highly": 3, "a notably": 2, "a minorly": 1, "not at all a": 0
}

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

            # social media effectiveness
            social_media_effectiveness_matcher = {
                "always effective": 2, "usually effective": 1,
                "usually ineffective": -1, "always ineffective": -2
            }
            social_media_effectiveness = social_media_effectiveness_matcher[raw_entry[10]]
            clean_entry.append(("social_media_effectiveness", raw_entry[10],
                                social_media_effectiveness))

            # skipping honors specific question because it was covered in
            # communities question

            # honors color environment
            honors_color_comfort_matcher = {
                "very comfortable": 2, "somewhat comfortable": 1,
                "somewhat uncomfortable": -1, "very uncomfortable": -2,
                "": None
            }
            honors_color_comfort = honors_color_comfort_matcher[raw_entry[12]]
            clean_entry.append(("honors_color_comfort", raw_entry[12], honors_color_comfort))

            # honors diversity
            honors_diversity_matcher = {
                "actively promotes": 2,
                "somewhat promotes": 1,
                "fails to promote": 0,
                "": None
            }
            honors_diversity = honors_diversity_matcher[raw_entry[13]]
            clean_entry.append(("honors_diversity", raw_entry[13], honors_diversity))

            # discrimination
            experienced_discrim_matcher = {"have": True, "have not": False}
            experienced_discrim = experienced_discrim_matcher[raw_entry[14]]
            clean_entry.append(("experienced_discrim", raw_entry[14], experienced_discrim))

            # discrimination demographic reasons
            discrim_demographic = tools.parse_discrim_demographic(raw_entry[15])
            clean_entry.append(("discrim_demographic", raw_entry[15], discrim_demographic))

            # discrimination due to involvement with selected groups
            discrim_involvement = tools.parse_discrim_involvement(raw_entry[16])
            clean_entry.append(("discrim_involvement", raw_entry[16], discrim_involvement))

            # discrimination due to LACK of involvement with selected groups
            discrim_lack_involvement = tools.parse_discrim_involvement(raw_entry[17])
            clean_entry.append(("discrim_lack_involvement", raw_entry[17], discrim_lack_involvement))

            # how diverse campus is
            campus_diversity = generic_matcher_1[raw_entry[18]]
            clean_entry.append(('campus_diversity', raw_entry[18], campus_diversity))

            # campus diveristy needs
            campus_diversity_needs_matcher = {
                "needs a lot more": 2, "needs some more": 1,
                "has just the right amount of": 0, "needs some less": -1,
                "needs a lot less": -2
            }
            campus_diversity_needs = campus_diversity_needs_matcher[raw_entry[19]]
            clean_entry.append(('campus_diversity_needs', raw_entry[19], campus_diversity_needs))

            # groups discriminated against on campus
            groups_discrim_against = tools.parse_groups(raw_entry[20])
            clean_entry.append(('groups_discrim_against', raw_entry[20], groups_discrim_against))

            # groups favored on campus
            groups_favored = tools.parse_groups(raw_entry[21])
            clean_entry.append(('groups_favored', raw_entry[21], groups_favored))

            # college favortism
            college_favortism_matcher = {"does": True, "does not": False}
            college_favortism = college_favortism_matcher[raw_entry[22]]
            clean_entry.append(('college_favortism', raw_entry[22], college_favortism))

            # satisfied with living conditions
            living_satisfied_matcher = {
                "very satisfied": 2, "decently satisfied": 1,
                "minorly unsatisfied": -1, "not at all satisfied": -2
            }
            living_satisfied = living_satisfied_matcher[raw_entry[23]]
            clean_entry.append(('living_satisfied', raw_entry[23], living_satisfied))

            # living diversity
            living_diversity = generic_matcher_1[raw_entry[24]]
            clean_entry.append(('living_diversity', raw_entry[24], living_diversity))

            student_clean_data.append(clean_entry)



        except Exception as e:
            print("\nProcessing failed for entry {}".format(i))
            raise(e)


    print('\nFinsihed processing {} students'.format(len(student_clean_data)))

    tools.print_first(3, student_clean_data)




if __name__ == "__main__":
    print("Starting clean_data.py\n")
    main()
    print("\nExiting clean_data.py")
