# import matplotlib features
import matplotlib
matplotlib.use('TkAgg') 
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.lines as lines
import matplotlib.patches as patches
import numpy as np
import matplotlib.gridspec as gridspec


# other imports
import tkinter as tk
from tkinter import simpledialog
import time
from datetime import datetime
import math
import sys
from bidi import algorithm as bidialg

# custom tkinter dialog box in order to display the 'task end' message in a larger font
class CustomDialog(simpledialog.Dialog):
    def body(self, master):
        self.state('normal')  # Maximize the dialog box
        self.title("End of Test")
        self.label = tk.Label(master, text=".המשימה הסתיימה, אנא קראי לבודק", font=("TkDefaultFont", 46))
        self.label_M = tk.Label(master, text=".המשימה הסתיימה, אנא קרא לבודק", font=("TkDefaultFont", 46))
        self.label.pack()


##################
# task specifications
##################
# First 4 are example items, the next 12 are the actual test items
TASK_ITEMS = [
    ("ןומעפה", "ץעה", "ףותה", 306),
    ("ףותה", "רוזמרה", "לגלגה", 57),
    ("ןומעפה", "ץעה", "תיבחה", 326),
    ("חפה", "ףותה", "ןומעפה", 49),
    ("לגלגה", "תיבחה", "רוזמרה", 143),
    ("ףותה", "ץעה", "לגלגה", 249),
    ("רוזמרה", "ףותה", "חפה", 93),
    ("ףותה", "ןומעפה", "לגלגה", 165),
    ("רוזמרה", "ץעה", "תיבחה", 318),
    ("רוזמרה", "ןומעפה", "לגלגה", 250),
    ("תיבחה", "חפה", "ןומעפה", 333),
    ("חפה", "ןומעפה", "רוזמרה", 268),
    ("לגלגה", "רוזמרה", "ץעה", 266),
    ("תיבחה", "ףותה", "לגלגה", 41),
    ("ץעה", "ןומעפה", "חפה", 25),
    ("ףותה", "חפה", "תיבחה", 151)
]

##################




##################
# Global variables for the plot creator functions and instructions
##################
fig = None
answer_line = None
example_line_1 = None
example_line_2 = None
example_line_3 = None
picture_ax = None
text_bottom = None
text_top = None
text_example = None
text_instruction = None
example_task_instruction = None
task_id = None

##################
# Global variables for text boxes
##################

TASK_EXAMPLE_0 = None # this is the text to be shown on top of the practice first example ,(the one that was presented initially as a fixed image)
TASK_EXAMPLE_1 = None # this is the text to be shown alone, before the three practice examples
TASK_EXAMPLE_2 = None # this is the text to be shown below each of the three practice examples lines, below the TASK_TEXT_1, TASK_TEXT_2, and TASK_TEXT_3 combination
TASK_EXAMPLE_3 = None # this is the text to be shown alone, before the 12 test trials
TASK_EXAMPLE_4 = None # this is the text to be shown below each of the test trials , below the TASK_TEXT_1, TASK_TEXT_2, and TASK_TEXT_3 combination
INSTRUCTION_TEXT = None # this is the text to be shown at the beginning of the test (first window)
INSTRUCTION_TEXT_TITLE = None # title of the instruction window

# the next three are shown along with the sentences in the TASK_ITEMS list
TASK_TEXT_1 = None
TASK_TEXT_2 = None
TASK_TEXT_3 = None
###########
# Global variables for the tkinter and font and dpi settings
#########
root = tk.Tk() # open a tkinter window to get the screen size
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.withdraw()  # Hide the tkinter window
dpi = 100 # set the dpi for the instructions window and the test window
# Convert screen size from pixels to inches for matplotlib
screen_width_in = screen_width / dpi  
screen_height_in = screen_height / dpi
fontsize_instruction = 15  # Set font size for the instructions window
fontsize_test = 13  # Set font size for the test window

##########
# Global variables for time
##########
start_time = 0 # start time of the test
timer = None # timer for the test
elapsed_time = 0 # elapsed time of the test
now = datetime.now() # Get the current date and time
date_time = now.strftime("%Y-%m-%d_%H-%M-%S") # Format the date and time as a string

##########
# Global variables for the calculation of the angle,errors and saving the results as a text file and csv file
##########
result_file = None # file to write the results
result_csv = None # csv file to write the results
csv_file_name = None # name of the csv file
errors = [] # list of errors

