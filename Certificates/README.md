# Certificate Generation script

cert-gen can be run from the commandline, assuming you have Inkscape in your path and the relevant python modules installed.

```

usage: cert-gen.py [-h] [-i INPUT_DATA] [-o OUTPUT_PATH] template_svg

positional arguments:
  template_svg          Input svg template with text matching 'NAME OF STUDENT
                        IN CAPS' and 'NAME OF SCHOOL IN CAPS' for replacement
                        with the students' names and schools'/teams' names,
                        respectively, on the produced certificates.

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_DATA, --input_data INPUT_DATA
                        Input csv with columns of 'First Name', 'Last Name',
                        and 'School'.In absence of this argument, the script's
                        own test data will be used.
  -o OUTPUT_PATH, --output_path OUTPUT_PATH
                        Path in which the output will be deposited. Defaults
                        to current working directory.

```