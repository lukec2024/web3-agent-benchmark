### Requirements
surfpool - https://github.com/lukec2024/surfpool/actions/runs/20140125200
```
pip install gunicorn
pip install -r requirements.txt
```

### How to run
```
surfpool start --no-tui -u <rpc_url> -t 390

# Dev
python run.py
# Prod
gunicorn -c gunicorn.conf.py run:server
```