##########
# All text box versions
##########

###
# Hebrew Female version
###
TASK_EXAMPLE_0_F = "לפניך תרגיל לדוגמה בו מסומנת התשובה הנכונה.  התאמני על סימון התשובה שלך בעזרת העכבר. כדי להתאמן על סימון התשובה, לחצי על היקף מעגל הסימון וקו יופיע בהתאם. הזיזי את הקו לאורך מעגל הסימון בעזרת העכבר לתשובה הרצויה. התאימי את התשובה שלך לתשובה הנכונה המסומנת. לחצי על מקש הרווח כשתסיימי"
TASK_EXAMPLE_1_F = ".ךלש הבושתה תא ןמסל ידכ ןומיסה לגעמ לע וקה תא יזיזה אמגוד לכב .ןומיאל תואמגוד שולש ךינפל ועיפוי תעכ\n" +\
".םודא עבצב עיפות הנוכנה הבושתהו חוורה שקמ לע יצחל ןכמ רחאל\n\n"
TASK_EXAMPLE_2_F = ".ימייסתשכ חוורה שקמ לע יצחל\n"
TASK_EXAMPLE_3_F ="כעת יתחיל המבדק. לרשותך 5 דקות להשלים 12 משימות. נסי לענות במדויק, אבל אל תבזבזי יותר מדי זמן על משימה אחת.  אם יש לך שאלות אחרונות לגבי המבדק שאלי עכשיו. אם לא, הודיעי לבודק שאת מוכנה להתחיל"
TASK_EXAMPLE_4_F = ".ימייסתשכ חוורה שקמ לע יצחל\n"
TASK_TEXT_1_F = "םוקמב תדמוע תאש יניימד"
TASK_TEXT_2_F = "ןוויכל הנופו"
TASK_TEXT_3_F = "ןוויכל יעיבצה"
INSTRUCTION_TEXT_F = ".ןומיס לגעמ הדיצלו טפשמ עיפוי הנומתל תחתמ .םיטקייבוא רפסמ םימקוממ הבו הנומת יארת קדבמב .בחרמב תונוש טבמ תודוקנו םינוויכ ןיימדל ךלש תלוכיה תא ןחוב הז קדבמ\n" + \
                   ".תראותמה הביטקפסרפהמ ישילש טקייבוא אצמנ וב ןוויכה תא ףקשמש וק רייצל היהת ךלש המישמה .רחא טקייבוא ןוויכל הנופו ,הנומתבש םיטקייבואה דחא םוקמב תדמוע תאש ןיימדל ישקבתת תא\n" + \
                   ".ךיילא סחיב והשלכ ישילש טקייבוא לש םוקימה תא ףקשמש וק רייצל ןכמ רחאלו ,שדח טקייבוא ןוויכל הנופו הנומתב רחא טקייבוא םוקמב תדמוע תאש ןיימדל ישקבתת בלש לכב\n\n" + \
                   ",(ןושארה ץפחה םוקמב) בלש ותואב ךלש ןיימודמה םוקימה תא תפקשמ לגעמה זכרמבש הדוקנה .בשחמה לש רבכעה תרזעב הנומתה דצלש ןומיסה לגעמ יבג לע רייצל ךיילע וקה תא\n" + \
                   ".וללה תודוקנה יתשל סחיב ישילשה ץפחה לש ןוויכה תא גציימש וק רייצל הכירצ תא .(הנופ תא וילא ינשה ץפחה לש ןוויכה) ךלש תניימודמה טבמה תדוקנ תא ףקשמ יכנאה ץחהו\n\n" + \
                   ".ףותה לש ןוויכה לא עיבצמש וק רייצל התייה אמגודב המישמה .ץעה ןוויכל הנופו ןומעפה םוקמב תדמוע תאש ןיימדל תשקבתמ תא וז אמגודב .דומעה תיתחתבש אמגודל בלשב יטיבה\n" + \
                   "?וקווקמה וקה עיבצמ וילא ןוויכב היה ףותה , ץעה ןוויכל הנופו ןומעפה םוקמב תדמוע תייה םאש ןיימדל הלוכי תא םאה .וקווקמ וקכ אמגודב עיפומ רייצל ךירצ היהש וקה\n\n" + \
                   ".המישמה יבגל תולאש ךל שי םא ןחובה תא ילאש\n"
