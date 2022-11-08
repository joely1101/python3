import json
class RemoveModuleNameJSON(json.JSONEncoder):
    def default(self, o,iskey=False):
        if iskey == True and type(o) == type(''):
            if ':' in o:
                o=o.split(':',1)[1]
            return o
        elif type(o) == dict:
            return {self.default(key,True): self.default(value) for key, value in o.items()}
        elif type(o) == list or type(o) == tuple:
            return [self.default(item) for item in o]
        return o
    def encode(self, o):
        #do not strip root module name
        newo={}
        for key, value in o.items():
            print(f"{key}")
            newo[key]=self.default(value)
        return super().encode(newo)

str=""
with open("vrouter.json","r") as f:
    str=f.read()
    node=json.loads(str)

a=json.dumps(node, indent=4,sort_keys = False,cls=RemoveModuleNameJSON)
with open("./after.json","w+") as f:
    f.write(a)