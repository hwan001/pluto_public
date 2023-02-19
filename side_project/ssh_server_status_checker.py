import paramiko

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware

def ssh_command_sender(ip, port, user, pw, cmds):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    ssh.connect(ip, port, user, pw, timeout=1)

    stdin, stdout, stderr = ssh.exec_command(";".join(cmds))

    lines = stdout.read()
    res = ''.join(str(lines))
    
    return res

def _health_check(ip, port, user, pw):
    try:
        ssh_command_sender(ip, port=port, user=user, pw=pw, cmds=[])
        return True
    except:
        return False


origins = ["*"]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class serverSettings(BaseModel):
    key: str
    ip: str
    port: str
    id: str
    pw: str
    
dict_server_info = {
    #"server1":{"ip":"", "port":"22", "id":"", "pw":"", "status":""},
}

@app.post("/statusCheck")
async def statusCheck(info: serverSettings):
    key = info.key
    try:
        dict_server_info[key]["ip"] = info.ip
        dict_server_info[key]["port"] = info.port
        dict_server_info[key]["id"] = info.id
        dict_server_info[key]["pw"] = info.pw
    except:
        dict_server_info[key] = {"ip":info.ip, "port":info.port, "id":info.id, "pw":info.pw, "status":""}
        
    print(dict_server_info[key])

    print(f"{key} health check ...", end="")
    if _health_check(dict_server_info[key]["ip"], dict_server_info[key]["port"] , dict_server_info[key]["id"], dict_server_info[key]["pw"]) == False:
        print("error")
        return {"status":f"fail - {key} connect"}
    
    print("ok")
    dict_server_info[key]["status"] = "ok"
    return {"status":"ok"}
 

if __name__ == "__main__":
    uvicorn.run(app, port=8000, reload=False)
