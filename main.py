import requests, json, idna, time, time, ctypes, gc
from bs4 import BeautifulSoup

ctypes.windll.kernel32.SetConsoleTitleW("JVZTH | API BALL [V 1.0]")

def dooball():
    
    data = []
    
    URL = "https://www.ballzaa.com/linkdooball.php"
    htmlPage = requests.get(URL)
    page = BeautifulSoup(htmlPage.content, "html.parser")

    data_detail = page.find_all('div', {'class': ['link_rows open-close', 'link_rows open-close bg-bigmatch']})
    data_link = page.find_all('div', {'class': 'desc'})

    for detail in data_detail:
        time = str(detail).split('<div class="l_time"><strong>')[1]
        time = time.split('</strong></div>')[0]
        live_time = str(detail).split('<div class="l_logo" id="l-tsod">')[1]
        if live_time.find('<img src="https://www.ballzaa.com/img/in.gif"/>') != -1:
            live_time = live_time.split('<img src="https://www.ballzaa.com/img/in.gif"/></div>')[0]
        else:
            live_time = ""
        team1 = str(detail).split('<div class="l_team1">')[1]
        team1 = team1.split('</div>')[0]
        team2 = str(detail).split('<div class="l_team2">')[1]
        if team2.find('<img height="9"') != -1:
            team2 = team2.split('<img height="9"')[0]
            team2 = team2.replace(" ", "")
            team2 = team2.replace("\n", "")
        else:
            team2 = team2.split('</div>')[0]
            team2 = team2.replace(" ", "")
            team2 = team2.replace("\n", "")
        score_data = str(detail).split('<span class="sc-home">')[1]
        score_home = score_data.split('</span>')[0]
        score_data = score_data.split('</span>')[1]
        score_text = score_data.split('<span class="sc-away">')[0]
        score_away = score_data.split('<span class="sc-away">')[1]
        score = str(score_home) + str(score_text) + str(score_away)
        program = str(detail).split('<div class="l_program"><strong>')[1]
        program = program.split('</strong></div>')[0]
        data.append({"time":time, "live_time": live_time, "team1": team1, "team2": team2, "score": score, "program": program})

    index = 0
    for link_data in data_link:
        link = []
        link_list = link_data.find_all('div', {'class': 'link_right'})
        for link_live in link_list:
            raw_link = str(link_live).split('<a href="')[1]
            url = raw_link.split('#')[0]
            name = raw_link.split('<strong>')
            if int(len(name)) != 1:
                name = name[1].split('</strong>')[0]
            if url != 'https://www.ballzaa.com/บอลซ่าดูบอลสด\"><span class=\"txtb115\"> &gt;&gt; อัพเดทลิ้งคลิกที่นี่ &lt;&lt;</span></a></h3></div>':
                if ('Xn--') in name != -1:
                    punycode = name.split(" ")[0]
                    names = name.split(" ")[1]
                    name = idna.decode(punycode) + ' ' + names
                link.append({"name": name, "url": url})
                print(str(url) + ' --> ' + str(name))
        data[index].update({"link": link})
        index += 1

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def ball_table():
    table = []
    mainteam = ''
    
    URL = "https://www.ballzaa.com/%E0%B8%95%E0%B8%B2%E0%B8%A3%E0%B8%B2%E0%B8%87%E0%B8%9A%E0%B8%AD%E0%B8%A5%E0%B8%A7%E0%B8%B1%E0%B8%99%E0%B8%99%E0%B8%B5%E0%B9%89/"
    htmlPage = requests.get(URL)
    page = BeautifulSoup(htmlPage.content, "html.parser")
    html_p_league = page.find_all('div', {'class': ['p_league']})

    for raw_data in html_p_league:
        table_data = []
        league = str(raw_data).split('<div class="p_league">')[1]
        league = league.split('</div>')[0]
        if league.find('<img') != -1:  
            league = str(league).split('/>')[1]
        league = league.lstrip()
        league = league.rstrip()
        html_p_content = page.find_all('div', {'class': 'p_content', 'rel': [league, league + ' ']})
        for p_content in html_p_content:
            time = str(p_content).split('<div class="p_time p1 time-mark">')[1]
            time = time.split('</div>')[0]
            live_time = str(p_content).split('<div align="center" class="p_sod p1 l-tsod">')[1]
            live_time = live_time.split('</div>')[0]
            live_time = live_time.strip()
            if live_time.find('FT') != -1:
                live_time = 'FT'
            elif live_time.find('HT') != -1:
                live_time = 'HT'
            if str(p_content).find('<div class="main_team1 tx_blue tx_bold"><span class="tx_blue tx_bold">') != -1:
                team1_division = str(p_content).split('<div class="main_team1 tx_blue tx_bold"><span class="tx_blue tx_bold">')[1]
                team1_division = team1_division.split('<span class="team1-name-mark">')[0]
                mainteam = "team1"
            else:
                team1_division = str(p_content).split('<div class="main_team1">')[1]
                team1_division = team1_division.split('<span class="team1-name-mark">')[0]
            team1_name = str(p_content).split('<span class="team1-name-mark">')[1]
            team1_name = team1_name.split('</span>')[0]
            team1 = str(team1_division) + str(team1_name)
            if str(p_content).find('<span class="tx_blue tx_bold"><span class="team2-name-mark">') != -1:
                team2_name = str(p_content).split('<span class="tx_blue tx_bold"><span class="team2-name-mark">')[1]
                team2_name = team2_name.split('</span>')[0]
                team2_division = str(p_content).split(team2_name + '</span>')[1]
                team2_division = team2_division.split('</span>')[0]
                mainteam = "team2"
            else:
                team2_name = str(p_content).split('<span class="team2-name-mark">')[1]
                team2_name = team2_name.split('</span>')[0]
                team2_division = str(p_content).split(team2_name + '</span>')[1]
                team2_division = team2_division.split(' ')[0]
                team2_division = team2_division.replace("<img", "")
            team2 = str(team2_name) + str(team2_division)
            team2 = team2.rstrip()
            half_time = str(p_content).split('<span class="tx_sky l-hscore">')[1]
            half_time = half_time.split('</span>')[0]
            half_time = half_time.lstrip()
            half_time = half_time.rstrip()
            score_data = str(p_content).split('<span class="sc-home">')[1]
            score_home = score_data.split('</span>')[0]
            score_data = score_data.split('</span>')[1]
            score_text = score_data.split('<span class="sc-away">')[0]
            score_away = score_data.split('<span class="sc-away">')[1]
            full_time = str(score_home) + str(score_text) + str(score_away)
            odds = str(p_content).split('<span class="txtw13 odds-mark">')[1]
            odds = odds.split('</span>')[0]
            tded = str(p_content).split('<div class="tded p1 tdeds-mark">')[1]
            tded = tded.split('</div>')[0]
            tded = tded.rstrip()
            print(str(league) + ' --> ' + str(team1) + ' VS ' + str(team2))
            table_data.append({"time": time, "live_time": live_time, "main_team": mainteam, "team1": team1, "half_time": half_time, "full_time": full_time, "team2": team2, "odds": odds, "tded": tded})
        table.append({"league": league, "data": table_data})
            
    # print(json.dumps(table, indent=4))
    with open('table.json', 'w', encoding='utf-8') as f:
        json.dump(table, f, ensure_ascii=False, indent=4)
           
if __name__ == "__main__":
    while True:
        dooball()
        ball_table()
        print('----------------------------')
        print('Please wait 60 seconds.')
        time.sleep(60)
        gc.collect()
