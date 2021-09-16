import time
import json
import requests
import pyEmail


class Miner:
    def __init__(self, name, wallet):
        self.__workers = []
        self.__minerName = name
        self.__wallet = wallet

    def add_worker(self, name, hashrate):
        __worker = Worker(self.__minerName, name, hashrate)
        self.__workers.append(__worker)
    
    def check(self):
        walletUrl = f"https://gpumine.org/api/worker?currency=ETH&address={self.__wallet}&rig="
        for worker in self.__workers:
            worker.check(walletUrl)
            time.sleep(60)
        
class Worker:
    def __init__(self, minerName = "NULL" , name = "NULL", hashrate = 0):
        self.__name   = name
        self.__minerName = minerName
        self.__hashrate = hashrate

    def get_worker_hashrate(self, url):
        while 1:
            try:
                minerData = requests.get(url).text
                minerDataJSON = json.loads(minerData)
                localHashrate = minerDataJSON['data']['hashChart']['day'][-1]['submitHashrate'] // 10**6
                return localHashrate
            except:
                print("Get info error...\n Retry in 60s")
                time.sleep(60)

    def check(self, url):
        workerLocalHashrate = self.get_worker_hashrate(f"{url}{self.__name}")

        if (self.__hashrate - workerLocalHashrate) > self.__hashrate*0.1:
            print(f"{self.__name}({self.__hashrate}) low hashrate.")
            pyEmail.alert_email(self.__minerName, self.__name)
        else:
            print(f"{self.__name}({self.__hashrate}) is mining in {workerLocalHashrate}MH.")

def main():
    with open("config.json") as configFile:
        workersDict = json.load(configFile)['miner']

    minerList = []
    for miner in workersDict.items():
        _miner = Miner(miner[0],miner[1]['wallet'])
        for worker in miner[1]['workers'].items():
            _miner.add_worker(worker[0],worker[1])
        minerList.append(_miner)
    
    # Check each worker work properly
    while 1:
        for miner in minerList:
            miner.check()


if __name__ == "__main__":
    main()