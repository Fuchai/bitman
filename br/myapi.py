# so that I don't have to publish my binance api to github

with open("/home/jasonhu/Documents/binance2.api",'r') as api_info:
    api_info.readline()
    api_key=api_info.readline().strip()
    api_info.readline()
    api_secret=api_info.readline().strip()

# print(api_secret)
# print(api_key)