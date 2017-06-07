start: clean
	@ ./start_script.sh

clean:
	@ rm -rf ./env
	@ rm -f trades.txt prices.txt states.txt
	@ find . -name "*.pyc" -type f -delete
