PY3 := $(shell command -v python3 2> /dev/null)
ifdef PY3
  PY?=python3
else
  PY?=python
endif

help:
	@echo 'Makefile to create the HTTP Observatory website'
	@echo ''
	@echo 'Usage:'
	@echo '    make generate                    (re)generate the site'
	@echo '    make devserver                   constantly regen site with automatic refreshing'

devserver:
	$(PY) devserver.py

deploy:
	cd .. && git subtree push --prefix httpobsdashboard/dist origin gh-pages

generate: json-generate www-generate

improvements:
	PYTHONPATH='..' $(PY) scripts/improvements.py

json-generate:
	PYTHONPATH='..' $(PY) run.py json-generate

www-generate:
	PYTHONPATH='..' $(PY) run.py www-generate
