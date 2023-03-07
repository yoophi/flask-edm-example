# flask with json logging

JSON 방식의 Logger 를 적용하기 위한 테스트 

```bash
$ poetry install
$ poetry run flask run 
```

examples

```bash
$ http :5005  # fail
$ http :5005 message=="hello, world!" # sucess
```
