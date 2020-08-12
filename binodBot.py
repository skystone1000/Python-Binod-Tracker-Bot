from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import re

total_comments_xpath = '/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[4]/div[1]/div/ytd-comments/ytd-item-section-renderer/div[1]/ytd-comments-header-renderer/div[1]/h2/yt-formatted-string'
keyword_list = ['Binod','binod','BINOD']

class BinodBot():
    def __init__(self):
        self.browserProfile = webdriver.ChromeOptions()
        self.browser = webdriver.Chrome(ChromeDriverManager().install(), options=self.browserProfile)
        self.browser.get('https://www.youtube.com/watch?v=n8vlEklS3gA')
        self.browser.maximize_window()

    def scroll_to_bottom_of_page(self):
        sleep(5)

        get_scroll_height_command = (
            "return (document.documentElement || document.body).scrollHeight;"
        )
        scroll_to_command = "scrollTo(0, {});"

        y_position = 0
        scroll_height = self.browser.execute_script(get_scroll_height_command)
        print("Scrolling to bottom")

        loopCount = 0
        while y_position != scroll_height:
            print("Scroll Count : {}".format(loopCount))
            loopCount = loopCount + 1
            if(loopCount > 20):
                break
            y_position = scroll_height
            self.browser.execute_script(scroll_to_command.format(scroll_height))
            sleep(1)
            scroll_height = self.browser.execute_script(get_scroll_height_command)

    def comments(self):
        self.browser.execute_script("window.scrollTo(0,720)")
        sleep(3)

        totalComments = self.browser.find_element_by_xpath(total_comments_xpath).text
        totalComments = re.sub('\D','',totalComments)
        totalComments = int(totalComments.replace(',',''))
        print("Total Comments = {}".format(totalComments))

        # Scroll to bottom
        self.scroll_to_bottom_of_page()

        # Getting comments
        print("Creating Comments List ")
        comment_list = [
            comment_element.text + "\n\n"
            for comment_element in self.browser.find_elements_by_xpath(
                "//*[@id='content-text']"
            )
        ]

        # Get BINOD comments (LOL)
        print("Searching Binod Comments .. ")
        BinodCount = 0
        saved_comments = []
        for comment in comment_list:
            for keyword in keyword_list:
                if keyword in comment:
                    print("-------------------------------------------")
                    print("Binod Count : {}".format(BinodCount))
                    BinodCount = BinodCount + 1
                    print(comment)
                    saved_comments.append(comment)
                    break

        print("=========================")
        # print(saved_comments)
        self.save_to_file(saved_comments)

        
    def save_to_file(self,saved_comments):
        # Saving comments in file
        print("========================")
        if saved_comments:
            print("Writing comment to file")
            with open(
                "BINOD.txt","a+"
            ) as comment_file:
                comment_file.writelines(saved_comments)
                comment_file.write(" ---------------------------------------------------- \n\n\n")



bot = BinodBot()
sleep(5)
bot.comments()