###
# Hebrew Male version
###
TASK_EXAMPLE_0_M_HEB = "לפניך תרגיל לדוגמה בו מסומנת התשובה הנכונה. התאמן על סימון התשובה שלך בעזרת העכבר. כדי להתאמן על סימון התשובה, לחץ על היקף מעגל הסימון וקו יופיע בהתאם. הזז את הקו לאורך מעגל הסימון בעזרת העכבר לתשובה הרצויה. התאם את התשובה שלך לתשובה הנכונה המסומנת. לחץ על מקש הרווח כשתסיים"
TASK_EXAMPLE_1_M_HEB = ". ךלש הבושתה תא ןמסל ידכ ןומיסה לגעמ לע וקה תא זזה אמגוד לכב .ןומיאל תואמגוד שולש ךינפל ועיפוי תעכ\n" +\
".םודא עבצב עיפות הנוכנה הבושתהו חוורה שקמ לע ץחל ןכמ רחאל\n\n"
TASK_EXAMPLE_2_M_HEB = ".םייסתשכ חוורה שקמ לע ץחל\n"
TASK_EXAMPLE_3_M_HEB = "כעת יתחיל המבדק. לרשותך 5 דקות להשלים 12 משימות. נסה לענות במדויק, אבל אל תבזבז יותר מדי זמן על משימה אחת.  אם יש לך שאלות אחרונות לגבי המבדק שאל עכשיו. אם לא, הודע לבודק שאתה מוכן להתחיל" 
TASK_EXAMPLE_4_M_HEB = ".םייסתשכ חוורה שקמ לע ץחל\n"
TASK_TEXT_1_M_HEB = "םוקמב דמוע התאש ןיימד"
TASK_TEXT_2_M_HEB = "ןוויכל הנופו"
TASK_TEXT_3_M_HEB = "ןוויכל עבצה"
INSTRUCTION_TEXT_M_HEB = ".ןומיס לגעמ ודיצלו טפשמ עיפוי הנומתל תחתמ .םיטקייבוא רפסמ םימקוממ הבו הנומת הארת קדבמב .בחרמב תונוש טבמ תודוקנו םינוויכ ןיימדל ךלש תלוכיה תא ןחוב הז קדבמ\n" + \
                   ".תראותמה הביטקפסרפהמ ישילש טקייבוא אצמנ וב ןוויכה תא ףקשמש וק רייצל היהת ךלש המישמה .רחא טקייבוא ןוויכל הנופו ,הנומתבש םיטקייבואה דחא םוקמב דמוע התאש ןיימדל שקבתת התא\n" + \
                   ".ךיילא סחיב והשלכ ישילש טקייבוא לש םוקימה תא ףקשמש וק רייצל ןכמ רחאלו ,שדח טקייבוא ןוויכל הנופו הנומתב רחא טקייבוא םוקמב דמוע התאש ןיימדל שקבתת בלש לכב\n\n" + \
                   ",(ןושארה ץפחה םוקמב) בלש ותואב ךלש ןיימודמה םוקימה תא תפקשמ לגעמה זכרמבש הדוקנה .בשחמה לש רבכעה תרזעב הנומתה דצלש ןומיסה לגעמ יבג לע רייצל ךיילע וקה תא\n" + \
                   ".וללה תודוקנה יתשל סחיב ישילשה ץפחה לש ןוויכה תא גציימש וק רייצל ךירצ התא .(הנופ התא וילא ינשה ץפחה לש ןוויכה) ךלש תניימודמה טבמה תדוקנ תא ףקשמ יכנאה ץחהו\n\n" + \
                   ".ףותה לש ןוויכה לא עיבצמש וק רייצל התייה אמגודב המישמה .ץעה ןוויכל הנופו ןומעפה םוקמב דמוע התאש ןיימדל שקבתמ התא וז אמגודב .דומעה תיתחתבש אמגודל בלשב טבה\n" + \
                   "?וקווקמה וקה עיבצמ וילא ןוויכב היה ףותה ,ץעה ןוויכל הנופו ןומעפה םוקמב דמוע תייה םאש ןיימדל לוכי התא םאה .וקווקמ וקכ אמגודב עיפומ רייצל ךירצ היהש וקה\n\n" + \
                   ".המישמה יבגל תולאש ךל שי םא ןחובה תא לאש\n"
###
# Hebrew title
###
INSTRUCTION_TEXT_TITLE_HEB = " (Spatial Orientation Test) בחרמב תואצמתה קדבמ \n"




