import argparse

import settings
import clean_fac_staff_data
import clean_student_data
import stats

def main():
    parser = argparse.ArgumentParser(description="Takes clean data and creates PDF results")
    parser.add_argument('data', metavar='D', type=str, nargs=1,
                        choices=["student", "fac_staff", "both"],
                        help='fac_staff, student, both')
    parser.add_argument('action', metavar='A', type=str, nargs=1,
                        choices=["clean", "stats", "full_process"],
                        help='clean, stats, full_process')
    parser.add_argument('--stats', metavar='S', type=str, nargs=1,
                        choices=['correlation', 'category', 'all'],
                        required=False,
                        default="both",
                        help="correlation, category, all")
    parser.add_argument('--highlights', help='if choosen will save only significant results',
                            action='store_true')

    args = parser.parse_args()


    process_student = args.data[0] in ["student", "both"]
    process_fac_staff = args.data[0] in ["fac_staff", "both"]

    action_clean = args.action[0] in ["clean", "full_process"]
    action_stats = args.action[0] in ["stats", "full_process"]

    highlights = args.highlights
    stats_arg = args.stats[0]

    if action_clean:
        if process_student:
            clean_student_data.main()
        if process_fac_staff:
            clean_fac_staff_data.main()

    if action_stats:
        if process_student:
            stats.process_data("student", stats_arg, highlights)
        if process_fac_staff:
            stats.process_data("fac_staff", stats_arg, highlights)

if __name__ == "__main__":
    print("Starting run_stats.py\n")
    main()
    print("\nEnding run_stats.py")
