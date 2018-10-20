#! /bin/sh

pandoc "${1:?filen name?}" -c "$HOME/raas-garba/pr2html.css" -s -o /tmp/"${1%.*}.html"