###
# Lists of all texts boxes
###
### Hebrew text boxes
LIST_OF_TEXTS_M_HEB = [TASK_EXAMPLE_0_M_HEB, TASK_EXAMPLE_1_M_HEB, TASK_EXAMPLE_2_M_HEB, TASK_EXAMPLE_3_M_HEB, TASK_EXAMPLE_4_M_HEB, TASK_TEXT_1_M_HEB, TASK_TEXT_2_M_HEB, TASK_TEXT_3_M_HEB, INSTRUCTION_TEXT_M_HEB]
LIST_OF_TEXTS_F_HEB = [TASK_EXAMPLE_0_F, TASK_EXAMPLE_1_F, TASK_EXAMPLE_2_F, TASK_EXAMPLE_3_F, TASK_EXAMPLE_4_F, TASK_TEXT_1_F, TASK_TEXT_2_F, TASK_TEXT_3_F, INSTRUCTION_TEXT_F]


##################
# main function
##################
def main():
    global dpi ,fontsize_instruction, fontsize_test, screen_height_in, screen_width_in, result_file, errors, task_id,result_csv, csv_file_name,TASK_EXAMPLE_0, TASK_EXAMPLE_1, TASK_EXAMPLE_2, TASK_EXAMPLE_3, TASK_EXAMPLE_4,INSTRUCTION_TEXT_TITLE, INSTRUCTION_TEXT, TASK_TEXT_1, TASK_TEXT_2, TASK_TEXT_3
    variables = ["TASK_EXAMPLE_0", "TASK_EXAMPLE_1", "TASK_EXAMPLE_2", "TASK_EXAMPLE_3", "TASK_EXAMPLE_4", "TASK_TEXT_1", "TASK_TEXT_2", "TASK_TEXT_3", "INSTRUCTION_TEXT"]
    matplotlib.rcParams['toolbar'] = 'None'
    subject_id = input("Please insert your participant ID: ") # get the subject ID
    
    gender = input("Please enter the gender of the participant (M/F): ") # set all the text boxes to the correct gender
    if gender == "M":

        for var, val in zip(variables, LIST_OF_TEXTS_M_HEB):
            globals()[var] = val

        print("Male participant")


    elif gender == "F":
        for var, val in zip(variables, LIST_OF_TEXTS_F_HEB):
            globals()[var] = val
        print("Female participant")



    ###### ONLY FOR RTL TEXTS ######
    TASK_EXAMPLE_0 = linebreak_text(RTL_text(TASK_EXAMPLE_0)) # added linebreaks and RTL to the text
    TASK_EXAMPLE_3 = linebreak_text(RTL_text(TASK_EXAMPLE_3)) # added linebreaks and RTL to the text
    ##############
    INSTRUCTION_TEXT_TITLE = INSTRUCTION_TEXT_TITLE_HEB # set the title of the instruction window in hebrew
    ##############



    input_values = input("Enter dpi and font size for the instructions window and the test window separated by a space, press 'Enter' for default values(Example input- 100 13 15): ")
    if input_values.strip() == "":
        # if non given, use the default values
        print("Using default values for dpi and font size (dpi=100, fontsize_instruction=15, fontsize_test=13)")
    else:
        dpi, fontsize_instruction, fontsize_test = map(int, input_values.split())
        screen_width_in = screen_width / dpi  
        screen_height_in = screen_height / dpi

    print (f'screen width in inches: {screen_width_in}, screen height in inches: {screen_height_in}')
    result_file = open('results-' + str(subject_id) + '.txt', 'w+')
    csv_file_name = 'results-' + str(subject_id) + '-' + date_time + '.csv'
    with open(csv_file_name, 'a', newline='') as result_csv:
        result_csv.write('task_id' + ',' + 'correct_angle' + ',' + 'logged_angle' + ',' + 'error' + ',' + 'Time elapsed (s)' + '\n')

    create_test_window(subject_id)


    # save to global variables
    result_file = result_file
    result_csv = result_csv
    csv_file_name = csv_file_name

    task_id = 0
    load_task(task_id)
    
    plt.show()

##################
# plot creator functions
##################


