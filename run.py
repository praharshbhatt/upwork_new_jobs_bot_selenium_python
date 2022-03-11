# main run file
from selenium_driver.selenium_driver import *
import time as time
import pprint

def run():
    pp = pprint.PrettyPrinter(depth=6)
    
    while True:
        
        print('Starting the bot...')
        
        # This dict stores all the loaded jobs
        loaded_jobs = {}
        
        # Initialize SeleniumDriver
        sd = SeleniumDriver()

        # Open the webpage
        # Enter your search url below
        sd.open_webpage('https://www.upwork.com/search/jobs/?client_hires=1-9,10-&contractor_tier=1,2,3&from_recent_search=true&proposals=0-4&q=flutter&sort=recency')
        updated_jobs = sd.list_all_results()
        
        # Get the new jobs
        newly_added_jobs = []
        for updated_job in updated_jobs.values():
            if (updated_job['link'] not in loaded_jobs.keys()):
                newly_added_jobs.append(updated_job)
                loaded_jobs[updated_job['link']] = updated_job
        
        # Prints the newly added jobs
        if (newly_added_jobs):
            print("Loaded updated jobs:")
            pp.pprint(newly_added_jobs)
        else:
            print("No new jobs found")
        
        # Sleep for 5 minutes
        time.sleep(5 * 60)


if __name__ == '__main__':
    run()
