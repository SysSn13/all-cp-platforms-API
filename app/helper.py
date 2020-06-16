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
        r = session.get(url)
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
        return {'status':'OK','rating':rating,'max_rating':max_rating,
                'global_rank':global_rank,'country_rank':country_rank,
                'contests':get_contests_details(),}
    def codeforces(self):
        url = 'https://codeforces.com/api/user.info?handles={}'.format(self.__username)
        r = requests.get(url)
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
        r = session.get(url)
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

    def get_info(self):
        if self.__platform=='codechef':
            return self.codechef()
        if self.__platform=='codeforces':
            return self.codeforces()
        if self.__platform == 'atcoder':
            return self.atcoder()
        raise PlatformError('Platform not Found')




if __name__ == '__main__':
    platform = input("Enter platform: ")
    username = input("Enter username: ")
    obj = User(username,platform)
    print(obj.get_info())
