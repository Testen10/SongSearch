import re
import json
import requests
from bs4 import BeautifulSoup
import bs4
import urllib
import simplejson
from selenium import webdriver
from selenium.webdriver.chrome.service import Service # **
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
import undetected_chromedriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys 
import urllib.request
from PIL import Image
import urllib.parse
import tkinter
from tkinter import ttk
from tkinter import Tk, font
from PIL import ImageTk as itk
from tkinter import messagebox
import os, sys
from pytube import YouTube
from pytube import Channel
from multiprocessing import freeze_support


def set_chrome_driver():
    chrome_options = webdriver.ChromeOptions()
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        chromedriver_path = os.path.join(sys._MEIPASS, "chromedriver.exe")
        service = Service(executable_path=chromedriver_path)
        driver = undetected_chromedriver.Chrome(service=service, options=chrome_options)

    else:
        service = Service(executable_path='./chromedriver.exe')
        driver = undetected_chromedriver.Chrome(service=service, options=chrome_options)
    
    return driver
    

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:  # running as script, return unmodified path
        return relative_path  
    else:  # running as exe, return MEI path
        return os.path.join(base_path, relative_path)

class MainWindow():
    def __init__(self):
        # 메인 윈도우 생성
        self.window=tkinter.Tk()
        self.window.title("음원 구매 경로 검색")
        self.window.geometry("900x650+100+100")
        self.window.resizable(False, False)

        # 폰트 설정
        self.Title_font=tkinter.font.Font(root=self.window, family="S-Core Dream", size=43)
        self.subtitle_font=tkinter.font.Font(root=self.window, family="S-Core Dream", size=30)
        self.normaltxt_font=tkinter.font.Font(root=self.window, family="S-Core Dream", size=20)
        self.entrytxt_font=tkinter.font.Font(root=self.window, family="S-Core Dream", size=18)

        # 웹사이트 열 때 driver를 저장하는 list
        self.driver_list = []

        self.initGUI()
        self.window.mainloop()

    def initGUI(self):
        title_label = tkinter.Label(self.window, text="음원 구매 경로 검색 프로그램", font = self.Title_font, width=20, height=1,fg="black", relief="flat")
        title_label.place(x=177,y=30)

        # 도움말
        self.help_img = tkinter.PhotoImage(file=resource_path('./img_resource/help.png'))
        self.label_help = tkinter.Label(self.window, image = self.help_img)
        self.label_help.bind("<Enter>", self.show_help)
        self.label_help.bind("<Leave>", self.hide_help)
        self.label_help.place(x=820,y=30)

        # 곡 링크 입력하는 곳
        url_label = tkinter.Label(self.window, text="링크:", font = self.subtitle_font, width=3, height=1,fg="black", relief="flat")
        url_label.place(x=45,y=130)

        self.entry_url = ttk.Entry(self.window, width=55, textvariable=str, font = self.normaltxt_font)
        self.window.bind_class("Entry", "<Button-3><ButtonRelease-3>", self.ctrl_event)
        self.entry_url.place(x=120,y=135)

        self.btn_getInfo = tkinter.Button(self.window, text = "곡 정보 가져오기", font = self.normaltxt_font, width    = 15, height=1,fg="black", pady = 3, command = self.get_video_info)
        self.btn_getInfo.place(x=617,y=180)

        # 썸네일 이미지
        self.thumbnail_img = tkinter.PhotoImage(file=resource_path('./img_resource/thumbnail.png'))
        self.lbl_tbnail = tkinter.Label(self.window, image = self.thumbnail_img)
        self.lbl_tbnail.place(x=45,y=240)

        # 곡 정보 가져오기
        # 1. 곡 제목
        song_info_y = 240

        self.lbl_song_title = tkinter.Label(self.window, text="곡 제목: ", font = self.subtitle_font, width=6, height=1,fg="black", relief="flat")
        self.lbl_song_title.place(x=345,y=song_info_y)

        self.var_EntrySongTitle = tkinter.StringVar()
        self.var_EntrySongTitle.trace_add(mode = 'write', callback=self._write_callback_songTitle)

        self.entry_song_title = ttk.Entry(self.window, width=29, textvariable=self.var_EntrySongTitle, font = self.normaltxt_font)
        self.entry_song_title.place(x=460,y=song_info_y+5)
        

        self.var_include_songTitle = tkinter.IntVar()
        self.checkbtn_songTitle = tkinter.Checkbutton(self.window, variable = self.var_include_songTitle, font = self.normaltxt_font)
        self.checkbtn_songTitle.place(x=855, y= song_info_y+5)

        # 2. 추가 입력란 1
        self.var_EntrySongTitleEng = tkinter.StringVar()
        self.var_EntrySongTitleEng.trace_add(mode = 'write', callback=self._write_callback_songTitleEng)

        self.entry_song_title_eng = ttk.Entry(self.window, width=29, textvariable=self.var_EntrySongTitleEng, font = self.normaltxt_font)
        self.entry_song_title_eng.place(x=460,y=song_info_y+42)

        self.var_include_songTitleEng = tkinter.IntVar()
        self.checkbtn_songTitleEng = tkinter.Checkbutton(self.window, variable = self.var_include_songTitleEng, font = self.normaltxt_font)
        self.checkbtn_songTitleEng.place(x=855, y= song_info_y+42)

        song_info_y += 75

        # 3. 작곡가 이름
        self.var_EntryCompName = tkinter.StringVar()
        self.var_EntryCompName.trace_add(mode = 'write', callback=self._write_callback_compName)

        self.lbl_composer_name = tkinter.Label(self.window, text="작곡가: ", font = self.subtitle_font, width=6, height=1,fg="black", relief="flat")
        self.lbl_composer_name.place(x=345,y=song_info_y)

        self.entry_composer_name = ttk.Entry(self.window, width=29, textvariable=self.var_EntryCompName, font = self.normaltxt_font)
        self.entry_composer_name.place(x=460,y=song_info_y+5)

        self.var_include_compName = tkinter.IntVar()
        self.checkbtn_compName = tkinter.Checkbutton(self.window, variable = self.var_include_compName, font = self.normaltxt_font)
        self.checkbtn_compName.place(x=855, y= song_info_y+5)

        # 4. 추가 입력란2
        self.var_EntryCompNameEng = tkinter.StringVar()
        self.var_EntryCompNameEng.trace_add(mode = 'write', callback=self._write_callback_compNameEng)

        self.entry_composer_name_eng = ttk.Entry(self.window, width=29, textvariable=self.var_EntryCompNameEng, font = self.normaltxt_font)
        self.entry_composer_name_eng.place(x=460,y=song_info_y+42)

        self.var_include_compNameEng = tkinter.IntVar()
        self.checkbtn_compNameEng = tkinter.Checkbutton(self.window, variable = self.var_include_compNameEng, font = self.normaltxt_font)
        self.checkbtn_compNameEng.place(x=855, y= song_info_y+42)

        # 사이트 선택
        self.lbl_site = tkinter.Label(self.window, text="검색할 사이트", font = self.subtitle_font, width=10, height=1,fg="black", relief="flat")
        self.lbl_site.place(x=45,y=440)

        self.var_am = tkinter.IntVar()
        self.var_amjp = tkinter.IntVar()
        self.var_oty = tkinter.IntVar()
        self.var_vibe = tkinter.IntVar()
        self.var_reko = tkinter.IntVar()
        self.var_bcamp= tkinter.IntVar()
        
        checkbtn_x = 45
        checkbtn_y = 500

        self.checkbtn_am = tkinter.Checkbutton(self.window,text=" Amazon", variable = self.var_am, font = self.normaltxt_font)
        self.checkbtn_am.place(x=checkbtn_x, y= checkbtn_y)
        
        self.window.update()
        checkbtn_y += self.checkbtn_am.winfo_height() + 10
        
        self.checkbtn_amjp = tkinter.Checkbutton(self.window,text=" Amazon Jp", variable = self.var_amjp, font = self.normaltxt_font)
        self.checkbtn_amjp.place(x=checkbtn_x, y= checkbtn_y)
       
        self.window.update()
        checkbtn_x += 200
        checkbtn_y = 500
       
        self.checkbtn_oty = tkinter.Checkbutton(self.window,text=" Ototoy", variable = self.var_oty, font = self.normaltxt_font)
        self.checkbtn_oty.place(x=checkbtn_x, y= checkbtn_y)

        self.window.update()
        checkbtn_y +=self.checkbtn_amjp.winfo_height() + 10
       
        self.checkbtn_vibe = tkinter.Checkbutton(self.window,text=" Naver Vibe", variable = self.var_vibe, font = self.normaltxt_font)
        self.checkbtn_vibe.place(x=checkbtn_x, y= checkbtn_y)

        self.window.update()
        checkbtn_x += 200
        checkbtn_y = 500
        
        self.checkbtn_bandcamp = tkinter.Checkbutton(self.window,text=" Bandcamp", variable = self.var_bcamp, font = self.normaltxt_font)
        self.checkbtn_bandcamp.place(x=checkbtn_x, y= checkbtn_y)

        self.window.update()
        checkbtn_y +=self.checkbtn_vibe.winfo_height() + 10
     
        self.checkbtn_reko = tkinter.Checkbutton(self.window,text="レコチョク", variable = self.var_reko, font = self.normaltxt_font)
        self.checkbtn_reko.place(x=checkbtn_x, y= checkbtn_y)

        self.btn_getInfo = tkinter.Button(self.window, text = "검색하기", font = self.normaltxt_font, width = 15, height=1,fg="black", pady = 3, command = self.searchSong)
        self.btn_getInfo.place(x=640,y=500)

        self.btn_getTip = tkinter.Button(self.window, text = "음원 검색 Tip", font = self.normaltxt_font, width = 15, height=1,fg="black", pady = 3, command = self.show_tip)
        self.btn_getTip.place(x=640,y=550)

    def _get_video_id(self, url):
        video_id =''
        query = urllib.parse.urlparse(url)
        if query.hostname == 'youtu.be':
            video_id = query.path[1:]
        if query.hostname in ('www.youtube.com', 'youtube.com'):
            if query.path == '/watch':
                p = urllib.parse.parse_qs(query.query)
                video_id = p['v'][0]
            if query.path[:7] == '/embed/':
                video_id = query.path.split('/')[2]
            if query.path[:3] == '/v/':
                video_id = query.path.split('/')[2]
        
        return video_id
        
    def _get_video_tmbnail(self, video_id):
        img_link = 'thumbnail'
        try:
            urllib.request.urlretrieve(
             'https://i.ytimg.com/vi/{}/maxresdefault.jpg'.format(video_id), resource_path("./img_resource/thumbnail2.png"))
            img_link = 'thumbnail2'
        except:
            try:
                urllib.request.urlretrieve(
                'https://i.ytimg.com/vi/{}/original.jpg'.format(video_id), resource_path(("./img_resource/thumbnail2.png")))
                img_link = 'thumbnail2'
            except:
                pass
                
        img = Image.open(resource_path("./img_resource/{}.png").format(img_link))
        img = img.resize((280, 157))
        
        return img

    def _get_video_title(self,url):
        r = requests.get(url)
        s = BeautifulSoup(r.text, "lxml")

        try:    
            # finding meta info for title
            return s.select_one('meta[itemprop="name"][content]')['content']

        except Exception as exp:
            print(exp)
            messagebox.showerror('Python Error', 'Error: This is an Error Message!')

    def _get_channel_name(self,url):
        video = YouTube(url)
        channel_url = video.channel_url
        channel = Channel(channel_url)
        channel_name = channel.channel_name

        return channel_name
    
    def get_video_info(self):
        url = self.entry_url.get()

        # get video id
        video_id = self._get_video_id(url)

        if video_id == '':
            self.lbl_tbnail = tkinter.Label(self.window, image = self.thumbnail_img)
            return
        
        # get thumbnail img
        self.pImage_tbnail = itk.PhotoImage(self._get_video_tmbnail(video_id))
        self.lbl_tbnail.config(image = self.pImage_tbnail)

        # get video title
        title = self._get_video_title(url)
        self.entry_song_title.delete(0, 'end')
        self.entry_song_title.insert(0,title)

        # get channel name
        channel_name = self._get_channel_name(url)
        self.entry_composer_name.delete(0, 'end')
        self.entry_composer_name.insert(0, channel_name)

    # 각 entry에 어떤 값이 입력된 경우, 자동으로 활성화. 값이 없는 경우는 자동으로 비활성화        
    def _write_callback_songTitle(self, var, index, mode):
        if self.entry_song_title.get() != '' and self.entry_song_title.get() != "곡 검색시 영상의 이 곳에 제목이 자동으로 입력됩니다.":
            self.checkbtn_songTitle.select()
        else:
            self.checkbtn_songTitle.deselect()

    def _write_callback_songTitleEng(self, var, index, mode):
        if self.entry_song_title_eng.get() != '':
            self.checkbtn_songTitleEng.select()
        else:
            self.checkbtn_songTitleEng.deselect()

    def _write_callback_compName(self, var, index, mode):
        if self.entry_composer_name.get() != '':
            self.checkbtn_compName.select()
        else:
            self.checkbtn_compName.deselect()

    def _write_callback_compNameEng(self, var, index, mode):
        if self.entry_composer_name_eng.get() != '':
            self.checkbtn_compNameEng.select()
        else:
            self.checkbtn_compNameEng.deselect()

    # entry에 복사 붙여넣기 할 수 있도록 하는 기능
    def ctrl_event(self, event):
        e_widget = event.widget
        self.txtbox_url.entryconfigure("Cut",command=lambda: e_widget.event_generate("<<Cut>>"))
        self.txtbox_url.entryconfigure("Copy",command=lambda: e_widget.event_generate("<<Copy>>"))
        self.txtbox_url.entryconfigure("Paste",command=lambda: e_widget.event_generate("<<Paste>>"))
        self.txtbox_url.tk.call("tk_popup", self.txtbox_url, event.x_root, event.y_root)  
    
    # 음원 사이트에 곡 검색하는 기능
    def searchSong(self):
        keyword_list = []
        # 곡 정보의 4개의 entry 각각에 어떤 값이 입력되어 있을 때 + 유저가 체크 박스를 활성화했을 때만 검색어에 포함시킴
        if self.var_include_songTitle.get() == 1 and self.entry_song_title.get() != '':
            keyword_list.append(self.entry_song_title.get())
        if self.var_include_songTitleEng.get() == 1 and self.entry_song_title_eng.get() != '':
            keyword_list.append(self.entry_song_title_eng.get())
        if self.var_include_compName.get() == 1 and self.entry_composer_name.get() != '':
            keyword_list.append(self.entry_composer_name.get())
        if self.var_include_compNameEng.get() == 1 and self.entry_composer_name_eng.get() != '':
            keyword_list.append(self.entry_composer_name_eng.get())

        # 검색할 음원 사이트 리스트에 저장
        website_list = []
        if self.var_am.get() == 1:
            website_list.append("amazon")
        if self.var_amjp.get() == 1:
            website_list.append("amazon jp")
        if self.var_oty.get() == 1:
            website_list.append("ototoy")
        if self.var_vibe.get() == 1:
            website_list.append("vibe")
        if self.var_bcamp.get() == 1:
            website_list.append("bandcamp")
        if self.var_reko.get() == 1:
            website_list.append("recochoku")

        # 1개 이상의 검색어가 있고 1개 이상의 음원 사이트를 선택한 경우에만 검색 진행
        if len(keyword_list) != 0 and len(website_list) != 0:
            for elem in website_list:
                self._openBrowser(elem, keyword_list)

    # 음원 사이트에서 자동으로 검색어들 입력시키는 기능
    def _openBrowser(self, site, keyword_list):
        open = False # 처음으로 여는 건지 이미 열린 window가 있는지 검사하는 용도
        if site == 'amazon':
            self.driver_amazon=set_chrome_driver()
            self.driver_list.append(self.driver_amazon)
            self.driver_amazon.get("https://amazon.com/")

            for keyword in keyword_list:
                if open: # 이미 열린 window가 있는 경우 그 window에 탭을 추가하는 방식
                    self.driver_amazon.switch_to.new_window('tab')
                    self.driver_amazon.get("https://amazon.com/")
                
                while True:
                    try:
                        elem = WebDriverWait(self.driver_amazon, 10).until(
                            EC.presence_of_element_located((By.ID, "twotabsearchtextbox"))
                        )
                        select=Select(self.driver_amazon.find_element(By.ID, 'searchDropdownBox'))
                        select.select_by_visible_text("Digital Music")
                        break
                    except:
                        # 아마존 사이트 중에 dropdown이 없는 사이트가 로딩될 경우 기다리면 자동으로 새로고침 됨
                        self.driver_amazon.refresh()

                try:
                    element = self.driver_amazon.find_element(By.ID, 'twotabsearchtextbox')
                except:
                    element = self.driver_amazon.find_element(By.ID, 'nav-bb-search')
                
                element.send_keys(keyword)

                try:
                    search_button = self.driver_amazon.find_element(By.ID, 'nav-search-submit-button')
                except:
                    search_button = self.driver_amazon.find_element(By.CLASS_NAME, 'nav-bb-button')

                search_button.click()
            
                self.driver_amazon.implicitly_wait(5)  
                open = True

        elif site == 'amazon jp':
            self.driver_amazonjp=set_chrome_driver()
            self.driver_list.append(self.driver_amazonjp)

            self.driver_amazonjp.get("https://amazon.co.jp/")

            for keyword in keyword_list:
                if open:   
                    self.driver_amazonjp.switch_to.new_window('tab')
                    self.driver_amazonjp.get("https://amazon.co.jp/")

                while True:
                    try:
                        elem = WebDriverWait(self.driver_amazonjp, 10).until(
                            EC.presence_of_element_located((By.ID, "twotabsearchtextbox"))
                        )
                        select=Select(self.driver_amazonjp.find_element(By.ID, 'searchDropdownBox'))
                        select.select_by_visible_text("Digital Music")
                        break
                    except:
                        # 아마존 재팬 사이트 중에 dropdown이 없는 사이트가 로딩될 경우 기다리면 자동으로 새로고침 됨
                        self.driver_amazonjp.refresh()

                try:
                    element = self.driver_amazonjp.find_element(By.ID, 'twotabsearchtextbox')
                except:
                    element = self.driver_amazonjp.find_element(By.ID, 'nav-bb-search')
                
                element.send_keys(keyword)

                try:
                    search_button = self.driver_amazonjp.find_element(By.ID, 'nav-search-submit-button')
                except:
                    search_button = self.driver_amazonjp.find_element(By.CLASS_NAME, 'nav-bb-button')

                search_button.click()
                self.driver_amazonjp.implicitly_wait(5)
                open = True

        elif site == 'ototoy':
            self.driver_ototoy=set_chrome_driver()
            self.driver_list.append(self.driver_ototoy)

            open = False
            self.driver_ototoy.get("https://ototoy.jp/")

            for keyword in keyword_list:
                if open:
                    self.driver_ototoy.switch_to.new_window('tab')
                    self.driver_ototoy.get("https://ototoy.jp/")

                try:
                    element = self.driver_ototoy.find_element(By.ID, 'search-start-button')
                    element.send_keys(Keys.ENTER)
                    self.driver_ototoy.implicitly_wait(5)
                except:
                    print('error1')
                    return

                try:
                    element = self.driver_ototoy.find_element(By.NAME, 'q')
                except Exception as e:
                    print(e)
                    return
                
                element.send_keys(keyword)

                try:
                    search_button = self.driver_ototoy.find_element(By.ID, 'search-submit-button')
                except:
                    return

                search_button.click()
                self.driver_ototoy.implicitly_wait(5)
                open = True

        elif site == 'vibe':
            self.driver_vibe=set_chrome_driver()
            self.driver_list.append(self.driver_vibe)

            open = False

            for keyword in keyword_list:
                if open:
                    self.driver_vibe.switch_to.new_window('tab')

                url = "https://vibe.naver.com/search?query={}".format(keyword.replace(' ', '+'))
                self.driver_vibe.get(url)

                self.driver_vibe.implicitly_wait(5)
                open = True

        elif site == "bandcamp":
            self.driver_bcamp=set_chrome_driver()
            self.driver_list.append(self.driver_bcamp)

            open = False
            self.driver_bcamp.get("https://bandcamp.com/")

            for keyword in keyword_list:
                if open:
                    self.driver_bcamp.switch_to.new_window('tab')
                    self.driver_bcamp.get("https://bandcamp.com/")

                try:
                    element = self.driver_bcamp.find_element(By.NAME, 'q')
                except Exception as e:
                    print(e)
                    return
                
                element.send_keys(keyword)
                element.send_keys(Keys.ENTER)

                self.driver_bcamp.implicitly_wait(5)
                open = True

        elif site == "recochoku":
            self.driver_reko=set_chrome_driver()
            self.driver_list.append(self.driver_reko)

            open = False
            self.driver_reko.get("https://recochoku.jp/")

            for keyword in keyword_list:
                if open:
                    self.driver_reko.switch_to.new_window('tab')
                    self.driver_reko.get("https://recochoku.jp/")
                try:
                    element = self.driver_reko.find_element(By.NAME, 'q')
                except Exception as e:
                    print(e)
                    return
                
                element.send_keys(keyword)
                element.send_keys(Keys.ENTER)

                self.driver_reko.implicitly_wait(5)
                open = True

    # 도움말 element에 커서를 가져다 댄 경우 보임
    def show_help(self, event):
        self.lbl_urlHelp = tkinter.Label(self.window, text="유튜브 링크를 입력한 후 곡 정보 가져오기 버튼을 눌러주세요.", font = self.entrytxt_font, width=47, height=1,fg="green", bg = "white")
        self.lbl_urlHelp.place(x=220,y=139)

        self.lbl_tmbnailHelp = tkinter.Label(self.window, text="썸네일이 자동으로 추가됩니다", font = self.normaltxt_font, width=20, height=1,fg="green", bg = "#c6c6c6")
        self.lbl_tmbnailHelp.place(x=55,y=302)

        self.lbl_entryHelp1 = tkinter.Label(self.window, text="영상의 제목이 자동으로 추가됩니다.", font = self.entrytxt_font, width=28, height=1,fg="green", bg = "white")
        self.lbl_entryHelp1.place(x=510,y=248)
        self.lbl_entryHelp2 = tkinter.Label(self.window, text="추가로 검색하고 싶은 내용을 입력하세요", font = self.entrytxt_font, width=28, height=1,fg="green", bg = "white")
        self.lbl_entryHelp2.place(x=500,y=285)
        self.lbl_entryHelp3 = tkinter.Label(self.window, text="채널명이 자동으로 추가됩니다", font = self.entrytxt_font, width=28, height=1,fg="green", bg = "white")
        self.lbl_entryHelp3.place(x=500,y=323)
        self.lbl_entryHelp4 = tkinter.Label(self.window, text="추가로 검색하고 싶은 내용을 입력하세요", font = self.entrytxt_font, width=28, height=1,fg="green", bg = "white")
        self.lbl_entryHelp4.place(x=500,y=360)
        self.lbl_entryHelp5 = tkinter.Label(self.window, text="* 검색어는 직접 수정하실 수 있습니다.", font = self.normaltxt_font, width=30, height=1,fg="green")
        self.lbl_entryHelp5.place(x=450,y=395)
        self.lbl_entryHelp6 = tkinter.Label(self.window, text="* 박스가 체크되어 있는 항목만 검색됩니다.", font = self.normaltxt_font, width=30, height=1,fg="green")
        self.lbl_entryHelp6.place(x=450,y=430)

        self.lbl_searchHelp = tkinter.Label(self.window, text="검색을 진행할 사이트들을 선택한 후 검색하기 버튼을 눌러주세요.", font = self.normaltxt_font, width=45, height=1,fg="green")
        self.lbl_searchHelp.place(x=150,y=590)

    # 도움말 element에 커서를 뗀 경우 사라짐
    def hide_help(self, event):
        self.lbl_urlHelp.place_forget()
        self.lbl_tmbnailHelp.place_forget()
        self.lbl_entryHelp1.place_forget()
        self.lbl_entryHelp2.place_forget()
        self.lbl_entryHelp3.place_forget()
        self.lbl_entryHelp4.place_forget()
        self.lbl_entryHelp5.place_forget()
        self.lbl_entryHelp6.place_forget()
        self.lbl_searchHelp.place_forget()
        
    # 음원 검색 tip window 여는 기능
    def show_tip(self):
        self.sub_win= tkinter.Toplevel(self.window)
        self.sub_win.geometry(("610x400+100+100"))
        self.sub_win.title("음원 검색 tip")

        self.lbl_tip = tkinter.Label(self.sub_win, text="* j pop 음원 검색 위주의 팁입니다.\n\n* 아마존에 음원을 검색하기 전에 네이버 vibe에서 검색해보는 걸\n추천드립니다.생각보다 많은 음원이 판매되고 있습니다.\n\n* 곡 이름의 영어 버전과 원곡자 닉네임/이름의 영어 버전도\n함께 검색해보세요. (ex: 死ぬな! -> SHINUNA!)\n보통은 나무위키에서 찾으실 수 있지만, 없는 경우 구글에\n“(곡 이름)+lyrics”라고 검색하시면 영어로 번역된 제목이 나올겁니다.\n\n*음원 사이트에서 원곡자가 발매된 곡들 리스트 중 찾으시는 곡이\n보이지 않는 경우에는 곡을 포함하고 있는 앨범의 이름을\n검색해보세요. 콜라보 앨범에 수록된 곡일 경우 이런 식으로\n해야 찾기 쉽습니다.", font = self.normaltxt_font,fg="black", relief="flat",anchor="w", justify="left")
        self.lbl_tip.place(x=10, y=10)

if __name__ == '__main__':
    freeze_support() # 무한 로딩 방지용
    program = MainWindow()
    try:
        # 열려있는 window가 있는 경우 프로그램을 종료하면 같이 종료됨
        for elem in program.driver_list:
            elem.quit()
    except:
        pass