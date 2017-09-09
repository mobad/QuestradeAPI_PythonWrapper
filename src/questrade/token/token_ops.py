'''Token Operations

@summary: A simple module that provides Token operations on a locally stored token.

@note: To store a new token file locally, call function get_token(new=True).  This
    will call a helper module to launch a browser and allow the user to login and
    authorize this app to store a new token file.

@note: The locally stored token is assumed to be located in the user's home directory
    under the filename 'questrade_token.json'.

    Windows:    C:\\Users\\<username>\\questrade_token.json
    OS X:       /Users/<username>/questrade_token.json
    Linux:      /home/<username>/questrade_token.json

@copyright: 2016
@author: Peter Cinat
@license: Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
'''

import os
import json
import time
import webbrowser
import questrade.browser.wrapper as browser


def get_token(new=False):
    if new == True:
        webbrowser.get('firefox').open_new_tab('https://login.questrade.com/Signin.aspx?ReturnUrl=%2fAPIAccess%2f')
    else:
        try:
            with open(os.path.join(os.path.expanduser('~'), '.questrade_token.json')) as f:
                jsonStr = f.read()
                token = json.loads(jsonStr)
        except IOError:
            token = None

    if not is_valid_token(token):
        token = None

    return token


def refresh_token(refresh_token):
    token = browser.refresh_token(refresh_token)
    return token


def delete_token():
    os.remove(os.path.join(os.path.expanduser('~'), '.questrade_token.json'))


def get_token_value(key):
    token = get_token()

    if token == None:
        return None

    try:
        value = token[key]
    except KeyError:
        value = None

    return value


def get_access_token(token=None):
    if token == None:
        return get_token_value('access_token')
    else:
        return token['access_token']


def get_refresh_token(token=None):
    if token == None:
        return get_token_value('refresh_token')
    else:
        return token['refresh_token']


def get_api_server(token=None):
    if token == None:
        return get_token_value('api_server')
    else:
        return token['api_server']


def get_token_type(token=None):
    if token == None:
        return get_token_value('token_type')
    else:
        return token['token_type']


def is_valid_token(token):
    if token == None:
        return False

    is_valid = False
    try:
        token['access_token']
        token['refresh_token']
        token['api_server']
        token['token_type']
        is_valid = True
    except KeyError:
        is_valid = False
    finally:
        return is_valid


def is_token_expired(token):
    if token == None:
        expires_in = get_token_value('expires_in')
    else:
        expires_in = token['expires_in']

    if expires_in == None:
        return True
    else:
        last_modified = os.stat(os.path.join(os.path.expanduser('~'), '.questrade_token.json')).st_mtime
        return time.time() > (last_modified + expires_in)


def print_token(token):
    print(json.dumps(token))



if __name__ == "__main__":
    token = get_token()
    print_token(token)
