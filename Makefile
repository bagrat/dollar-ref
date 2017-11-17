ARGS = "$(filter-out $@,$(MAKECMDGOALS))"

help:
	@echo "# dollar-ref dev makefile"

install:
	@pipenv install

test: clean
	@pipenv run pytest --cov=dollar_ref -v --tb=long $(ARGS)

build: clean
	@echo "[INFO] installing dev dependencies"
	pipenv install --dev
	@echo "[INFO] installing the package"
	python setup.py install
	@echo "[INFO] running tests"
	pipenv run pytest --cov=dollar_ref -v --tb=long

clean:
	@echo "[INFO] Removing all *.pyc files..."
	@find . -name "*.pyc" -delete


# All the below lines are for the purposes of enabling
# to pass the arguments passed at the command invocation
# into the target recepies.
.PHONY: ACTION

ACTION:

%: ACTION
	@:
