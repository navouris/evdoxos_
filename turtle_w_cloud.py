__author__ = 'user'
import turtle as t
import random
import tkinter

MINIMUM_VISIBLE_FONT = 10

class Word():
    all_words = []

    def __init__(self, text, x,y, w,h, areax, areay, r,g,b):
        self.text = text
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.r = r
        self.g = g
        self.b = b
        self.left = self.x
        self.right = self.x + w
        self.top = self.y + h
        self.bottom = self.y
        self.areax = areax
        self.areay = areay
        Word.all_words.append(self)
        print("number of Word objects =", len(Word.all_words))
        self.turtle = t.Turtle()
        self.turtle.penup()
        #self.draw_outline()  # only for debugging purposes
        self.overlap_areas=[]
        self.check_collisions()
        self.draw_word()
        #
        #self.rect_collision()

    def check_collisions(self):
        count =0

        # check 10 times and if all overlap draw at the best choice
        for places in range(15):
            count += 1
            print("check_collisions.................... round", count, "for position", self.x, self.y)
            overlap_area = 0
            for other_word in Word.all_words:
                if other_word is not self :
                    overlap_area += self.overlaps(other_word)
            print("after checking all object it was found that overlap = ", overlap_area)
            if overlap_area:
                self.overlap_areas.append([self.x, self.y, overlap_area])
                self.update_position()
                #self.draw_outline() # to be removed only for debugging
            else:
                return 1
        self.find_best_place()
        return 1

    def update_position(self):
        self.x = random.randrange(self.areax[0], self.areax[1])
        self.y = random.randrange(self.areay[0], self.areay[1])
        self.left = self.x
        self.right = self.x + self.w
        self.top = self.y + self.h
        self.bottom = self.y

    def find_best_place(self):
        # the optimal solution is that of less overlap area
        print("find_best_place", self.overlap_areas)
        min_overlap = abs(self.areax[1]-self.areax[0]) * abs(self.areay[1]-self.areay[0])
        for place in self.overlap_areas:
            if place[2]< min_overlap:
                self.x = place[0]
                self.y = place[1]
                self.left = self.x
                self.right = self.x + self.w
                self.top = self.y + self.h
                self.bottom = self.y
                min_overlap = place[2]

    def overlaps(self, obstacle):
    #Overlapping rectangles overlap both horizontally & vertically, this calculates the area
    # of overlap between self and obstacle
        (x_overlap,y_overlap) = (0,0)
        print("checking overlap " + obstacle.text + "...x=" + str(obstacle.left) + "..." + str(obstacle.right) + " y=" + str(obstacle.top) + "..." + str(obstacle.bottom))
        print("with self... " +  self.text + "...x=" + str( self.left) + "..." + str( self.right) + " y=" + str( self.top) + "..." + str( self.bottom))#check for horizontal overlap
        if (self.left >= obstacle.right) or (self.right <= obstacle.left):
            return 0
        else:
            x_overlap = min(self.right,obstacle.right) - max(self.left, obstacle.left)
        #check for vertical overlap
        if (self.top <= obstacle.bottom) or (self.bottom >= obstacle.top):
            return 0
        else:
            y_overlap = min(self.top,obstacle.top) - max(self.bottom, obstacle.bottom)
        print ("overlap found = ", x_overlap * y_overlap)
        return x_overlap * y_overlap


    def draw_word(self) :
        #input('draw_word x= '+str(self.x)+" y=  "+str(self.y))
        self.turtle._tracer()
        self.turtle.speed('fastest')
        self.turtle.ht()
        self.turtle.setpos(self.x, self.y)
        self.turtle.pendown()
        self.turtle.color(self.r, self.g, self.b)
        self.turtle.write(self.text, align='left', font =("Arial", int(self.h*0.8), "normal"))
        self.turtle._update()
        #a.end_fill()
        self.turtle.penup()

    def draw_outline(self) :
        input('draw outline x= '+str(self.x)+" y=  "+str(self.y)+"of height ="+str(self.h*0.8))

        self.turtle.penup()
        self.turtle.speed('fastest')
        self.turtle.ht()
        self.turtle.color('red')
        self.turtle.setpos(self.x, self.y)
        print(self.x, self.y)
        self.turtle.pendown()
        self.turtle.goto(self.x+self.w, self.y)
        self.turtle.goto(self.x+self.w, self.y+self.h)
        self.turtle.goto(self.x, self.y+self.h)
        self.turtle.goto(self.x, self.y)
        print(self.x+self.w, self.y)
        print(self.x+self.w, self.y+self.h)
        print(self.x, self.y+self.h)
        print(self.x, self.y)
        self.turtle.penup()


#
# WEIGHT = 0.5
# max_weight = 50
# main_term = new_strings[0]
# main_frequency = int(main_term[1])
# # let us suppose that we use the max value of weight
# # then calculate the length of the word
# w_length = len(main_term)*max_weight

#

# def process_text(text):
#     strings = text.split('\n')
#     new_strings=[]
#     for x in strings:
#         x_new = x.strip().split(' ')
#         if len(x_new[0])>2 and x_new[1].isdigit():
#             new_strings.append(x_new)
#     #print (new_strings)
#     new_strings = sorted(new_strings, key=lambda x: int(x[1]), reverse=True)
#     # for x in new_strings:
#     #     print (x)
#     return new_strings[:50]

