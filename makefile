start:
	@ ./start_script.sh

clean:
	@ rm -rf ./env
	@ rm -f trades.txt
	@ find . -name "*.pyc" -type f -delete
