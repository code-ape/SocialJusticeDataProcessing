import json
import sys

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from scipy import stats

import settings
import tools


def process_data(data_type, stats, test):
    print("Starting student data processing.")

    all_pdf_path, highlight_pdf_path = (None,None)
    question_types = None


    if data_type == "student":
        question_types = tools.get_student_question_types()

        if not test:
            all_pdf_path = settings.student_stats_path
            highlight_pdf_path = settings.student_stats_highlight_path
        else:
            all_pdf_path = "student_all_test.pdf"
            highlight_pdf = "student_highlight_test.pdf"

    elif data_type == "fac_staff":
        question_types = tools.get_fac_staff_question_types()

        if not test:
            all_pdf_path = settings.fac_staff_stats_path
            highlight_pdf_path = settings.fac_staff_stats_highlight_path
        else:
            all_pdf_path = "fac_staff_all_test.pdf"
            highlight_pdf = "fac_staff_highlight_test.pdf"


    all_pdf = PdfPages(all_pdf_path)
    highlight_pdf = PdfPages(highlight_pdf_path)

    data = load_data(data_type)

    correlation_to_run = gen_num_correlations(data, question_types)
    correlation_results = run_num_correlations(correlation_to_run, data)
    if test:
        correlation_results = correlation_results[:10]
    interesting_correlations = find_interesting_correlations(correlation_results, data)
    print_interesting_correlations(interesting_correlations, data)

    # plot all correlations
    if stats in ["complete", "both"]:
        plot_correlations(correlation_results, data, all_pdf)

    # plot highlight correlations
    if stats in ["highlight", "both"]:
        plot_correlations(interesting_correlations, data, highlight_pdf)

    print("Closing {} plots pdfs.".format(data_type))
    all_pdf.close()
    highlight_pdf.close()

    print("Ending {} data processing.".format(data_type))



def load_data(data_type):
    print("Loading {} data.".format(data_type))
    data = None
    file_path = None
    if data_type == "student":
        file_path = settings.student_clean_path
    elif data_type == "fac_staff":
        file_path = settings.fac_staff_clean_path
    print("Opening: {}".format(file_path))
    with open(file_path, "r") as f:
        print("Reading JSON into memory.")
        data = json.loads(f.read())
    print("Loaded {} {} records.".format(len(data), data_type))
    print("Done loading {} data.".format(data_type))
    return data


def gen_num_correlations(data, question_types):
    numerical_questions = tools.get_num_questions(question_types)

    response_dict = {}

    for question in numerical_questions:
        response_dict[question] = tools.get_responses_to_number(question, data)

    num_numerical_questions = len(numerical_questions)
    total_correlations = sum(xrange(1,num_numerical_questions))
    print("There are {} numerical questions.".format(num_numerical_questions))
    print("Thus {} correlation tests will be run.".format(total_correlations))

    print("Building correlations to run.")
    correlations_to_run = []
    count = 0
    for question in numerical_questions:
        linking_questions = xrange(count+1, len(numerical_questions))
        for i in linking_questions:
            correlations_to_run.append((question, numerical_questions[i]))
        count+=1

    print("Created {} tests to run.".format(len(correlations_to_run)))
    assert(len(correlations_to_run) == total_correlations)
    return correlations_to_run

def run_num_correlations(question_pairs, data):
    print("Running correlations.")
    correlation_results = []
    for t in question_pairs:
        full_response_entries = tools.get_responses_to_numbers(t, data)
        answers_1, answers_2 = tools.extract_vals_from_responses(*full_response_entries)
        invalid_1, invalid_2 = tools.get_indexes_of_invalid_repsonse_types(
                [int], answers_1, answers_2
        )
        invalid_all = tools.merge_invalid_indexes(invalid_1, invalid_2)

        final_answers_1, final_answers_2 = tools.remove_entries_at_indexes(
            invalid_all, answers_1, answers_2)

        # print(answers_1, answers_2)
        # print(final_answers_1, final_answers_2)
        # print(len(answers_1), len(answers_2))
        # print(len(final_answers_1), len(final_answers_2))

        slope, intercept, r_value, p_value, std_err = stats.linregress(
            final_answers_1, final_answers_2
        )

        r_squared = r_value**2
        result = {"questions": t, "slope": slope, "intercept": intercept,
            "r_value": r_value, "p_value": p_value, "std_err": std_err,
            "r_squared": r_squared
        }
        correlation_results.append(result)
    print("Finished running correlations.")
    return correlation_results

def find_interesting_correlations(correlation_results, data):
    print("\nBeginning search for interesting correlations.")
    print("Searching through {} results.".format(len(correlation_results)))
    r_squared_threshold = 0.5
    print("R Squared threshold = {}".format(r_squared_threshold))

    interesting_results = []
    for result in correlation_results:
        if result["r_squared"] > r_squared_threshold:
            interesting_results.append(result)

    print("Finished Searching.\n")
    return interesting_results


def print_interesting_correlations(interesting_correlations, data):
    for result in interesting_correlations:
        num_1, num_2 = result["questions"]
        title_1, title_2 = (tools.get_question_title(num_1, data),
                            tools.get_question_title(num_2, data))
        print(("Notable correlation between:\n" +
            "\t'{}'({})\n" +
            "\t'{}'({})\n" +
            "\tr_squared = {:.3f}")
            .format(
            title_1, num_1, title_2, num_2, result["r_squared"]
        ))
        print("\n")

def plot_correlations(results, data, pdf):
    print("Saving {} result plots to pdf.".format(len(results)))
    for result in results:
        print('.'),
        sys.stdout.flush()

        q1, q2 = result['questions']
        title_1 = tools.get_question_title(q1, data)
        title_2 = tools.get_question_title(q2, data)

        x_raw = tools.get_responses_to_number(q1, data)
        y_raw = tools.get_responses_to_number(q2, data)
        x,y = tools.extract_vals_from_responses(x_raw, y_raw)
        invalid_x, invalid_y = tools.get_indexes_of_invalid_repsonse_types(
                [int], x, y
        )
        invalid_all = tools.merge_invalid_indexes(invalid_x, invalid_y)

        x, y = tools.remove_entries_at_indexes(invalid_all, x, y)
        # Calculate the point density
        xy = np.vstack([x,y])
        try:
            z = stats.gaussian_kde(xy)(xy)
        except Exception as e:
            print(xy)
            raise e
        size = 5000*z
        final_size = []
        for s in size:
            final_size.append(max(s,60))


        # Calculate axis numbers
        x_range = (min(x)-1, max(x)+1)
        y_range = (min(y)-1, max(y)+1)

        # generate data for best fit line
        slope = result['slope']
        intercept = result['intercept']
        x_fit_points = x_range
        y_fit_points = (x_range[0]*slope + intercept, x_range[1]*slope + intercept)

        fig = plt.figure()
        ax = fig.add_subplot(1,1,1)

        ax.set_title("{} vs {}\nr_squared = {:.4f}".format(title_1, title_2, result['r_squared']))

        ax.set_xlabel("{} (Q{})".format(title_1, q1))
        ax.set_ylabel("{} (Q{})".format(title_2, q2))

        ax.scatter(x, y, c=z, s=final_size, edgecolor='')
        ax.plot(x_fit_points, y_fit_points, '-')

        pdf.savefig(fig)
        plt.close(fig)
    print("\nDone saving plots to pdf.\n")
