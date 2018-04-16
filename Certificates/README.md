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