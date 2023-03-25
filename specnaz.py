#! /usr/bin/env python3
# Autor @Sztuczka-Magiczka
# Ostatnia Aktualizacja: 24/03/2023 - version 1.2

import os, re, sys, time, json, requests, textwrap, socket
from email_validator import validate_email, EmailNotValidError
from googlesearch import search
from lxml.html import fromstring
from getpass import getpass
from shutil import which

r = "\033[31m"
g = "\033[32m"
y = "\033[33m"
b = "\033[34m"
p = "\033[35m"
d = "\033[2;37m"
w = "\033[0m"

W = f"{w}\033[1;47m"
R = f"{w}\033[1;41m"
G = f"{w}\033[1;42m"
Y = f"{w}\033[1;43m"
B = f"{w}\033[1;44m"

home = os.getenv("HOME")
cokifile = ".cookies"
space = "         "
lines = space + "-"*44
apihack = "https://api.hackertarget.com/{}/?q={}"
mbasic = "https://mbasic.facebook.com{}"
graph = "https://graph.facebook.com{}"
headers = {"User-Agent":"Opera/9.80 (J2ME/MIDP; Opera Mini/9.80 (S60; SymbOS; Opera Mobi/23.334; U; id) Presto/2.5.25 Version/10.54"}
logo = f"""{r}

                     {w}[ S.P.E.C.N.A.Z ]{r}
           {d}Podstawowa Wyszukiwarka Informacji{w}
               {d}Autor {w}{r}@Sztuczka-Magiczka{w}"""

def menu():
    os.system("clear")
    print(logo)
    print(f"""
         {W}\033[2;30m Wybierz numer lub wpisz exit aby wyjść {w}
    
        {w}{r}  01{w} Poszukiwacz  {d} Wyszukuje wybranego użytkownika 
        {w}{r}  02{w} Fejsorzut    {d} Pobiera informacje z Facebooka
        {w}{r}  03{w} Listonosz    {d} Wyszukuje email o podanej nazwie
        {w}{r}  04{w} Gugle Hrom   {d} Szczegółowe wyszukiwanie wyszukiwarką
        {w}{r}  05{w} Infofon      {d} Informacje na temat numeru telefonu
        {w}{r}  06{w} System Domeny{d} Wyświetla informacje o serwerze domeny
        {w}{r}  07{w} Domownik     {d} Identyfikuje właściciela domeny
        {w}{r}  08{w} Pod Siecią   {d} Skanuje serwer w poszukiwaniu podsieci
        {w}{r}  09{w} Pokaż Hosta  {d} Szuka hosta domeny
        {w}{r}  10{w} De En Es Host{d} Wskazuje adresy DNS wybranego hosta
        {w}{r}  11{w} Aj Pi Rewers {d} Przeprowadza odwrotną translację adresów IP
        {w}{r}  12{w} Aj Pi Mapa   {d} Wskazuje lokalizację adresu IP
        """)
    mainmenu()

def mainmenu():
    while True:
        try:
            cmd = str(input(f"{space}{w}{b}>{w} Wybierz:{r} "))
            if int(len(cmd)) < 6:
                if cmd in ("exit","Exit"): exit(r+space+"* Zakończono !"+w)
                elif cmd in ("1","01"): userrecon()
                elif cmd in ("2","02"): fb.facedumper()
                elif cmd in ("3","03"): mailfinder()
                elif cmd in ("4","04"): godorker()
                elif cmd in ("5","05"): phoneinfo()
                elif cmd in ("6","06"): infoga("dnslookup")
                elif cmd in ("7","07"): infoga("whois")
                elif cmd in ("8","08"): infoga("subnetcalc")
                elif cmd in ("9","09"): infoga("hostsearch")
                elif cmd in ("10"): infoga("mtr")
                elif cmd in ("11"): infoga("reverseiplookup")
                elif cmd in ("12"): iplocation()
                else: continue
            else: continue
        except KeyboardInterrupt:
            exit(f"{r}\n{space}* Przerwano !")

