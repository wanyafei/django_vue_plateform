from django.conf import settings
# 获取/解析token用到的模块
import itsdangerous
import uuid

# class Token():
#     # 把settings中的一串字符串作为 secretkey
#     tjss=itsdangerous.TimedJSONWebSignatureSerializer(settings.SECRET_KEY)
#     @classmethod
#     def create_token(cls,data):
#         token=cls.tjss.dumps(data).decode()
#         # data是根据什么获取的token,比如根据用户的用户名和密码
#         return token

def generatetoken():
    token=str(uuid.uuid4()).replace('-',"")
    return token

a=[1,2,3,4,5,6]
b=[4,5]
aa=3
bb=8
print()



