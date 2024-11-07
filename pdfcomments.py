import fitz  # PyMuPDF library
from itertools import groupby
from optparse import OptionParser
parser = OptionParser()
parser.add_option( "--pdffile",
                  action="store", dest="pdffile", default=None,
                  help="FILE containing pdf comments", metavar="FILE")
(options, args) = parser.parse_args()

def print_hightlight_text(page, rect):
    """Return text containted in the given rectangular highlighted area.

    Args:
        page (fitz.page): the associated page.
        rect (fitz.Rect): rectangular highlighted area.
    """
    words = page.getText("words")  # list of words on page
    words.sort(key=lambda w: (w[3], w[0]))  # ascending y, then x
    mywords = [w for w in words if fitz.Rect(w[:4]).intersects(rect)]
    group = groupby(mywords, key=lambda w: w[3])
    for y1, gwords in group:
        print(" ".join(w[4] for w in gwords))
    print("\n\n")



# Load the PDF
if (options.pdffile != None ):
  doc = fitz.open(options.pdffile)
  
  # print and capture
  for page_num in range(len(doc)):
      page = doc[page_num]
      for annot in page.annots():
          if annot.info != None:  # Checking for comment annotations
              comment = annot.info["content"]
              print(f"Page {page_num + 1}: {comment}")
          print_hightlight_text(page, annot.rect)
else:
  parser.print_help()
  print (options)
