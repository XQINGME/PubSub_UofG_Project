#import xmppy
import xmpp

def TestSendMsg():
    from_user = ""
    from_user_pwd = ""

    to_user = "test02"
    
    server_ip = "192.168.247.17"
    server_port = 5223

    msg = "hello world!!!"



    client = xmpp.Client( server_ip )
    client.connect( server = (server_ip, server_port) )
    client.auth(from_user, from_user_pwd, "botty")
    client.sendInitPresence()
    message = xmpp.Message(to_user, msg, typ = "chat")
    client.send(message)




if __name__ == "__main__":
    TestSendMsg()