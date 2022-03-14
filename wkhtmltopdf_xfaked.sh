#!/bin/bash
xvfb-run -a -s "-screen 0 1300x800x24" wkhtmltopdf -q $*