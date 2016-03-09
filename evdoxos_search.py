import sqlite3 as lite
import evdoxos
import stemmer
import turtle_w_cloud
db = "evdoxos_db"

def greek_to_upper(w):
    gr_up = {'Ύ':'Υ', 'Έ':'Ε', 'Ά':'Α', 'Ό':'Ο', 'Ί':'Ι', 'Ή':'Η', 'Ώ':'Ω'}
    w_up = w.upper().strip()
    for x in gr_up:
        w_up = w_up.replace(x, gr_up[x])
    return w_up

def establish_set_of_keywords(keyword):
    keyword = keyword.strip()
    terms =[keyword]
    if keyword.upper() == keyword :
        key_l = keyword.lower()
        terms.append(keyword.lower())
        terms.append(keyword.title())
        terms.append(keyword.capitalize())
        key_title = key_l.title()
    else:
        key_u = keyword.upper()
        terms.append(key_u)
        # eliminated accedent characters from capital letters
        key_u = key_u.replace('Ύ','Υ')
        key_u = key_u.replace('Έ','Ε')
        key_u = key_u.replace('Ά','Α')
        key_u = key_u.replace('Ό','Ο')
        key_u = key_u.replace('Ί','Ι')
        key_u = key_u.replace('Ή','Η')
        key_u = key_u.replace('Ώ','Ω')
        terms.append(key_u)
    return (set(terms))

def get_uni_name(uni_id):
    try:
        con = lite.connect(db)
        with con:
            con.row_factory = lite.Row
            cur = con.cursor()
            cur.execute("SELECT name FROM universities where id = ?", (uni_id,))
            row = cur.fetchone()
            if len(row['name']) > 0 : return row['name']
            else:
                return 0
    except lite.Error as e:
        print("error in opening table universities", e)
        return 0

def get_uni_id(uni_name):
    try:
        con = lite.connect(db)
        with con:
            con.row_factory = lite.Row
            cur = con.cursor()
            cur.execute("SELECT id FROM universities where name = ?", (uni_name,) )
            row = cur.fetchone()
            uni_id =row[0]
            return uni_id
    except lite.Error as e:
        print("error in opening table universities", e)
        return 0


def get_uni_list():
    try:
        con = lite.connect(db)
        with con:
            con.row_factory = lite.Row
            cur = con.cursor()
            cur.execute("SELECT id, name FROM universities ")
            rows = cur.fetchall()
            unis = []
            for row in rows:
                unis.append(row['name'])
            return unis
    except lite.Error as e:
        print("error in opening table universities", e)
        return 0

def get_dept_list(uni_name):
    uni_id = get_uni_id(uni_name)
    try:
        con = lite.connect(db)
        with con:
            con.row_factory = lite.Row
            cur = con.cursor()
            cur.execute("SELECT id, name FROM departments where uni_id = ?", (uni_id,) )
            rows = cur.fetchall()
            depts = []
            for row in rows:
                depts.append([row['id'], row['name']])
            return depts
    except lite.Error as e:
        print("error in opening table universities", e)
        return 0

def get_dept_id(dept_name, uni_id):
    try:
        con = lite.connect(db)
        with con:
            con.row_factory = lite.Row
            cur = con.cursor()
            cur.execute("SELECT id FROM departments where uni_id = ? and name = ?", (uni_id, dept_name))
            row = cur.fetchone()
            if len(row['id']) > 0 : return row['id']
            else:
                return 0
    except lite.Error as e:
        print("error in opening table departments", e)
        return 0

def get_dept_name(dept):
    print("get_dept_name", dept)
    try:
        con = lite.connect(db)
        with con:
            con.row_factory = lite.Row
            cur = con.cursor()
            cur.execute("SELECT name FROM departments where id = ?", (dept,))
            row = cur.fetchone()
            print (row)
            if len(row[0]) > 0 : return row[0]
            else:
                return 0
    except lite.Error as e:
        print("error in opening table departments", e)
        return 0

