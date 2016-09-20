PY?=python3

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

publish:
	PYTHONPATH='..' $(PY) run.py www-generate
