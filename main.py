from argparse import ArgumentParser
from pypdf import PdfReader,PdfWriter,PageObject
from pprint import pprint
from copy import copy,deepcopy
import math

class pos:
    def __init__(self,x,y):
        self.x=x
        self.y=y


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--input",required=True)
    parser.add_argument("--output",default="output/output.pdf",required=False)
    args=parser.parse_args()
    input=args.input
    output=args.output
    reader = PdfReader(input)
    writer = PdfWriter()
    for i,page in enumerate(reader.pages):
        #pprint(page)
        x0,y0 = page.mediabox.upper_left
        x1,y1 = page.mediabox.lower_right

        pages_new = [deepcopy(page)]*4
        for i,p in enumerate(pages_new):
            # 0,0 ~ 1,1 
            # 1,0 ~ 2,1
            # 0,1 ~ 1,2
            # 1,1 ~ 2,2
            upper_left = pos(
                x0+(x1-x0)*(i%2)/2,
                y0+(y1-y0)*math.floor(i/2)/2
            )
            lower_right = pos(
                upper_left.x+(x1-x0)/2,
                upper_left.y+(y1-y0)/2
            )
            p.cropbox.upper_left=(upper_left.x,upper_left.y)
            p.cropbox.upper_right=(lower_right.x,upper_left.y)
            p.cropbox.lower_left=(upper_left.x,lower_right.y)
            p.cropbox.lower_right=(lower_right.x,lower_right.y)
            #pages_new[i]=p
            writer.add_page(p)
    #writer.add_blank_page(width=512,height=512)
    writer.write(output)

