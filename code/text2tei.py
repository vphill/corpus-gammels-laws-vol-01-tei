import sys
import glob
import os.path
import xml.etree.ElementTree as ET


def filename_to_seq_number(filename):
    filename = filename.replace('.txt', '')
    seq = filename[:len(filename)//2] # Split filename in half, first part
    pages = filename[len(filename)//2:] # Split filename in half, last part
    seq = seq.lstrip('0')
    page_id = "P{}".format(pages) # we want the identifier before we strip the leading zeros
    pages = pages.lstrip('0')


    return seq, pages, page_id

def encode_hyphens(text):
    new_text = []
    for line in text.split('\n'):
        if line.endswith('-'):
            line = line[:-1] + '<pc force="weak">-</pc><lb break="no"/>'
        new_text.append(line)

    return '\n'.join(new_text)

def new_encode_hyphens(text):
    lines = [line.strip('\n') for line in text.split('\n')]
    for num, line in enumerate(lines):
        if line.endswith('-'):
            # the end of the word is at the start of next line
            end = lines[num+1].split()[0]
            # we remove the - and append the end of the word
            lines[num] = line[:-1]  + '<pc force="weak">-</pc><lb break="no"/>' + end
            # and remove the end of the word and possibly the
            # following space from the next line
            lines[num+1] = lines[num+1][len(end)+1:]

    return '\n'.join(lines)

if len(sys.argv) != 2:
    print('usage: python3 text2tei.py <text-folder>')
    exit()

text_path = sys.argv[1] + '/*.txt'
text_files = glob.glob(text_path)


root = ET.Element("text")

front = ET.SubElement(root, "front")
body = ET.SubElement(root, "body")
main_div = ET.SubElement(body, 'div')
main_div.set('type', 'document')


for file in sorted(text_files):
    filename = os.path.basename(file)
    seq_n, pg_n, pg_id = filename_to_seq_number(filename)

    with open(file, encoding='utf-8-sig') as fp:
        text = fp.read()

    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    text = new_encode_hyphens(text)
    url = 'https://texashistory.unt.edu/ark:/67531/metapth5872/m1/{}/'.format(seq_n)

    pb = ET.SubElement(main_div, 'pb')
    pb.set('n', pg_n)
    pb.set('xml:id', pg_id)
    pb.set('facs', url)
    p = ET.XML('<p>{}</p>'.format(text))
    main_div.append(p)

# ET.indent(root, space=' ', level=0)
print(ET.tostring(root, encoding='unicode'))