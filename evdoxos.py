class uni():
    def __init__(self,name):
        self.name = name
        self.dept =[]

    def create_dept(self, dept_name, dept_code=""):
        self.dept.append(dept(dept_name, dept_code))

    def get_depts(self):
        return dept

    def __str__(self):
        return self.name

class dept(uni):
    def __init__(self, uni, name, code):
        self.name = name
        self.code = code

    def get_dept(self, code):
        if self.code == code:
            return self.name
        else:
            return 0

class course():
    def __init__(self, uni, dept, code, name, semester="", autumn=""):
        self.uni = str(uni)
        self.dept = str(dept)
        self.code = str(code)
        self.name = name
        self.semester = str(semester)
        self.autumn = autumn

    def get_code(self):
        return self.code

    def __str__(self):
        return self.uni+"-"+self.dept+";"+self.code+";"+ self.name+";"+str(self.semester)+";"+self.autumn

    def get_course(self):
        return self.code+"\t"+ self.name+"\t"+str(self.semester)+"\t"+self.autumn

class book():
    def __init__(self, code, name):
        self.code = code
        self.name = name

    def __str__(self):
        return self.code+";"+self.name

    def get_code(self):
        return self.code


class relate_course_book(course, book):
    def __init__(self, c, b):
        self.course = c
        self.book =  b

    def get_book(self):
        return self.book

    def get_course(self):
        return self.course

    def get_relation(self):
        return (self.course, self.book)

    def __str__(self):
        return self.course.code+";"+self.course.name+";"+self.book.code+";"+self.book.name

