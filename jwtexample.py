import jwt

payload_data = {
    "sub":"4242",
    "name":"jessica",
    "nickname":"ak"
}

token = jwt.encode(payload=payload_data,key="akshay")

print(token)

"""eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI0MjQyIiwibmFtZSI6Implc3NpY2EiLCJuaWNrbmFtZSI6ImFrIn0.xg3zh-8VpcpI1QNLVngz6NzuANid5jvWQJBHflKP6fI"""
