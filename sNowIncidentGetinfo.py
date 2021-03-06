
# AUTHOR: Created by John Singer, 4.13.15
# Any usage must include giving credit to the above author,
# but there is no warranty, express or implied for the use of this code.
# If problems are encountered, your 'best bet' is to ask for help
# on the bigfix forum (http://forum.bigfix.com).
#
import sys
import requests
from argparse import ArgumentParser
from time import strftime
import xml.etree.ElementTree as E

usage = """sNowIncidentGetinfo.py <incident#> [options]

Get ServiceNow Incident information, based on commandline Incident#
The first parameter, the ID of the incident-in-question
    must currently exist within SN

Options:
  --user USERNAME             IEM console-login USERNAME
                               (no default)
  --password PASSWORD         IEM console-login PASSWORD for above user
                               (no default)
  -h, --help                   Print this help message and exit


Examples:

    sNowIncidentGetinfo INC0000055 -u Admin -p A1rb0rn3

"""
__author__ = 'singerj'
el = ''

def editTargetString(sourceStr, lookingFor, replaceStr):
    '''Replaces the lookingFor part of the sourceStr, with replaceStr'''
    newStr = sourceStr.replace(lookingFor, replaceStr)
    return newStr

# When invoked as the main program, figure out the cmdline parms, assign them to variables, handle usage & help, and go get the
#      prototype XML & names of the group-members from the cmdline filename.
if __name__ == '__main__':
    try:
        parser = ArgumentParser(add_help=False, usage=usage)
        parser.add_argument('incident_name')
        parser.add_argument('-u', '--user')
        parser.add_argument('-p', '--password')

        if '-h' in sys.argv or '--help' in sys.argv:
          print(usage)
          exit()

        args = parser.parse_args()

        if args.incident_name == None:
            exit(status=0)
        incident_name = args.incident_name

        if args.user: user = args.user
        if args.password: password = args.password

# Now, try 'tapping into' the ServiceNow instance
        snUrlBase = 'https://mjones1.service-now.com'

        headers = {"Accept":"application/json"}
        r = requests.get(snUrlBase+'/api/now/table/incident?sysparm_limit=10',auth=(user,password),headers=headers)

        if r.status_code != 200:
            print('sNowIncidentGetinfo ERROR -- Status: ', r.status_code, 'Headers:', r.headers, 'Error Response:', r.json())
            exit()

        else:
            print('Status:', r.status_code, 'Headers:', r.headers, 'Response:', r.json())
            print('Cookies:', r.cookies)
            print('\nAnd now; time for something REALLY special...')
            for record in r.json()['result']:
                print ('\n', record)

# Handle any exceptions, printing out error code
    except SystemExit:
        pass
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise
    finally:
        print("\n")

