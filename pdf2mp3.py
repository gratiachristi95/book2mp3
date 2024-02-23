# Import Modules
import os

# Start with a clear screen
os.system('clear')

# Define File Browser Function
def sel_show_file(fList):
    index_len = len(str(len(fList)))
    for idx,f in enumerate(fList):
        print(f"{idx:>{index_len}}. {f}")
    answer = ask_sel_file()
    return answer

def ask_sel_file():
    answer = input("Path: ")
    return answer

def file_browser(dir):
    index = 0
    default_path = ['../', './']

    dir_info = os.walk(dir)
    cur_dir = next(dir_info)

    file_list = []
    file_list.append(default_path[0])
    file_list.append(default_path[1])
    if cur_dir[1]:
        for item in cur_dir[1]:
            file_list.append(item + '/')
    if cur_dir[2]:
        for item in cur_dir[2]:
            file_list.append(item)
    sel_ans = sel_show_file(file_list)
    sel_name = ""
    while True:
        if sel_ans.isnumeric():
            sel_idx = int(sel_ans)
            if sel_idx >= len(file_list) or sel_idx < 0:
                print("Invalid index number, Try Again!")
                sel_ans = ask_sel_file()
            else:
                sel_name = file_list[sel_idx]
                break
        else:
            if sel_ans.lower() == 'q':
               sel_name = ""
               break
            elif sel_ans in file_list:
                sel_name = sel_ans
                break
            else:
                print("Invalid index number,", sel_ans, "does not exist.")
                sel_ans = ask_sel_file()

    if sel_name == "":  #q
        global file_name
        file_name = sel_name
    elif sel_name == default_path[1]: #./
        file_name = os.path.abspath(cur_dir[0])
    else:
        global go_path
        if sel_name == default_path[0]:  # ../
            cur_path = os.path.abspath(cur_dir[0])
            go_path = os.path.dirname(cur_path)
        else:
            cur_path = os.path.join(cur_dir[0], sel_name)
            go_path = os.path.abspath(cur_path)
        if os.path.isdir(go_path):
            os.system('clear')
            file_name = file_browser(go_path)
        else:
            file_name = go_path
            os.system('clear')

# Execute Function
file_browser('.')

# Convert PDF To TXT 
quote = '"'
pdf2txt = str('pdftotext ')
outputdottxt = str(' output.txt')
pdftotext = pdf2txt + quote +  go_path + quote + outputdottxt
os.system(pdftotext)

# Execute Function
file_browser('.')

# Convert Text To Only Letters & Punctuation
z = quote +  go_path + quote
rmunknownchr = "sed -i 's/[^a-zA-Z ]//g' " + z
os.system(rmunknownchr)

# Convert Text To A Single Line
os.system('mkdir files')
rmlnbreaks = 'tr "\\n\" " " < ' + z + ' > ./files/output-new.txt'
os.system(rmlnbreaks)

# Split File Into Parts
os.system('split -b 10KB -d  ./files/output-new.txt ./files/file')
os.system('rm ./files/output-new.txt')

# Convert Text To WAV Speech Format
directory = './files'

for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    if os.path.isfile(f):
        output = "cat -A " + f +" |piper --model en_US-lessac-high -d ./files"
        os.system(output)

# Remove all TXT Files from Files Folder
os.system('rm -rf ./files/file*')

# Combine All WAV Files To One File
os.system("sox './files/*' ./files/long.wav")

# Convert WAV To MP3 Speech Format
os.system("lame -b 448 ./files/long.wav output.mp3")
os.system("rm -rf ./files")

# Remove Unneeded Files
os.system("rm -rf ./files")
os.system('rm -rf output-new.txt')
os.system('rm -rf output.txt')
os.system ('rm -rf en*')
os.system('clear')