def get_uni_of_dept(dept):
    try:
        con = lite.connect(db)
        with con:
            con.row_factory = lite.Row
            cur = con.cursor()
            cur.execute("SELECT uni_id FROM departments where id = ?", (dept,))
            row = cur.fetchone()
            if row[0] > 0 : return get_uni_name(row[0])
            else:
                return -1
    except lite.Error as e:
        print("error in opening table departments", e)
        return -1

def dept_program(uni,dept):

    # prints the program of study of department dept
    print ("to print the program ", uni, dept)
    try:
        con = lite.connect(db)
        with con:
            con.row_factory = lite.Row
            cur = con.cursor()
            cur.execute("SELECT * FROM courses where dept_id = ?", (dept,))
            rows = cur.fetchall()
            courses = []

            for row in rows:
                #print ("%s %s %s" % (row["code"], row["name"], row["semester"]))
                code=row['code']
                name = row['name']
                sem = row['semester']
                spr = row['spring_winter']
                c = evdoxos.course(uni, dept, code, name, sem, spr)
                courses.append(c)
            prog ={}
            for c in courses:
                if int(c.semester) in prog.keys():
                    prog[int(c.semester)].append(c)
                else:
                    prog[int(c.semester)] = [c]
            ################# print the program ##########################
            out = get_uni_name(uni)
            print(out)
            out += "\nTMHMA " + get_dept_name(dept)
            for sem in sorted(prog):
                out += "\nΕξάμηνο :"+str(sem)
                print(prog)
                for c in prog[sem]:
                    out += "\n"+c.__str__()
                print(out)
            print (out)
            return out
    except lite.Error as e:
        print("error in opening table courses", e)

def dept_word_cloud(dept):
    word_cloud =[]
    # derives a word cloud of the program of study of department dept
    try:
        con = lite.connect(db)
        with con:
            con.row_factory = lite.Row
            cur = con.cursor()
            cur.execute("SELECT name FROM courses where dept_id = ?", (dept,))
            rows = cur.fetchall()

            for row in rows:
                course_name = row[0]
                #print ("%s %s %s" % (row["code"], row["name"], row["semester"]))
                word_cloud.append(course_name)

            uni_dept = get_uni_of_dept(dept) + " TMHMA " + get_dept_name(dept)
            word_cloud = " ".join(word_cloud)
            print (uni_dept, "\n", word_cloud)
            word_cloud = process_word_cloud(word_cloud)
            #call a word cloud on the string word cloud
            # tried to use the code of http://peekaboo-vision.blogspot.gr/2012/11/a-wordcloud-in-python.html
            # instead developed one on turtle a simpler method
            turtle_w_cloud.show_word_cloud (uni_dept, word_cloud)
    except lite.Error as e:
        print("error in opening table courses", e)

def process_word_cloud(word_cloud):
    latin_numbers = "1234567890IIIVXIVIΙΙΙ"
    symbols ="[]():-!?&,'//"
    #create a list of stopwords
    stop_words = []
    with open('greek_stop_words.txt', 'r') as fo:
        for line in fo:
            w = line.strip()
            if w[-1] == ',': w = w[:-1]
            w = greek_to_upper(w)
            if w not in stop_words: stop_words.append(w)
    for x in symbols:
        word_cloud = word_cloud.replace(x,' ')
    wc = word_cloud.split(' ')
    wc_up=[]
    for w in wc:
        wc_up.append(greek_to_upper(w))

    new_wc = []
    for w in wc_up:
        if w not in stop_words and w not in latin_numbers and len(w)>2: new_wc.append(w)
        else : print ("stop word eliminated:", w)
    print(len(new_wc))
    print(new_wc)
    stems_list ={}
    for w in new_wc:
        st_w = stemmer.stem(w)
        print (w, st_w)
        if st_w not in stems_list: stems_list[st_w]=[w]
        else: stems_list[st_w].append(w)
    for x in stems_list:
        print (x, stems_list[x])
    word_frequencies={}
    for x in stems_list:
        # find the shortest member of the corresponding list for the stem
        word_frequencies[min(stems_list[x], key=len)]= len ( stems_list[x])
    #for x in word_frequencies: print (x.lower(), word_frequencies[x])
    # new_text =""
    # for x in word_frequencies:
    #     new_text += (" "+x)*word_frequencies[x]
    # print(new_text.lower())
    # return new_text.lower()
    print (word_frequencies)
    #input()
    return word_frequencies

