
# run all test files
test:
	(cd src; python3 -m unittest)


tags: 
	ctags -R src/
