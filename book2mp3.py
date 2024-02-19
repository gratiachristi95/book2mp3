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

# Convert HTML to TXT
quote = '"'
html2txt = ('lynx --dump ') + quote + go_path + quote + (' > output.txt')
os.system(html2txt)

# Convert Other Book Formats To TXT
book2txt = ('pandoc -o output.txt ')
pandoc = book2txt + quote + go_path + quote
os.system(pandoc)

# Convert PDF To TXT
pdf2txt = str('pdftotext ')
outputdottxt = str(' output.txt')
pdftotext = pdf2txt + quote +  go_path + quote + outputdottxt
os.system(pdftotext)

# Execute Function
file_browser('.')

# Convert Text To Only Letters & Punctuation
z = quote +  go_path + quote
rmunknownchr = "sed -i 's/[^a-zA-Z ]//g' " + z
rmwords = "sed -i -e 's/\(xml\|html\|image\|img\|svg\|jpg\|png\|jpeg\|div\|height\|titlepage\|version\|indexsplit\|width\|xlinkhrefcover\|cover\)//g' " + z
os.system(rmunknownchr)
os.system(rmwords)

# Convert Text To A Single Line
rmlnbreaks = 'tr -d \"\\n\" < ' + z + ' > output-new.txt'
os.system(rmlnbreaks)

# Convert Text To WAV Speech Format
txt2wav = "cat -A output-new.txt |piper --model en_US-lessac-medium --output_file output.wav"
os.system(txt2wav)

# Convert WAV To MP3 Speech Format
os.system("lame -b 448 output.wav output.mp3")

# Remove Unneeded Files
os.system('rm -rf output-new.txt')
os.system('rm -rf output.txt')
os.system('rm -rf output.wav')
os.system('clear')
