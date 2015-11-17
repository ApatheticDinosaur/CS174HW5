__author__ = 'Andy'

from bs4 import BeautifulSoup
from collections import defaultdict
import urllib.request, webbrowser, os.path

#Open a connection with the url and create a soup
try:
    html = urllib.request.urlopen("https://www.open2study.com/courses")
    soup = BeautifulSoup(html, "html.parser")
    html.close()
except IOError:
    print('Cannot open URL')

#dictionary for course, title is key and a list with image source and link is the value
courses = defaultdict(list)

#Find all of the courses in the soup
for div in soup.findAll("div", {"class" : "courses_adblock_start"}):
    course_title = ""
    course_image = ""
    course_link = ""
    for child in div.children: #get course title and image source
        if(child.name == "h2"): #title is in an h2 tag
            course_title = child.contents[0]
        if(child.name == "figure"): #image is in a figure tag
            image_content = child.contents[0].attrs
            course_image = image_content['src']
    for parent in div.parents: #get link from parent tag
        if parent.name == "a":
            course_link = parent.attrs['href']
    courses[course_title].append([course_image, course_link])

#HTML template start
pageTemplateStart = '''
<html>
<head>
<link rel="stylesheet" type="text/css" href="./style.css">
</head>
<body>
<div>'''

#Course template to be added to the starting template
pageTemplateCourse = '''
<div class="course">
<div class="image">
<a href="https://www.open2study.com{0}">
<img src="{1}" border="0">
</a>
</div>
<div class="title">{2}
</div>
</div>'''

#End of the template
pageTemplateEnd = '''
<div>
<a href="./report.txt">Report</a>
</div>
</div>
</body>
</html>'''

#Add every course's content to the templete and add to the main template
for key in courses:
    #print(courses.get(key))
    course_content = courses.get(key)[0]
    newCourse = pageTemplateCourse.format(course_content[1], course_content[0], key)
    pageTemplateStart += newCourse

#Add the end template
pageTemplateStart += pageTemplateEnd

#Write the string to a html file to open with the browser
output = open("index.html", "w")
output.write(pageTemplateStart)
output.close()

#Open html file
webbrowser.open("file:///" + os.path.abspath("index.html"))