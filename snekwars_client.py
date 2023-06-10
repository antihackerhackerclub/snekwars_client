###############################################################################
# SnekWars Client
# @0xAHHC
###############################################################################
import requests, json, codecs, datetime, os, ast
from tabulate import tabulate

class event(object):
    def __init__(self, event_url):
        self.event_url = event_url
        self.client_session = requests.session()
        self.client_session.headers['User-Agent']='snekwars client 1.0'
        self.challenge_names = []
        self.challenge_index = {}
        self.email_address_cache = None
        self.password_cache = None
        self.loggedin = False
        
    def register_account(self, email_address, display_name, password, reg_code):
        """Create an account. Four arguments: an email address, a display name, a password, and a registration code."""
        url = self.event_url + "/register_account/"
        resp = self._post_json(url, {'email_address':email_address, 'display_name':display_name, 'password':password, "reg_code":reg_code})
        result = resp.get("data","Error - Account registration failed.")
        if result == "Success":
            self.email_address_cache = email_address
            self.password_cache = password
        return result

    def login(self, email_address = None, password = None):
        """Login. Two optional arguments, an email address and password. Otherwise it tries to use the cached creds."""
        if not email_address:
            email_address = self.email_address_cache
        if not password:
            password = self.password_cache
        if not email_address or not password:
            return "Email Address and Password are required."

        url = self.event_url + "/login/"
        resp = self._post_json(url,{'user':email_address,'password':password})
        login = resp.get("data")
        try:
            if "Login Success" in login:
                self.email_address_cache = email_address
                self.password_cache = password
                self.challenge_index = resp.get("challenge_index")
                self.challenge_names = [self.challenge_index[x] for x in self.challenge_index]
                self.loggedin = True
                return "Login Success"
            else:
                return login
        except Exception:
            print('Error - Could not login.')

    def logout(self):
        """Logout."""
        url = self.event_url + "/logout/"
        self.challenge_names = []
        self.loggedin = False
        resp = self.client_session.get(url).json()
        return resp.get("data")

    def scoreboard(self):
        """Print current scores."""
        if not self.loggedin:
            return "Please login first"
        url = self.event_url + "/scoreboard/"
        resp = self._post_json(url, {'show_all':True} )
        sb = resp.get("data",{})

        if not isinstance(sb,dict):
            print(sb)
            return

        tableHeader = ['Rank', 'Name', 'Score', 'Last Scored', 'Completed']
        sb_table = []

        rank = 1
        for name,score_tuple in sorted(sb.items(), key=lambda x:(x[1][0],_time_elapsed(x[1][2])), reverse=True):
            score,completed_challenges,lastscore = score_tuple
            lsd = datetime.datetime.strptime(lastscore, "%a, %d %b %Y %H:%M:%S")
            lsd = lsd.replace(tzinfo=datetime.timezone.utc).astimezone()
            date_hour = datetime.datetime.strftime(lsd, "%b,%d %H:%M:%S")
            finished = _collapse_points(completed_challenges)
            sb_table.append([f"{rank:0>3}",f"{name}", f"{score:0>3}", f"{date_hour}", f"{finished}"])
            rank += 1

        sb_table.insert(0, tableHeader)
        print(tabulate(sb_table, headers='firstrow', tablefmt='fancy_grid'))
        return None

    def challenge(self, challenge_num):
        """Return the challenge text."""
        if not self.loggedin:
            print("Please login first")
            return None

        url = self.event_url + "/challenge/" + str(challenge_num)
        resp = self.client_session.get(url).json()
        qtxt = resp.get("data")
        if 'Event is currently disabled' in qtxt:
            print(qtxt)
            return None

        # Get terminal width and adjust table to fill it. 
        rows, columns = os.popen('stty size', 'r').read().split()
        qtxt_width = int(columns) - 52
        if qtxt_width < 0:
            qtxt_width = 80
        qtxt_split = [qtxt[i:i+qtxt_width] for i in range(0, len(qtxt), qtxt_width)]
        qtxt_final = ''
        for text in qtxt_split:
            qtxt_final += text + '\n'

        tableHeader = ['#', 'Challenge Name', 'Challenge', 'Points']
        qTable = []

        qTable.append([
                "{}".format(challenge_num),
                "{}".format(self.challenge_index[str(challenge_num)]),
                "{}".format(qtxt_final or "NONE"),
                "{}".format(resp.get("points"))])
        qTable.insert(0, tableHeader)
        try:
            print(tabulate(qTable, headers='firstrow', tablefmt='fancy_grid'))
        except Exception:
            print('Invalid Challenge Number')
        return None        

    def data(self, challenge_num):
        """Return the data for a challenge."""
        if not self.loggedin:
            return "Please login first"

        url = self.event_url + "/data/" + str(challenge_num)
        try:
            data = self.client_session.get(url).json()['data']
            return data
        except Exception as e:
            print('Unable to query data')
            return None

    def solve(self, solution):
        """Submit an solution."""
        if not self.loggedin:
            return "Please login first"
        # chal no 1337 debug solution = 'blinkys_are_life'
        url = self.event_url + "/solve/"
        resp = self._post_json(url, {'solution':str(solution).strip()})
        return resp.get("data")

    def change_password(self, current_password, new_password):
        """Change your password. Two argument, the current password and the new password."""
        if not self.loggedin:
            return "Please login first.  If you dont know your password contact AHHC to reset it."

        url = self.event_url + "/change_password/"
        resp = self._post_json(url, {'current_password':current_password,"new_password":new_password})

        if resp.get("data","") == "Success":
            self.password_cache = new_password

        return resp.get("data")

    def change_displayname(self, new_displayname):
        """Changes your display name on the scoreboard."""
        if not self.loggedin:
            return "Please login first"

        url = self.event_url + "/change_displayname/"
        resp = self._post_json(url, {'displayname':new_displayname})
        return resp.get("data")

    def _post_json(self, url, dict):
        """Internal - post data to server."""
        try:
            data = json.dumps(dict)
        except Exception as e:
            print("Improperly Formatted Data")
            return {}

        resp = self.client_session.post(url,data)

        if resp.status_code != 200:
            print(f"Bad Request. Response {resp.status_code}")
            return {}

        return resp.json()

    def _adminResetPassword(self, emailaddress, new_password):
        """This changes a given users password. Provide the display name and new password."""
        if not self.loggedin:
            return "Please login first."
        url = self.event_url + "/admin/resetpassword"
        resp = self._post_json(url, {'emailaddress':emailaddress,"new_password":new_password})
        return resp.get("data")

    def _adminSetRegistrationCode(self, new_reg_code):
        """This changes a the active registration code."""
        if not self.loggedin:
            return "Please login first."
        url = self.event_url + "/admin/setregcode"
        resp = self._post_json(url, {'reg_code':new_reg_code})
        return resp.get("data")

    def _adminResetScoreboard(self, display_name=0):
        """This reset the scoreboard."""
        if not self.loggedin:
            return "Please login first."
        url = self.event_url + "/admin/resetscoreboard"
        resp = self._post_json(url, {'display_name':str(display_name)})
        return resp.get("data")

    def _adminListUsers(self):
        """This returns a list of all users."""
        if not self.loggedin:
            return "Please login first."
        url = self.event_url + "/admin/listusers"
        resp = self.client_session.get(url).json()
        for user in ast.literal_eval(resp.get("data")):
            print(user)
        return None

    def _adminToggleAdmin(self, display_name):
        """This will toggle admin abilities for the provided display_name."""
        if not self.loggedin:
            return "Please login first."
        url = self.event_url + "/admin/toggleadmin"
        resp = self._post_json(url, {'display_name':str(display_name)})
        return resp.get("data")

    def _adminDeleteUser(self, display_name):
        """This deletes a user associated with the provided display_name."""
        if not self.loggedin:
            return "Please login first."
        url = self.event_url + "/admin/deleteuser"
        resp = self._post_json(url, {'display_name':str(display_name)})
        return resp.get("data")

    def _adminToggleEvent(self):
        """This will toggle the event from disabled to active and vice versa."""
        if not self.loggedin:
            return "Please login first."
        url = self.event_url + "/admin/toggleevent"
        resp = self.client_session.get(url).json()
        return resp.get("data")

    def _adminStatus(self):
        """This will return the status of the event."""
        if not self.loggedin:
            return "Please login first."
        url = self.event_url + "/admin/status"
        resp = self.client_session.get(url).json()

        print(json.dumps(ast.literal_eval(resp['data']), indent=4))
        return None

    def _adminSetRateLimit(self, new_rate_limit):
        """This updates the rate limit."""
        if not self.loggedin:
            return "Please login first."
        url = self.event_url + "/admin/updateratelimit"
        resp = self._post_json(url, {'new_rate_limit':str(new_rate_limit)})
        return resp.get("data")

def _time_elapsed(timestr):
    as_dt = datetime.datetime.strptime(timestr, "%a, %d %b %Y %H:%M:%S")
    return (datetime.datetime.now() - as_dt).total_seconds()

def _collapse_points(completed_challenges):
    """Internal - Condense completed challenges."""
    completed_challenges.sort()
    completed_challenges.append(-999999999999999999999999)
    inrange = False
    result = []

    for pos,eachnum in enumerate(completed_challenges[:-1]):
        if (not inrange) and (eachnum == completed_challenges[pos+1]-1):
            inrange = True
            result.append(str(eachnum)+"-" ) 
        elif not eachnum == completed_challenges[pos+1]-1:
            inrange = False
            result.append(str(eachnum))

    answer = ""

    for eachval in result:
        if eachval[-1] == "-":
            answer += eachval
        else:
            answer += eachval+","
    return answer[:-1]

