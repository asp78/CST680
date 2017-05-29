start:
	@ ./start_script.sh

clean:
	@ rm -rf ./env
	@ find . -name "*.pyc" -type f -delete
