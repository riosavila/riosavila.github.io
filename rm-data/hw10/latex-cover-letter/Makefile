# Makefile for Professional LaTeX Cover Letter

# Compiler selection
LATEX = xelatex
BUILDDIR = ../build

# Source and output files
SRC = main.tex
PDF = $(BUILDDIR)/cover_letter.pdf

# Compilation flags
LATEXFLAGS = -output-directory=$(BUILDDIR) -interaction=nonstopmode -halt-on-error

# Compilation rules
all: $(PDF)

$(PDF): $(SRC)
	mkdir -p $(BUILDDIR)
	cd src && $(LATEX) $(LATEXFLAGS) $(SRC)
	cd src && $(LATEX) $(LATEXFLAGS) $(SRC)

view: $(PDF)
	open $(PDF)

clean:
	rm -rf $(BUILDDIR)/*.aux \
		   $(BUILDDIR)/*.log \
		   $(BUILDDIR)/*.out \
		   $(BUILDDIR)/*.pdf

.PHONY: all view clean