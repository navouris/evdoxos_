### N Avouris extract programs and books from evdoxos.gr tested on December 2015

from bs4 import BeautifulSoup
import csv
import evdoxos

YEAR = '2016'
UNI =  'Πανεπιστήμιο Πατρών'
DEPT = u'ΗΛΕΚΤΡΟΛΟΓΩΝ ΜΗΧΑΝΙΚΩΝ ΚΑΙ ΤΕΧΝΟΛΟΓΙΑΣ ΥΠΟΛΟΓΙΣΤΩΝ'
FIND_BOOKS = False

courses = []
books = []
relate = []

#import httplib

#import requests
#import urllib2
import urllib.request

def get_name(tag):
    #print (tag)
    t = tag.find(":") + 1
    e = tag.find("Λεπτομέρειες")
    if e != -1:
        return tag[t:e].strip()
    else:
        return tag[t:].strip()

def get_code(tag):
    f1=tag.find("[")
    f2=tag.find("]")
    return tag[f1+1:f2]

def get_course_semester(tag):
    t = tag.split()
    for x in t:
        if x.isdigit():
            return x
    return 0

def get_autumn_spring(tag):
    t = tag.split()
    return t[-1]

def print_course(dep,course):
    c=dep+";"+course['code']+";"+course['semester']+";"+course['autumn']+';'+course['name']
    print(c)

def find_courses(url2,department, uni):
    FIND_BOOKS = False
    courses=[]
    #global books, courses, relate
    print(department, "\n", url2)
    out ="{}\n{}\nΠρόγραμμα Σπουδών:\n".format(uni,department)
    print (out)
    try:
        with urllib.request.urlopen(url2) as response:
            result = response.read()
        soup = BeautifulSoup(result)
    except:
        return  "error connecting with web page "+url2

    course={}
    book={}
    assoc = []
    #print ("============>\n",soup)
    count_tags=0
    for t in soup.find_all():
        count_tags += 1
        print(count_tags, t.name)
        if t.name == 'h2' and ":" in t.get_text():
            print("found course", t.get_text())
            course['name'] = get_name(t.get_text())
            course['code'] = get_code(t.get_text())
        elif t.name == "h3" and "Εξάμηνο" in t.get_text():
            print("found semester", t.get_text())
            course["semester"] =  get_course_semester(t.get_text())
            course['autumn'] = get_autumn_spring(t.get_text())
            out += print_course(department, course)+"\n"
            for c in courses:
                if c.get_code() == course['code']:
                    x = c
                else:
                    x = evdoxos.course(uni, department, course['code'],course['name'], course['semester'], course['autumn'])
                    courses.append(x)
    #print (out)
    return out


def print_courses_old(url2,department):
    global books, courses, relate
    #print(department, "\n", url2)
    with urllib.request.urlopen(url2) as response:
        html = response.read()
    soup = BeautifulSoup(html)
    course={}
    book={}
    assoc = []
    for tag in soup.find_all():
        if tag.name == 'h2' and "Μάθημα" in tag.get_text():
            course['name'] = get_name(tag.get_text())
            course['code'] = get_code(tag.get_text())
        if tag.name == "h3" and "Εξάμηνο" in tag.get_text():
            course["semester"] =  get_course_semester(tag.get_text())
            course['autumn'] = get_autumn_spring(tag.get_text())
            print_course(department, course)
            c = evdoxos.course(department, course['code'],course['name'], course['semester'], course['autumn'])
            courses.append(c)
        if tag.name == "ol" and FIND_BOOKS :
            for b in tag.descendants:
                if b.name == 'li':
                    #print (b.get_text())
                    book['code'] = get_code(b.get_text())
                    book['name'] = get_name(b.get_text())
                    if len(book['code']) > 0 and [course['code'], book['code']] not in assoc:
                        #print("\t\t",book['code'],": ", book['name'])
                        b = evdoxos.book(book['code'], book['name'] )
                        books.append(b)
                        r = evdoxos.relate_course_book(c,b)
                        relate.append(r)
                        assoc.append([course['code'], book['code']])
    # for i in assoc:
    #     print ( "course", i[0], ": ", i[1])

    ######### count books ###########
    count  = 0
    uniquebooks =[]
    uniquecourses = []
    for i in assoc:
        if i[1] not in uniquebooks:
            uniquebooks.append(i[1])
    print("total books in ", DEPT, ": ", len(uniquebooks))

    for i in assoc:
        if i[0] not in uniquecourses:
            uniquecourses.append(i[0])
    print("total courses in ", DEPT, ": ", len(uniquecourses))



####### main ##################################################################


def search_in_dept(url1, university):

    #url1 = input("Enter a website to extract the URL's from: ")
    # print(url1)
    with urllib.request.urlopen(url1) as response:
        h  = response.read()
    #h = urllib2.urlopen(url1).read()
    # soup = BeautifulSoup(url1, 'html.parser')

    soup = BeautifulSoup(h)

    # search for university in list
    uni=False
    acad_year = int(YEAR)-1
    acad_year = str(acad_year)
    acad_year = acad_year + " - " + str(YEAR)
    acad_year = 'Πρόγραμμα Σπουδών ('+ acad_year + ")"
    print ("Academic year = ", acad_year)

    for tag in soup.find_all():
        #print(tag.get_text())
        if tag.name == 'h2':
            if tag.get_text() == university:
                uni = True
            else:
                uni = False
        if uni:
            if tag.name == 'p':
                department = tag.get_text()
            if tag.name == 'a' and department == DEPT:
                #if tag.get_text() == u'Πρόγραμμα Σπουδών (2015 - 2016)':
                if tag.get_text() == acad_year:
                    url2 = tag['href']
                    url2= "https://service.eudoxus.gr"+url2
                    print_courses(url2,department)

