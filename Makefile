setup: requirements.txt
	pip install -r requirements.txt

run:
	python app.py

clean:
	rm -rf __pycache__

.PHONY: setup run clean