def create_first_instruction_window():

    # create figure
    ins_fig = plt.figure("Instructions", figsize = (screen_width_in, screen_height_in),dpi=dpi)

    # create subplots with different sizes
    gs = ins_fig.add_gridspec(3, 1)  # adjust the number of rows as needed
    txt_ax = ins_fig.add_subplot(gs[0, :])  # Text on top
    img_ax = ins_fig.add_subplot(gs[1:, :])  # Image on the bottom

    # load image
    img = mpimg.imread('Data/heb_screenshot_.png')

    # display image
    img_ax.imshow(img, aspect='equal')

    # remove ticks and 'axis lines' from subplots
    img_ax.axis('off')
    txt_ax.axis('off')

    txt_ax.text(0.99, 0.9, INSTRUCTION_TEXT_TITLE, verticalalignment='top', horizontalalignment='right', fontsize=fontsize_instruction, weight='bold')
    txt_ax.text(0.99, 0.8, INSTRUCTION_TEXT, verticalalignment='top', horizontalalignment='right', fontsize=fontsize_instruction)
    ins_fig.tight_layout()


def create_second_instruction_window():

    # create figure
    ins_fig = plt.figure("Instructions", figsize = (screen_width_in, screen_height_in),dpi=dpi)

    # create subplots
    txt_ax = ins_fig.add_subplot(1, 1, 1)
    # remove ticks and 'axis lines' from plot
    txt_ax.axis('off')
    txt_ax.set_xticks([])
    txt_ax.set_yticks([])

    txt_ax.text(0.99, 0.9, TASK_EXAMPLE_1, verticalalignment='top', horizontalalignment='right', fontsize=fontsize_instruction+5, weight='bold')
    ins_fig.tight_layout()
    plt.show()


def create_third_instruction_window():

    # create figure
    ins_fig = plt.figure("Instructions", figsize = (screen_width_in, screen_height_in),dpi=dpi)
    # create subplots
    txt_ax = ins_fig.add_subplot(1, 1, 1)
    # remove ticks and 'axis lines' from plot
    txt_ax.axis('off')
    txt_ax.set_xticks([])
    txt_ax.set_yticks([])

    txt_ax.text(0.99, 0.9, TASK_EXAMPLE_3, verticalalignment='top', horizontalalignment='center', fontsize=fontsize_instruction+5, weight='bold')
    ins_fig.tight_layout()
    ins_fig.canvas.mpl_connect('close_event', on_close)
    plt.show()

def create_test_window(SUBJECT_ID):
    global fig, answer_line, example_line_1, example_line_2, example_line_3, picture_ax, text_bottom, text_top, text_example, text_instruction, example_task_instruction
    test_fig = plt.figure("Perspective Taking Test - Participant " + str(SUBJECT_ID), figsize = (screen_width_in, screen_height_in), dpi=dpi)
    plt.rcParams['text.usetex'] = False
    # Define the grid
    gs = gridspec.GridSpec(2, 2, width_ratios=[1.5, 1], height_ratios=[1, 1])

    # object array subplot
    pic_ax = test_fig.add_subplot(gs[:, 0])
    pic_ax.imshow(mpimg.imread('Data/2019v_object_array.png'), aspect='equal')
    pic_ax.set_xticks([])
    pic_ax.set_yticks([])
    pic_ax.axis('off')


    # user input subplot
    input_ax = test_fig.add_subplot(gs[:, 1])
    input_ax.axis('equal')
    circle = patches.Circle((0, 0), 1.0, facecolor='none', edgecolor='black', linewidth=3)
    input_ax.add_patch(circle)
    upright_line = lines.Line2D((0, 0), (0, 1), linewidth=3, color='black')
    input_ax.add_line(upright_line)
    input_ax.add_line(lines.Line2D((0, -0.03), (1, 0.95), linewidth=3, color='black')) # left arrow wedge
    input_ax.add_line(lines.Line2D((0, 0.03), (1, 0.95), linewidth=3, color='black')) # right arrow wedge


    # creating main line and example lines
    answer_line = lines.Line2D((0, 0), (0, 1), linewidth=3, color='black')
    example_line_1 = lines.Line2D((0, 0.838), (0, 0.544), visible=False, linewidth=3, color='red') # added example line 1 
    example_line_2 = lines.Line2D((0, -0.56), (0, 0.83), visible=False, linewidth=3, color='red') # added example line 2
    example_line_3 = lines.Line2D((0, 0.755), (0, 0.656), visible=False, linewidth=3, color='red') # added example line 3

    # adding main line and example lines to axes
    input_ax.add_line(answer_line)
    input_ax.add_line(example_line_1) # added example line
    input_ax.add_line(example_line_2) # added example line
    input_ax.add_line(example_line_3) # added example line


    text_bottom = input_ax.text(0.0, -0.15, 'text_bottom', fontsize=fontsize_test, horizontalalignment='center')
    text_top = input_ax.text(0.0, 1.15, 'text_top', fontsize=fontsize_test, horizontalalignment='center')
    text_example = input_ax.text(-1.0, 0.58, 'text_example', fontsize=fontsize_test, horizontalalignment='center')
    text_instruction = input_ax.text(0.0, -1.2, 'text_instruction', fontsize=fontsize_test, horizontalalignment='center')
    # example_task_instruction = pic_ax.text(300, 480, ' ', fontsize=fontsize_test, horizontalalignment='center')
    example_task_instruction = input_ax.text(1.45, -1.3, ' ', fontsize=fontsize_test,horizontalalignment='right', verticalalignment='top',wrap=True)
    input_ax.set_xlim(-1.5, 1.5)
    input_ax.set_ylim(-1.5, 1.5)
    input_ax.set_xticks([])
    input_ax.set_yticks([])
    input_ax.axis('off')
    test_fig.tight_layout()


    # event handling
    fig = test_fig
    answer_line = answer_line
    example_line_1 = example_line_1
    example_line_2 = example_line_2
    example_line_3 = example_line_3
    picture_ax = pic_ax
    text_bottom = text_bottom
    text_top = text_top
    text_example = text_example
    text_instruction = text_instruction
    example_task_instruction = example_task_instruction
    test_fig.canvas.mpl_connect('button_press_event', on_click)
    test_fig.canvas.mpl_connect('key_press_event', on_key_press)