def iplocation():
    print(f"{space}{r}>{w} local IP: {os.popen('curl ifconfig.co --silent').readline().strip()}")
    x = str(input(f"{space}{r}>{w} enter IP:{r} "))
    if x.split(".")[0].isnumeric(): pass
    else: menu()
    print(w+lines)
    req = requests.get("https://ipinfo.io/"+x+"/json").json()
    try: ip = "IP: "+req["ip"]
    except KeyError: ip = ""
    try: city = "MIASTO: "+req["city"]
    except KeyError: city = ""
    try: country = "KRAJ: "+req["country"]
    except KeyError: country = ""
    try: loc = "LOC: "+req["loc"]
    except KeyError: loc = ""
    try: org = "ORG: "+req["org"]
    except KeyError: org = ""
    try: tz = "STREFA CZASOWA: "+req["timezone"]
    except KeyError: tz = ""
    z = [ip, city, country, loc, org, tz]
    for res in z:
        print(f"{space}{r}-{w} {res}")
    print(w+lines)
    getpass(space+"Wciśnij ENTER aby wrócić do poprzedniego ekranu ")
    menu()

def infoga(opt):
    x = str(input(f"{space}{r}>{w} Wpisz domenę lub adres IP:{r} "))
    if not x: menu()
    if x.split(".")[0].isnumeric(): x = socket.gethostbyname(x)
    else: pass
    print(w+lines)
    req = requests.get(apihack.format(opt,x),stream=True)
    for res in req.iter_lines():
        print(f"{space}{r}-{w} {res.decode('UTF-8')}")
    print(w+lines)
    getpass(space+"Wciśnij ENTER aby wrócić do poprzedniego ekranu ")
    menu()

def phoneinfo():
    no = str(input(f"{space}{r}>{w} Wpisz numer:{r} "))
    if not no: menu()
    print(w+lines)
    url = "https://api.veriphone.io/v2/verify?phone={}&key=5F3F2D6300E445DEA88684053144966C"
    req = requests.get(url.format(no))
    res = json.loads(req.text)
    print(f"{space}{B} DONE {R} {no} {w}")
    try: print(f"{space}{r}-{w} Rodzaj    : {y}{res['phone_type']}{w}")
    except KeyError: pass
    try: print(f"{space}{r}-{w} Prefix  : {y}{res['country_prefix']}{w}")
    except KeyError: pass
    try: print(f"{space}{r}-{w} Kod    : {y}{res['country_code']}{w}")
    except KeyError: pass
    try: print(f"{space}{r}-{w} Kraj : {y}{res['country']}{w}")
    except KeyError: pass
    try: print(f"{space}{r}-{w} Globalny  : {y}{res['international_number']}{w}")
    except KeyError: pass
    try: print(f"{space}{r}-{w} Lokalny   : {y}{res['local_number']}{w}")
    except KeyError: pass
    try: print(f"{space}{r}-{w} Usługodawca: {y}{res['carrier']}{w}")
    except KeyError: pass
    print(w+lines)
    getpass(space+"Wciśnij ENTER aby wrócić do poprzedniego ekranu ")
    menu()
    
def godorker():
    dork = str(input(f"{space}{r}>{w} Wpisz frazę (adres/tekst/etc):{r} ").lower())
    if not dork: menu()
    print(w+lines)
    url = []
    s = search(dork,num_results=30)
    for line in s:
        url.append(line)
    f = open("wyniki_gugle_hrome.txt","w")
    f.write("# Dork: "+dork+"\n\n")
    for u in url:
        try:
            req = requests.get(u,headers=headers)
            res = fromstring(req.content)
            string = res.findtext(".//title")
            wrapper = textwrap.TextWrapper(width=47)
            dedented_text = textwrap.dedent(text=string)
            original = wrapper.fill(text=dedented_text)
            shortened = textwrap.shorten(text=original, width=47)
            title = wrapper.fill(text=shortened)
            f.write(u+"\n")
            print(f"{space}{R} FOUND {w} {str(title)}\n{space}{d}{u}{w}")
        except TypeError: pass
        except requests.exceptions.InvalidSchema: break
        except requests.exceptions.ConnectionError: break
        except KeyboardInterrupt: break
    f.close()
    print(w+lines)
    print(f"{space}{r}>{w} {str(len(url))} Przechwycono jako: {y}wyniki_gugle_hrome.txt{w}")
    getpass(space+"Wciśnij ENTER aby wrócić do poprzedniego ekranu ")
    menu()
    
