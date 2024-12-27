REJECT poetry, EMBRACE pip!

## Run in docker
```shell
docker compose --env-file compose/envs/local.env up --build -d
```

## Run locally
```shell
python src/manage.py runserver
```


## Logs
```shell
tail -n 50 /tmp/logs/uwsgi.log
```

```shell
tail -n 50 /var/log/nginx/access.log
```
