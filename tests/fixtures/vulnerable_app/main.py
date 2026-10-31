from vendor.lib_auth import verify_token_weak
from worker import background_task

def process_request(auth_header, data):
    # This path calls the vulnerable weak token function!
    if verify_token_weak(auth_header):
        return background_task(data)
    return "unauthorized"

def main():
    token = "guest:demo"
    return process_request(token, "sample data")

if __name__ == "__main__":
    main()
