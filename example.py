from MyTTPy.client import MyTTClient

if __name__ == "__main__":
    client = MyTTClient()
    #client.log_in("username", "password")
    me = client.get_player("Timo", "Boll", "Düsseldorf")
    print(me)