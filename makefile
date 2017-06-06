start:
	@ ./start_script.sh

clean:
	@ rm -rf ./env
	@ rm -f prices.txt state.txt
	@ find . -name "*.pyc" -type f -delete
