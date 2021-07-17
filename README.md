# XKCD Websraping TUI 
> A software to scrape comic title, id, url, image url and the alternative text from the website [xkcd](https://xkcd.com/) in form of a textuserinterface (TUI) 


## Tools & Technologies 
![](https://img.shields.io/badge/Editor-VSC-idk?style=flat&logo=visual-studio-code&logoColor=white&color=ff00) 
![](https://img.shields.io/badge/Code-Python-idk?style=flat&logo=python&logoColor=white&color=ff00)
![](https://img.shields.io/badge/Technologie-Scrapy-idk?style=flat&logo=scrapy&logoColor=white&color=ff00)
![](https://img.shields.io/badge/Technologie-img2text-idk?style=flat&logo=img2text&logoColor=white&color=ff00)
![](https://img.shields.io/badge/Technologie-psutil-idk?style=flat&logo=psutil&logoColor=white&color=ff00)

## Features 
+ scrape comic title, id, url, image url and the alternative text from [xkcd](https://xkcd.com/)
+ scrape a specific queue with comic id's from [xkcd](https://xkcd.com/) (800-1000)
+ save scraped comic data in a json/csv file
+ CPU ussage
+ GPU ussage

## How it works?
+ go to field `Comic ID(s):` and enter the number of your comic id's
  + input format for **one** ID `1000`
  + input format for more specific ID's `1, 800, 1000`
  + input format for several comic ID's `800-1000`
  + input format for **one** specific ID and several ID's in a range `1, 800-1000`
  + input format for several queues of ID's `1-50, 800-1000`
+ to select the file format of the output click on the text behind `File Format:`
  + can change between JSON or CSV
+ click on `START` to start crawling process
+ click on `Show Image` to show the image in console in ASCII art
+ with buttons `Back` & `Next` you can switch between results
+ see the magic
![](/images/start_tui.png)
![](/images/executed_tui.png)
![](/images/ASCII_image_tui.png)
