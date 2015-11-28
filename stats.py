import json

import correlation
import category
import tools
import settings

from matplotlib.backends.backend_pdf import PdfPages


def process_data(data_type, stats, highlights):
    print("Starting student data processing.")

    all_pdf_path, highlight_pdf_path = (None,None)
    question_types, demographic_questions, opinion_questions = (None,)*3
    demographic_save_file = None


    if data_type == "student":
        question_types = settings.student_question_types
        all_pdf_path = settings.student_stats_path
        highlight_pdf_path = settings.student_stats_highlight_path
        demographic_questions = settings.student_demographic_questions
        opinion_questions = settings.student_opinion_questions
        demographic_save_file = settings.student_categories_highlight_path


    elif data_type == "fac_staff":
        question_types = settings.fac_staff_question_types
        all_pdf_path = settings.fac_staff_stats_path
        highlight_pdf_path = settings.fac_staff_stats_highlight_path
        demographic_questions = settings.fac_staff_demographics_questions
        opinion_questions = settings.fac_staff_opinion_questions
        demographic_save_file = settings.fac_staff_categories_highlight_path

    data = load_data(data_type)

    # correlation calculations
    if stats in ["correlation", "all"]:
        correlation_to_run = correlation.gen_num_correlations(data, question_types)
        correlation_results = correlation.run_num_correlations(correlation_to_run, data)
        interesting_correlations = correlation.find_interesting_correlations(
                                                    correlation_results, data)
        correlation.print_interesting_correlations(interesting_correlations, data)


        # plot all correlations
        if not highlights:
            all_pdf = PdfPages(all_pdf_path)
            correlation.plot_correlations(correlation_results, data, all_pdf)
            all_pdf.close()

        # plot highlight correlations
        highlight_pdf = PdfPages(highlight_pdf_path)
        correlation.plot_correlations(interesting_correlations, data, highlight_pdf)
        highlight_pdf.close()

        print("Done with {} correlation stats.".format(data_type))

    # category calculations
    if stats in ["category", "all"]:
        print("Staring demographic processing for {} data.".format(data_type))
        base_demographic = category.base_demographic(data, demographic_questions)
        answer_response_lists = category.generate_answer_response_lists(
                                data, opinion_questions)
        opinion_demographic_dict = category.generate_demographic_for_response_lists(
                                                        answer_response_lists, data)

        opinion_demographic_diff_dict = category.calc_demographic_diff(
                                        base_demographic, opinion_demographic_dict)

        interesting_demographic_changes = category.find_interesting_demographic_changes(
                                                    opinion_demographic_diff_dict)

        category.save_interesting_demographics_changes_to_file(
                    interesting_demographic_changes, demographic_save_file
        )


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
