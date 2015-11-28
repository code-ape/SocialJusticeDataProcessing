import tools
import settings

def base_demographic(data, demographic_questions):
    breakdowns = {}
    for question_num in demographic_questions:
        responses = tools.get_responses_to_number(question_num, data)
        title = tools.get_question_title(question_num, data)
        values = tools.extract_vals_from_responses(responses)[0]

        breakdown = create_breakdown(values)

        breakdowns[title] = breakdown

    return breakdowns

def generate_answer_response_lists(data, opinion_questions):
    print("Generating answer response list.")
    answer_response_dict = {}
    for question_num in opinion_questions:
        responses = tools.get_responses_to_number(question_num, data)
        values = tools.extract_vals_from_responses(responses, data)[0]
        title = tools.get_question_title(question_num, data)

        index_breakdown = create_index_breakdown(values)
        answer_response_dict[title] = index_breakdown
    print("Done generating answer response list.")
    return answer_response_dict


def generate_demographic_for_response_lists(answer_response_lists, data):
    count = 0
    question_dict = {}
    for title, response_dict in answer_response_lists.iteritems():
        question_num = tools.get_question_num_with_title(title, data)
        answer_breakdown_dict = {}
        for response_val, response_nums in response_dict.iteritems():
            responses = []
            for response_num in response_nums:
                responses.append(data[response_num])

            breakdowns = base_demographic(responses, settings.student_demographic_questions)
            count += len(breakdowns)
            answer_breakdown_dict[response_val] = breakdowns

        question_dict[title] = answer_breakdown_dict
    print("generate_demographic_for_response_lists did {} breakdowns.".format(count))
    return question_dict


def calc_demographic_diff(base_demographic, opinion_demographic_dict):
    opinion_demographic_diff_dict = {}
    for question_name, answer_dict in opinion_demographic_dict.iteritems():
        answer_diff_dict = {}
        for choice, demographic in answer_dict.iteritems():
            answer_diff_dict[choice] = create_demographic_diff(base_demographic, demographic)
        opinion_demographic_diff_dict[question_name] = answer_diff_dict
    return opinion_demographic_diff_dict


def find_interesting_demographic_changes(opinion_demographic_diff_dict):
    interesting_demographic_changes = []
    threshold = 0.3
    counter = 0
    for question_name, answer_dict in opinion_demographic_diff_dict.iteritems():
        for choice, demographic in answer_dict.iteritems():
            for title, breakdown in demographic.iteritems():
                for answer, nums in breakdown.iteritems():
                    percent_shift = nums["percent_shift"]
                    if percent_shift > 25 or percent_shift < -25:
                        interesting_demographic_changes.append({
                            "question": question_name,
                            "question_choice": choice,
                            "demographic_title": title,
                            "demographic_answer": answer,
                            "percent_shift": percent_shift
                        })
                        counter += 1

    print("Found {} interesting results".format(counter))
    return interesting_demographic_changes


def save_interesting_demographics_changes_to_file(interesting_demographic_changes, path):
    print("Saving {} interesting demographic change entries to: {}".format(
            len(interesting_demographic_changes), path
    ))
    with open(path, "w") as f:
        for entry in interesting_demographic_changes:
            f.write("Question: {}\n".format(entry["question"]))
            f.write("Choice: {}\n".format(entry["question_choice"]))
            f.write("Demographic Category: {}\n".format(entry["demographic_title"]))
            f.write("Demographic: {}\n".format(entry["demographic_answer"]))
            f.write("Shift: {}\n\n\n".format(entry["percent_shift"]))
    print("Done saving entries.")


def print_breakdown(title, breakdown):
    print("\n\nBreakdown for {}".format(title))
    for val, nums in breakdown.iteritems():
        print("{}: {}, {:.1f}%".format(val, nums['number'], nums['percentage']))


def create_breakdown(values):
    answer_dict = {}

    # really hacky way of handling answers with where multiple
    # options could be choosen
    for val in values:
        choices = None
        if not isinstance(val, list):
            choices = [val]
        else:
            choices = val
        for choice in choices:
            if choice not in answer_dict:
                answer_dict[choice] = 0
            answer_dict[choice] += 1

    breakdown_dict = {}
    total_values = float(len(values))
    for val, num in answer_dict.iteritems():
        breakdown_dict[val] = {"number": num, "percentage": 100*num/total_values}

    return breakdown_dict

def create_index_breakdown(values):
    breakdown = {}
    count = 0
    for val in values:
        choices = None
        if not isinstance(val, list):
            choices = [val]
        else:
            choices = val
        for choice in choices:
            if choice not in breakdown:
                breakdown[choice] = []
            breakdown[choice].append(count)
        count+=1
    return breakdown


def create_demographic_diff(base_demographic, contrast_demographic):
    demographic_diff = {}
    for title, breakdown in base_demographic.iteritems():
        contrast_breakdown = contrast_demographic[title]
        breakdown_diff = {}
        for answer, nums in breakdown.iteritems():
            contrast_nums = None
            if answer in contrast_breakdown:
                contrast_nums = contrast_breakdown[answer]
            else:
                contrast_nums = {"percentage": 0}
            shift = contrast_nums["percentage"] - nums["percentage"]
            breakdown_diff[answer] = {
                "percent_shift": shift
            }

        demographic_diff[title] = breakdown_diff
    return demographic_diff
