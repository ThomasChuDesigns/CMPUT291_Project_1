from uuid import uuid4
import requests


def main():
    r = requests.get('https://randomuser.me/api/?results=100')
    r.json()

    for k,v in r:
        print(k, v)

    #for i in range(0, 100):
        
    #print(str(uuid4()).split('-')[0])
        

if __name__ == "__main__":
    main()
