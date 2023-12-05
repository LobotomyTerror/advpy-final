PROGRAM = python3
MAIN = main.py
DATABASE = database.py
FLASK = f_app.py
TESTMAIN = ../test/test_main.py
TEST = pytest
STYLE_FIX = autopep8 --in-place --recursive --aggressive --aggressive

.PHONY: test
test:
	$(TEST) $(TESTMAIN)

.PHONY: run
run:
	$(PROGRAM) $(MAIN)

.PHONY: mypy
mypy:
	mypy --strict $(MAIN)
	mypy --strict $(DATABASE)
	mypy --strict $(FLASK)
	mypy --strict $(TESTMAIN)

.PHONY: style
style:
	flake8 $(MAIN)
	flake8 $(DATABASE)
	flake8 $(FLASK)
	flake8 $(TESTMAIN)

.PHONY: style-fix
style-fix:
	$(STYLE_FIX) $(MAIN)
	$(STYLE_FIX) $(DATABASE)
	$(STYLE_FIX) $(FLASK)
	$(STYLE_FIX) $(TESTMAIN)

.PHONY: clean
clean:
	@rm -rf __pycache__
	@rm -rf .mypy_cache
	@rm -rf .pytest_cache
	@echo "All Clean"

.PHONY: all
all: mypy style style-fix test