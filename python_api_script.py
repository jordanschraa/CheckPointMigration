from header import authenticate, api_post

def main():
    cred = authenticate()
    print("Sucessfully authenticated to managment server")
    print("SID: " + cred["sid"])

if __name__ == "__main__":
    main()