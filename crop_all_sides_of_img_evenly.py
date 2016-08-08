import sys
import os
from PIL import Image


if len(sys.argv) != 4:
   print "Usage:"
   print "python {} <img> <dest> <d>".format(sys.argv[0])
   print "Where d is how much out of 100 to trim off edges."
   sys.exit()

img = Image.open(sys.argv[1])

pct = float(sys.argv[3])/100.0

cropped = img.crop(
   (
      # img.size[0] is width
      img.size[0]*pct,

      # img.size[1] is height
      img.size[1]*pct,

      img.size[0]*(1 - pct),

      img.size[1]*(1 - pct)
   )
)

cropped.save(sys.argv[2])
