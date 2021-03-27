from fpdf import FPDF
from pathlib import Path
from PIL import Image
import re




def implement_style(text:str,style:str):
    type = Style
    if style=='it':
        return type.italic + text + type.it_end
    elif style=='bo':
        return type.bold + text + type.bold_end

def conversion_of_text(text:str):
    gen = list((x.start() for x in re.finditer('[\*\*__]{2}',text)))
    if gen:
        for x in range(0,len(gen)-1,2):
            word = implement_style(text[gen[x]+2:gen[x+1]],'bo')
            text = text[0:gen[x]] + word + text[gen[x+1]+2:] 
    gen = list((x.start() for x in re.finditer('[\*_]{2}',text)))
    if gen:
        for x in range(0,len(gen)-1,2):
            word = implement_style(text[gen[x]+2:gen[x+1]],'it')
            text = text[0:gen[x]] + word + text[gen[x+1]+2:]
        
    return text

def convertImage(image:str,path:str):
    img = Image.open(image)
    new_img_name_path = path + image[image.rindex('\\'):image.index('.png')]+'.jpg'
    img.save(new_img_name_path)
    return new_img_name_path

def writeToPDF(MDFiles:list,images:str,font:str='Arial'):
    pdf = FPDF()
    pdf.add_page()
    for file in MDFiles:
        with open(file, 'r') as mdFile:
            text = mdFile.readlines()
            for line in text:
                
                if line.startswith('#'):
                    num = line.count('#')
                    pdf.set_font(font,'B',size=35-(num-1)*8)
                    pdf.write(10,txt=line.strip('#').strip()+'\n\n')
        
                elif line.startswith('!'):
                    img_file = path + '\\' + line[line.index('(')+1:line.index(')')]
                    new_file = convertImage(img_file,path)
                    pdf.image(new_file,w=100,h=90)

                elif (line.strip().startswith('**') and line.strip().endswith('**')) or (line.strip().startswith('__') and line.strip().endswith('__')):
                    pdf.set_font(font,'B',size=12)
                    pdf.write(10,txt = line.strip().replace('**',"").replace('__',"") + '\n')
                

                elif (line.strip().startswith('*') and line.strip().endswith('*')) or (line.strip().startswith('_') and line.strip().endswith('_')):
                    pdf.set_font(font,'I',size=20)
                    pdf.write(10,txt = line.strip().replace('*',"").replace('_',"") + '\n')
                
                elif line.strip().startswith('*'):
                    num = 0
                    while True:
                        if line[num]==' ':
                            num += 1
                        else:
                            break
                    x_pos = pdf.get_x()
                    y_pos = pdf.get_y()
                    pdf.rect(x=x_pos-2,y=y_pos+5,w=2,h=2,style='F')
                    pdf.set_font(font,size=15)
                    pdf.write(10+(num*2),txt = line.strip().replace('*',"") + '\n')
                
                elif line.strip().startswith('-'):
                    num = 0
                    while True:
                        if line[num]==' ':
                            num += 1
                        else:
                            break
                    x_pos = pdf.get_x()
                    y_pos = pdf.get_y()
                    pdf.rect(x=x_pos-4,y=y_pos+3,w=3,h=3,style='F')
                    pdf.set_font(font,size=15)
                    pdf.write(10+(num*2),txt = line.strip().replace('-',"") + '\n')
                
                else:
                    pdf.set_font(font,size=15)
                    pdf.write(10,txt = line)  
        pdf.add_page()
    pdf.output('generated.pdf')

def getMDFiles(path):
    path_lib = Path(path)
    listFiles = path_lib.iterdir()
    MDFiles = []
    for file in listFiles:
        if file.is_file():
            if str(file).endswith('.md') and 'README' not in str(file):
                MDFiles.append(str(file))
    return MDFiles
    

if __name__=='__main__':
    print('Enter the path where the markdown files are present')
    path = input()
    print('Enter the path where the images are present')
    image_path = input()
    files = getMDFiles(path)
    writeToPDF(files,image_path)
              