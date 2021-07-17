# XKCD Webscraping TUI
> A software to scrape comic title, id, url, image url and the alternative text from the website [xkcd](https://xkcd.com/) in form of a Text-based User Inferface (Terminal-based User Interface) (TUI)


## Tools & Technologies
![https://www.python.org/](https://img.shields.io/badge/Code-Python-idk?style=flat&logo=python&logoColor=white&color=ff00)
![https://pypi.org/project/bs4/](https://img.shields.io/badge/Technology-BeautifulSoup-idk?style=flat&logo=scrapy&logoColor=white&color=ff00)
![https://pypi.org/project/img2text/](https://img.shields.io/badge/Technology-img2text-idk?style=flat&logo=img2text&logoColor=white&color=ff00)
![https://pypi.org/project/psutil/](https://img.shields.io/badge/Technology-psutil-idk?style=flat&logo=psutil&logoColor=white&color=ff00)
![](https://img.shields.io/badge/Technology-Curses-idk?style=flat&logo=curses&logoColor=white&color=ff00)
![https://github.com/git/git-scm.com/blob/main/MIT-LICENSE.txt](https://img.shields.io/badge/License-MIT-idk?style=flat&logo=windows-curses&logoColor=white&color=ff00)

## Features
+ scrape comic title, id, url, image url and the alternative text from [xkcd](https://xkcd.com/)
+ scrape a specific queue with comic id's from [xkcd](https://xkcd.com/) (800-1000)
+ save scraped comic data in a json/csv file
+ CPU usage
+ GPU usage

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
+ click on `Show Image` to show the image in console in ASCII art (picture 2&3)
+ with buttons `Back` & `Next` you can switch between results
+ see the magic
![](/images/start_tui.png)
![](/images/executed_tui.png)
![](/images/ASCII_image_tui.png)

## Installation

Clone this repository

```bash
  git clone git@github.com:aiyayayaya/canny-capybaras-collab-code-contest.git
```

Create a virtual environment (in this example  we will be using [pipenv](https://pypi.org/project/pipenv/))

```bash
  pipenv --python 3.9
```

Install the required packages

```bash
  pipenv install -r requirement.txt
  pipenv install -d dev-requirements.txt
```

Run the project

```bash
  pipenv run py <start_file>
```
## Authors

- [@aiyayayaya](https://www.github.com/aiyayayaya)
- [@miladog](https://www.github.com/miladog)
- [@mariothedog](https://www.github.com/mariothedog)
- [@paulchen5](https://www.github.com/paulchen5)
- [@voidoffi](https://www.github.com/voidoffi)
- [@marty321](https://www.github.com/marty321)
