
class BaseResponse(object):
    def __init__(self,code=20000,data=None,message=None):
        self.code=code
        self.data=data
        self.message=message
    @property
    def dict(self):
        return self.__dict__

if __name__ == '__main__':

    def tt():
        a = 98
        b = 67
        return a==b


    print(tt())