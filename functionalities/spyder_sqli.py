import requests

#check for SQLi by SQL chars
def check_sqli(url,action,params):
    data = {}
    for x in params:
        data[x] = 'test'
    r = requests.post(f'{url}+{action}',data=data,verify=False)
    print(r.status_code)

    #check 1
    for x in params:
        data[x] = "'"
        r = requests.post(f'{url}+{action}',data=data,verify=False)
        if r.status_code == 500 or 302:
            print(f'Parameter {x} is vuln to SQLi')
        data[x] = 'test'
    print(data)