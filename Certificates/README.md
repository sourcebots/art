# Requirements

In order for the certificates to render correctly and the certificate generation script to function, you need to have the URW Chancery L font installed, python installed, InkScape installed and in your path, and the PyPDF2 and csv python modules.

http://www.fontsplace.com/urw-chancery-l-medium-italic-free-font-download.html

https://inkscape.org/en/release/0.92.3/

# Certificate Generation script

cert-gen can be run from the commandline, assuming you have Inkscape in your path and the relevant python modules installed.

```

usage: cert-gen.py [-h] template_svg input_data output_file

positional arguments:
  template_svg  Input svg template with text matching 'NAME OF THE STUDENT IN
                CAPS' and 'NAME OF THE SCHOOL IN CAPS' for replacement with
                the students' names and schools'/teams' names, respectively,
                on the produced certificates.
  input_data    Input csv with columns of 'Name', and 'School'.
  output_file   Name of the output file with the certificates in it for
                printing.

optional arguments:
  -h, --help    show this help message and exit

```