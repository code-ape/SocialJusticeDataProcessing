import json

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

import settings
import tools

def main():
    print("Initiating fac / staff data processing...")
    process_fac_staff_data()

def process_fac_staff_data():
    print("Starting fac / staff data processing.")

    fac_staff_plot = plt
    data = load_fac_staff_data()

    coorelation_to_run = gen_num_coorelations(data)
    coorelation_results = run_num_coorelations(coorelation_to_run, data)
    interesting_coorelations = find_interesting_coorelations(coorelation_results, data)
    print_interesting_coorelations(interesting_coorelations, data)
    plot_coorelations(interesting_coorelations, data, fac_staff_plot)

    print("Showing plotted data")
    plt.show()

    print("Ending fac / staff data processing.")


def load_fac_staff_data():
    print("Loading fac / staff data.")
    data = None
    print("Opening: {}".format(settings.fac_staff_clean_path))
    with open(settings.fac_staff_clean_path, "r") as f:
        print("Reading JSON into memory.")
        data = json.loads(f.read())
    print("Loaded {} fac / staff records.".format(len(data)))
    print("Done loading fac / staff data.")
    return data


def gen_num_coorelations(data):
    question_types = tools.get_fac_staff_question_types()
    numerical_questions = tools.get_num_questions(question_types)

    response_dict = {}

    for question in numerical_questions:
        response_dict[question] = tools.get_responses_to_number(question, data)

    num_numerical_questions = len(numerical_questions)
    total_coorelations = sum(xrange(1,num_numerical_questions))
    print("There are {} numerical questions.".format(num_numerical_questions))
    print("Thus {} coorelation tests will be run.".format(total_coorelations))

    print("Building coorelations to run.")
    coorelations_to_run = []
    count = 0
    for question in numerical_questions:
        linking_questions = xrange(count+1, len(numerical_questions))
        for i in linking_questions:
            coorelations_to_run.append((question, numerical_questions[i]))
        count+=1

    print("Created {} tests to run.".format(len(coorelations_to_run)))
    assert(len(coorelations_to_run) == total_coorelations)
    return coorelations_to_run

def run_num_coorelations(question_pairs, data):
    print("Running coorelations.")
    coorelation_results = []
    for t in question_pairs:
        full_response_entries = tools.get_responses_to_numbers(t, data)
        answers_1, answers_2 = tools.turn_responses_into_values(*full_response_entries)
        slope, intercept, r_value, p_value, std_err = stats.linregress(
            answers_1, answers_2
        )
        r_squared = r_value**2
        result = {"questions": t, "slope": slope, "intercept": intercept,
            "r_value": r_value, "p_value": p_value, "std_err": std_err,
            "r_squared": r_squared
        }
        coorelation_results.append(result)
    print("Finished running coorelations.")
    return coorelation_results

def find_interesting_coorelations(coorelation_results, data):
    print("\nBeginning search for interesting coorelations.")
    print("Searching through {} results.".format(len(coorelation_results)))
    r_squared_threshold = 0.5
    print("R Squared threshold = {}".format(r_squared_threshold))

    interesting_results = []
    for result in coorelation_results:
        if result["r_squared"] > r_squared_threshold:
            interesting_results.append(result)

    print("Finished Searching.\n")
    return interesting_results


def print_interesting_coorelations(interesting_coorelations, data):
    for result in interesting_coorelations:
        num_1, num_2 = result["questions"]
        title_1, title_2 = (tools.get_question_title(num_1, data),
                            tools.get_question_title(num_2, data))
        print(("Notable coorelation between:\n" +
            "\t'{}'({})\n" +
            "\t'{}'({})\n" +
            "\tr_squared = {:.3f}")
            .format(
            title_1, num_1, title_2, num_2, result["r_squared"]
        ))

def plot_coorelations(results, data, plot):
    for result in results:
        q1, q2 = result['questions']
        x_raw = tools.get_responses_to_number(q1, data)
        y_raw = tools.get_responses_to_number(q2, data)
        x = tools.turn_responses_into_values(x_raw)
        y = tools.turn_responses_into_values(y_raw)

        # Calculate the point density
        xy = np.vstack([x,y])
        z = stats.gaussian_kde(xy)(xy)

        fig, ax = plot.subplots()
        ax.scatter(x, y, c=z, s=100, edgecolor='')

    return plot


if __name__ == "__main__":
    print("Starting run_stats.py\n")
    main()
    print("\nEnding run_stats.py")
