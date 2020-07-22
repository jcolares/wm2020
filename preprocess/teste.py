from preprocessing import json_2_bitmap
import cv2

sourcefile = 'data/bike-mountain-mountain-biking-trail-163491.png.json'
destfile = 'data/bike-mountain-mountain-biking-trail-163491-mask.png'

mask_img = json_2_bitmap(sourcefile, destfile)

# Display results
if destfile != '':
    cv2.imshow('image', mask_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
