PY?=python

help:
	@echo 'Makefile to create the HTTP Observatory website'
	@echo ''
	@echo 'Usage:'
	@echo '    make publish                     (re)generate the site'
	@echo '    make devserver                   constantly regen site with automatic refreshing'

devserver:
	$(PY) devserver.py

deploy:
	cd .. && git subtree push --prefix httpobsdashboard/dist origin gh-pages

generate: json-generate www-generate

json-generate:
	PYTHONPATH='..' $(PY) run.py json-generate

www-generate:
	PYTHONPATH='..' $(PY) run.py www-generate