def search_in_evdoxos(keyword):
    terms = establish_set_of_keywords(keyword)
    for t in terms:
        try:
            print ("term searched.............", t)
            conn = lite.connect(db)
            conn.row_factory = lite.Row
            print ("database opened")
            with conn:
                cur = conn.cursor()
                cur.execute("SELECT * FROM courses where name like ?", ('%'+t+'%',))
                rows = cur.fetchall()
                if len(rows)>0: print ("found in courses.........")
                for row in rows:
                    #print ("%s %s " % (row["id"], row["name"]), end="")
                    cur.execute("SELECT * FROM departments where id =?", (row["dept_id"],))
                    department = cur.fetchone()
                    dep_name = department[3]
                    uni_id = department[4]
                    cur.execute("SELECT * FROM universities where id =?", (uni_id,))
                    u = cur.fetchone()
                    u_name = u['name']
                    print (u_name, dep_name, 'MΑΘΗΜΑ: ', row['name'])

            with conn:
                cur = conn.cursor()
                cur.execute("SELECT * FROM books where title like ?", ('%'+t+'%',))
                rows = cur.fetchall()
                if len(rows)> 0: print("found in books.............")
                for row in rows:
                    print ("%s %s %s" % (row["id"], row["title"], row['author']))
            with conn:
                cur = conn.cursor()
                cur.execute("SELECT * FROM books where author like ?", ('%'+t+'%',))
                rows = cur.fetchall()
                if len(rows)> 0: print("found in authors.............")
                for row in rows:
                    print ("%s %s %s" % (row["id"], row["title"], row['author']))
            conn.close()
        except lite.Error as e:
            print("error in opening database", db, e)
    return terms


def depts_of_university(uni) :
    try:
        conn = lite.connect(db)
        conn.row_factory = lite.Row
        depts = []
        with conn:
            cur = conn.cursor()
            cur.execute("SELECT id FROM departments where uni_id = ?", (uni,))
            rows = cur.fetchall()
            if len(rows)>0: print ("found in courses.........")
            for row in rows:
                depts.append(row[0])
        return depts
    except lite.Error as e:
        print('error openning table departments')



def search_for_departments(keywords):
    keyw = keywords.split()
    dept_ids = []
    try:
        conn = lite.connect(db)
        conn.row_factory = lite.Row
        with conn:
            for k in keyw:
                k_stemmed = stemmer.stem(k)
                print( k_stemmed)
                cur = conn.cursor()
                cur.execute("SELECT id FROM departments where name like ?", ("%"+k_stemmed+"%",))
                rows = cur.fetchall()
                if len(rows)>0: print ("found in courses.........")
                for row in rows:
                    dept_ids.append(row[0])
            count_keywords = len(keyw)
            common_ids = {x:dept_ids.count(x) for x in dept_ids}
            out =[]
            for x in common_ids:
                if common_ids[x] == count_keywords:
                    cur.execute("SELECT name FROM departments where id = ?", (x,))
                    rows = cur.fetchone()
                    out.append(str(x)+":"+rows[0])
            return out
    except lite.Error as e:
        print('error openning table departments', e)
        return []


