import requests
import bs4

"""
Manages connection to robot through RobotWebServices
"""


ROBOT_IP = "" # TODO find out the robot IP
BASE_URL = f"http://{ROBOT_IP}/rw"

HEADERS = {
    "Content-Type" : "application/json",
    "Accept" : "application/json"
    # TODO: Check if RWS for our controller requires authentication
    # "Authorization" : "Bearer --access token--"
}

# particularly interested in following directories:
# - rw/mastership/[request | release]/[e]
# - 
# - rw/rapid


class RBNetwork:
    def __init__(self,
            base_url: str=BASE_URL,
            headers: dict[str, str]=HEADERS) -> None:
        self.__base_url: str = base_url
        self.__headers: dict[str, str] = headers

    
    def acquire_mastership(self) -> bool:
        url = f"{self.__base_url}/mastership/acquire"
        response = requests.post(url, headers=self.__headers)

        if response.ok:
            print("Mastership of robot acquired!")
            return True
        else:
            print("ERROR: Failed to acquire mastership.")
            return False
    
    def query_endpoint(self, endpoint: str):
        a = self.__base_url+endpoint
        print(f"Finding endpoints after {a}")
        response = requests.get(a)
        if response.ok:
            soup = bs4.BeautifulSoup(response.content, 'html.parser')

            print('Discovered endpoints:')
            for link in soup.find_all('a'):
                href = link.get('href')
                if href:
                    print(href)
        else:
            print("ERROR: Failed to retrieve base URL: ", response.status_code)

    
    
        
        