def mailfinder():
    fullname = str(input(f"{space}{r}>{w} Wpisz nazwę:{r} ").lower())
    if not fullname: menu()
    print(w+lines)
    data = [
        "gmail.com",
        "yahoo.com",
        "hotmail.com",
        "aol.com",
        "msn.com",
        "comcast.net",
        "live.com",
        "rediffmail.com",
        "ymail.com",
        "outlook.com",
        "cox.net",
        "googlemail.com",
        "rocketmail.com",
        "att.net",
        "facebook.com",
        "bellsouth.net",
        "charter.net",
        "sky.com",
        "earthlink.net",
        "optonline.net",
        "qq.com",
        "me.com",
        "gmx.net",
        "mail.com",
        "ntlworld.com",
        "frontiernet.net",
        "windstream.net",
        "mac.com",
        "centurytel.net",
        "aim.com",
        ]
    listuser = [
        fullname.replace(" ",""),
        fullname.replace(" ","")+"123",
        fullname.replace(" ","")+"1234",
        ]
    for name in fullname.split(" "):
        listuser.append(name)
        listuser.append(name+"123")
        listuser.append(name+"1234")
    f = open("result_mailfinder.txt","w")
    ok = []
    try:
        for user in listuser:
            for domain in data:
                email = user + "@" + domain
                api = "0c6ad1fd-f753-4628-8c0a-7968e722c6c7"
                response = requests.get(
                    "https://isitarealemail.com/api/email/validate",
                    params = {'email': email},
                    headers = {'Authorization': "Bearer " + api })
                status = response.json()['status']
                if status == "valid":
                    ok.append(email)
                    f.write(email+"\n")
                    print(f"{space}{R} ZAKOŃCZONO {w} Status: {g}valid{w} Email: {email}")
                else: pass
    except KeyboardInterrupt:
        print("\r"),;sys.stdout.flush()
        pass
    f.close()
    print(w+lines)
    print(f"{space}{r}>{w} {str(len(ok))} Przechwycono jako: {y}wyniki_listonosz.txt{w}")
    getpass(space+"Wciśnij ENTER aby wrócić do poprzedniego ekranu ")
    menu()

def userrecon():
    username = str(input(f"{space}{w}{r}>{w} Wpisz użytkownika:{r} ").lower())
    if not username: menu()
    urllist = [
        "https://facebook.com/{}",
        "https://instagram.com/{}",
        "https://twitter.com/{}",
        "https://youtube.com/{}",
        "https://vimeo.com/{}",
        "https://github.com/{}",
        "https://plus.google.com/{}",
        "https://pinterest.com/{}",
        "https://flickr.com/people/{}",
        "https://vk.com/{}",
        "https://about.me/{}",
        "https://disqus.com/{}",
        "https://bitbucket.org/{}",
        "https://flipboard.com/@{}",
        "https://medium.com/@{}",
        "https://hackerone.com/{}",
        "https://keybase.io/{}",
        "https://buzzfeed.com/{}",
        "https://slideshare.net/{}",
        "https://mixcloud.com/{}",
        "https://soundcloud.com/{}",
        "https://badoo.com/en/{}",
        "https://imgur.com/user/{}",
        "https://open.spotify.com/user/{}",
        "https://pastebin.com/u/{}",
        "https://wattpad.com/user/{}",
        "https://canva.com/{}",
        "https://codecademy.com/{}",
        "https://last.fm/user/{}",
        "https://blip.fm/{}",
        "https://dribbble.com/{}",
        "https://en.gravatar.com/{}",
        "https://foursquare.com/{}",
        "https://creativemarket.com/{}",
        "https://ello.co/{}",
        "https://cash.me/{}",
        "https://angel.co/{}",
        "https://500px.com/{}",
        "https://houzz.com/user/{}",
        "https://tripadvisor.com/members/{}",
        "https://kongregate.com/accounts/{}",
        "https://{}.blogspot.com/",
        "https://{}.tumblr.com/",
        "https://{}.wordpress.com/",
        "https://{}.devianart.com/",
        "https://{}.slack.com/",
        "https://{}.livejournal.com/",
        "https://{}.newgrounds.com/",
        "https://{}.hubpages.com",
        "https://{}.contently.com",
        "https://steamcommunity.com/id/{}",
        "https://www.wikipedia.org/wiki/User:{}",
        "https://www.freelancer.com/u/{}",
        "https://www.dailymotion.com/{}",
        "https://www.etsy.com/shop/{}",
        "https://www.scribd.com/{}",
        "https://www.patreon.com/{}",
        "https://www.behance.net/{}",
        "https://www.goodreads.com/{}",
        "https://www.gumroad.com/{}",
        "https://www.instructables.com/member/{}",
        "https://www.codementor.io/{}",
        "https://www.reverbnation.com/{}",
        "https://www.designspiration.net/{}",
        "https://www.bandcamp.com/{}",
        "https://www.colourlovers.com/love/{}",
        "https://www.ifttt.com/p/{}",
        "https://www.trakt.tv/users/{}",
        "https://www.okcupid.com/profile/{}",
        "https://www.trip.skyscanner.com/user/{}",
        "http://www.zone-h.org/archive/notifier={}",
        ]
    print(w+lines)
    for url in urllist:
        try:
            req = requests.get(url.format(username), headers=headers)
            if req.status_code == 200: color = g
            elif req.status_code == 404: color = r
            else: color = y
            print(f"  {space}{r}[{color}{req.status_code}{r}] {w}{url.format(username)}")
        except requests.exceptions.Timeout: continue
        except requests.exceptions.TooManyRedirects: continue
        except requests.exceptions.ConnectionError: break
    print(w+lines)
    getpass(space+"Wciśnij ENTER aby wrócić do poprzedniego ekranu ")
    menu()

