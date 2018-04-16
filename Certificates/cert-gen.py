# Requires inkscape in path and PDF module
import argparse
from csv import DictReader
import os
from PDF import PdfFileReader, PdfFileWriter
import subprocess
from tempfile import NamedTemporaryFile

STUDENT_NAME_PLACEHOLDER = "NAME OF THE STUDENT IN CAPS"
SCHOOL_NAME_PLACEHOLDER = "NAME OF THE SCHOOL IN CAPS"
CWD = os.getcwd()


def argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'template_svg',
        help="Input svg template with text matching '{}' and '{}' for "
             "replacement with the students' names and schools'/teams' names, respectively, "
             "on the produced certificates.".format(STUDENT_NAME_PLACEHOLDER, SCHOOL_NAME_PLACEHOLDER),
        type=argparse.FileType('r'),
    )
    parser.add_argument(
        'input_data',
        help="Input csv with columns of 'Name', and 'School'.",
        type=argparse.FileType('r'),
    )
    parser.add_argument(
        'output_file',
        help="Name of the output file with the certificates in it for printing.",
        type=argparse.FileType('wb'),
    )
    return parser


def main():
    options = argument_parser().parse_args()
    
    with options.input_data as datacsv:
        csvdata = [row for row in DictReader(datacsv)]
    
    print("Certificates generated from:\n - {}\n - {}".format(options.template_svg.name,
                                                              options.input_data.name))
    with options.template_svg as templatefile:
        template = templatefile.read()
    
    # Generate pdf output file and facility for adding pages to it
    with options.output_file as outfile:
        outwriter = PdfFileWriter()
        
        print("Create Document...")
        for i, row in enumerate(csvdata):
            print(" - Start cert {}...".format(i + 1))
            name = row["Name"]
            # Generate temporary svg with the name and school substituted in, and temporary pdf for converted file
            print("    - Create SVG...")
            with NamedTemporaryFile(dir=CWD, suffix=".svg") as svgfile, \
                    NamedTemporaryFile(dir=CWD, suffix=".pdf") as pdffile:
                cert = template.replace(STUDENT_NAME_PLACEHOLDER, name.upper())
                cert = cert.replace(SCHOOL_NAME_PLACEHOLDER, row["School"].upper())
                svgfile.write(bytes(cert, 'utf-8'))
                # Command inkscape to convert it into a pdf
                print("    - SVG created. Convert to PDF...")
                subprocess.run(['inkscape',
                                svgfile.name,
                                '--export-pdf',
                                pdffile.name],
                               check=True)
                # Adds the generated certificate to the document
                print("    - PDF created. Add to document...")
                certpdf = PdfFileReader(pdffile)
                outwriter.addPage(certpdf.getPage(0))
                outwriter.write(outfile)
                print("    - Added to document. Cert", i + 1, "Complete.")
                
        print("Document complete. Saved to:\n -", options.output_file.name)


if __name__ == '__main__':
    main()
