from requests_html import HTMLSession
import json
import requests
class UsernameError(Exception):
    pass
class PlatformError(Exception):
    pass

class User:
    def __init__(self,username=None,platform=None):
        self.__username = username
        self.__platform = platform
    def codechef(self):
        url = "https://codechef.com/users/{}".format(self.__username)
        session = HTMLSession()
        r = session.get(url,timeout=10)
        if r.status_code!=200:
            raise UsernameError("User not found")
        try:
            rating_header = r.html.find(".rating-header",first=True)
        except:
            raise UsernameError('User not found')

        try:
            rating = rating_header.find(".rating-number",first=True).text
        except:
            raise UsernameError('User not found')
        max_rating = rating_header.find('small')[0].text[1:-1].split()[2]
        rating_star = len(r.html.find(".rating-star",first=True).find('span'))
        ranks = r.html.find('.rating-ranks',first=True).find('strong')
        global_rank = ranks[0].text
        country_rank = ranks[1].text
        def get_contests_details():
            rating_table = r.html.find('.rating-table',first=True)
            data_rows = rating_table.find('tr')[1:]
            data = list()
            for row in data_rows:
                td = row.find('td')
                d = dict()
                d['name'] = td[0].text.replace("\n", " ")
                d['rating'] = td[1].text
                d['global_rank'] = td[2].text
                d['country_rank'] = td[3].text
                data.append(d)
            return data
        def get_problems_solved():
            div = r.html.find('.problems-solved',first=True)
            problems_solved = dict()
            fully_solved=dict()
            partial_solved =dict()
            articles = div.find('article')
            h5s = div.find('h5')
            for a,h in zip(articles,h5s):
                ps = a.find('p')
                prob_data = dict()
                for p in ps:
                    txt = p.text.split()
                    type = txt[0][:-1]
                    txt = txt[1:]
                    prob_data[type] =list()
                    for t in txt:
                        if t==txt[len(txt)-1]:
                            prob_data[type].append(t)
                        else:
                            prob_data[type].append(t[:-1])

                if h.text.split()[0]=='Fully':
                    fully_solved['count'] = h.text.split()[2][1:-1]
                    fully_solved['problems'] = prob_data
                elif h.text.split()[0]=='Partially':
                    partial_solved['count'] = h.text.split()[2][1:-1]
                    partial_solved['problems'] = prob_data
            problems_solved['fully_solved'] = fully_solved
            problems_solved['partial_solved'] = partial_solved
            return problems_solved
        return {'status':'OK','rating':rating,'max_rating':max_rating,
                'global_rank':global_rank,'country_rank':country_rank,
                'contests':get_contests_details(),'problems_solved':get_problems_solved()}
    def codeforces(self):
        url = 'https://codeforces.com/api/user.info?handles={}'.format(self.__username)
        r = requests.get(url,timeout=10)
        if r.status_code !=200:
            raise UsernameError('User not found')
        r_data = r.json()
        if r_data['status']!='OK':
            raise UsernameError('User not found')
        data  = dict()
        data['status'] = 'OK'
        data.update(r_data['result'][0])
        return data
    def atcoder(self):
        url = "https://atcoder.jp/users/{}".format(self.__username)
        session = HTMLSession()
        r = session.get(url,timeout=10)
        if r.status_code != 200:
            raise UsernameError('User not found')
        data_tables = r.html.find('.dl-table')
        if not len(data_tables):
            raise UsernameError('User not found')
        data = dict()
        data['status']='OK'
        for table in data_tables:
            data_rows = table.find('tr')
            for row in data_rows:
                attr = row.find('th',first=True).text
                val = row.find('td',first=True).text
                data[attr]=val
                if attr == 'Highest Rating':
                    val = val.split()[0]
                    data[attr]=val
        return data
    def spoj(self):
        url = "https://www.spoj.com/users/{}/".format(self.__username)
        session = HTMLSession()
        r = session.get(url,timeout=10)
        if r.status_code !=200:
            raise UsernameError("User not found")
        user_profile_left = r.html.find("#user-profile-left")
        if not len(user_profile_left):
            raise UsernameError
        user_profile_left = user_profile_left[0]
        data = dict()
        data['status'] = 'OK'
        data['full_name'] = user_profile_left.find('h3',first=True).text
        data['img_src'] =   user_profile_left.find('img')[0].attrs['src']
        p_data = user_profile_left.find('p')
        data['location'] = p_data[0].text
        data['joined'] = p_data[1].text.replace("Joined ","")
        data['world_rank'] = p_data[2].text.split()[2][1:]
        data['institution'] =  p_data[3].text.replace("Institution: ","")
        data_stats = r.html.find('.profile-info-data-stats',first=True)
        dts = data_stats.find('dt')
        dds = data_stats.find('dd')
        for dt,dd in zip(dts,dds):
            data[dt.text] =dd.text
        return data
    def leetcode(self):
        session = HTMLSession()
        url = "https://leetcode.com/{}/".format(self.__username)
        r = session.get(url,timeout=10)
        if r.status_code!=200:
            raise UsernameError('User not found')
        check = r.html.find('.username')
        if not len(check):
            raise UsernameError('User not found')
        target = r.html.find('.list-group-item')
        basic_profile = dict()
        contest = dict()
        progress = dict()
        contribution = dict()
        for li in target:
            text = li.text.split()
            if len(text)<6:
                    if len(text)>=2 and text[0]=='Location':
                        basic_profile['location'] = li.text.replace("Location ","")
                    elif len(text)>=1 and text[0]=='School':
                        basic_profile['school'] = li.text.replace("School ","")
                    elif len(text)>=2 and text[1]=='Rating':
                        contest['rating']=text[0]
                    elif len(text)>=3 and text[1]+text[2]=='FinishedContests':
                        contest['finished_contests']=text[0]
                    elif len(text)>=5 and text[len(text)-2]+text[len(text)-1]=='GlobalRanking':
                        contest['global_ranking'] = text[0]
                        contest['total_participants'] = text[2]
                    elif len(text)>=5 and text[len(text)-2]+text[len(text)-1]=='SolvedQuestion':
                        progress['solved_question'] = text[0]
                        progress['total_question'] = text[2]
                    elif len(text)>=5 and text[len(text)-2]+text[len(text)-1]=='AcceptedSubmission':
                        progress['accepted_submission'] = text[0]
                        progress['total_submission'] = text[2]
                    elif len(text)>=4 and text[len(text)-2]+text[len(text)-1]=='AcceptanceRate':
                        progress['acceptance_rate'] = text[0]+ " %"
                    elif len(text)>=2 and text[1]=="Problems":
                        contribution['problems'] = text[0]
                    elif len(text)>=2 and text[1]=="Points":
                        contribution['points']=text[0]
                    elif len(text)>=3 and text[len(text)-2]+text[len(text)-1]=='TestCases':
                        contribution['test_cases'] = text[0]
                    elif len(text)>=2 and text[0] == 'Website':
                        basic_profile['website'] = text[1]
                    elif len(text)>=2 and text[0]=='Company':
                        basic_profile['company'] = text[1]
        data = {'status':'OK','basic_profile':basic_profile,'contest':contest,'progress':progress,'contribution':contribution,}
        return data
    def get_info(self):
        if self.__platform=='codechef':
            return self.codechef()
        if self.__platform=='codeforces':
            return self.codeforces()
        if self.__platform == 'atcoder':
            return self.atcoder()
        if self.__platform == 'spoj':
            return self.spoj()
        if self.__platform =='leetcode':
            return self.leetcode()
        raise PlatformError('Platform not Found')
if __name__ == '__main__':
    platform = input("Enter platform: ")
    username = input("Enter username: ")
    obj = User(username,platform)
    print(obj.get_info())
