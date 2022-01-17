#! /usr/bin/env python3
import sys

class Image:
    def __init__(self, pixelmap, oob_pixel=0):
        self.xmin = 0
        self.xmax = 0
        self.ymin = 0
        self.ymax = 0
        self.pixelmap = pixelmap
        self.lit_pixels = set()
        self.oob_pixel = oob_pixel

    def lit(self, x,y):
        self.xmin=min(self.xmin, x)
        self.xmax=max(self.xmax, x)
        self.ymin=min(self.ymin, y)
        self.ymax=max(self.ymax, y)
        self.lit_pixels.add( (x,y) )

    def enhance(self):
        oob_pixel = self.pixelmap[0 if self.oob_pixel==0 else 511]
        img = Image(self.pixelmap, oob_pixel)
        for y in range(self.ymin-1, self.ymax+2):
            for x in range(self.xmin-1, self.xmax+2):
                signature = 0
                for j in y-1,y,y+1:
                    for i in x-1,x,x+1:
                        if i<self.xmin or self.xmax<i or j<self.ymin or self.ymax<j:
                            pixel = self.oob_pixel
                        else:
                            pixel = 1 if (i,j) in self.lit_pixels else 0
                        signature = (signature*2) + pixel
                assert(0<=signature and signature<512)
                if self.pixelmap[signature] == 1:
                    img.lit(x,y)
        return img

    def pixelcount(self):
        return len(self.lit_pixels)

    def __repr__(self):
        res = []
        for y in range(self.ymin-5, self.ymax+6):
            s = ''
            for x in range(self.xmin-5, self.xmax+6):
                if x<self.xmin or self.xmax<x or y<self.ymin or self.ymax<y:
                    pixel = '+' if self.oob_pixel==1 else ':'
                else:
                    pixel = '#' if (x,y) in self.lit_pixels else '.'
                s += pixel
            res.append(s)
        return '\n'.join(res)


def parse(inputs):
    pixelmap = list(map(lambda x: 1 if x=='#' else 0, inputs[0]))
    assert(len(pixelmap)==512)
    img = Image(pixelmap)
    for y,line in enumerate(inputs[2:]):
        for x,pixel in enumerate(line):
            if pixel=='#':
                img.lit(x,y)

    return img



if __name__=='__main__':
    mode = '1' if len(sys.argv)<2 else sys.argv[1]
    img = parse([line.strip() for line in sys.stdin])

    if mode == '1':
        img = img.enhance().enhance()
        print(img)
        print(img.pixelcount())

    if mode == '2':
        for _ in range(50):
            img = img.enhance()
        print(img.pixelcount())
