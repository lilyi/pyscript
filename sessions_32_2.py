# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 15:28:09 2017

@author: Lily
"""

# -*- coding: utf-8 -*-

import argparse
import csv
from googleapiclient.errors import HttpError
from googleapiclient import sample_tools
from oauth2client.client import AccessTokenRefreshError
from oauth2client.service_account import ServiceAccountCredentials

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--stime",
                    help="start time")
parser.add_argument("-e", "--etime", 
                    help="end time")
#parser.add_argument("-c", "--cname", 
#                    help="country name")
args = parser.parse_args()

lan = "/zh-tw/"
pID = "233"

def get_top_keywords(service, profile_id, cname):
    """Executes and returns data from the Core Reporting API.
    This queries the API for the top 25 organic search terms by visits.
    Args:
    service: The service object built by the Google API Python client library.
    profile_id: String The profile ID from which to retrieve analytics data.
    Returns:
    The response returned from the Core Reporting API.
    """
    return service.data().ga().get(
            ids='ga:' + profile_id,
            start_date=args.stime,
            end_date=args.etime,
            metrics='ga:sessions',
            dimensions='ga:date',
            sort="ga:date",
            segment = "sessions::condition::ga:country=@{}".format(cname)
#            filters = "ga:pagePath=@{};ga:pagePath=~/model\.php\?II={}".format(lan, pID)
            ).execute()

def print_results(results):
    """Prints out the results.
    This prints out the profile name, the column headers, and all the rows of
    data.
    Args:
        results: The response returned from the Core Reporting API.
    """
    print()
    print('Profile Name: %s' % results.get('profileInfo').get('profileName'))
    print()
    # Open a file.
    filepath = 'C:\\Users\\Lily\\Documents\\GA\\data'     #change this to your actual file path
    filename = '0324_TVS.csv'#.format(args.cname)         #change this to your actual file name
    f = open(filepath.strip('\\') + '\\' + filename, 'wt')
    # Wrap file with a csv.writer
    writer = csv.writer(f, lineterminator='\n')
    # Write header.
    header = [h['name'][3:] for h in results.get('columnHeaders')] #this takes the column headers and gets rid of ga: prefix
    writer.writerow(header)
    print(''.join('%30s' %h for h in header))
    # Write data table.
    if results.get('rows', []):
        for row in results.get('rows'):
            writer.writerow(row)
            print(''.join('%30s' %r for r in row))
        print('\n')
        print ('Success Data Written to CSV File')
        print ('filepath = ' + filepath)
        print ('filename = '+ filename)
    else:
        print ('No Rows Found')
    # Close the file.
    f.close()

def main():
    clist = ["Australia","Austria","Belgium","Canada","Czechia","Denmark","France","Germany","Greece","Hong Kong","Hungary","India","Iran","Israel","Italy","Japan","Mexico","Netherlands","Norway","Poland","Portugal","Romania","South Africa","South Korea","Spain","Sweden","Switzerland","Taiwan","Thailand","Turkey","United Kingdom","United States"]

    try:
        scopes = ['https://https://www.googleapis.com/auth/analytics']
        ServiceAccountCredentials.from_json_keyfile_name(
                'C:/Users/Lily/Documents/GA/R/key_secrets.json', scopes=scopes)
        service, flags = sample_tools.init("", 
        'analytics', 'v3', __doc__, __file__,
        scope='https://www.googleapis.com/auth/analytics.readonly')
        
        profile_id = '3035421'
        for c in clist:
            results = get_top_keywords(service, profile_id, c)
            #print(results)
            print_results(results)
    except TypeError as error:
        # Handle errors in constructing a query.
        print(('There was an error in constructing your query : %s' % error))
    
    except HttpError as error:
        # Handle API errors.
        print(('Arg, there was an API error : %s : %s' %
               (error.resp.status, error._get_reason())))
    except AccessTokenRefreshError:
        # Handle Auth errors.
        print ('The credentials have been revoked or expired, please re-run '
               'the application to re-authorize')
    
if __name__ == '__main__':
  main()