########## print to csv file #########################################

def search_for_unis(url1):
    unis = []
#this will look for all universities found in url1
    with urllib.request.urlopen(url1) as response:
        h  = response.read()
    soup = BeautifulSoup(h)

    # search for university in list
    uni=False
    acad_year = int(YEAR)-1
    acad_year = str(acad_year)
    acad_year = acad_year + " - " + str(YEAR)
    acad_year = 'Πρόγραμμα Σπουδών ('+ acad_year + ")"
    #print ("Academic year = ", acad_year)

    for tag in soup.find_all():
        #print(tag.get_text())
        if tag.name == 'h2':
            unix = tag.get_text()
            if unix not in unis and unix not in ['Λίστα Ιδρυμάτων και Τμημάτων', 'Περιεχόμενα']:
                unis.append(unix)
    return unis

## it returns all the departments of a specific University as a dictionary with key the department name and value it s url
def search_for_departments(url, university):
    print(university)
    # search for the departments of uni
    with urllib.request.urlopen(url) as response:
        h  = response.read()
    soup = BeautifulSoup(h)

    # search for university in list
    uni=False
    depts={}
    acad_year = int(YEAR)-1
    acad_year = str(acad_year)
    acad_year = acad_year + " - " + str(YEAR)
    #acad_year = 'Πρόγραμμα Σπουδών ('+ acad_year + ")"
    print ("Academic year = ", acad_year)

    for tag in soup.find_all():
        #print(tag.get_text())
        if tag.name == 'h2':
            #print(tag.get_text())
            if university in tag.get_text() :
                uni = True
            else:
                uni = False
        if uni:
            if tag.name == 'p':
                #print(tag.get_text())
                department = tag.get_text()
                if department not in depts.keys():
                    depts[department] = ""
            if tag.name == 'a' :
            #if tag.get_text() == u'Πρόγραμμα Σπουδών (2015 - 2016)':
                if acad_year in tag.get_text() :
                    print (tag.get_text())
                    url2 = tag['href']
                    url2= "https://service.eudoxus.gr"+url2
                    depts[department] = url2
                    #print_courses(url2,department)
    print(depts)
    return depts

#------------------------------------------------------------------
def get_name(tag):
    #print (tag)
    t = tag.find(":") + 1
    e = tag.find("Λεπτομέρειες")
    if e != -1:
        return tag[t:e].strip()
    else:
        return tag[t:].strip()

def get_code(tag):
    f1=tag.find("[")
    f2=tag.find("]")
    return tag[f1+1:f2]

def get_course_semester(tag):
    t = tag.split()
    for x in t:
        if x.isdigit():
            return x
    return 0

def get_autumn_spring(tag):
    t = tag.split()
    return t[-1]

def print_course(dep,course):
    c=course['code']+";"+course['semester']+";"+course['autumn']+';'+course['name']
    print("------------------>", c)
    return(c)

def find_courses(url2,department, uni):
    FIND_BOOKS = False
    courses=[]
    #global books, courses, relate
    print(department, "\n", url2)
    out ="{}\n{}\nΠρόγραμμα Σπουδών:\n".format(uni,department)
    print (out)
    try:
        with urllib.request.urlopen(url2) as response:
            result = response.read()
        soup = BeautifulSoup(result)
    except:
        return  "error connecting with web page "+url2

    course={}
    book={}
    assoc = []
    #print ("============>\n",soup)
    count_tags=0
    for t in soup.find_all():
        count_tags += 1
        print(count_tags, t.name)
        if t.name == 'h2' and ":" in t.get_text():
            print("found course", t.get_text())
            course['name'] = get_name(t.get_text())
            course['code'] = get_code(t.get_text())
        elif t.name == "h3" and "Εξάμηνο" in t.get_text():
            print("found semester", t.get_text())
            course["semester"] =  get_course_semester(t.get_text())
            course['autumn'] = get_autumn_spring(t.get_text())
            course_out = print_course(department, course)+"\n"
            out += course_out
            for c in courses:
                if c.get_code() == course['code']:
                    x = c
                else:
                    x = evdoxos.course(uni, department, course['code'],course['name'], course['semester'], course['autumn'])
                    courses.append(x)
    #print (out)
    return out

#this is the main not to run in gui mode
# url1 = 'https://service.eudoxus.gr/public/departments'
# #search_in_dept(url1, u'ΠΑΝΕΠΙΣΤΗΜΙΟ ΠΑΤΡΩΝ')
#
# u = search_for_unis(url1)
#
# for uni in u:
#     print(uni)
#     d = search_for_departments(url1, uni)
#     for dept in d:
#         print("...", dept, d[dept])
#     x = input("x for exit")
#     if x == "x":
#         break





#===========books
for i in books:
     print (i)
     for x in relate:
         if x.get_book() == i:
             print ("\t", x.get_course())


for j in courses:
    print(j)
    for x in relate:
        if x.get_course() == j:
            print ("\t", x.get_book())

# for x in relate:
#     print (x.course, x.book)