def load_task(INDEX):
    global answer_line,text_example, example_task_instruction, fig, text_bottom, text_top, text_instruction

    item_tuple = TASK_ITEMS[INDEX]
    located_at = item_tuple[0].replace(r' ', r'\; ')
    facing_to = item_tuple[1].replace(r' ', r'\; ')
    pointing_to = item_tuple[2].replace(r' ',r'\; ')


    instruction_text =  r'$\bf{' +  '.' + pointing_to + '}$ '  + TASK_TEXT_3  + ' ' + r'$\bf{' + facing_to +  '}$ ' + TASK_TEXT_2 + \
                   ' ' + r'$\bf{' + located_at + '}$ ' + TASK_TEXT_1
                   
    text_instruction.set_text(instruction_text)
    
    
    if INDEX == 0:
        create_first_instruction_window() 
        answer_line.set_data([0.0, -0.809], [0.0, 0.587])
        text_example.set_text('ףות')
    else:
        answer_line.set_data([0.0, 0.0], [0.0, 1.0])
        text_example.set_text('')

    if INDEX == 0:
        example_task_instruction.set_text(TASK_EXAMPLE_0)
    if INDEX == 1:
        print("INDEX 1")
        create_second_instruction_window()
    if INDEX > 0:
        example_task_instruction.set_text(TASK_EXAMPLE_2)
    if INDEX == 4:
        create_third_instruction_window() # Show the final instructions before the test starts
    text_bottom.set_text(item_tuple[0][:-1]) # set the text at the bottom of the test window (First task item from TASK_ITEMS)
    text_top.set_text(item_tuple[1][:-1]) # set the text at the top of the test window (Second task item from TASK_ITEMS)
    fig.canvas.draw()


##################
# callbacks
##################
def on_click(EVENT):
    global answer_line, fig
    if EVENT.inaxes is None:
        return
    length = euclidean_distance([0, 0], [EVENT.xdata, EVENT.ydata])
    answer_line.set_data([0.0, EVENT.xdata/length], [0.0, EVENT.ydata/length])
    fig.canvas.draw()


