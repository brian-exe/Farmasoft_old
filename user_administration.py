class User():
    def __init__(self, name, password,active =False):
        self.name = name
        self.password = password
        self.active = active

    def __repr__(self):
        return '<User %r>' % self.name
    def is_authenticated(self):
        return True
    def is_active(self):
        return self.active
    def is_anonymous(self):
        return False
    def get_id(self):
        return str(self.name)

class UserRepository():
    def __init__(self,path=''):
        self.filePath=path
    def authenticate_user(self,name,password):
        with open(self.filePath,'r') as usersFile:
            user = None
            for line in usersFile:
                line_list= line.split(",")
                str_user=line_list[0].strip()
                str_pass=line_list[1].strip()
                str_active=line_list[2].strip()
                bool_active=str_active=='1'

                if (name == str_user):
                    if (password== str_pass):
                        user=User(name,password,bool_active)
        return user
    def getUser(self,name):
        with open(self.filePath,'r') as usersFile:
            user = None
            for line in usersFile:
                line_list= line.split(",")
                str_user=line_list[0].strip()
                str_pass=line_list[1].strip()
                str_active=line_list[2].strip()
                bool_active=str_active=='1'
                
                if (name == str_user):
                    user=User(name,str_pass,bool_active)
        return user 
