## Test Setup

```bash
# from project root
pip install requests==2.19.1 --no-warn-script-location --root ./one/
pip install requests==2.25.0 --no-deps --no-warn-script-location --root ./two
PYTHONPATH="$PYTHONPATH:one/Users/jeremyp/.pyenv/versions/3.8.6/envs/import/lib/python3.8/site-packages/:two/Users/jeremyp/.pyenv/versions/3.8.6/envs/import/lib/python3.8/site-packages/" python run.py
