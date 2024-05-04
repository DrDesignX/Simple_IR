install:
    pip install -r requirements.txt

# test:
#     python -m unittest discover -s tests -p '*_test.py'

run:
    python app.py

clean:
    rm -rf __pycache__ .pytest_cache