def on_key_press(EVENT):
    global task_id,result_file,errors,example_line_1,example_line_2,example_line_3,fig, result_csv, csv_file_name
    if EVENT.key == ' ':
        if task_id > 0: # exclude the first task item (example)
            correct_angle = round(TASK_ITEMS[task_id][3], 4)
            logged_angle = round(compute_response_line_angle(), 4)
            error = round(angle_difference(correct_angle, logged_angle), 4)
            result_file.write(str(task_id) + ',' + str(correct_angle) + ',' + str(logged_angle) + ',' + str(error) + '\n')
            
            with open(csv_file_name, 'a', newline='') as result_csv:
                result_csv.write(str(task_id) + ',' + str(correct_angle) + ',' + str(logged_angle) + ',' + str(error) + ',' + str(elapsed_time) + '\n')

            errors.append(error)
            
                        

        # If the task id is between 1 and 3, show the corresponding example line
        if 1 <= task_id <= 3:
            if task_id == 1:
                example_line_1.set_visible(True)
                fig.canvas.draw()
                plt.pause(5)
                example_line_1.set_visible(False)

            elif task_id == 2:
                example_line_2.set_visible(True)
                fig.canvas.draw()
                plt.pause(5)
                example_line_2.set_visible(False)
            
            elif task_id == 3:
                example_line_3.set_visible(True)
                fig.canvas.draw()
                plt.pause(5)
                example_line_3.set_visible(False)
        task_id += 1

        
        if task_id < len(TASK_ITEMS): # move on to the next task
            load_task(task_id)

        else: # no more tasks, terminate the test
            avg_error = np.mean(errors)
            test_avg_error = np.mean(errors[4:]) # mean error of only the test items
            result_file.write('Average Error: ' + str(round(avg_error, 4)) + ','  +
                              'Test Only Average Error: ' + str(round(test_avg_error, 4)))
            result_file.close()
            print('The test has terminated successfully. Results saved to file ' + result_file.name + '.')
            sys.exit(0)



def on_close(EVENT):
    global fig, start_time, timer
    timer = fig.canvas.new_timer(interval=1000) # create a timer that fires every 1 second
    timer.add_callback(update_time) # add a callback to the timer
    start_time = time.time() # set the start time
    timer.start() # start the timer



def update_time():
    global start_time, elapsed_time,result_file,errors, result_csv, csv_file_name
    elapsed_time = time.time() - start_time
    if elapsed_time > 300.0:
        show_popup_message()
        avg_error = np.mean(errors)
        test_avg_error = np.mean(errors[4:]) # mean error of only the test items
        result_file.write('Average Error: ' + str(round(avg_error, 4)) + ',' +
                          'Test Only Average Error: ' + str(round(test_avg_error, 4)))      
        result_file.close()
        print('The test has terminated successfully. Results saved to file ' + result_file.name + '.')
        sys.exit(0)
    print(f'Time elapsed: {elapsed_time} seconds')
   


def show_popup_message():
    # show a popup message if the task is not completed within 5 minutes
    d = CustomDialog(root)
##################
# math helpers
##################
def compute_response_line_angle():
    global answer_line
    answer_line_data = answer_line.get_data()
    answer_line_endpoint = (answer_line_data[0][1], answer_line_data[1][1])
    upright_endpoint = (0.0, 1.0)
    cosine_value = answer_line_endpoint[0]*upright_endpoint[0] + \
                   answer_line_endpoint[1]*upright_endpoint[1]

    angle = angle_between_normalized_2d_vectors(upright_endpoint, answer_line_endpoint) * 180.0/math.pi

    # convert angle to range (0; 360]
    if angle < 0:
        angle *= -1
    else:
        angle = 360.0 - angle

    return angle


def euclidean_distance(POINT_1, POINT_2):
    return math.sqrt(pow(POINT_1[0]-POINT_2[0], 2) + pow(POINT_1[1]-POINT_2[1], 2))


def angle_between_normalized_2d_vectors(VEC1, VEC2):
    return math.atan2(VEC1[0]*VEC2[1] - VEC1[1]*VEC2[0], VEC1[0]*VEC2[0] + VEC1[1]*VEC2[1])

def angle_difference(ANGLE_1, ANGLE_2):
    phi = math.fmod(abs(ANGLE_2-ANGLE_1), 360)
    distance = 360 - phi if phi > 180 else phi
    return distance

##################
# Text helpers
##################

def RTL_text(text):
    '''
    This function receives a text string and returns the same text string with the proper RTL formatting
    it -
    1. flips the text from left to right and adds break lines at every period
    2. splits the text into sentences by periods
    3. reverses the order of the sentences in the text
    4. returns properly formatted text
    :param text: string
    :return: string

    '''
    text = bidialg.get_display(text)
    # New code to reverse sentence order
    sentences = text.split('.')
    sentences.reverse()
    text = '.'.join(sentences)
    return text


def linebreak_text(text):
    '''
    This function receives a text string and returns the same text string with a break line at every period
    :param text: string
    :return: string

    '''
    text = text.replace(".", "\n .")
    return text



if __name__ == '__main__':
    main()