from header import authenticate, api_post

def main():
    cred = authenticate()
    print(cred)

if __name__ == "__main__":
    main()