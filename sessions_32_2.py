# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 15:28:09 2017

@author: Lily
"""

# -*- coding: utf-8 -*-

import argparse
import csv
import os, httplib2, webbrowser
from googleapiclient.errors import HttpError
from oauth2client.client import AccessTokenRefreshError
from oauth2client import client
from apiclient import discovery

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

file_path = os.path.dirname(__file__)

def acquire_oauth2_credentials():
    """
    Flows through OAuth 2.0 authorization process for credentials.
    Create credentials file as cre.json
    """
    if os.path.isfile("%s/cre.json" % file_path):
        f = open("%s/cre.json" % file_path, "r")
        credentials = client.OAuth2Credentials.from_json(f.read())
        f.close()
    else:    
        flow = client.flow_from_clientsecrets(
            "%s/client_secrets.json" % file_path,
            scope='https://www.googleapis.com/auth/analytics.readonly',
            redirect_uri='urn:ietf:wg:oauth:2.0:oob')
        auth_uri = flow.step1_get_authorize_url()
        webbrowser.open(auth_uri)
        auth_code = input('Enter the authentication code: ')
        credentials = flow.step2_exchange(auth_code)
        write_credentials("%s/cre.json" % file_path, credentials)
    return credentials

def write_credentials(fname, credentials):
    """Writes credentials as JSON to file.""" 
    f = open(fname, "w")
    f.write(credentials.to_json())
    f.close()

def create_service_object(credentials):
    """Creates Service object for credentials."""
    http_auth = httplib2.Http()
    http_auth = credentials.authorize(http_auth)
    service = discovery.build('analytics', 'v3', http=http_auth)
    return service

def get_top_keywords(credentials, profile_id, cname):
    try:
        service = create_service_object(credentials) #The service object built by the Google API Python client library.
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

def print_results(results, cname):
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
    filepath = 'C:\\Users\\Lily\\Documents\\GA\\data\\total_sessions_32'     #change this to your actual file path
    filename = '{}.csv'.format(cname)         #change this to your actual file name
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
        credentials = acquire_oauth2_credentials()
        profile_id = '3035421'
        for c in clist:
            results = get_top_keywords(credentials, profile_id, c)
            #print(results)
            print_results(results, c)
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