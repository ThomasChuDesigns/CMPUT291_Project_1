from uuid import uuid4
import requests


def main():
    r = requests.get('https://randomuser.me/api/?nat=us&results=100').json()

    for result in r['results']:
        name = result['name']
        user = result['login']
        print("NAME: {}, USER: {}, PASS: {}".format(name['first'] + ' ' + name['last'], user['username'], user['password']))
        

if __name__ == "__main__":
    main()
