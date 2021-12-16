import xmpp



def test_message(sess, mess):
    nick=mess.getFrom().getResource()
    text=mess.getBody()
    print("[Message]{}:{}".format(nick,text))



def TestRecMsg():
    from_user = "test02"
    from_user_pwd = "123456"

    
    server_ip = "192.168.247.17"
    server_port = 5223

    msg = "hello world!!!"

    client = xmpp.Client( server_ip )
    client.connect( server = (server_ip, server_port) )
    client.auth(from_user, from_user_pwd)

    client.RegisterHander("message",test_message)
    client.sendInitPresence()




if __name__ == "__main__":
    TestRecMsg()