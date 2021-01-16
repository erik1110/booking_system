import requests

def get():
    url = "http://127.0.0.1:8090/get_sample?name=hello"

    with requests.Session() as s:
        res = s.get(url)

    print(res.text)


def post():
    url = "http://127.0.0.1:8090/post_sample"
    data = {'key':'value'}

    with requests.Session() as s:
        res = s.post(url,data=data)

    print(res.text)
    
if __name__ == '__main__':
    get()
    post()