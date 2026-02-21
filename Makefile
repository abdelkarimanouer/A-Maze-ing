run:
	@python3 a_maze_ing.py config.txt

clean:
	rm -rf __pycache__ *.pyc .mypy_cache

build:
	python3 -m poetry build

install:
	pip install *.whl
