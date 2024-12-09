import os
import subprocess
import time
import json

# Khởi tạo các biến toàn cục
ngrok_processes = {}
ngrok_urls = {}


def start_ngrok(port):
    global ngrok_processes, ngrok_urls
    if port in ngrok_processes:
        print(f"Ngrok is already running on port {port}.")
        return ngrok_urls.get(port)  # Trả về URL nếu ngrok đã chạy

    ngrok_path = os.path.join(os.path.dirname(__file__), "ngrok.exe")
    print(f"Ngrok path: {ngrok_path}")
    ngrok_command = [
        ngrok_path,
        "http",  # Lệnh ngrok tạo một HTTP tunnel
        "--host-header=rewrite",  # Thêm tham số để rewrite header 'Host'
        f"http://localhost:{port}",
    ]

    process = subprocess.Popen(ngrok_command)
    ngrok_processes[port] = process
    time.sleep(10)  # Đợi ngrok khởi động

    # Lấy thông tin về URL ngrok
    url_process = subprocess.Popen(
        ["curl", "-s", "http://localhost:4040/api/tunnels"], stdout=subprocess.PIPE
    )
    output, _ = url_process.communicate()

    try:
        tunnels = json.loads(output)
        print("Ngrok response:", tunnels)  # In JSON ngrok trả về để kiểm tra

        # Lấy URL ngrok cho port được chỉ định
        for tunnel in tunnels.get("tunnels", []):
            public_url = tunnel.get("public_url")
            if f"localhost:{port}" in tunnel.get("config", {}).get("addr", ""):
                print(f"Ngrok URL for port {port}:", public_url)
                ngrok_urls[port] = public_url
                return public_url  # Trả về URL ngrok

        return None
    except json.JSONDecodeError:
        print("Error parsing JSON response from Ngrok.")
        return None


url = start_ngrok(11434)


def main_ngrok():
    return url
