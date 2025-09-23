all: clean requirements

requirements.tex: requirements.md requirements-template.tex
	pandoc \
		requirements.md \
		-f markdown+pipe_tables+table_captions+lists_without_preceding_blankline \
		--template=requirements-template.tex \
		-t latex \
		-o requirements.tex

requirements.docx: requirements.md
	pandoc \
		requirements.md \
		-f markdown+pipe_tables+table_captions+lists_without_preceding_blankline \
		--toc=true \
		-t docx \
		-o requirements.docx

requirements.pdf: requirements.tex
	latexmk -lualatex requirements.tex 
	latexmk -c requirements.tex

requirements: requirements.pdf

clean:
	latexmk -c
	rm -f \
		requirements.docx \
		requirements.tex \
		requirements.pdf
