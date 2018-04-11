# Certificate Generation script

cert-gen can be run from the commandline, assuming you have Inkscape in your path and the relevant python modules installed.

```

usage: cert-gen.py [-h] template_svg [input_data] [output_path]

positional arguments:
  template_svg  Input svg template with text matching 'NAME OF STUDENT IN
                CAPS' and 'NAME OF SCHOOL IN CAPS' for replacement with the
                students' names and schools'/teams' names, respectively, on
                the produced certificates.
  input_data    Input csv with columns of 'First Name', 'Last Name', and
                'School'.In absence of this argument, the script's own test
                data will be used.
  output_path   Path in which the output will be deposited. Defaults to
                current working directory.

optional arguments:
  -h, --help    show this help message and exit

```