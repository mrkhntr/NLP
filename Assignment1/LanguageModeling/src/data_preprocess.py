import os
import io


#  ? will be known as our <unk>
def replace_unk(line):
    unk = ['\x98', '\x85', '\x12', '\xa9', '\x18', '\x16', '\xf3', '\x0f', '\x13',
           '\xe8', '\x1a', '\xe9', '\x15', '\xe6', '\x14', '\x03' '\x11', '\xee', '\x11',
           '\x03']
    if any(s in line for s in unk):
        for sym in unk:
            line = line.replace(sym, '?')
    return line


def format_line(line):
    punctuation = ',.-";\'!_?:`)(&[]*}/$%>@<+=~\r'

    line = line.rstrip()  # remove blank lines
    line = ' '.join(line.split())  # remove duplicate spaces
    remove_punc = str.maketrans('', '', punctuation)
    line = line.translate(remove_punc)  # remove punctuation
    line = replace_unk(line)
    return line


def format_file(filename):
    with io.open(filename, 'r', encoding='iso-8859-15') as f:
        text = f.read()

    text = format_line(text)

    with io.open(filename, 'w', encoding='iso-8859-15') as f:
        f.write(text)


def data_preprocess():
    training_set_path = os.getcwd() + '/gutenberg/'
    file_names = os.listdir(training_set_path)

    for filename in file_names:
        format_file(training_set_path + filename)


data_preprocess()