class Facebook():
    
    def user_token(self):
        x = requests.get('https://m.facebook.com/composer/ocelot/async_loader/?publisher=feed#_=_', headers = {
            'user-agent'                : 'Mozilla/5.0 (Linux; Android 8.1.0; MI 8 Build/OPM1.171019.011) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.86 Mobile Safari/537.36', # don't change this user agent.
            'referer'                   : 'https://m.facebook.com/',
            'host'                      : 'm.facebook.com',
            'origin'                    : 'https://m.facebook.com',
            'upgrade-insecure-requests' : '1',
            'accept-language'           : 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
            'cache-control'             : 'max-age=0',
            'accept'                    : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'content-type'              : 'text/html; charset=utf-8'
        }, cookies={"cookie":open(cokifile).read()})
        find = re.search("(EAAA\w+)",x.text)
        if find == None:
            exit(r+"[!] Błąd w załadowaniu tokena sesji"+w)
        else:
            return find.group(1)
    
    def facedumper(self):
        try:
            coki = open(cokifile).read()
        except FileNotFoundError:
            while True:
                coki = getpass(f"{space}{r}>{w} Wpisz adres ciasteczek z Facebooka (ukryte wejście): ")
                if coki: break
                else: continue
        cookies = {"cookie":coki}
        sesi = requests.Session()
        req = requests.get(mbasic.format("/me",verify=False),cookies=cookies).content
        if "mbasic_logout_button" in str(req):
            if "Apa yang Anda pikirkan sekarang" in str(req):
                open(cokifile,"a").write(coki)
            else:
                try:
                    requests.get(mbasic.format(parser(req,"html.parser").find("a",string="Bahasa Indonesia")["href"]),cookies=cookies)
                    x = parser(requests.get(mbasic.format("/termuxhackers.id"),cookies=cookies).content,"html.parser").find("a",string="Ikuti")["href"]
                    sesi.get(mbasic.format(x),cookies=cookies)
                except: pass
        else:
            exit(r+"* invalid credentials: cookies"+w)
            time.sleep(3)
            menu()
        print(f"""
        {w}{r}  01{w} Zrzuć wszystko    {d} Zrzuca wszystkie informacje z listy znajomych
        {w}{r}  02{w} Zrzuć użytkownika {d} Zrzuca użytkownika z listy znajomych
        {w}{r}  03{w} Zrzuć email       {d} Zrzuca email z listy znajomych
        {w}{r}  04{w} Zrzuć telefon     {d} Zrzuca telefon z listy znajomych
        {w}{r}  05{w} Zrzuć urodziny    {d} Zrzuca urodziny z listy znajomych
        {w}{r}  06{w} Zrzuć lokalizację {d} Zrzuca lokalizację z listy znajomych
        """)
        while True:
            usr = str(input(f"{space}{w}{r}>{w} Wybierz: {r}"))
            if not usr: menu()
            if usr in ("1","01"):
                fb.dump_all()
            elif usr in ("2","02"):
                fb.dump_id()
            elif usr in ("3","03"):
                fb.dump_email()
            elif usr in ("4","04"):
                fb.dump_phone()
            elif usr in ("5","05"):
                fb.dump_birthday()
            elif usr in ("6","06"):
                fb.dump_location()
            else: continue
        
    def dump_all(self):
        token = fb.user_token()
        req = requests.get(graph.format("/v3.2/me/friends/?fields=name,email&access_token="+token+"&limit=5000"),headers=headers)
        res = json.loads(req.text)
        print(w+lines)
        i = 0
        for data in res["data"]:
            try:
                i += 1
                REQ = requests.get(graph.format("/"+data["id"]+"?access_token="+token+"&limit=5000"),headers=headers)
                RES = json.loads(REQ.text)
                id = data["id"]
                name = data["name"]
                print(f"{space}{R} ZAKOŃCZONO {R} {str(i)} {w}")
                print(f"{space}{r}-{w} Imię: {name}")
                print(f"{space}{r}-{w} ID: {id}")
                try: print(f"{space}{r}-{w} Email: {RES['email']}")
                except KeyError: pass
                try: print(f"{space}{r}-{w} Email: {RES['phone']}")
                except KeyError: pass
                try: print(f"{space}{r}-{w} Email: {RES['birthday']}")
                except KeyError: pass
                try:
                    location = RES["location"]["name"]
                    print(f"{space}{r}-{w} Lokalizacja: {location}")
                except KeyError: pass
            except KeyboardInterrupt: break
        print(w+lines)
        getpass(space+"Wciśnij ENTER aby wrócić do poprzedniego ekranu ")
        menu()
        
    def dump_id(self):
        token = fb.user_token()
        req = requests.get(graph.format("/v3.2/me/friends/?fields=name,email&access_token="+token+"&limit=5000"),headers=headers)
        res = json.loads(req.text)
        listid = []
        print(w+lines)
        f = open("zrzut_id_znajomych.txt","w")
        for data in res["data"]:
            try:
                id = data["id"]
                name = data["name"]
                print(f"{space}{R} ZAKOŃCZONO {w} ID: {id} {r}->{w} {name}")
                listid.append(data["id"])
                f.write(id+"|"+name+"\n")
            except KeyboardInterrupt:
                break
        f.close()
        print(w+lines)
        print(f"{space}{r}>{w} {str(len(listid))} Przechwycono jako: {y}zrzut_id_znajomych.txt{w}")
        getpass(space+"Wciśnij ENTER aby wrócić do poprzedniego ekranu ")
        menu()

    def dump_email(self):
        token = fb.user_token()
        req = requests.get(graph.format("/v3.2/me/friends/?fields=name,email&access_token="+token+"&limit=5000"),headers=headers)
        res = json.loads(req.text)
        listmail = []
        print(w+lines)
        f = open("zrzut_email.txt","w")
        for data in res["data"]:
            try:
                REQ = requests.get(graph.format("/"+data["id"]+"?access_token="+token+"&limit=5000"),headers=headers)
                RES = json.loads(REQ.text)
                try:
                    name = RES["name"]
                    email = RES["email"]
                    print(f"{space}{R} ZAKOŃCZONO {w} Email: {email} {r}->{w} {name}")
                    listmail.append(email)
                    f.write(email+"|"+RES['id']+"|"+name+"\n")
                except KeyError: pass
            except KeyboardInterrupt:
                break
        f.close()
        print(w+lines)
        print(f"{space}{r}>{w} {str(len(listmail))} Przechwycono jako: {y}zrzut_email.txt{w}")
        getpass(space+"Wciśnij ENTER aby wrócić do poprzedniego ekranu ")
        menu()

    def dump_phone(self):
        token = fb.user_token()
        req = requests.get(graph.format("/v3.2/me/friends/?fields=name,email&access_token="+token+"&limit=5000"),headers=headers)
        res = json.loads(req.text)
        listphone = []
        print(w+lines)
        f = open("zrzut_telefon.txt","w")
        for data in res["data"]:
            try:
                REQ = requests.get(graph.format("/"+data["id"]+"?access_token="+token+"&limit=5000"),headers=headers)
                RES = json.loads(REQ.text)
                try:
                    name = RES["name"]
                    phone = RES["mobile_phone"]
                    print(f"{space}{R} ZAKOŃCZONO {w} Telefon: {phone} {r}->{w} {name}")
                    listphone.append(phone)
                    f.write(phone+"|"+RES['id']+"|"+name+"\n")
                except KeyError: pass
            except KeyboardInterrupt:
                break
        f.close()
        print(w+lines)
        print(f"{space}{r}>{w} {str(len(listphone))} Przechwycono jako: {y}zrzut_telefon.txt{w}")
        getpass(space+"Wciśnij ENTER aby wrócić do poprzedniego ekranu ")
        menu()

    def dump_birthday(self):
        token = fb.user_token()
        req = requests.get(graph.format("/v3.2/me/friends/?fields=name,email&access_token="+token+"&limit=5000"),headers=headers)
        res = json.loads(req.text)
        listday = []
        print(w+lines)
        f = open("zrzut_urodziny.txt","w")
        for data in res["data"]:
            try:
                REQ = requests.get(graph.format("/"+data["id"]+"?access_token="+token+"&limit=5000"),headers=headers)
                RES = json.loads(REQ.text)
                try:
                    name = RES["name"]
                    day = RES["birthday"]
                    print(f"{space}{R} ZAKOŃCZONO {w} Urodziny: {day} {r}->{w} {name}")
                    listday.append(day)
                    f.write(day+"|"+RES['id']+"|"+name+"\n")
                except KeyError: pass
            except KeyboardInterrupt:
                break
        f.close()
        print(w+lines)
        print(f"{space}{r}>{w} {str(len(listday))} Przechwycono jako: {y}zrzut_urodziny.txt{w}")
        getpass(space+"Wciśnij ENTER aby wrócić do poprzedniego ekranu ")
        menu()

    def dump_location(self):
        token = fb.user_token()
        req = requests.get(graph.format("/v3.2/me/friends/?fields=name,email&access_token="+token+"&limit=5000"),headers=headers)
        res = json.loads(req.text)
        listloc = []
        print(w+lines)
        f = open("dump_lokalizacja.txt","w")
        for data in res["data"]:
            try:
                REQ = requests.get(graph.format("/"+data["id"]+"?access_token="+token+"&limit=5000"),headers=headers)
                RES = json.loads(REQ.text)
                try:
                    name = RES["name"]
                    loc = RES["location"]["name"] 
                    f.write(loc+"|"+RES['id']+"|"+name+"\n")
                    listloc.append(loc)
                    print(f"{space}{R} ZAKOŃCZONO {w} Lokalizacja: {loc} {r}->{w} {name}")
                except KeyError: pass
            except KeyboardInterrupt:
                break
        f.close()
        print(w+lines)
        print(f"{space}{r}>{w} {str(len(listloc))} Przechwycono jako: {y}zrzut_lokalizacja.txt{w}")
        getpass(space+"Wciśnij ENTER aby wrócić do poprzedniego ekranu ")
        menu()

if __name__ == "__main__":
    arg = sys.argv
    fb = Facebook()
    if len(arg) == 1: menu()
    elif len(arg) == 2:
        if arg[1] in ("update"):
            if which("termux-setup-storage"): path = "$PREFIX/bin/specnaz"
            else:
                if os.path.isdir("/usr/local/bin/"): path = "/usr/local/bin/specnaz"
                else: path = "/usr/bin/specnaz"
            os.system(f"wget https://raw.githubusercontent.com/Sztuczka-Magiczka/Specnaz/main/specnaz.py -O {path} && chmod +x {path}")
            print(f"{r}>{w} wrapper script have been updated")
        else: exit(r+"* no command found for: "+str(arg[1:]).replace("[","").replace("]",""))
    else: exit(r+"* no command found for: "+str(arg[1:]).replace("[","").replace("]",""))