def process_text(text):
    #
    new_strings = []
    for w in sorted(text, key=text.get, reverse=True):
        new_strings.append ([w.lower(), text[w]])
    #new_strings = sorted(new_strings, key=lambda x: int(x[1]), reverse=True)
    # for x in new_strings:
    #     print (x)
    return new_strings[:50]

def calculate_word_rectangle(word, font_size=''):
    #this is the reference measure on turtle for Arial size 400 in pixels
    # we should add len( word)*55+15
    print("calculate rectangle",word, font_size)
    ref_font_size = 400
    if font_size == '': font_size = ref_font_size
    if font_size < MINIMUM_VISIBLE_FONT : font_size = MINIMUM_VISIBLE_FONT
    ttf_rectangles= {"α": 270, "β": 270,"γ": 220, "δ": 270, "ε": 200, "ζ": 200,
                     "η": 270, "θ": 270, "ι": 50, "κ": 270, "λ": 220, "μ": 270,
                    "ν": 220, "ξ": 200, "ο": 270, "π": 340, "ρ": 270, "σ": 270,
                    "τ": 180, "υ": 250, "φ": 370, "χ": 255, "ψ": 335, "ω": 380, "ς": 235}
    width = 0
    for letter in word:
        if letter in ttf_rectangles.keys():
            width += ttf_rectangles[letter]
    width += 50*len(word)+15
    height = 500
    print ("word rectangle is ...", int((font_size/ref_font_size)*width),int((font_size/ref_font_size)*height))
    return (int((font_size/ref_font_size)*width),int((font_size/ref_font_size)*height))

def calculate_max_font(string, screen_x):
    ref_font_size = 400
    (ref_x, ref_y) = calculate_word_rectangle (string, ref_font_size)
    print("calculate max font", ref_x)
    max_font = ref_font_size*(screen_x/ref_x)
    print ("calculate max_font", max_font)
    return max_font


def print_xy(x,y):
    print (str(x)+"  "+str(y))


def calculate_optimal_congestion_font(strings, con_rate, ref_font, screen_x, screen_y, max_freq):
    import math
    area = 0
    for s in strings:
        (s_w, s_h) = calculate_word_rectangle(s[0], ref_font*(int(s[1])/max_freq))
        area += s_w*s_h
    optimal_font = round(ref_font*math.sqrt( (screen_x * screen_y)* con_rate/area))
    return optimal_font

def find_best_font_fit(strings, screen_x, screen_y) :
    con_rate = 0.6
    error = 0.5
    ref_font = 400
    max_freq = int(strings[0][1])
    max_freq_length = len(strings[0][0])
    print ("most popular term f, l = ", max_freq, " ", max_freq_length)
    f1 = calculate_max_font(strings[0][0], screen_x-40)
    f2 = calculate_optimal_congestion_font(strings, con_rate, ref_font, screen_x, screen_y, max_freq)
    print (f1, ".........", f2)
    return int(min(f1,f2))

#
# new_text =  process_text(text2)
# print("length of terms = ",len(new_text))
# print (find_best_font_fit(new_text[:30]))


def draw_cloud(t, screen_xy):
    new_strings = process_text(t)
    #limit the word cloud to be drawn to just 40 words
    font_size = 70
    max_freq = int(new_strings[0][1])
    minx = -int(screen_xy[0]/2)
    maxx = int(screen_xy[0]/2)
    miny = - int(screen_xy[1]/2)
    maxy = int(screen_xy[1]/2)
    padxy = 10
    new_font_size = find_best_font_fit(new_strings[:40], screen_xy[0]-2*padxy, screen_xy[1]-2*padxy)
    print('new_font_size=', new_font_size)
    print (minx, maxx, miny, maxy, padxy)
    for word in new_strings[:40]:
        r = random.randrange(120, 255)
        g = random.randrange(120, 255)
        b = random.randrange(50, 150)
        (w,h) = calculate_word_rectangle(word[0],int(new_font_size*int(word[1])/max_freq))
        print (w,h)
        areax = minx+padxy, maxx-w-padxy
        areay = miny+padxy, maxy-h-padxy
        print("areax, areay ...", areax, areay)
        x = random.randrange(areax[0], areax[1])
        y = random.randrange(areay[0], areay[1])
        Word(word[0], x, y, w, h, areax, areay, r,g,b)
    #wn.clear()

# for word in new_strings:
#     print (calculate_word_rectangle(word[0], 400))

def handler():
    ts = t._getscreen()
    ts.getcanvas().postcript(file = "file1.eps")
    wn.exit()


def show_word_cloud(uni_dept, wc):

    wn = t.Screen() # Creates a turtle object
    #define max string and normalize the rest
    wn.bgcolor ('black')
    wn.screensize(600, 600)
    wn.setup( startx = 500, starty = 50)
    screen_xy  = wn.screensize()
    print(screen_xy)
    wn.colormode(255)
    wn.title(uni_dept)
    a = t.Turtle()
    a.ht()
    a.penup()
    draw_cloud(wc, screen_xy )
    wn.onscreenclick(handler)
    #wn.mainloop()             # Wait for user to close window

if __name__ == '__main__':
    show_word_cloud()