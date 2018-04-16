# Requires inkscape in path and PDF module
import argparse
import csv
import numpy as np
import os
import pathlib
from PDF import PdfFileReader, PdfFileWriter
from subprocess import run

STUDENT_NAME_PLACEHOLDER = "NAME OF THE STUDENT IN CAPS"
SCHOOL_NAME_PLACEHOLDER = "NAME OF THE SCHOOL IN CAPS"


def argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'template_svg',
        help="Input svg template with text matching '{}' and '{}' for "
             "replacement with the students' names and schools'/teams' names, respectively, "
             "on the produced certificates.".format(STUDENT_NAME_PLACEHOLDER, SCHOOL_NAME_PLACEHOLDER),
        type=pathlib.Path,
    )
    parser.add_argument(
        '-i', '--input_data',
        help="Input csv with columns of 'First Name', 'Last Name', and 'School'."
             "In absence of this argument, the script's own test data will be used.",
        nargs=1,
        type=pathlib.Path,
    )
    parser.add_argument(
        '-o','--output_path',
        help="Path in which the output will be deposited. Defaults to current working directory.",
        type=pathlib.Path,
        nargs=1,
        default=os.getcwd(),
    )
    return parser

def main():
    options = argument_parser().parse_args()
    
    outpath = pathlib.Path(options.output_path, "Certificates.pdf")
    tempsvgpath = pathlib.Path(options.output_path, ".temp-cert.svg")
    temppdfpath = pathlib.Path(options.output_path, ".temp-cert.pdf")
    
    if options.input_data == None:
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
    
    print(options.template_svg)
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
            cert = template.replace(STUDENT_NAME_PLACEHOLDER, name.upper())
            cert = cert.replace(SCHOOL_NAME_PLACEHOLDER, schools[i].upper())
            tempfile.write(cert)
        # Command inkscape to convert it into a pdf
        print("    - SVG created. Convert to PDF...")
        run(["inkscape",
             str(tempsvgpath),
             r"--export-pdf=%s" % str(temppdfpath)])
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
    main()
