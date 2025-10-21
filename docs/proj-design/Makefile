all: clean design.pdf

design.pdf: design.tex
	latexmk -lualatex -shell-escape design.tex

clean:
	latexmk -c
