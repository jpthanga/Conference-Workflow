import requests
import json

def login():

    url = "https://cmt3.research.microsoft.com/api/odata/{conference}/{page}?{query}"

    session = requests.Session()

    session.headers = {
        'User-Agent':
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36',
        'Content-Type':
        'application/json'
    }

    # add user name and password for CMT or from config
    data = json.dumps({
        "Request": {
            "Email": '<email>',
            "Password": '<password>'
        }
    })

    session.post(
        url.format(
            conference='Users', page='Login', query="ReturnUrl=User/Index"), data)

    return session

# Example of service call
# response = session.get('https://cmt3.research.microsoft.com/api/odata/NIPS2018/Submissions(1)/Reviews')
# returns a JSON

