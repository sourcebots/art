# Requires inkscape in path and PDF module
import argparse
import csv
import numpy as np
import os
import pathlib
import sys
from PDF import PdfFileReader, PdfFileWriter
from subprocess import Popen

def argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'template_svg',
        help="Input svg template with text matching 'NAME OF STUDENT IN CAPS' and 'NAME OF SCHOOL IN CAPS' for "
             "replacement with the students' names and schools'/teams' names, respectively, "
             "on the produced certificates.",
        type=pathlib.Path,
    )
    parser.add_argument(
        'input_data',
        help="Input csv with columns of 'First Name', 'Last Name', and 'School'."
             "In absence of this argument, the script's own test data will be used.",
        type=pathlib.Path,
        nargs='?',
        default=-1,
    )
    parser.add_argument(
        'output_path',
        help="Path in which the output will be deposited. Defaults to current working directory.",
        type=pathlib.Path,
        nargs='?',
        default=os.getcwd(),
    )
    return parser

def main(arguments):
    options = argument_parser().parse_args(arguments)
    
    outpath = pathlib.Path(options.output_path, "Certificates.pdf")
    tempsvgpath = pathlib.Path(options.output_path, ".temp-cert.svg")
    temppdfpath = pathlib.Path(options.output_path, ".temp-cert.pdf")
    
    if options.input_data == -1:
        firstnames = ["", "WWWWWWW",
                      "Cave", "Aleph",
                      "Theresa", "Blon Fel-Fotch Passameer-Day"]
        lastnames = ["", "WWWWWWWW",
                     "Johnson", "Null",
                     "Green", "Slitheen"]
        schools = ["", "WWWWWWWWWWWWWWWWWWWWWWWWW",
                   "Aperture Fixtures", "Hilbert's Hotel",
                   "L33T Haxxor$ and C00L K@s", "High Raxicoricofallapatorian School of Interplanetary Conquest"]
    else:
        with open(str(options.input_data)) as datacsv:
            csvreader = csv.reader(datacsv)
            rows = np.array([row for row in csvreader])
        headings = list(rows[0])
        data = rows[1:]
        firstnames = data[:, headings.index("First Name")]
        lastnames = data[:, headings.index("Last Name")]
        schools = data[:, headings.index("School")]
            
    studentno = len(firstnames)
    
    with options.template_svg.open() as tempfile:
        template = tempfile.read()
    
    # Generate pdf output file and facility for adding pages to it
    outfile = open(str(outpath), "wb")
    outwriter = PdfFileWriter()
    
    print("Create Document...")
    for i in range(studentno):
        print(" - Start cert %s..." % (i + 1))
        name = firstnames[i] + " " + lastnames[i]
        # Generate temporary svg with the name and school substituted in
        print("    - Create SVG...")
        with open(str(tempsvgpath), "w") as tempfile:
            cert = name.upper().join(template.split("NAME OF THE STUDENT IN CAPS"))
            cert = schools[i].upper().join(cert.split("NAME OF THE SCHOOL IN CAPS"))
            tempfile.write(cert)
        # Command inkscape to convert it into a pdf
        print("    - SVG created. Convert to PDF...")
        a = Popen(["inkscape",
                   str(tempsvgpath),
                   r"--export-pdf=%s" % str(temppdfpath)])
        # Force the script to wait for it to convert before moving on
        a.communicate()
        # Adds the generated certificate to the document
        print("    - PDF created. Add to document...")
        with open(str(temppdfpath), "rb") as tempfile:
            certpdf = PdfFileReader(tempfile)
            outwriter.addPage(certpdf.getPage(0))
            outwriter.write(outfile)
        print("    - Added to document. Cert %s Complete." % (i + 1))
    
    print("Document complete.")
    
    # Clean up the mess
    outfile.close()
    os.remove(str(tempsvgpath))
    os.remove(str(temppdfpath))

if __name__ == '__main__':
    main(sys.argv[1:])
