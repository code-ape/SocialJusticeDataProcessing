import json

import correlation
import tools
import settings

from matplotlib.backends.backend_pdf import PdfPages


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

    correlation_to_run = correlation.gen_num_correlations(data, question_types)
    correlation_results = correlation.run_num_correlations(correlation_to_run, data)
    if test:
        correlation_results = correlation_results[:10]
    interesting_correlations = correlation.find_interesting_correlations(
                                                correlation_results, data)
    correlation.print_interesting_correlations(interesting_correlations, data)

    # plot all correlations
    if stats in ["complete", "both"]:
        correlation.plot_correlations(correlation_results, data, all_pdf)

    # plot highlight correlations
    if stats in ["highlight", "both"]:
        correlation.plot_correlations(interesting_correlations, data, highlight_pdf)

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