def main():
    while True:
        select = input('Επιλογή; (1) για αναζήτηση *2) για πρόγραμμα σπουδών 3) σύγκριση προγραμμάτων σπουδών')
        if select == '1':
            keyword = input("give a term or phrase to search for (enter to exit): ")
            t = search_in_evdoxos(keyword)
        elif select == '2' :
            u = input("University (1 to 42):")
            try:
                u1 = int(u)
                if 1<= u1 <= 42 :
                    print ( depts_of_university(u))
                    sel = input("select department: ")
                    dept_program(u,sel)
            except:
                pass
        elif select == '3':
            keyword = input('give the discipline: ')
            results = search_for_departments(greek_to_upper(keyword))
            count = 0
            for x in results:
                print ("{}" .format(x))
            selecton = input("\nSelect the departments to compare (enter to exit):")
            selecton = selecton.split()
            for d in selecton: dept_word_cloud(d)
        else:
            break

            #print (t)

if __name__ == '__main__':
    main()
    # wcloud = 'ΕΙΣΑΓΩΓΙΚΑ ΘΕΜΑΤΑ ΕΠΙΣΤΗΜΗΣ ΤΩΝ ΥΛΙΚΩΝ ΕΦΑΡΜΟΣΜΕΝΑ ΜΑΘΗΜΑΤΙΚΑ Ι ΠΛΗΡΟΦΟΡΙΚΗ Ι ΦΥΣΙΚΗ Ι ΕΡΓΑΣΤΗΡΙΟ Ι ΦΥΣΙΚΗΣ ΧΗΜΕΙΑ Ι ΕΠΙΣΤΗΜΗ ΤΩΝ ΥΛΙΚΩΝ Ι ΕΡΓΑΣΤΗΡΙΟ Ι ΕΠΙΣΤΗΜΗΣ ΤΩΝ ΥΛΙΚΩΝ ΕΦΑΡΜΟΣΜΕΝΑ ΜΑΘΗΜΑΤΙΚΑ ΙΙ ΠΛΗΡΟΦΟΡΙΚΗ ΙΙ ΦΥΣΙΚΗ ΙΙ ΕΡΓΑΣΤΗΡΙΟ ΙΙ ΦΥΣΙΚΗΣ ΧΗΜΕΙΑ ΙΙ ΒΙΟΛΟΓΙΑ ΚΥΤΤΑΡΟΥ Ι ΕΠΙΣΤΗΜΗ ΤΩΝ ΥΛΙΚΩΝ ΙΙ ΕΡΓΑΣΤΗΡΙΟ ΙΙ ΕΠΙΣΤΗΜΗΣ ΤΩΝ ΥΛΙΚΩΝ ΕΦΑΡΜΟΣΜΕΝΑ ΜΑΘΗΜΑΤΙΚΑ ΙΙΙ ΦΥΣΙΚΗ ΙΙΙ ΕΡΓΑΣΤΗΡΙΟ ΙΙΙ ΦΥΣΙΚΗΣ ΦΥΣΙΚΟΧΗΜΕΙΑ Ι ΒΙΟΛΟΓΙΑ ΚΥΤΤΑΡΟΥ ΙΙ ΕΡΓΑΣΤΗΡΙΟ ΒΙΟΛΟΓΙΑΣ ΕΠΙΣΤΗΜΗ ΤΩΝ ΥΛΙΚΩΝ ΙΙΙ ΕΡΓΑΣΤΗΡΙΟ ΙΙΙ ΕΠΙΣΤΗΜΗΣ ΤΩΝ ΥΛΙΚΩΝ ΕΦΑΡΜΟΣΜΕΝΑ ΜΑΘΗΜΑΤΙΚΑ IV ΘΕΩΡΙΑ ΠΙΘΑΝΟΤΗΤΩΝ ΚΑΙ ΣΤΟΧΑΣΤΙΚΕΣ ΔΙΑΔΙΚΑΣΙΕΣ ΦΥΣΙΚΗ IV ΕΡΓΑΣΤΗΡΙΟ IV ΦΥΣΙΚΗΣ ΕΙΔΙΚΑ ΘΕΜΑΤΑ ΜΗΧΑΝΙΚΗΣ ΕΠΙΣΤΗΜΗ ΤΩΝ ΥΛΙΚΩΝ IV ΗΛΕΚΤΡΟΝΙΚΕΣ ΒΑΘΜΙΔΕΣ ΚΑΙ ΚΥΚΛΩΜΑΤΑ ΠΛΗΡΟΦΟΡΙΚΗ ΙΙΙ ΥΛΙΚΑ ΤΗΣ ΓΗΣ ΦΙΛΟΣΟΦΙΑ ΤΗΣ ΕΠΙΣΤΗΜΗΣ ΕΡΓΑΣΤΗΡΙΟ IV ΕΠΙΣΤΗΜΗΣ ΤΩΝ ΥΛΙΚΩΝ ΦΥΣΙΚΟΧΗΜΕΙΑ ΙΙ ΕΡΓΑΣΤΗΡΙΟ ΦΥΣΙΚΟΧΗΜΕΙΑΣ ΕΙΣΑΓΩΓΗ ΣΤΗΝ ΚΒΑΝΤΟΜΗΧΑΝΙΚΗ ΧΗΜΕΙΑ ΙΙΙ ΓΕΩΛΟΓΙΑ ΓΝΩΣΤΙΚΗ ΨΥΧΟΛΟΓΙΑ ΟΙΚΟΝΟΜΙΚΑ ΤΟΥ ΠΕΡΙΒΑΛΛΟΝΤΟΣ ΚΑΙ ΤΩΝ ΦΥΣΙΚΩΝ ΠΟΡΩΝ ΓΙΑ ΜΗ ΟΙΚΟΝΟΜΟΛΟΓΟΥΣ ΕΠΙΣΤΗΜΗ ΤΩΝ ΥΛΙΚΩΝ V ΥΛΙΚΑ ΚΑΙ ΠΕΡΙΒΑΛΛΟΝ ΔΟΜΙΚΑ ΥΛΙΚΑ ΒΙΟΜΗΧΑΝΙΚΑ ΠΛΑΣΤΙΚΑ ΕΡΓΑΣΤΗΡΙΟ V ΕΠΙΣΤΗΜΗΣ ΤΩΝ ΥΛΙΚΩΝ ΣΤΑΤΙΣΤΙΚΗ ΜΗΧΑΝΙΚΗ ΣΤΟΙΧΕΙΑ ΜΟΡΙΑΚΗΣ ΦΥΣΙΚΗΣ ΚΑΙ ΚΒΑΝΤΙΚΗΣ ΧΗΜΕΙΑΣ Αγγλική Γλώσσα και Ορολογία στην Επιστήμη των Υλικών ΕΠΙΣΤΗΜΗ ΚΑΙ ΤΕΧΝΟΛΟΓΙΑ ΥΓΡΟΚΡΥΣΤΑΛΛΙΚΩΝ ΥΛΙΚΩΝ ΜΕΛΕΤΗ ΤΗΣ ΔΟΜΗΣ ΤΩΝ ΥΛΙΚΩΝ ΜΕ ΤΕΧΝΙΚΕΣ ΣΚΕΔΑΣΗΣ ΠΛΗΡΟΦΟΡΙΚΗ IV ΔΙΔΑΚΤΙΚΗ ΤΗΣ ΦΥΣΙΚΗΣ ΕΠΙΣΤΗΜΗ ΤΩΝ ΥΛΙΚΩΝ VI ΣΥΝΘΕΤΑ ΥΛΙΚΑ ΦΩΤΟΝΙΚΗ Ι ΒΙΟΜΗΧΑΝΙΚΑ ΜΕΤΑΛΛΑ ΚΑΙ ΚΡΑΜΑΤΑ ΕΡΓΑΣΤΗΡΙΟ VI ΕΠΙΣΤΗΜΗΣ ΤΩΝ ΥΛΙΚΩΝ ΔΙΠΛΩΜΑΤΙΚΗ ΕΡΓΑΣΙΑ Ι ΔΙΠΛΩΜΑΤΙΚΗ ΕΡΓΑΣΙΑ Ι ΕΙΔΙΚΑ ΘΕΜΑΤΑ ΥΠΟΛΟΓΙΣΤΙΚΗΣ ΕΠΙΣΤΗΜΗΣ ΤΩΝ ΥΛΙΚΩΝ Θέματα Βιομηχανικών και Τεχνολογικών Εφαρμογών των Υλικών Ι ΟΠΤΙΚΑ ΚΑΙ ΟΠΤΟΗΛΕΚΤΡΟΝΙΚΑ ΥΛΙΚΑ ΜΑΓΝΗΤΙΚΑ ΥΛΙΚΑ ΑΜΟΡΦΑ ΚΡΑΜΑΤΑ ΚΑΙ ΝΑΝΟΔΟΜΗΜΕΝΑ ΥΛΙΚΑ ΚΟΙΝΩΝΙΟΛΟΓΙΑ ΤΗΣ ΕΚΠΑΙΔΕΥΣΗΣ ΚΑΙ ΤΟΥ ΣΧΟΛΕΙΟΥ ΠΡΑΚΤΙΚΗ ΑΣΚΗΣΗ ΑΣΚΗΣΗ ΜΕΣΩ ΤΟΥ ΠΡΟΓΡΑΜΜΑΤΟΣ ΚΙΝΗΤΙΚΟΤΗΤΑΣ LLP/ERASMUS PLACEMENTS ΔΙΠΛΩΜΑΤΙΚΗ ΕΡΓΑΣΙΑ ΙΙ ΕΙΣΑΓΩΓΗ ΣΤΑ ΥΛΙΚΑ ΚΑΙ ΣΤΙΣ ΔΙΕΡΓΑΣΙΕΣ ΚΒΑΝΤΙΚΗΣ ΗΛΕΚΤΡΟΝΙΚΗΣ ΥΛΙΚΑ ΓΙΑ ΑΝΑΝΕΩΣΙΜΕΣ ΠΗΓΕΣ ΕΝΕΡΓΕΙΑΣ ΜΟΡΙΑΚΑ ΝΑΝΟ-ΥΛΙΚΑ ΜΙΚΡΟΤΕΧΝΟΛΟΓΙΑ ΚΑΙ ΝΑΝΟΤΕΧΝΟΛΟΓΙΑ: ΥΛΙΚΑ ΚΑΙ ΔΙΑΤΑΞΕΙΣ ΕΠΙΣΤΗΜΗ ΕΠΙΦΑΝΕΙΩΝ-ΛΕΠΤΑ ΥΜΕΝΙΑ ΕΥΦΥΗ ΥΛΙΚΑ ΗΜΙΑΓΩΓΙΜΑ ΥΛΙΚΑ ΚΑΙ ΔΙΑΤΑΞΕΙΣ Θέματα Βιομηχανικών και Τεχνολογικών Εφαρμογών των Υλικών ΙΙ ΚΕΡΑΜΙΚΑ ΚΑΙ ΥΑΛΟΙ ΠΡΟΗΓΜΕΝΑ ΒΙΟΥΛΙΚΑ ΥΠΕΡΑΓΩΓΟΙ ΦΩΤΟΝΙΚΗ ΙΙ ΠΡΑΚΤΙΚΗ ΑΣΚΗΣΗ ΑΣΚΗΣΗ ΜΕΣΩ ΤΟΥ ΠΡΟΓΡΑΜΜΑΤΟΣ ΚΙΝΗΤΙΚΟΤΗΤΑΣ LLP/ERASMUS PLACEMENTS'
    # process_word_cloud(wcloud)