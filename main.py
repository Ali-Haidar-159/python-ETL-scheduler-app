import argparse

from vrs_analytics.cron.holibob_cron import run
import config.global_config as gc

def main():

    parser = argparse.ArgumentParser(
        description="This is filter by date for API call."
    )

    parser.add_argument(
        "-start-date","--start", metavar="start_date" ,
        required=True , help="Give a start date like : 2025-03-01"
    )

    parser.add_argument(
        "-end-date","--end", metavar="end_date" ,
        required=True , help="Give a end date like : 2026-03-01"
    )


    # parser.add_argument(
    #     "-cron","--cron", metavar="cron_name" ,
    #     required=True , help="Give a cron name like booking/holibob_cron"
    # )

    args = parser.parse_args()

    gc.START_DATES = args.start
    gc.END_DATES = args.end
    # cron = args.cron

    # print(start_date)
    # print(end_date)
    # print(cron)



    run()


if __name__ == "__main__":
    main()
