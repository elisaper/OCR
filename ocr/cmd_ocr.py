###command line tool for running tesseract from CMD

import sys
import ocr


filename = sys.argv[1]
exitcode, result = ocr.process_file(filename)
print(result)
exit(exitcode)