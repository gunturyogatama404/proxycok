import threading
import queue
import requests

# Initialize the queue
q = queue.Queue()
lock = threading.Lock()  # For thread-safe writing to the file

# Read proxies from file and populate the queue
with open('allproxy.txt', 'r') as f:
    proxies = f.read().strip().split("\n")
    for proxy in proxies:
        q.put(proxy)

# Function to check proxy validity
def check_proxy():
    global q
    while not q.empty():
        proxy = q.get()
        try:
            # Send a request using the proxy
            res = requests.get('http://ipinfo.io/json', proxies={'http': proxy, 'https': proxy}, timeout=5)
            if res.status_code == 200:
                print(f"Valid proxy: {proxy}")
                # Save the valid proxy to the file in real-time
                with lock:
                    with open('valid.txt', 'a') as f:
                        f.write(proxy + '\n')
        except requests.RequestException as e:
            # Handle request errors (timeout, connection errors, etc.)
            print(f"Proxy failed: {proxy} | Error: {e}")
        finally:
            q.task_done()  # Mark the task as done

# Create and start threads
threads = []
for _ in range(100):  # Adjust the number of threads as needed
    t = threading.Thread(target=check_proxy)
    t.start()
    threads.append(t)

# Wait for all threads to complete
for t in threads:
    t.join()

# Final message
print("\nProxy checking complete. Valid proxies have been saved to valid.txt.")
